/* SPDX-License-Identifier: GPL-3.0-or-later
 * A native-only RADV transfer/readback/presentation acceptance test.
 * No Java, SDL, shader pipeline or Minecraft code is executed here.
 */
#define VK_NO_PROTOTYPES
#include <vulkan/vulkan.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern PFN_vkVoidFunction vk_icdGetInstanceProcAddr(VkInstance, const char *);
extern void graphics_report(const char *stage, int result);
#define COMMANDS(X) \
 X(DestroyInstance) X(EnumeratePhysicalDevices) X(GetPhysicalDeviceProperties) \
 X(GetPhysicalDeviceQueueFamilyProperties) X(GetPhysicalDeviceMemoryProperties) \
 X(CreateDevice) X(GetDeviceProcAddr) X(GetPhysicalDeviceDisplayPropertiesKHR) \
 X(GetDisplayModePropertiesKHR) X(CreateDisplayPlaneSurfaceKHR) \
 X(GetPhysicalDeviceSurfaceSupportKHR) X(GetPhysicalDeviceSurfaceCapabilitiesKHR) \
 X(GetPhysicalDeviceSurfaceFormatsKHR) X(DestroySurfaceKHR)
#define DEVICE_COMMANDS(X) \
 X(DestroyDevice) X(GetDeviceQueue) X(CreateCommandPool) X(AllocateCommandBuffers) \
 X(ResetCommandBuffer) X(BeginCommandBuffer) X(EndCommandBuffer) X(CmdPipelineBarrier) \
 X(CmdClearColorImage) X(CmdCopyImageToBuffer) X(CmdCopyBufferToImage) \
 X(CreateBuffer) X(GetBufferMemoryRequirements) X(AllocateMemory) X(BindBufferMemory) \
 X(MapMemory) X(FlushMappedMemoryRanges) X(InvalidateMappedMemoryRanges) \
 X(CreateSemaphore) X(CreateFence) X(ResetFences) X(WaitForFences) X(QueueSubmit) \
 X(QueueWaitIdle) X(CreateSwapchainKHR) X(GetSwapchainImagesKHR) X(AcquireNextImageKHR) X(QueuePresentKHR)
#define DECLARE(n) static PFN_vk##n vk##n;
COMMANDS(DECLARE)
DEVICE_COMMANDS(DECLARE)
#undef DECLARE
static VkInstance instance;
static VkDevice device;
static VkQueue queue;
static VkCommandBuffer cmd;
static VkFence fence;
static VkSemaphore acquired, rendered;
static VkPhysicalDevice physical;
static VkSwapchainKHR swapchain;
static VkImage images[8];
static uint32_t image_count;
static VkExtent2D extent;
static VkBuffer transfer;
static VkDeviceMemory memory;
static unsigned char *mapped;
static VkDeviceSize read_offset, memory_size;
#define REQUIRE(x, name) do { if (!(x)) { graphics_report(name, -1); return -1; } graphics_report(name, 0); } while (0)
#define VK_TRY(x) do { graphics_report(#x,INT32_MIN); VkResult result_ = (x); if (result_ != VK_SUCCESS) { graphics_report(#x, result_); return -1; } } while (0)

/* Five-by-seven bitmap alphabet drawn on the CPU, then copied by the GPU.
 * This test card is not a claim that a Vulkan shader renderer exists yet. */
