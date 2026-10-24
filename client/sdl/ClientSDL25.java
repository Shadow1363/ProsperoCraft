import java.nio.*;
import org.lwjgl.PointerBuffer;
import org.lwjgl.system.*;
import org.lwjgl.system.ps5.PS5Library;
import org.lwjgl.vulkan.*;
import static org.lwjgl.system.MemoryUtil.*;
import static org.lwjgl.vulkan.VK10.*;
import static org.lwjgl.vulkan.VK11.VK_API_VERSION_1_1;
import static org.lwjgl.vulkan.KHRDisplay.*;
import static org.lwjgl.vulkan.KHRSurface.*;
import static org.lwjgl.vulkan.KHRSwapchain.*;
import org.lwjgl.sdl.*;
import static org.lwjgl.sdl.SDLInit.*;
import static org.lwjgl.sdl.SDLError.*;
import static org.lwjgl.sdl.SDLVideo.*;
import static org.lwjgl.sdl.SDLVulkan.*;
import static org.lwjgl.sdl.SDLGamepad.*;
import static org.lwjgl.sdl.SDLEvents.*;

/** Direct PS5 display probe. No CPU VideoOut owner, SDL or game launch. */
public final class ClientSDL25 {
 public static native void checkpoint(String text);
 private static void stage(String text){checkpoint("SDL012 @"+System.nanoTime()+"ns: "+text);}
 private static void check(int result,String call){if(result!=VK_SUCCESS)throw new IllegalStateException(call+" VkResult="+result+"; close/reopen app; partial native/display resources retained");}
 private static int expected(int x,int y,int phase){if(x<16||y<16||x>=240||y>=240)return 0xff000000;if(Math.abs(x-y)<3)return 0xffffffff;return switch((x/32+y/32+phase)%4){case 0->0xffff0000;case 1->0xff00ff00;case 2->0xff0000ff;default->0xffffff00;};}
 private static long window,pad;private static int inputMask,stateMask;private static boolean armed;
 private static void sdl(boolean result,String call){if(!result)throw new IllegalStateException(call+": "+SDL_GetError());}
 private static void ask(String text){checkpoint("SDL012 USER:"+text);}
 private static void input(MemoryStack stack) {
  SDL_Event event=SDL_Event.calloc(stack);
  while(SDL_PollEvent(event)) {
   if(!armed)continue;
   if(event.type()==SDL_EVENT_GAMEPAD_BUTTON_DOWN&&event.gbutton().which()==SDL_GetGamepadID(pad)) {
    int button=event.gbutton().button();
    if(button==SDL_GAMEPAD_BUTTON_SOUTH)inputMask|=1;
    if(button==SDL_GAMEPAD_BUTTON_EAST)inputMask|=2;
    if(button==SDL_GAMEPAD_BUTTON_DPAD_LEFT)inputMask|=4;
   }
   if(event.type()==SDL_EVENT_GAMEPAD_AXIS_MOTION&&event.gaxis().which()==SDL_GetGamepadID(pad)&&(event.gaxis().axis()==SDL_GAMEPAD_AXIS_LEFTX||event.gaxis().axis()==SDL_GAMEPAD_AXIS_LEFTY)&&Math.abs((int)event.gaxis().value())>16384)inputMask|=8;
  }
  boolean a=SDL_GetGamepadButton(pad,SDL_GAMEPAD_BUTTON_SOUTH),b=SDL_GetGamepadButton(pad,SDL_GAMEPAD_BUTTON_EAST),left=SDL_GetGamepadButton(pad,SDL_GAMEPAD_BUTTON_DPAD_LEFT);
  int x=SDL_GetGamepadAxis(pad,SDL_GAMEPAD_AXIS_LEFTX),y=SDL_GetGamepadAxis(pad,SDL_GAMEPAD_AXIS_LEFTY);
  if(!armed&&!a&&!b&&!left&&Math.abs(x)<4000&&Math.abs(y)<4000){armed=true;ask("Input ready: press X, Circle, D-pad Left, then move left stick strongly. Hold each briefly.");}
  if(armed){if(a)stateMask|=1;if(b)stateMask|=2;if(left)stateMask|=4;if(Math.abs(x)>16384||Math.abs(y)>16384)stateMask|=8;}
 }
 private static void run() {
  // This first WSI probe intentionally retains all native display resources on
  // success or failure. Reacquisition, teardown and timeout recovery are not tested.
  try(MemoryStack stack=MemoryStack.stackPush()) {
   PointerBuffer ptr=stack.mallocPointer(1);LongBuffer handle=stack.mallocLong(1);IntBuffer count=stack.mallocInt(1);
   VkApplicationInfo app=VkApplicationInfo.calloc(stack).sType$Default().pApplicationName(stack.UTF8("PS5 Java SDL012")).apiVersion(VK_API_VERSION_1_1);
   VkInstanceCreateInfo ii=VkInstanceCreateInfo.calloc(stack).sType$Default().pApplicationInfo(app).ppEnabledExtensionNames(SDL_Vulkan_GetInstanceExtensions());
   stage("create instance with SDL-provided Vulkan extensions");check(vkCreateInstance(ii,null,ptr),"vkCreateInstance");VkInstance instance=new VkInstance(ptr.get(0),ii);
   check(vkEnumeratePhysicalDevices(instance,count,null),"count devices");if(count.get(0)<1||count.get(0)>16)throw new AssertionError("GPU count");PointerBuffer devices=stack.mallocPointer(count.get(0));check(vkEnumeratePhysicalDevices(instance,count,devices),"enumerate devices");VkPhysicalDevice physical=new VkPhysicalDevice(devices.get(0),instance);
   IntBuffer w=stack.mallocInt(1),h=stack.mallocInt(1);sdl(SDL_GetWindowSizeInPixels(window,w,h),"SDL_GetWindowSizeInPixels");int width=w.get(0),height=h.get(0);if(width<640||width>3840||height<480||height>2160)throw new AssertionError("SDL window pixel extent bound");
   stage("create actual surface through SDL_Vulkan_CreateSurface");sdl(SDL_Vulkan_CreateSurface(window,instance,null,handle),"SDL_Vulkan_CreateSurface");long surface=handle.get(0);
   vkGetPhysicalDeviceQueueFamilyProperties(physical,count,null);if(count.get(0)<1||count.get(0)>64)throw new AssertionError("Queue bound");VkQueueFamilyProperties.Buffer families=VkQueueFamilyProperties.malloc(count.get(0),stack);vkGetPhysicalDeviceQueueFamilyProperties(physical,count,families);int family=-1;
   for(int i=0;i<count.get(0);i++)if(families.get(i).queueCount()>0&&(families.get(i).queueFlags()&VK_QUEUE_GRAPHICS_BIT)!=0){IntBuffer support=stack.mallocInt(1);check(vkGetPhysicalDeviceSurfaceSupportKHR(physical,i,surface,support),"queue surface support");if(support.get(0)!=0&&SDL_Vulkan_GetPresentationSupport(instance,physical,i)){family=i;break;}}
   if(family<0)throw new AssertionError("No graphics/present queue");VkDeviceQueueCreateInfo.Buffer qi=VkDeviceQueueCreateInfo.calloc(1,stack);qi.get(0).sType$Default().queueFamilyIndex(family).pQueuePriorities(stack.floats(1));VkDeviceCreateInfo di=VkDeviceCreateInfo.calloc(stack).sType$Default().pQueueCreateInfos(qi).ppEnabledExtensionNames(stack.pointers(stack.UTF8(VK_KHR_SWAPCHAIN_EXTENSION_NAME)));
   check(vkCreateDevice(physical,di,null,ptr),"vkCreateDevice");VkDevice device=new VkDevice(ptr.get(0),physical,di);vkGetDeviceQueue(device,family,0,ptr);VkQueue queue=new VkQueue(ptr.get(0),device);
   VkSurfaceCapabilitiesKHR caps=VkSurfaceCapabilitiesKHR.malloc(stack);check(vkGetPhysicalDeviceSurfaceCapabilitiesKHR(physical,surface,caps),"surface capabilities");int usage=VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT|VK_IMAGE_USAGE_TRANSFER_SRC_BIT;
   if((caps.supportedUsageFlags()&usage)!=usage||(caps.supportedTransforms()&VK_SURFACE_TRANSFORM_IDENTITY_BIT_KHR)==0||(caps.supportedCompositeAlpha()&VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR)==0)throw new AssertionError("Surface color/readback/identity/opaque capabilities");if(caps.currentExtent().width()!=width||caps.currentExtent().height()!=height)throw new AssertionError("Surface/mode extent mismatch");
   check(vkGetPhysicalDeviceSurfaceFormatsKHR(physical,surface,count,null),"format count");if(count.get(0)<1||count.get(0)>32)throw new AssertionError("Format bound");VkSurfaceFormatKHR.Buffer formats=VkSurfaceFormatKHR.malloc(count.get(0),stack);check(vkGetPhysicalDeviceSurfaceFormatsKHR(physical,surface,count,formats),"surface formats");boolean found=false;for(int i=0;i<count.get(0);i++)if(formats.get(i).format()==VK_FORMAT_B8G8R8A8_UNORM&&formats.get(i).colorSpace()==VK_COLOR_SPACE_SRGB_NONLINEAR_KHR)found=true;if(!found)throw new AssertionError("BGRA8 UNORM nonlinear surface format");
   int requested=Math.max(3,caps.minImageCount());if(requested>8||(caps.maxImageCount()!=0&&requested>caps.maxImageCount()))throw new AssertionError("Swapchain image bound");VkSwapchainCreateInfoKHR sc=VkSwapchainCreateInfoKHR.calloc(stack).sType$Default().surface(surface).minImageCount(requested).imageFormat(VK_FORMAT_B8G8R8A8_UNORM).imageColorSpace(VK_COLOR_SPACE_SRGB_NONLINEAR_KHR).imageArrayLayers(1).imageUsage(usage).imageSharingMode(VK_SHARING_MODE_EXCLUSIVE).preTransform(VK_SURFACE_TRANSFORM_IDENTITY_BIT_KHR).compositeAlpha(VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR).presentMode(VK_PRESENT_MODE_FIFO_KHR).clipped(true);sc.imageExtent().set(width,height);
   stage("create direct graphics swapchain");check(vkCreateSwapchainKHR(device,sc,null,handle),"vkCreateSwapchainKHR");long swapchain=handle.get(0);check(vkGetSwapchainImagesKHR(device,swapchain,count,null),"swapchain count");if(count.get(0)<1||count.get(0)>8)throw new AssertionError("Swapchain inventory bound");int imageCount=count.get(0);LongBuffer images=stack.mallocLong(imageCount);check(vkGetSwapchainImagesKHR(device,swapchain,count,images),"swapchain images");
   VkAttachmentDescription.Buffer attachment=VkAttachmentDescription.calloc(1,stack);attachment.get(0).format(VK_FORMAT_B8G8R8A8_UNORM).samples(VK_SAMPLE_COUNT_1_BIT).loadOp(VK_ATTACHMENT_LOAD_OP_CLEAR).storeOp(VK_ATTACHMENT_STORE_OP_STORE).stencilLoadOp(VK_ATTACHMENT_LOAD_OP_DONT_CARE).stencilStoreOp(VK_ATTACHMENT_STORE_OP_DONT_CARE).initialLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL).finalLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL);VkAttachmentReference.Buffer reference=VkAttachmentReference.calloc(1,stack);reference.get(0).attachment(0).layout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL);VkSubpassDescription.Buffer subpass=VkSubpassDescription.calloc(1,stack);subpass.get(0).pipelineBindPoint(VK_PIPELINE_BIND_POINT_GRAPHICS).colorAttachmentCount(1).pColorAttachments(reference);VkRenderPassCreateInfo rp=VkRenderPassCreateInfo.calloc(stack).sType$Default().pAttachments(attachment).pSubpasses(subpass);check(vkCreateRenderPass(device,rp,null,handle),"vkCreateRenderPass");long renderPass=handle.get(0);
   long[] framebuffers=new long[imageCount],rendered=new long[imageCount];VkSemaphoreCreateInfo sem=VkSemaphoreCreateInfo.calloc(stack).sType$Default();for(int i=0;i<imageCount;i++){VkImageViewCreateInfo vi=VkImageViewCreateInfo.calloc(stack).sType$Default().image(images.get(i)).viewType(VK_IMAGE_VIEW_TYPE_2D).format(VK_FORMAT_B8G8R8A8_UNORM);vi.subresourceRange().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).levelCount(1).layerCount(1);check(vkCreateImageView(device,vi,null,handle),"swapchain image view");VkFramebufferCreateInfo fb=VkFramebufferCreateInfo.calloc(stack).sType$Default().renderPass(renderPass).pAttachments(stack.longs(handle.get(0))).width(width).height(height).layers(1);check(vkCreateFramebuffer(device,fb,null,handle),"swapchain framebuffer");framebuffers[i]=handle.get(0);check(vkCreateSemaphore(device,sem,null,handle),"render semaphore per image");rendered[i]=handle.get(0);}
   check(vkCreateSemaphore(device,sem,null,handle),"acquire semaphore");long acquired=handle.get(0);
   int[] samples={0,32,96,160,224,255};int sampleCount=samples.length*samples.length,bytes=sampleCount*4+256;VkBufferCreateInfo bi=VkBufferCreateInfo.calloc(stack).sType$Default().size(bytes).usage(VK_BUFFER_USAGE_TRANSFER_DST_BIT).sharingMode(VK_SHARING_MODE_EXCLUSIVE);check(vkCreateBuffer(device,bi,null,handle),"readback buffer");long buffer=handle.get(0);VkMemoryRequirements req=VkMemoryRequirements.malloc(stack);vkGetBufferMemoryRequirements(device,buffer,req);VkPhysicalDeviceMemoryProperties mp=VkPhysicalDeviceMemoryProperties.malloc(stack);vkGetPhysicalDeviceMemoryProperties(physical,mp);int type=-1;for(int i=0;i<mp.memoryTypeCount();i++)if((req.memoryTypeBits()&(1<<i))!=0&&(mp.memoryTypes(i).propertyFlags()&VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)!=0){type=i;break;}if(type<0)throw new AssertionError("Host visible readback memory");VkMemoryAllocateInfo ai=VkMemoryAllocateInfo.calloc(stack).sType$Default().allocationSize(req.size()).memoryTypeIndex(type);check(vkAllocateMemory(device,ai,null,handle),"readback allocation");long memory=handle.get(0);check(vkBindBufferMemory(device,buffer,memory,0),"readback binding");check(vkMapMemory(device,memory,0,VK_WHOLE_SIZE,0,ptr),"readback map");ByteBuffer pixels=memByteBuffer(ptr.get(0),bytes).order(ByteOrder.nativeOrder());
   long vertex,fragment,pipelineLayout,pipeline,commandPool,fence;
   VkShaderModuleCreateInfo sm=VkShaderModuleCreateInfo.calloc(stack).sType$Default();sm.pCode(ClientPresentCode25.vertex(stack));check(vkCreateShaderModule(device,sm,null,handle),"vertex module");vertex=handle.get(0);sm.pCode(ClientPresentCode25.fragment(stack));check(vkCreateShaderModule(device,sm,null,handle),"fragment module");fragment=handle.get(0);
   VkPushConstantRange.Buffer push=VkPushConstantRange.calloc(1,stack);push.get(0).stageFlags(VK_SHADER_STAGE_FRAGMENT_BIT).offset(0).size(12);VkPipelineLayoutCreateInfo pl=VkPipelineLayoutCreateInfo.calloc(stack).sType$Default().pPushConstantRanges(push);check(vkCreatePipelineLayout(device,pl,null,handle),"vkCreatePipelineLayout");pipelineLayout=handle.get(0);
   VkPipelineShaderStageCreateInfo.Buffer stages=VkPipelineShaderStageCreateInfo.calloc(2,stack);stages.get(0).sType$Default().stage(VK_SHADER_STAGE_VERTEX_BIT).module(vertex).pName(stack.UTF8("main"));stages.get(1).sType$Default().stage(VK_SHADER_STAGE_FRAGMENT_BIT).module(fragment).pName(stack.UTF8("main"));
   VkPipelineVertexInputStateCreateInfo input=VkPipelineVertexInputStateCreateInfo.calloc(stack).sType$Default();VkPipelineInputAssemblyStateCreateInfo assembly=VkPipelineInputAssemblyStateCreateInfo.calloc(stack).sType$Default().topology(VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST);
   VkViewport.Buffer viewport=VkViewport.calloc(1,stack);viewport.get(0).x(0).y(0).width(width).height(height).minDepth(0).maxDepth(1);VkRect2D.Buffer scissors=VkRect2D.calloc(1,stack);scissors.get(0).extent().set(width,height);
   VkPipelineViewportStateCreateInfo vp=VkPipelineViewportStateCreateInfo.calloc(stack).sType$Default().pViewports(viewport).pScissors(scissors);
   VkPipelineRasterizationStateCreateInfo raster=VkPipelineRasterizationStateCreateInfo.calloc(stack).sType$Default().polygonMode(VK_POLYGON_MODE_FILL).cullMode(VK_CULL_MODE_NONE).frontFace(VK_FRONT_FACE_COUNTER_CLOCKWISE).lineWidth(1);
   VkPipelineMultisampleStateCreateInfo ms=VkPipelineMultisampleStateCreateInfo.calloc(stack).sType$Default().rasterizationSamples(VK_SAMPLE_COUNT_1_BIT);
   VkPipelineColorBlendAttachmentState.Buffer colors=VkPipelineColorBlendAttachmentState.calloc(1,stack);colors.get(0).colorWriteMask(VK_COLOR_COMPONENT_R_BIT|VK_COLOR_COMPONENT_G_BIT|VK_COLOR_COMPONENT_B_BIT|VK_COLOR_COMPONENT_A_BIT);
   VkPipelineColorBlendStateCreateInfo blend=VkPipelineColorBlendStateCreateInfo.calloc(stack).sType$Default().pAttachments(colors);
   VkGraphicsPipelineCreateInfo.Buffer gp=VkGraphicsPipelineCreateInfo.calloc(1,stack);gp.get(0).sType$Default().pStages(stages).pVertexInputState(input).pInputAssemblyState(assembly).pViewportState(vp).pRasterizationState(raster).pMultisampleState(ms).pColorBlendState(blend).layout(pipelineLayout).renderPass(renderPass).subpass(0);
   stage("compile real vertex/fragment graphics pipeline");check(vkCreateGraphicsPipelines(device,VK_NULL_HANDLE,gp,null,handle),"vkCreateGraphicsPipelines");pipeline=handle.get(0);stage("graphics pipeline compiled");
   VkCommandPoolCreateInfo cp=VkCommandPoolCreateInfo.calloc(stack).sType$Default().queueFamilyIndex(family).flags(VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT);check(vkCreateCommandPool(device,cp,null,handle),"vkCreateCommandPool");commandPool=handle.get(0);
   VkCommandBufferAllocateInfo ca=VkCommandBufferAllocateInfo.calloc(stack).sType$Default().commandPool(commandPool).level(VK_COMMAND_BUFFER_LEVEL_PRIMARY).commandBufferCount(1);check(vkAllocateCommandBuffers(device,ca,ptr),"vkAllocateCommandBuffers");VkCommandBuffer cmd=new VkCommandBuffer(ptr.get(0),device);check(vkCreateFence(device,VkFenceCreateInfo.calloc(stack).sType$Default(),null,handle),"vkCreateFence");fence=handle.get(0);
   ask("SDL window rendering. Release controls, then press X, Circle, D-pad Left and move the left stick. Two-minute input limit.");
   long deadline=System.nanoTime()+120_000_000_000L;int previousMask=-1,frames=0;
   for(int frame=0;frame<90||inputMask!=15||stateMask!=15;frame++) {
    if(System.nanoTime()>deadline)throw new IllegalStateException("SDL input deadline: event mask"+inputMask+" state mask"+stateMask+"; need X/Circle/D-pad Left/left stick; keep app open for logs");
    try(MemoryStack poll=MemoryStack.stackPush()){input(poll);}
    if(inputMask!=previousMask){stage("real SDL event input mask"+inputMask+" state mask"+stateMask);previousMask=inputMask;}
    frames=frame+1;
    int phase=(frame/30)%3;IntBuffer indexBuffer=stack.mallocInt(1);check(vkAcquireNextImageKHR(device,swapchain,5_000_000_000L,acquired,VK_NULL_HANDLE,indexBuffer),"vkAcquireNextImageKHR frame"+frame);int index=indexBuffer.get(0);if(index<0||index>=imageCount)throw new AssertionError("Acquired image bound");
    for(int i=0;i<bytes;i++)pixels.put(i,(byte)0x6d);
    try(MemoryStack work=MemoryStack.stackPush()) {
     VkMappedMemoryRange.Buffer range=VkMappedMemoryRange.calloc(1,work);range.get(0).sType$Default().memory(memory).size(VK_WHOLE_SIZE);check(vkFlushMappedMemoryRanges(device,range),"flush readback guards");check(vkResetCommandBuffer(cmd,0),"reset commands");check(vkBeginCommandBuffer(cmd,VkCommandBufferBeginInfo.calloc(work).sType$Default().flags(VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)),"begin commands");
     VkBufferMemoryBarrier.Buffer bb=VkBufferMemoryBarrier.calloc(1,work);bb.get(0).sType$Default().srcAccessMask(VK_ACCESS_HOST_WRITE_BIT).dstAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).buffer(buffer).size(VK_WHOLE_SIZE);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_HOST_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,null,bb,null);
     VkImageMemoryBarrier.Buffer ib=VkImageMemoryBarrier.calloc(1,work);ib.get(0).sType$Default().srcAccessMask(0).dstAccessMask(VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT).oldLayout(VK_IMAGE_LAYOUT_UNDEFINED).newLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).image(images.get(index));ib.get(0).subresourceRange().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).levelCount(1).layerCount(1);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,0,null,null,ib);
     VkClearValue.Buffer clear=VkClearValue.calloc(1,work);clear.get(0).color().float32(0,1).float32(2,1).float32(3,1);VkRenderPassBeginInfo begin=VkRenderPassBeginInfo.calloc(work).sType$Default().renderPass(renderPass).framebuffer(framebuffers[index]).pClearValues(clear);begin.renderArea().extent().set(width,height);vkCmdBeginRenderPass(cmd,begin,VK_SUBPASS_CONTENTS_INLINE);vkCmdBindPipeline(cmd,VK_PIPELINE_BIND_POINT_GRAPHICS,pipeline);vkCmdPushConstants(cmd,pipelineLayout,VK_SHADER_STAGE_FRAGMENT_BIT,0,work.ints(phase,width,height));vkCmdDraw(cmd,3,1,0,0);vkCmdEndRenderPass(cmd);
     ib.get(0).srcAccessMask(VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT).dstAccessMask(VK_ACCESS_TRANSFER_READ_BIT).oldLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL).newLayout(VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,null,null,ib);
     VkBufferImageCopy.Buffer copy=VkBufferImageCopy.calloc(sampleCount,work);int n=0;for(int sy:samples)for(int sx:samples){int x=Math.min(width-1,(sx*width+255)/256),y=Math.min(height-1,(sy*height+255)/256);copy.get(n).bufferOffset(n*4);copy.get(n).imageSubresource().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).layerCount(1);copy.get(n).imageOffset().set(x,y,0);copy.get(n).imageExtent().set(1,1,1);n++;}vkCmdCopyImageToBuffer(cmd,images.get(index),VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,buffer,copy);
     bb.get(0).srcAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).dstAccessMask(VK_ACCESS_HOST_READ_BIT);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,null,bb,null);ib.get(0).srcAccessMask(VK_ACCESS_TRANSFER_READ_BIT).dstAccessMask(0).oldLayout(VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL).newLayout(VK_IMAGE_LAYOUT_PRESENT_SRC_KHR);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT,0,null,null,ib);check(vkEndCommandBuffer(cmd),"end commands");check(vkResetFences(device,fence),"reset fence");
     VkSubmitInfo.Buffer submit=VkSubmitInfo.calloc(1,work);submit.get(0).sType$Default().pWaitSemaphores(work.longs(acquired)).pWaitDstStageMask(work.ints(VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT)).pCommandBuffers(work.pointers(cmd.address())).pSignalSemaphores(work.longs(rendered[index]));check(vkQueueSubmit(queue,submit,fence),"submit frame"+frame);check(vkWaitForFences(device,fence,true,5_000_000_000L),"fence frame"+frame);check(vkInvalidateMappedMemoryRanges(device,range),"invalidate samples");
     n=0;for(int sy:samples)for(int sx:samples){int x=Math.min(width-1,(sx*width+255)/256),y=Math.min(height-1,(sy*height+255)/256);if(pixels.getInt(n++*4)!=expected(x*256/width,y*256/height,phase))throw new AssertionError("Swapchain pixel sample mismatch frame"+frame+" x"+x+" y"+y);}for(int i=sampleCount*4;i<bytes;i++)if(pixels.get(i)!=(byte)0x6d)throw new AssertionError("Swapchain readback guard mismatch");
     VkPresentInfoKHR present=VkPresentInfoKHR.calloc(work).sType$Default().pWaitSemaphores(work.longs(rendered[index])).swapchainCount(1).pSwapchains(work.longs(swapchain)).pImageIndices(work.ints(index));check(vkQueuePresentKHR(queue,present),"vkQueuePresentKHR frame"+frame);stage("present frame"+frame+" phase"+phase+" image"+index+" samples/guards PASS");
    }
   }
   stage("PASS SDL window/Vulkan surface/gamepad state+events: frames"+frames+" eventMask"+inputMask+" stateMask"+stateMask+"; sampled pixels/guards and direct FIFO presents; SDL/native display context retained until app closes");
  }
 }
 public static void main(String[] args){
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.VULKAN_EXPLICIT_INIT.set(true);Configuration.SDL_LIBRARY_NAME.set(System.mapLibraryName("ps5sdl"));Library.initialize();System.loadLibrary("ps5clientgpu");System.loadLibrary("ps5sdl");
  sdl(SDL_Init(SDL_INIT_VIDEO|SDL_INIT_GAMEPAD),"SDL_Init VIDEO/GAMEPAD");
  if(!"ps5".equals(SDL_GetCurrentVideoDriver()))throw new AssertionError("Expected actual PS5 SDL video backend: "+SDL_GetCurrentVideoDriver());
  try(MemoryStack stack=MemoryStack.stackPush()) {
   int display=SDL_GetPrimaryDisplay();SDL_DisplayMode mode=SDL_GetCurrentDisplayMode(display);if(mode==null)throw new IllegalStateException("SDL display mode: "+SDL_GetError());
   window=SDL_CreateWindow("PS5 Java SDL012",mode.w(),mode.h(),SDL_WINDOW_VULKAN|SDL_WINDOW_FULLSCREEN);if(window==0)throw new IllegalStateException("SDL_CreateWindow: "+SDL_GetError());
   java.nio.IntBuffer pads=SDL_GetGamepads();if(pads==null||pads.remaining()==0)throw new IllegalStateException("No SDL gamepad: "+SDL_GetError());
   try{pad=SDL_OpenGamepad(pads.get(0));}finally{org.lwjgl.sdl.SDLStdinc.SDL_free(pads);}
   if(pad==0)throw new IllegalStateException("SDL_OpenGamepad: "+SDL_GetError());stage("real SDL video="+SDL_GetCurrentVideoDriver()+" version="+SDLVersion.SDL_GetVersion()+" gamepad="+SDL_GetGamepadName(pad));
   long proc=SDL_Vulkan_GetVkGetInstanceProcAddr();if(proc==0)throw new IllegalStateException("SDL Vulkan function provider: "+SDL_GetError());
   VK.create((FunctionProvider)name -> memASCII(memAddress(name)).equals("vkGetInstanceProcAddr")?proc:JNI.invokePPP(0L,memAddress(name),proc));
   try{run();}finally{VK.destroy();}
  }
 }
}
