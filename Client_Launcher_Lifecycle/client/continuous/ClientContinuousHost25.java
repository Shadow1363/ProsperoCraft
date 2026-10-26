import java.nio.*;
import org.lwjgl.PointerBuffer;
import org.lwjgl.system.*;
import org.lwjgl.system.ps5.PS5Library;
import org.lwjgl.vulkan.*;
import static org.lwjgl.vulkan.VK10.*;
import static org.lwjgl.vulkan.VK11.VK_API_VERSION_1_1;
import static org.lwjgl.system.MemoryUtil.*;

/** Original LWJGL graphics pipeline with full image readback; existing CPU-menu presentation. */
public final class ClientContinuousHost25 {
 public static native void checkpoint(String text);

 private static final int WIDTH=256,HEIGHT=256,BYTES=WIDTH*HEIGHT*4;
 private static void stage(String text){checkpoint("DirectHost023 @"+System.nanoTime()+"ns: "+text);}
 private static void check(int result,String call){if(result!=VK_SUCCESS)throw new IllegalStateException(call+" VkResult="+result);}
 private static void cycle(int cycle,boolean host) {
  VkInstance instance=null;VkDevice device=null;
  long buffer=0,memory=0,image=0,imageMemory=0,view=0,renderPass=0,framebuffer=0,vertex=0,fragment=0,pipelineLayout=0,pipeline=0,commandPool=0,fence=0;
  ClientDirectScene25 renderer=null;
  boolean mapped=false,incomplete=false;
  try(MemoryStack stack=MemoryStack.stackPush()) {
   PointerBuffer ptr=stack.mallocPointer(1);LongBuffer handle=stack.mallocLong(1);IntBuffer count=stack.mallocInt(1);
   VkApplicationInfo app=VkApplicationInfo.calloc(stack).sType$Default().pApplicationName(stack.UTF8("PS5 Java DirectHost023")).apiVersion(VK_API_VERSION_1_1);
   VkInstanceCreateInfo ii=VkInstanceCreateInfo.calloc(stack).sType$Default().pApplicationInfo(app);
   stage("create render session "+cycle);check(vkCreateInstance(ii,null,ptr),"vkCreateInstance");instance=new VkInstance(ptr.get(0),ii);
   check(vkEnumeratePhysicalDevices(instance,count,null),"count devices");if(count.get(0)<1||count.get(0)>16)throw new AssertionError("GPU count");
   PointerBuffer devices=stack.mallocPointer(count.get(0));check(vkEnumeratePhysicalDevices(instance,count,devices),"enumerate devices");VkPhysicalDevice physical=new VkPhysicalDevice(devices.get(0),instance);
   VkPhysicalDeviceProperties properties=VkPhysicalDeviceProperties.malloc(stack);vkGetPhysicalDeviceProperties(physical,properties);
   VkFormatProperties fp=VkFormatProperties.malloc(stack);vkGetPhysicalDeviceFormatProperties(physical,VK_FORMAT_B8G8R8A8_UNORM,fp);
   if((fp.optimalTilingFeatures()&VK_FORMAT_FEATURE_COLOR_ATTACHMENT_BIT)==0)throw new AssertionError("RGBA8 color attachment unsupported");
   stage("device "+properties.deviceNameString());
   vkGetPhysicalDeviceQueueFamilyProperties(physical,count,null);if(count.get(0)<1||count.get(0)>64)throw new AssertionError("Queue count");
   VkQueueFamilyProperties.Buffer families=VkQueueFamilyProperties.malloc(count.get(0),stack);vkGetPhysicalDeviceQueueFamilyProperties(physical,count,families);
   int family=-1;for(int i=0;i<count.get(0);i++)if(families.get(i).queueCount()>0&&(families.get(i).queueFlags()&VK_QUEUE_GRAPHICS_BIT)!=0){family=i;break;}
   if(family<0)throw new AssertionError("No graphics queue");
   VkDeviceQueueCreateInfo.Buffer qi=VkDeviceQueueCreateInfo.calloc(1,stack);qi.get(0).sType$Default().queueFamilyIndex(family).pQueuePriorities(stack.floats(1));
   VkDeviceCreateInfo di=VkDeviceCreateInfo.calloc(stack).sType$Default().pQueueCreateInfos(qi);
   if(host){check(vkEnumerateDeviceExtensionProperties(physical,(ByteBuffer)null,count,null),"count extensions");VkExtensionProperties.Buffer ex=VkExtensionProperties.malloc(count.get(0),stack);check(vkEnumerateDeviceExtensionProperties(physical,(ByteBuffer)null,count,ex),"enumerate extensions");for(int i=0;i<count.get(0);i++)if(ex.get(i).extensionNameString().equals("VK_KHR_portability_subset")){di.ppEnabledExtensionNames(stack.pointers(stack.UTF8("VK_KHR_portability_subset")));break;}}
   check(vkCreateDevice(physical,di,null,ptr),"vkCreateDevice");device=new VkDevice(ptr.get(0),physical,di);vkGetDeviceQueue(device,family,0,ptr);VkQueue queue=new VkQueue(ptr.get(0),device);
   VkPhysicalDeviceMemoryProperties mp=VkPhysicalDeviceMemoryProperties.malloc(stack);vkGetPhysicalDeviceMemoryProperties(physical,mp);
   VkBufferCreateInfo bi=VkBufferCreateInfo.calloc(stack).sType$Default().size(BYTES+256).usage(VK_BUFFER_USAGE_TRANSFER_DST_BIT|VK_BUFFER_USAGE_TRANSFER_SRC_BIT).sharingMode(VK_SHARING_MODE_EXCLUSIVE);
   check(vkCreateBuffer(device,bi,null,handle),"vkCreateBuffer");buffer=handle.get(0);VkMemoryRequirements req=VkMemoryRequirements.malloc(stack);vkGetBufferMemoryRequirements(device,buffer,req);
   int type=-1;for(int i=0;i<mp.memoryTypeCount();i++)if((req.memoryTypeBits()&(1<<i))!=0&&(mp.memoryTypes(i).propertyFlags()&VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)!=0){type=i;break;}
   if(type<0)throw new AssertionError("No host visible readback memory");
   VkMemoryAllocateInfo ai=VkMemoryAllocateInfo.calloc(stack).sType$Default().allocationSize(req.size()).memoryTypeIndex(type);
   check(vkAllocateMemory(device,ai,null,handle),"vkAllocateMemory readback");memory=handle.get(0);check(vkBindBufferMemory(device,buffer,memory,0),"vkBindBufferMemory");check(vkMapMemory(device,memory,0,VK_WHOLE_SIZE,0,ptr),"vkMapMemory");mapped=true;ByteBuffer pixels=memByteBuffer(ptr.get(0),BYTES+256).order(ByteOrder.nativeOrder());
   VkImageCreateInfo im=VkImageCreateInfo.calloc(stack).sType$Default().imageType(VK_IMAGE_TYPE_2D).format(VK_FORMAT_B8G8R8A8_UNORM).mipLevels(1).arrayLayers(1).samples(VK_SAMPLE_COUNT_1_BIT).tiling(VK_IMAGE_TILING_OPTIMAL).usage(VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT|VK_IMAGE_USAGE_TRANSFER_SRC_BIT).sharingMode(VK_SHARING_MODE_EXCLUSIVE).initialLayout(VK_IMAGE_LAYOUT_UNDEFINED);im.extent().set(WIDTH,HEIGHT,1);
   check(vkCreateImage(device,im,null,handle),"vkCreateImage");image=handle.get(0);vkGetImageMemoryRequirements(device,image,req);
   type=-1;for(int i=0;i<mp.memoryTypeCount();i++)if((req.memoryTypeBits()&(1<<i))!=0){type=i;if((mp.memoryTypes(i).propertyFlags()&VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT)!=0)break;}
   if(type<0)throw new AssertionError("No image memory type");ai.allocationSize(req.size()).memoryTypeIndex(type);check(vkAllocateMemory(device,ai,null,handle),"vkAllocateMemory image");imageMemory=handle.get(0);check(vkBindImageMemory(device,image,imageMemory,0),"vkBindImageMemory");
   VkCommandPoolCreateInfo cp=VkCommandPoolCreateInfo.calloc(stack).sType$Default().queueFamilyIndex(family).flags(VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT);check(vkCreateCommandPool(device,cp,null,handle),"vkCreateCommandPool");commandPool=handle.get(0);
   VkCommandBufferAllocateInfo ca=VkCommandBufferAllocateInfo.calloc(stack).sType$Default().commandPool(commandPool).level(VK_COMMAND_BUFFER_LEVEL_PRIMARY).commandBufferCount(1);check(vkAllocateCommandBuffers(device,ca,ptr),"vkAllocateCommandBuffers");VkCommandBuffer cmd=new VkCommandBuffer(ptr.get(0),device);check(vkCreateFence(device,VkFenceCreateInfo.calloc(stack).sType$Default(),null,handle),"vkCreateFence");fence=handle.get(0);
   renderer=new ClientDirectScene25(device,physical,WIDTH,HEIGHT,new long[]{image},cmd,queue,fence,buffer,memory,pixels);
   for(int frame=0;frame<9;frame++) {int phase=frame%3;

    for(int i=0;i<BYTES+256;i++)pixels.put(i,(byte)0x6d);
    try(MemoryStack work=MemoryStack.stackPush()) {
     VkMappedMemoryRange.Buffer range=VkMappedMemoryRange.calloc(1,work);range.get(0).sType$Default().memory(memory).size(VK_WHOLE_SIZE);check(vkFlushMappedMemoryRanges(device,range),"vkFlushMappedMemoryRanges");
     check(vkResetCommandBuffer(cmd,0),"vkResetCommandBuffer");check(vkBeginCommandBuffer(cmd,VkCommandBufferBeginInfo.calloc(work).sType$Default().flags(VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)),"vkBeginCommandBuffer");
     VkBufferMemoryBarrier.Buffer bb=VkBufferMemoryBarrier.calloc(1,work);bb.get(0).sType$Default().srcAccessMask(VK_ACCESS_HOST_WRITE_BIT).dstAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).buffer(buffer).size(VK_WHOLE_SIZE);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_HOST_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,null,bb,null);
     VkImageMemoryBarrier.Buffer ib=VkImageMemoryBarrier.calloc(1,work);ib.get(0).sType$Default().srcAccessMask(0).dstAccessMask(VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT).oldLayout(VK_IMAGE_LAYOUT_UNDEFINED).newLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).image(image);ib.get(0).subresourceRange().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).levelCount(1).layerCount(1);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,0,null,null,ib);
     renderer.record(cmd,0,phase,work);
     ib.get(0).srcAccessMask(VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT).dstAccessMask(VK_ACCESS_TRANSFER_READ_BIT).oldLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL).newLayout(VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,null,null,ib);
     VkBufferImageCopy.Buffer copy=VkBufferImageCopy.calloc(1,work);copy.get(0).imageSubresource().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).layerCount(1);copy.get(0).imageExtent().set(WIDTH,HEIGHT,1);vkCmdCopyImageToBuffer(cmd,image,VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,buffer,copy);
     bb.get(0).srcAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).dstAccessMask(VK_ACCESS_HOST_READ_BIT);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,null,bb,null);check(vkEndCommandBuffer(cmd),"vkEndCommandBuffer");check(vkResetFences(device,fence),"vkResetFences");VkSubmitInfo.Buffer submit=VkSubmitInfo.calloc(1,work);submit.get(0).sType$Default().pCommandBuffers(work.pointers(cmd.address()));
     stage("draw graphics cycle"+cycle+" phase"+phase);incomplete=true;check(vkQueueSubmit(queue,submit,fence),"vkQueueSubmit");check(vkWaitForFences(device,fence,true,5_000_000_000L),"vkWaitForFences; relaunch if incomplete");incomplete=false;check(vkInvalidateMappedMemoryRanges(device,range),"vkInvalidateMappedMemoryRanges");
     for(int y=0;y<HEIGHT;y++)for(int x=0;x<WIDTH;x++)ClientDirectScene25.verify(pixels,(y*WIDTH+x)*4,ClientDirectScene25.expected(x,y,WIDTH,HEIGHT,phase));
     for(int i=BYTES;i<BYTES+256;i++)if(pixels.get(i)!=(byte)0x6d)throw new AssertionError("Readback guard mismatch"+i);

    }
   }
   stage("render cycle"+cycle+" all pixels/guards PASS");
  } finally {
   if(!incomplete && device!=null){if(renderer!=null)renderer.close();if(fence!=0)vkDestroyFence(device,fence,null);if(commandPool!=0)vkDestroyCommandPool(device,commandPool,null);if(pipeline!=0)vkDestroyPipeline(device,pipeline,null);if(pipelineLayout!=0)vkDestroyPipelineLayout(device,pipelineLayout,null);if(vertex!=0)vkDestroyShaderModule(device,vertex,null);if(fragment!=0)vkDestroyShaderModule(device,fragment,null);if(framebuffer!=0)vkDestroyFramebuffer(device,framebuffer,null);if(renderPass!=0)vkDestroyRenderPass(device,renderPass,null);if(view!=0)vkDestroyImageView(device,view,null);if(image!=0)vkDestroyImage(device,image,null);if(imageMemory!=0)vkFreeMemory(device,imageMemory,null);if(mapped)vkUnmapMemory(device,memory);if(buffer!=0)vkDestroyBuffer(device,buffer,null);if(memory!=0)vkFreeMemory(device,memory,null);vkDestroyDevice(device,null);}
   if(!incomplete && instance!=null)vkDestroyInstance(instance,null);
  }
 }
 public static void main(String[] args){
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.VULKAN_EXPLICIT_INIT.set(true);Library.initialize();String host=System.getProperty("ps5.test.vulkanLibrary");
  if(host==null){System.loadLibrary("ps5clientgpu");VK.create(new PS5Library(System.mapLibraryName("ps5clientgpu")));}else VK.create(new PS5Library(host));
  try{for(int i=0;i<3;i++)cycle(i,host!=null);}finally{VK.destroy();}
  stage("PASS direct renderer host:81 draws,27 full BGRA images/guards,3 sessions,all3phases;shared target renderer,offscreen only");
 }
}