static const uint8_t letters[26][7] = {
 {14,17,17,31,17,17,17},{30,17,17,30,17,17,30},{14,17,16,16,16,17,14},
 {30,17,17,17,17,17,30},{31,16,16,30,16,16,31},{31,16,16,30,16,16,16},
 {14,17,16,23,17,17,15},{17,17,17,31,17,17,17},{14,4,4,4,4,4,14},
 {7,2,2,2,18,18,12},{17,18,20,24,20,18,17},{16,16,16,16,16,16,31},
 {17,27,21,21,17,17,17},{17,25,21,19,17,17,17},{14,17,17,17,17,17,14},
 {30,17,17,30,16,16,16},{14,17,17,17,21,18,13},{30,17,17,30,20,18,17},
 {15,16,16,14,1,1,30},{31,4,4,4,4,4,4},{17,17,17,17,17,17,14},
 {17,17,17,17,17,10,4},{17,17,17,21,21,21,10},{17,17,10,4,10,17,17},
 {17,17,10,4,4,4,4},{31,1,2,4,8,16,31}
};
static const uint8_t digits[10][7] = {
 {14,17,19,21,25,17,14},{4,12,4,4,4,4,14},{14,17,1,2,4,8,31},
 {30,1,1,14,1,1,30},{2,6,10,18,31,2,2},{31,16,16,30,1,1,30},
 {14,16,16,30,17,17,14},{31,1,2,4,8,8,8},{14,17,17,14,17,17,14},
 {14,17,17,15,1,1,14}
};
static void text(unsigned y, const char *s) {
 unsigned scale=extent.width/480; if(scale<1)scale=1;
 unsigned x=extent.width/20;
 for(;*s;s++,x+=6*scale) {
  const uint8_t *glyph=*s>='A'&&*s<='Z'?letters[*s-'A']:*s>='0'&&*s<='9'?digits[*s-'0']:NULL;
  if(!glyph)continue;
  for(unsigned row=0;row<7;row++)for(unsigned col=0;col<5;col++)
   if(glyph[row]&(1u<<(4-col)))
    for(unsigned dy=0;dy<scale;dy++)for(unsigned dx=0;dx<scale;dx++) {
     unsigned px=x+col*scale+dx,py=y+row*scale+dy;
     if(px<extent.width&&py<extent.height) {
      uint8_t *p=mapped+((size_t)py*extent.width+px)*4;
      p[0]=p[1]=p[2]=p[3]=255;
     }
    }
 }
}
static void card(void) {
 for(unsigned y=0;y<extent.height;y++)for(unsigned x=0;x<extent.width;x++) {
  uint8_t *p=mapped+((size_t)y*extent.width+x)*4;
  p[0]=y<extent.height/3?128:24;p[1]=y<extent.height/3?96:48;p[2]=y<extent.height/3?16:16;p[3]=255;
 }
 text(extent.height/8,"PS5 JAVA CLIENT 003");
 text(extent.height/3+extent.height/10,"NATIVE GRAPHICS PASS");
 text(extent.height/2,"REAL RADV GPU COPY AND PRESENT");
 text(extent.height*2/3,"READBACK VERIFIED");
 text(extent.height*4/5,"LOGS ON PORT 8765");
}
static void barrier(VkImage image,VkImageLayout old,VkImageLayout next,VkAccessFlags src,VkAccessFlags dst) {
 const VkImageMemoryBarrier b={.sType=VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER,
  .srcAccessMask=src,.dstAccessMask=dst,.oldLayout=old,.newLayout=next,
  .srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,.dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
  .image=image,.subresourceRange={VK_IMAGE_ASPECT_COLOR_BIT,0,1,0,1}};
 vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_ALL_COMMANDS_BIT,VK_PIPELINE_STAGE_ALL_COMMANDS_BIT,0,0,NULL,0,NULL,1,&b);
}
static int frame(unsigned color,int upload) {
 uint32_t index=0;
 VK_TRY(vkAcquireNextImageKHR(device,swapchain,UINT64_C(5000000000),acquired,VK_NULL_HANDLE,&index));
 REQUIRE(index<image_count,"Acquired image index in bounds");
 VK_TRY(vkResetCommandBuffer(cmd,0));
 const VkCommandBufferBeginInfo begin={.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO,.flags=VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT};
 VK_TRY(vkBeginCommandBuffer(cmd,&begin));
 barrier(images[index],VK_IMAGE_LAYOUT_UNDEFINED,VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,0,VK_ACCESS_TRANSFER_WRITE_BIT);
 if(upload) {
  const VkBufferMemoryBarrier host={.sType=VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER,.srcAccessMask=VK_ACCESS_HOST_WRITE_BIT,.dstAccessMask=VK_ACCESS_TRANSFER_READ_BIT,.srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,.dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,.buffer=transfer,.size=read_offset};
  vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_HOST_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,0,NULL,1,&host,0,NULL);
  const VkBufferImageCopy copy={.imageSubresource={VK_IMAGE_ASPECT_COLOR_BIT,0,0,1},.imageExtent={extent.width,extent.height,1}};
  vkCmdCopyBufferToImage(cmd,transfer,images[index],VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,1,&copy);
 } else {
  VkClearColorValue clear={.float32={0,0,0,1}};clear.float32[color]=1;
  const VkImageSubresourceRange range={VK_IMAGE_ASPECT_COLOR_BIT,0,1,0,1};
  vkCmdClearColorImage(cmd,images[index],VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,&clear,1,&range);
 }
 barrier(images[index],VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,VK_ACCESS_TRANSFER_WRITE_BIT,VK_ACCESS_TRANSFER_READ_BIT);
 const VkBufferImageCopy copies[2]={
  {.bufferOffset=read_offset,.imageSubresource={VK_IMAGE_ASPECT_COLOR_BIT,0,0,1},.imageExtent={1,1,1}},
  {.bufferOffset=read_offset+4,.imageSubresource={VK_IMAGE_ASPECT_COLOR_BIT,0,0,1},.imageOffset={(int32_t)extent.width-1,(int32_t)extent.height-1,0},.imageExtent={1,1,1}}};
 vkCmdCopyImageToBuffer(cmd,images[index],VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,transfer,2,copies);
 const VkBufferMemoryBarrier host={.sType=VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER,.srcAccessMask=VK_ACCESS_TRANSFER_WRITE_BIT,.dstAccessMask=VK_ACCESS_HOST_READ_BIT,.srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,.dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,.buffer=transfer,.offset=read_offset,.size=8};
 vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,0,NULL,1,&host,0,NULL);
 barrier(images[index],VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,VK_IMAGE_LAYOUT_PRESENT_SRC_KHR,VK_ACCESS_TRANSFER_READ_BIT,0);
 VK_TRY(vkEndCommandBuffer(cmd));
 VK_TRY(vkResetFences(device,1,&fence));
 const VkPipelineStageFlags wait=VK_PIPELINE_STAGE_TRANSFER_BIT;
 const VkSubmitInfo submit={.sType=VK_STRUCTURE_TYPE_SUBMIT_INFO,.waitSemaphoreCount=1,.pWaitSemaphores=&acquired,.pWaitDstStageMask=&wait,.commandBufferCount=1,.pCommandBuffers=&cmd,.signalSemaphoreCount=1,.pSignalSemaphores=&rendered};
 VK_TRY(vkQueueSubmit(queue,1,&submit,fence));
 VK_TRY(vkWaitForFences(device,1,&fence,VK_TRUE,UINT64_C(5000000000)));
 const VkMappedMemoryRange range={.sType=VK_STRUCTURE_TYPE_MAPPED_MEMORY_RANGE,.memory=memory,.size=VK_WHOLE_SIZE};
 VK_TRY(vkInvalidateMappedMemoryRanges(device,1,&range));
 if(upload) {
  REQUIRE(!memcmp(mapped+read_offset,mapped,4)&&!memcmp(mapped+read_offset+4,mapped+read_offset-4,4),"Uploaded card first and last GPU pixels match");
 } else {
  uint8_t want[4]={0,0,0,255};want[2-color]=255;
  REQUIRE(!memcmp(mapped+read_offset,want,4)&&!memcmp(mapped+read_offset+4,want,4),"GPU clear first and last pixels match");
 }
 const VkPresentInfoKHR present={.sType=VK_STRUCTURE_TYPE_PRESENT_INFO_KHR,.waitSemaphoreCount=1,.pWaitSemaphores=&rendered,.swapchainCount=1,.pSwapchains=&swapchain,.pImageIndices=&index};
 VK_TRY(vkQueuePresentKHR(queue,&present));
 VK_TRY(vkQueueWaitIdle(queue));
 return 0;
}
int graphics_run(void) {
 PFN_vkCreateInstance create=(PFN_vkCreateInstance)vk_icdGetInstanceProcAddr(VK_NULL_HANDLE,"vkCreateInstance");
 REQUIRE(create!=NULL,"RADV entry point");
 const char *extensions[]={VK_KHR_SURFACE_EXTENSION_NAME,VK_KHR_DISPLAY_EXTENSION_NAME};
 const VkApplicationInfo app={.sType=VK_STRUCTURE_TYPE_APPLICATION_INFO,.pApplicationName="PS5 Java Client Native Graphics003",.apiVersion=VK_API_VERSION_1_2};
 const VkInstanceCreateInfo info={.sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,.pApplicationInfo=&app,.enabledExtensionCount=2,.ppEnabledExtensionNames=extensions};
 VK_TRY(create(&info,NULL,&instance));
#define LOAD(n) vk##n=(PFN_vk##n)vk_icdGetInstanceProcAddr(instance,"vk"#n); REQUIRE(vk##n!=NULL,"Load vk"#n);
 COMMANDS(LOAD)
#undef LOAD
 uint32_t count=1;VK_TRY(vkEnumeratePhysicalDevices(instance,&count,&physical));REQUIRE(count==1,"One physical GPU");
 VkPhysicalDeviceProperties properties;vkGetPhysicalDeviceProperties(physical,&properties);
 graphics_report(properties.deviceName,0);REQUIRE(properties.apiVersion>=VK_API_VERSION_1_2,"Vulkan at least one point two");
 VkQueueFamilyProperties families[16];count=16;vkGetPhysicalDeviceQueueFamilyProperties(physical,&count,families);
 REQUIRE(count<=16,"Queue family inventory fits");uint32_t family=UINT32_MAX;
 for(uint32_t i=0;i<count;i++)if(families[i].queueCount&&(families[i].queueFlags&VK_QUEUE_GRAPHICS_BIT)){family=i;break;}
 REQUIRE(family!=UINT32_MAX,"Graphics queue available");
 const float priority=1;const VkDeviceQueueCreateInfo qi={.sType=VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,.queueFamilyIndex=family,.queueCount=1,.pQueuePriorities=&priority};
 const char *device_extensions[]={VK_KHR_SWAPCHAIN_EXTENSION_NAME};
 const VkDeviceCreateInfo di={.sType=VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO,.queueCreateInfoCount=1,.pQueueCreateInfos=&qi,.enabledExtensionCount=1,.ppEnabledExtensionNames=device_extensions};
 VK_TRY(vkCreateDevice(physical,&di,NULL,&device));
#define LOAD(n) vk##n=(PFN_vk##n)vkGetDeviceProcAddr(device,"vk"#n); REQUIRE(vk##n!=NULL,"Load vk"#n);
 DEVICE_COMMANDS(LOAD)
#undef LOAD
 vkGetDeviceQueue(device,family,0,&queue);
 VkDisplayPropertiesKHR display;count=1;VK_TRY(vkGetPhysicalDeviceDisplayPropertiesKHR(physical,&count,&display));REQUIRE(count==1,"One VideoOut display");
 VkDisplayModePropertiesKHR modes[8];count=8;VK_TRY(vkGetDisplayModePropertiesKHR(physical,display.display,&count,modes));REQUIRE(count>0&&count<=8,"Display mode available");
 extent=modes[0].parameters.visibleRegion;REQUIRE(extent.width>=640&&extent.width<=7680&&extent.height>=480&&extent.height<=4320,"Bounded display extent");
 const VkDisplaySurfaceCreateInfoKHR si={.sType=VK_STRUCTURE_TYPE_DISPLAY_SURFACE_CREATE_INFO_KHR,.displayMode=modes[0].displayMode,.transform=VK_SURFACE_TRANSFORM_IDENTITY_BIT_KHR,.alphaMode=VK_DISPLAY_PLANE_ALPHA_OPAQUE_BIT_KHR,.imageExtent=extent};
 VkSurfaceKHR surface;VK_TRY(vkCreateDisplayPlaneSurfaceKHR(instance,&si,NULL,&surface));
 VkBool32 support;VK_TRY(vkGetPhysicalDeviceSurfaceSupportKHR(physical,family,surface,&support));REQUIRE(support,"Queue supports VideoOut surface");
 VkSurfaceCapabilitiesKHR caps;VK_TRY(vkGetPhysicalDeviceSurfaceCapabilitiesKHR(physical,surface,&caps));
 const VkImageUsageFlags usage=VK_IMAGE_USAGE_TRANSFER_SRC_BIT|VK_IMAGE_USAGE_TRANSFER_DST_BIT;
 REQUIRE((caps.supportedUsageFlags&usage)==usage,"Surface supports transfer and readback");
 REQUIRE(caps.currentExtent.width==extent.width&&caps.currentExtent.height==extent.height,"Mode and surface extents match");
 VkSurfaceFormatKHR formats[32];count=32;VK_TRY(vkGetPhysicalDeviceSurfaceFormatsKHR(physical,surface,&count,formats));int found=0;
 for(uint32_t i=0;i<count;i++)if(formats[i].format==VK_FORMAT_B8G8R8A8_UNORM&&formats[i].colorSpace==VK_COLOR_SPACE_SRGB_NONLINEAR_KHR)found=1;
 REQUIRE(found,"BGRA UNORM display format");
 uint32_t requested=caps.minImageCount>3?caps.minImageCount:3;REQUIRE(!caps.maxImageCount||requested<=caps.maxImageCount,"Swapchain image count supported");
 const VkSwapchainCreateInfoKHR sc={.sType=VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR,.surface=surface,.minImageCount=requested,.imageFormat=VK_FORMAT_B8G8R8A8_UNORM,.imageColorSpace=VK_COLOR_SPACE_SRGB_NONLINEAR_KHR,.imageExtent=extent,.imageArrayLayers=1,.imageUsage=usage,.imageSharingMode=VK_SHARING_MODE_EXCLUSIVE,.preTransform=VK_SURFACE_TRANSFORM_IDENTITY_BIT_KHR,.compositeAlpha=VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR,.presentMode=VK_PRESENT_MODE_FIFO_KHR,.clipped=VK_TRUE};
 VK_TRY(vkCreateSwapchainKHR(device,&sc,NULL,&swapchain));image_count=8;VK_TRY(vkGetSwapchainImagesKHR(device,swapchain,&image_count,images));REQUIRE(image_count>0&&image_count<=8,"Bounded swapchain inventory");
 const VkCommandPoolCreateInfo pool_info={.sType=VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO,.flags=VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT,.queueFamilyIndex=family};
 VkCommandPool pool;VK_TRY(vkCreateCommandPool(device,&pool_info,NULL,&pool));
 const VkCommandBufferAllocateInfo ca={.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO,.commandPool=pool,.level=VK_COMMAND_BUFFER_LEVEL_PRIMARY,.commandBufferCount=1};VK_TRY(vkAllocateCommandBuffers(device,&ca,&cmd));
 const VkSemaphoreCreateInfo sem={.sType=VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO};VK_TRY(vkCreateSemaphore(device,&sem,NULL,&acquired));VK_TRY(vkCreateSemaphore(device,&sem,NULL,&rendered));
 const VkFenceCreateInfo fi={.sType=VK_STRUCTURE_TYPE_FENCE_CREATE_INFO};VK_TRY(vkCreateFence(device,&fi,NULL,&fence));
 read_offset=(VkDeviceSize)extent.width*extent.height*4;
 const VkBufferCreateInfo bi={.sType=VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO,.size=read_offset+8,.usage=VK_BUFFER_USAGE_TRANSFER_SRC_BIT|VK_BUFFER_USAGE_TRANSFER_DST_BIT,.sharingMode=VK_SHARING_MODE_EXCLUSIVE};VK_TRY(vkCreateBuffer(device,&bi,NULL,&transfer));
 VkMemoryRequirements req;vkGetBufferMemoryRequirements(device,transfer,&req);VkPhysicalDeviceMemoryProperties mem;vkGetPhysicalDeviceMemoryProperties(physical,&mem);
 uint32_t type=UINT32_MAX;for(uint32_t i=0;i<mem.memoryTypeCount;i++)if((req.memoryTypeBits&(1u<<i))&&(mem.memoryTypes[i].propertyFlags&VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)){type=i;break;}
 REQUIRE(type!=UINT32_MAX,"Host visible transfer allocation");memory_size=req.size;
 const VkMemoryAllocateInfo ma={.sType=VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO,.allocationSize=memory_size,.memoryTypeIndex=type};VK_TRY(vkAllocateMemory(device,&ma,NULL,&memory));VK_TRY(vkBindBufferMemory(device,transfer,memory,0));VK_TRY(vkMapMemory(device,memory,0,VK_WHOLE_SIZE,0,(void**)&mapped));
 for(unsigned i=0;i<90;i++)if(frame(i/30,0))return -1;
 graphics_report("Ninety RGB clear readback and FIFO presents",0);
 card();const VkMappedMemoryRange range={.sType=VK_STRUCTURE_TYPE_MAPPED_MEMORY_RANGE,.memory=memory,.size=VK_WHOLE_SIZE};VK_TRY(vkFlushMappedMemoryRanges(device,1,&range));
 if(frame(0,1))return -1;
 graphics_report("Native graphics acceptance complete; final swapchain retained until app closes",0);
 return 0;
}
