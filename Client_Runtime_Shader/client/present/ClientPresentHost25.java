import java.nio.*;
import org.lwjgl.PointerBuffer;
import org.lwjgl.system.*;
import org.lwjgl.system.ps5.PS5Library;
import org.lwjgl.vulkan.*;
import static org.lwjgl.vulkan.VK10.*;
import static org.lwjgl.vulkan.VK11.VK_API_VERSION_1_1;
import static org.lwjgl.system.MemoryUtil.*;

/** Original LWJGL graphics pipeline with full image readback; existing CPU-menu presentation. */
public final class ClientPresentHost25 {
 public static native void checkpoint(String text);
 public static native void publishPixels(ByteBuffer pixels,int width,int height);
 private static final int WIDTH=256,HEIGHT=256,BYTES=WIDTH*HEIGHT*4;
 private static void stage(String text){checkpoint("Present host offscreen011 @"+System.nanoTime()+"ns: "+text);}
 private static void check(int result,String call){if(result!=VK_SUCCESS)throw new IllegalStateException(call+" VkResult="+result);}
 private static void cycle(int cycle,boolean host) {
  VkInstance instance=null;VkDevice device=null;
  long buffer=0,memory=0,image=0,imageMemory=0,view=0,renderPass=0,framebuffer=0,vertex=0,fragment=0,pipelineLayout=0,pipeline=0,commandPool=0,fence=0;
  boolean mapped=false,incomplete=false;
  try(MemoryStack stack=MemoryStack.stackPush()) {
   PointerBuffer ptr=stack.mallocPointer(1);LongBuffer handle=stack.mallocLong(1);IntBuffer count=stack.mallocInt(1);
   VkApplicationInfo app=VkApplicationInfo.calloc(stack).sType$Default().pApplicationName(stack.UTF8("PS5 Java Present host011")).apiVersion(VK_API_VERSION_1_1);
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
   VkBufferCreateInfo bi=VkBufferCreateInfo.calloc(stack).sType$Default().size(BYTES+256).usage(VK_BUFFER_USAGE_TRANSFER_DST_BIT).sharingMode(VK_SHARING_MODE_EXCLUSIVE);
   check(vkCreateBuffer(device,bi,null,handle),"vkCreateBuffer");buffer=handle.get(0);VkMemoryRequirements req=VkMemoryRequirements.malloc(stack);vkGetBufferMemoryRequirements(device,buffer,req);
   int type=-1;for(int i=0;i<mp.memoryTypeCount();i++)if((req.memoryTypeBits()&(1<<i))!=0&&(mp.memoryTypes(i).propertyFlags()&VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)!=0){type=i;break;}
   if(type<0)throw new AssertionError("No host visible readback memory");
   VkMemoryAllocateInfo ai=VkMemoryAllocateInfo.calloc(stack).sType$Default().allocationSize(req.size()).memoryTypeIndex(type);
   check(vkAllocateMemory(device,ai,null,handle),"vkAllocateMemory readback");memory=handle.get(0);check(vkBindBufferMemory(device,buffer,memory,0),"vkBindBufferMemory");check(vkMapMemory(device,memory,0,VK_WHOLE_SIZE,0,ptr),"vkMapMemory");mapped=true;ByteBuffer pixels=memByteBuffer(ptr.get(0),BYTES+256).order(ByteOrder.nativeOrder());
   VkImageCreateInfo im=VkImageCreateInfo.calloc(stack).sType$Default().imageType(VK_IMAGE_TYPE_2D).format(VK_FORMAT_B8G8R8A8_UNORM).mipLevels(1).arrayLayers(1).samples(VK_SAMPLE_COUNT_1_BIT).tiling(VK_IMAGE_TILING_OPTIMAL).usage(VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT|VK_IMAGE_USAGE_TRANSFER_SRC_BIT).sharingMode(VK_SHARING_MODE_EXCLUSIVE).initialLayout(VK_IMAGE_LAYOUT_UNDEFINED);im.extent().set(WIDTH,HEIGHT,1);
   check(vkCreateImage(device,im,null,handle),"vkCreateImage");image=handle.get(0);vkGetImageMemoryRequirements(device,image,req);
   type=-1;for(int i=0;i<mp.memoryTypeCount();i++)if((req.memoryTypeBits()&(1<<i))!=0){type=i;if((mp.memoryTypes(i).propertyFlags()&VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT)!=0)break;}
   if(type<0)throw new AssertionError("No image memory type");ai.allocationSize(req.size()).memoryTypeIndex(type);check(vkAllocateMemory(device,ai,null,handle),"vkAllocateMemory image");imageMemory=handle.get(0);check(vkBindImageMemory(device,image,imageMemory,0),"vkBindImageMemory");
   VkImageViewCreateInfo vi=VkImageViewCreateInfo.calloc(stack).sType$Default().image(image).viewType(VK_IMAGE_VIEW_TYPE_2D).format(VK_FORMAT_B8G8R8A8_UNORM);vi.subresourceRange().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).baseMipLevel(0).levelCount(1).baseArrayLayer(0).layerCount(1);check(vkCreateImageView(device,vi,null,handle),"vkCreateImageView");view=handle.get(0);
   VkAttachmentDescription.Buffer attachment=VkAttachmentDescription.calloc(1,stack);attachment.get(0).format(VK_FORMAT_B8G8R8A8_UNORM).samples(VK_SAMPLE_COUNT_1_BIT).loadOp(VK_ATTACHMENT_LOAD_OP_CLEAR).storeOp(VK_ATTACHMENT_STORE_OP_STORE).stencilLoadOp(VK_ATTACHMENT_LOAD_OP_DONT_CARE).stencilStoreOp(VK_ATTACHMENT_STORE_OP_DONT_CARE).initialLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL).finalLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL);
   VkAttachmentReference.Buffer reference=VkAttachmentReference.calloc(1,stack);reference.get(0).attachment(0).layout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL);
   VkSubpassDescription.Buffer subpass=VkSubpassDescription.calloc(1,stack);subpass.get(0).pipelineBindPoint(VK_PIPELINE_BIND_POINT_GRAPHICS).colorAttachmentCount(1).pColorAttachments(reference);
   VkRenderPassCreateInfo rp=VkRenderPassCreateInfo.calloc(stack).sType$Default().pAttachments(attachment).pSubpasses(subpass);check(vkCreateRenderPass(device,rp,null,handle),"vkCreateRenderPass");renderPass=handle.get(0);
   VkFramebufferCreateInfo fb=VkFramebufferCreateInfo.calloc(stack).sType$Default().renderPass(renderPass).pAttachments(stack.longs(view)).width(WIDTH).height(HEIGHT).layers(1);check(vkCreateFramebuffer(device,fb,null,handle),"vkCreateFramebuffer");framebuffer=handle.get(0);
   VkShaderModuleCreateInfo sm=VkShaderModuleCreateInfo.calloc(stack).sType$Default();sm.pCode(ClientPresentCode25.vertex(stack));check(vkCreateShaderModule(device,sm,null,handle),"vertex module");vertex=handle.get(0);sm.pCode(ClientPresentCode25.fragment(stack));check(vkCreateShaderModule(device,sm,null,handle),"fragment module");fragment=handle.get(0);
   VkPushConstantRange.Buffer push=VkPushConstantRange.calloc(1,stack);push.get(0).stageFlags(VK_SHADER_STAGE_FRAGMENT_BIT).offset(0).size(12);VkPipelineLayoutCreateInfo pl=VkPipelineLayoutCreateInfo.calloc(stack).sType$Default().pPushConstantRanges(push);check(vkCreatePipelineLayout(device,pl,null,handle),"vkCreatePipelineLayout");pipelineLayout=handle.get(0);
   VkPipelineShaderStageCreateInfo.Buffer stages=VkPipelineShaderStageCreateInfo.calloc(2,stack);stages.get(0).sType$Default().stage(VK_SHADER_STAGE_VERTEX_BIT).module(vertex).pName(stack.UTF8("main"));stages.get(1).sType$Default().stage(VK_SHADER_STAGE_FRAGMENT_BIT).module(fragment).pName(stack.UTF8("main"));
   VkPipelineVertexInputStateCreateInfo input=VkPipelineVertexInputStateCreateInfo.calloc(stack).sType$Default();VkPipelineInputAssemblyStateCreateInfo assembly=VkPipelineInputAssemblyStateCreateInfo.calloc(stack).sType$Default().topology(VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST);
   VkViewport.Buffer viewport=VkViewport.calloc(1,stack);viewport.get(0).x(0).y(0).width(WIDTH).height(HEIGHT).minDepth(0).maxDepth(1);VkRect2D.Buffer scissors=VkRect2D.calloc(1,stack);scissors.get(0).extent().set(WIDTH,HEIGHT);
   VkPipelineViewportStateCreateInfo vp=VkPipelineViewportStateCreateInfo.calloc(stack).sType$Default().pViewports(viewport).pScissors(scissors);
   VkPipelineRasterizationStateCreateInfo raster=VkPipelineRasterizationStateCreateInfo.calloc(stack).sType$Default().polygonMode(VK_POLYGON_MODE_FILL).cullMode(VK_CULL_MODE_NONE).frontFace(VK_FRONT_FACE_COUNTER_CLOCKWISE).lineWidth(1);
   VkPipelineMultisampleStateCreateInfo ms=VkPipelineMultisampleStateCreateInfo.calloc(stack).sType$Default().rasterizationSamples(VK_SAMPLE_COUNT_1_BIT);
   VkPipelineColorBlendAttachmentState.Buffer colors=VkPipelineColorBlendAttachmentState.calloc(1,stack);colors.get(0).colorWriteMask(VK_COLOR_COMPONENT_R_BIT|VK_COLOR_COMPONENT_G_BIT|VK_COLOR_COMPONENT_B_BIT|VK_COLOR_COMPONENT_A_BIT);
   VkPipelineColorBlendStateCreateInfo blend=VkPipelineColorBlendStateCreateInfo.calloc(stack).sType$Default().pAttachments(colors);
   VkGraphicsPipelineCreateInfo.Buffer gp=VkGraphicsPipelineCreateInfo.calloc(1,stack);gp.get(0).sType$Default().pStages(stages).pVertexInputState(input).pInputAssemblyState(assembly).pViewportState(vp).pRasterizationState(raster).pMultisampleState(ms).pColorBlendState(blend).layout(pipelineLayout).renderPass(renderPass).subpass(0);
   stage("compile real vertex/fragment graphics pipeline");check(vkCreateGraphicsPipelines(device,VK_NULL_HANDLE,gp,null,handle),"vkCreateGraphicsPipelines");pipeline=handle.get(0);stage("graphics pipeline compiled");
   VkCommandPoolCreateInfo cp=VkCommandPoolCreateInfo.calloc(stack).sType$Default().queueFamilyIndex(family).flags(VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT);check(vkCreateCommandPool(device,cp,null,handle),"vkCreateCommandPool");commandPool=handle.get(0);
   VkCommandBufferAllocateInfo ca=VkCommandBufferAllocateInfo.calloc(stack).sType$Default().commandPool(commandPool).level(VK_COMMAND_BUFFER_LEVEL_PRIMARY).commandBufferCount(1);check(vkAllocateCommandBuffers(device,ca,ptr),"vkAllocateCommandBuffers");VkCommandBuffer cmd=new VkCommandBuffer(ptr.get(0),device);check(vkCreateFence(device,VkFenceCreateInfo.calloc(stack).sType$Default(),null,handle),"vkCreateFence");fence=handle.get(0);
   for(int phase=0;phase<3;phase++) {
    for(int i=0;i<BYTES+256;i++)pixels.put(i,(byte)0x6d);
    try(MemoryStack work=MemoryStack.stackPush()) {
     VkMappedMemoryRange.Buffer range=VkMappedMemoryRange.calloc(1,work);range.get(0).sType$Default().memory(memory).size(VK_WHOLE_SIZE);check(vkFlushMappedMemoryRanges(device,range),"vkFlushMappedMemoryRanges");
     check(vkResetCommandBuffer(cmd,0),"vkResetCommandBuffer");check(vkBeginCommandBuffer(cmd,VkCommandBufferBeginInfo.calloc(work).sType$Default().flags(VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)),"vkBeginCommandBuffer");
     VkBufferMemoryBarrier.Buffer bb=VkBufferMemoryBarrier.calloc(1,work);bb.get(0).sType$Default().srcAccessMask(VK_ACCESS_HOST_WRITE_BIT).dstAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).buffer(buffer).size(VK_WHOLE_SIZE);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_HOST_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,null,bb,null);
     VkImageMemoryBarrier.Buffer ib=VkImageMemoryBarrier.calloc(1,work);ib.get(0).sType$Default().srcAccessMask(0).dstAccessMask(VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT).oldLayout(VK_IMAGE_LAYOUT_UNDEFINED).newLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).image(image);ib.get(0).subresourceRange().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).levelCount(1).layerCount(1);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,0,null,null,ib);
     VkClearValue.Buffer clear=VkClearValue.calloc(1,work);clear.get(0).color().float32(0,1).float32(1,0).float32(2,1).float32(3,1);
     VkRenderPassBeginInfo begin=VkRenderPassBeginInfo.calloc(work).sType$Default().renderPass(renderPass).framebuffer(framebuffer).pClearValues(clear);begin.renderArea().extent().set(WIDTH,HEIGHT);vkCmdBeginRenderPass(cmd,begin,VK_SUBPASS_CONTENTS_INLINE);vkCmdBindPipeline(cmd,VK_PIPELINE_BIND_POINT_GRAPHICS,pipeline);vkCmdPushConstants(cmd,pipelineLayout,VK_SHADER_STAGE_FRAGMENT_BIT,0,work.ints(phase,WIDTH,HEIGHT));vkCmdDraw(cmd,3,1,0,0);vkCmdEndRenderPass(cmd);
     ib.get(0).srcAccessMask(VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT).dstAccessMask(VK_ACCESS_TRANSFER_READ_BIT).oldLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL).newLayout(VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,null,null,ib);
     VkBufferImageCopy.Buffer copy=VkBufferImageCopy.calloc(1,work);copy.get(0).imageSubresource().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).layerCount(1);copy.get(0).imageExtent().set(WIDTH,HEIGHT,1);vkCmdCopyImageToBuffer(cmd,image,VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,buffer,copy);
     bb.get(0).srcAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).dstAccessMask(VK_ACCESS_HOST_READ_BIT);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,null,bb,null);check(vkEndCommandBuffer(cmd),"vkEndCommandBuffer");check(vkResetFences(device,fence),"vkResetFences");VkSubmitInfo.Buffer submit=VkSubmitInfo.calloc(1,work);submit.get(0).sType$Default().pCommandBuffers(work.pointers(cmd.address()));
     stage("draw graphics cycle"+cycle+" phase"+phase);incomplete=true;check(vkQueueSubmit(queue,submit,fence),"vkQueueSubmit");check(vkWaitForFences(device,fence,true,5_000_000_000L),"vkWaitForFences; relaunch if incomplete");incomplete=false;check(vkInvalidateMappedMemoryRanges(device,range),"vkInvalidateMappedMemoryRanges");
     for(int y=0;y<HEIGHT;y++)for(int x=0;x<WIDTH;x++)if(pixels.getInt((y*WIDTH+x)*4)!=expected(x,y,phase))throw new AssertionError("Graphics pixel mismatch x"+x+" y"+y+" phase"+phase+" actual0x"+Integer.toHexString(pixels.getInt((y*WIDTH+x)*4)));
     for(int i=BYTES;i<BYTES+256;i++)if(pixels.get(i)!=(byte)0x6d)throw new AssertionError("Readback guard mismatch"+i);
     if(cycle==2 && phase==2)publishPixels(pixels,WIDTH,HEIGHT);
    }
   }
   stage("render cycle"+cycle+" all pixels/guards PASS");
  } finally {
   if(!incomplete && device!=null){if(fence!=0)vkDestroyFence(device,fence,null);if(commandPool!=0)vkDestroyCommandPool(device,commandPool,null);if(pipeline!=0)vkDestroyPipeline(device,pipeline,null);if(pipelineLayout!=0)vkDestroyPipelineLayout(device,pipelineLayout,null);if(vertex!=0)vkDestroyShaderModule(device,vertex,null);if(fragment!=0)vkDestroyShaderModule(device,fragment,null);if(framebuffer!=0)vkDestroyFramebuffer(device,framebuffer,null);if(renderPass!=0)vkDestroyRenderPass(device,renderPass,null);if(view!=0)vkDestroyImageView(device,view,null);if(image!=0)vkDestroyImage(device,image,null);if(imageMemory!=0)vkFreeMemory(device,imageMemory,null);if(mapped)vkUnmapMemory(device,memory);if(buffer!=0)vkDestroyBuffer(device,buffer,null);if(memory!=0)vkFreeMemory(device,memory,null);vkDestroyDevice(device,null);}
   if(!incomplete && instance!=null)vkDestroyInstance(instance,null);
  }
 }
 private static int expected(int x,int y,int phase) {
  if(x<16||y<16||x>=240||y>=240)return 0xff000000;
  if(Math.abs(x-y)<3)return 0xffffffff;
  return switch((x/32+y/32+phase)%4){case 0->0xffff0000;case 1->0xff00ff00;case 2->0xff0000ff;default->0xffffff00;};
 }
 public static void main(String[] args){
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.VULKAN_EXPLICIT_INIT.set(true);Library.initialize();String host=System.getProperty("ps5.test.vulkanLibrary");
  if(host==null){System.loadLibrary("ps5clientgpu");VK.create(new PS5Library(System.mapLibraryName("ps5clientgpu")));}else VK.create(new PS5Library(host));
  try{for(int i=0;i<3;i++)cycle(i,host!=null);}finally{VK.destroy();}
  stage("PASS original LWJGL graphics pipeline:9 draws, full256x256 pixel/guard checks,3 session lifecycles; host offscreen pixels captured; no display/present tested");
 }
}
