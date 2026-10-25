import java.nio.*;
import org.lwjgl.PointerBuffer;
import org.lwjgl.system.*;
import org.lwjgl.system.ps5.PS5Library;
import org.lwjgl.vulkan.*;
import static org.lwjgl.vulkan.VK10.*;
import static org.lwjgl.vulkan.VK11.VK_API_VERSION_1_1;
import static org.lwjgl.system.MemoryUtil.*;

/** Selected original LWJGL compute commands; no window or game code. */
public final class ClientShader25 {
 public static native void checkpoint(String text);
 private static void stage(String text){checkpoint("LWJGL Shader009 @"+System.nanoTime()+"ns: "+text);}
 private static void check(int result,String call){if(result!=VK_SUCCESS)throw new IllegalStateException(call+" VkResult="+result);}
 private static void cycle(int cycle,boolean host) {
  VkInstance instance=null;VkDevice device=null;
  long buffer=0,memory=0,shader=0,setLayout=0,pipelineLayout=0,pipeline=0,descriptorPool=0,commandPool=0,fence=0;
  boolean mapped=false,incomplete=false;
  try(MemoryStack stack=MemoryStack.stackPush()) {
   PointerBuffer ptr=stack.mallocPointer(1);LongBuffer handle=stack.mallocLong(1);IntBuffer count=stack.mallocInt(1);
   VkApplicationInfo app=VkApplicationInfo.calloc(stack).sType$Default().pApplicationName(stack.UTF8("PS5 Java Shader009")).apiVersion(VK_API_VERSION_1_1);
   VkInstanceCreateInfo ii=VkInstanceCreateInfo.calloc(stack).sType$Default().pApplicationInfo(app);
   stage("create shader session "+cycle);check(vkCreateInstance(ii,null,ptr),"vkCreateInstance");instance=new VkInstance(ptr.get(0),ii);
   check(vkEnumeratePhysicalDevices(instance,count,null),"count devices");if(count.get(0)<1||count.get(0)>16)throw new AssertionError("GPU count");
   PointerBuffer devices=stack.mallocPointer(count.get(0));check(vkEnumeratePhysicalDevices(instance,count,devices),"enumerate devices");VkPhysicalDevice physical=new VkPhysicalDevice(devices.get(0),instance);
   VkPhysicalDeviceProperties properties=VkPhysicalDeviceProperties.malloc(stack);vkGetPhysicalDeviceProperties(physical,properties);
   if(properties.limits().maxComputeWorkGroupInvocations()<64||properties.limits().maxComputeWorkGroupSize(0)<64||Integer.compareUnsigned(properties.limits().maxStorageBufferRange(),65536)<0)throw new AssertionError("Compute limits");
   stage("device "+properties.deviceNameString());
   vkGetPhysicalDeviceQueueFamilyProperties(physical,count,null);if(count.get(0)<1||count.get(0)>64)throw new AssertionError("Queue count");
   VkQueueFamilyProperties.Buffer families=VkQueueFamilyProperties.malloc(count.get(0),stack);vkGetPhysicalDeviceQueueFamilyProperties(physical,count,families);
   int family=-1;for(int i=0;i<count.get(0);i++)if(families.get(i).queueCount()>0&&(families.get(i).queueFlags()&VK_QUEUE_COMPUTE_BIT)!=0){family=i;break;}
   if(family<0)throw new AssertionError("No compute queue");
   VkDeviceQueueCreateInfo.Buffer qi=VkDeviceQueueCreateInfo.calloc(1,stack);qi.get(0).sType$Default().queueFamilyIndex(family).pQueuePriorities(stack.floats(1));
   VkDeviceCreateInfo di=VkDeviceCreateInfo.calloc(stack).sType$Default().pQueueCreateInfos(qi);
   if(host){check(vkEnumerateDeviceExtensionProperties(physical,(ByteBuffer)null,count,null),"count extensions");VkExtensionProperties.Buffer ex=VkExtensionProperties.malloc(count.get(0),stack);check(vkEnumerateDeviceExtensionProperties(physical,(ByteBuffer)null,count,ex),"enumerate extensions");for(int i=0;i<count.get(0);i++)if(ex.get(i).extensionNameString().equals("VK_KHR_portability_subset")){di.ppEnabledExtensionNames(stack.pointers(stack.UTF8("VK_KHR_portability_subset")));break;}}
   check(vkCreateDevice(physical,di,null,ptr),"vkCreateDevice");device=new VkDevice(ptr.get(0),physical,di);vkGetDeviceQueue(device,family,0,ptr);VkQueue queue=new VkQueue(ptr.get(0),device);
   VkBufferCreateInfo bi=VkBufferCreateInfo.calloc(stack).sType$Default().size(65536).usage(VK_BUFFER_USAGE_STORAGE_BUFFER_BIT).sharingMode(VK_SHARING_MODE_EXCLUSIVE);
   check(vkCreateBuffer(device,bi,null,handle),"vkCreateBuffer");buffer=handle.get(0);
   VkMemoryRequirements req=VkMemoryRequirements.malloc(stack);vkGetBufferMemoryRequirements(device,buffer,req);
   VkPhysicalDeviceMemoryProperties mp=VkPhysicalDeviceMemoryProperties.malloc(stack);vkGetPhysicalDeviceMemoryProperties(physical,mp);
   int type=-1;for(int i=0;i<mp.memoryTypeCount();i++)if((req.memoryTypeBits()&(1<<i))!=0&&(mp.memoryTypes(i).propertyFlags()&VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)!=0){type=i;break;}
   if(type<0)throw new AssertionError("No host visible memory");
   VkMemoryAllocateInfo ai=VkMemoryAllocateInfo.calloc(stack).sType$Default().allocationSize(req.size()).memoryTypeIndex(type);
   check(vkAllocateMemory(device,ai,null,handle),"vkAllocateMemory");memory=handle.get(0);check(vkBindBufferMemory(device,buffer,memory,0),"vkBindBufferMemory");
   check(vkMapMemory(device,memory,0,VK_WHOLE_SIZE,0,ptr),"vkMapMemory");mapped=true;ByteBuffer words=memByteBuffer(ptr.get(0),65536).order(ByteOrder.nativeOrder());
   VkShaderModuleCreateInfo sm=VkShaderModuleCreateInfo.calloc(stack).sType$Default().pCode(ClientShaderCode25.code(stack));
   stage("create validated SPIR-V shader module");check(vkCreateShaderModule(device,sm,null,handle),"vkCreateShaderModule");shader=handle.get(0);
   VkDescriptorSetLayoutBinding.Buffer binding=VkDescriptorSetLayoutBinding.calloc(1,stack);binding.get(0).binding(0).descriptorType(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER).descriptorCount(1).stageFlags(VK_SHADER_STAGE_COMPUTE_BIT);
   VkDescriptorSetLayoutCreateInfo sl=VkDescriptorSetLayoutCreateInfo.calloc(stack).sType$Default().pBindings(binding);check(vkCreateDescriptorSetLayout(device,sl,null,handle),"vkCreateDescriptorSetLayout");setLayout=handle.get(0);
   VkPushConstantRange.Buffer push=VkPushConstantRange.calloc(1,stack);push.get(0).stageFlags(VK_SHADER_STAGE_COMPUTE_BIT).offset(0).size(8);
   VkPipelineLayoutCreateInfo pl=VkPipelineLayoutCreateInfo.calloc(stack).sType$Default().pSetLayouts(stack.longs(setLayout)).pPushConstantRanges(push);
   check(vkCreatePipelineLayout(device,pl,null,handle),"vkCreatePipelineLayout");pipelineLayout=handle.get(0);
   VkComputePipelineCreateInfo.Buffer ci=VkComputePipelineCreateInfo.calloc(1,stack);ci.get(0).sType$Default().layout(pipelineLayout);ci.get(0).stage().sType$Default().stage(VK_SHADER_STAGE_COMPUTE_BIT).module(shader).pName(stack.UTF8("main"));
   stage("compile real compute pipeline through vkCreateComputePipelines");check(vkCreateComputePipelines(device,VK_NULL_HANDLE,ci,null,handle),"vkCreateComputePipelines");pipeline=handle.get(0);stage("compute pipeline compiled");
   VkDescriptorPoolSize.Buffer ps=VkDescriptorPoolSize.calloc(1,stack);ps.get(0).type(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER).descriptorCount(1);
   VkDescriptorPoolCreateInfo dp=VkDescriptorPoolCreateInfo.calloc(stack).sType$Default().maxSets(1).pPoolSizes(ps);check(vkCreateDescriptorPool(device,dp,null,handle),"vkCreateDescriptorPool");descriptorPool=handle.get(0);
   VkDescriptorSetAllocateInfo sa=VkDescriptorSetAllocateInfo.calloc(stack).sType$Default().descriptorPool(descriptorPool).pSetLayouts(stack.longs(setLayout));check(vkAllocateDescriptorSets(device,sa,handle),"vkAllocateDescriptorSets");long set=handle.get(0);
   VkDescriptorBufferInfo.Buffer db=VkDescriptorBufferInfo.calloc(1,stack);db.get(0).buffer(buffer).offset(0).range(65536);
   VkWriteDescriptorSet.Buffer write=VkWriteDescriptorSet.calloc(1,stack);write.get(0).sType$Default().dstSet(set).dstBinding(0).descriptorType(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER).descriptorCount(1).pBufferInfo(db);vkUpdateDescriptorSets(device,write,null);
   VkCommandPoolCreateInfo cp=VkCommandPoolCreateInfo.calloc(stack).sType$Default().queueFamilyIndex(family).flags(VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT);check(vkCreateCommandPool(device,cp,null,handle),"vkCreateCommandPool");commandPool=handle.get(0);
   VkCommandBufferAllocateInfo ca=VkCommandBufferAllocateInfo.calloc(stack).sType$Default().commandPool(commandPool).level(VK_COMMAND_BUFFER_LEVEL_PRIMARY).commandBufferCount(1);check(vkAllocateCommandBuffers(device,ca,ptr),"vkAllocateCommandBuffers");VkCommandBuffer cmd=new VkCommandBuffer(ptr.get(0),device);
   check(vkCreateFence(device,VkFenceCreateInfo.calloc(stack).sType$Default(),null,handle),"vkCreateFence");fence=handle.get(0);
   for(int size:new int[]{1,63,64,65,1024,4096}) {
    int salt=0x5a00beef^cycle^size;
    for(int i=0;i<65536/4;i++)words.putInt(i*4,i<size?i^salt:0x6d6d6d6d);
    try(MemoryStack work=MemoryStack.stackPush()) {
     VkMappedMemoryRange.Buffer ranges=VkMappedMemoryRange.calloc(1,work);ranges.get(0).sType$Default().memory(memory).size(VK_WHOLE_SIZE);check(vkFlushMappedMemoryRanges(device,ranges),"vkFlushMappedMemoryRanges");
     check(vkResetCommandBuffer(cmd,0),"vkResetCommandBuffer");check(vkBeginCommandBuffer(cmd,VkCommandBufferBeginInfo.calloc(work).sType$Default().flags(VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)),"vkBeginCommandBuffer");
     VkBufferMemoryBarrier.Buffer barrier=VkBufferMemoryBarrier.calloc(1,work);barrier.get(0).sType$Default().srcAccessMask(VK_ACCESS_HOST_WRITE_BIT).dstAccessMask(VK_ACCESS_SHADER_READ_BIT|VK_ACCESS_SHADER_WRITE_BIT).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).buffer(buffer).size(VK_WHOLE_SIZE);
     vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_HOST_BIT,VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,0,null,barrier,null);
     vkCmdBindPipeline(cmd,VK_PIPELINE_BIND_POINT_COMPUTE,pipeline);vkCmdBindDescriptorSets(cmd,VK_PIPELINE_BIND_POINT_COMPUTE,pipelineLayout,0,work.longs(set),null);
     vkCmdPushConstants(cmd,pipelineLayout,VK_SHADER_STAGE_COMPUTE_BIT,0,work.ints(size,salt));vkCmdDispatch(cmd,(size+63)/64,1,1);
     barrier.get(0).srcAccessMask(VK_ACCESS_SHADER_WRITE_BIT).dstAccessMask(VK_ACCESS_HOST_READ_BIT);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,null,barrier,null);
     check(vkEndCommandBuffer(cmd),"vkEndCommandBuffer");check(vkResetFences(device,fence),"vkResetFences");VkSubmitInfo.Buffer submit=VkSubmitInfo.calloc(1,work);submit.get(0).sType$Default().pCommandBuffers(work.pointers(cmd.address()));
     stage("dispatch shader cycle"+cycle+" words"+size);incomplete=true;check(vkQueueSubmit(queue,submit,fence),"vkQueueSubmit");check(vkWaitForFences(device,fence,true,5_000_000_000L),"vkWaitForFences; relaunch if incomplete");incomplete=false;
     check(vkInvalidateMappedMemoryRanges(device,ranges),"vkInvalidateMappedMemoryRanges");
     for(int i=0;i<65536/4;i++){int expected=i<size?((i^salt)*1664525+1013904223)^salt:0x6d6d6d6d;if(words.getInt(i*4)!=expected)throw new AssertionError("Shader output/guard mismatch at word"+i+" count"+size);}
    }
   }
   stage("shader cycle"+cycle+" all output/guard words PASS");
  } finally {
   if(!incomplete && device!=null){if(fence!=0)vkDestroyFence(device,fence,null);if(commandPool!=0)vkDestroyCommandPool(device,commandPool,null);if(descriptorPool!=0)vkDestroyDescriptorPool(device,descriptorPool,null);if(pipeline!=0)vkDestroyPipeline(device,pipeline,null);if(pipelineLayout!=0)vkDestroyPipelineLayout(device,pipelineLayout,null);if(setLayout!=0)vkDestroyDescriptorSetLayout(device,setLayout,null);if(shader!=0)vkDestroyShaderModule(device,shader,null);if(mapped)vkUnmapMemory(device,memory);if(buffer!=0)vkDestroyBuffer(device,buffer,null);if(memory!=0)vkFreeMemory(device,memory,null);vkDestroyDevice(device,null);}
   if(!incomplete && instance!=null)vkDestroyInstance(instance,null);
  }
 }
 public static void main(String[] args){
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.VULKAN_EXPLICIT_INIT.set(true);Library.initialize();String host=System.getProperty("ps5.test.vulkanLibrary");
  if(host==null){System.loadLibrary("ps5clientgpu");VK.create(new PS5Library(System.mapLibraryName("ps5clientgpu")));}else VK.create(new PS5Library(host));
  try{for(int i=0;i<3;i++)cycle(i,host!=null);}finally{VK.destroy();}
  stage("PASS original LWJGL compute pipeline:18 dispatches, full output/guard checks,3 session lifecycles");
 }
}
