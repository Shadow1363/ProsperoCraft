import java.nio.*;
import org.lwjgl.PointerBuffer;
import org.lwjgl.system.*;
import org.lwjgl.system.ps5.PS5Library;
import org.lwjgl.vulkan.*;
import static org.lwjgl.vulkan.VK10.*;
import static org.lwjgl.vulkan.VK11.VK_API_VERSION_1_1;
import static org.lwjgl.system.MemoryUtil.*;
import static org.lwjgl.util.shaderc.Shaderc.*;

/** Selected original LWJGL compute commands; no window or game code. */
public final class ClientRuntimeShader25 {
 public static native void checkpoint(String text);
 private static void stage(String text){checkpoint("Runtime Shader018 @"+System.nanoTime()+"ns: "+text);}
 private static void check(int result,String call){if(result!=VK_SUCCESS)throw new IllegalStateException(call+" VkResult="+result);}
 private static final String SOURCE="""
#version 450
layout(local_size_x=64) in;
layout(set=0,binding=0,std430) buffer Words { uint values[]; } words;
layout(push_constant) uniform Parameters { uint count; uint salt; } parameters;
void main() {
    uint i=gl_GlobalInvocationID.x;
    if(i<parameters.count)
        words.values[i]=(words.values[i]*1664525u+1013904223u)^parameters.salt;
}
""";
 private static ByteBuffer compile(int cycle) {
  stage("before original Shaderc Java class initialization cycle"+cycle);
  try{Class.forName("org.lwjgl.util.shaderc.Shaderc");}catch(ClassNotFoundException e){throw new AssertionError(e);}
  stage("original Shaderc class initialized; before native shaderc_compiler_initialize cycle"+cycle);
  long compiler=shaderc_compiler_initialize();if(compiler==0)throw new IllegalStateException("shaderc compiler allocation failed");
  stage("native shaderc_compiler_initialize returned; before options");
  long options=0;
  try {
   stage("before native shaderc options allocation");
   options=shaderc_compile_options_initialize();if(options==0)throw new IllegalStateException("shaderc options allocation failed");
   shaderc_compile_options_set_target_env(options,shaderc_target_env_vulkan,shaderc_env_version_vulkan_1_1);
   shaderc_compile_options_set_target_spirv(options,shaderc_spirv_version_1_3);
   shaderc_compile_options_set_optimization_level(options,cycle%2==0?shaderc_optimization_level_zero:shaderc_optimization_level_size);
   stage("before native invalid-GLSL compile");
   long bad=shaderc_compile_into_spv(compiler,"#version 450\nvoid main(){ this_is_invalid; }\n",shaderc_compute_shader,"invalid-canary.comp","main",options);
   if(bad==0)throw new AssertionError("Invalid source returned null result");
   try {if(shaderc_result_get_compilation_status(bad)==shaderc_compilation_status_success||shaderc_result_get_num_errors(bad)==0||shaderc_result_get_error_message(bad).isEmpty())throw new AssertionError("Invalid GLSL did not produce real compiler diagnostics");}
   finally {shaderc_result_release(bad);}
   stage("invalid GLSL diagnostic control PASS; compile valid GLSL now");
   long result=shaderc_compile_into_spv(compiler,SOURCE,shaderc_compute_shader,"runtime-canary.comp","main",options);
   if(result==0)throw new IllegalStateException("shaderc compile returned null");
   try {
    if(shaderc_result_get_compilation_status(result)!=shaderc_compilation_status_success)throw new IllegalStateException("Actual shaderc error: "+shaderc_result_get_error_message(result));
    long length=shaderc_result_get_length(result);if(length<20||length>1024*1024||length%4!=0)throw new AssertionError("Bounded SPIR-V result length"+length);
    ByteBuffer actual=shaderc_result_get_bytes(result).order(ByteOrder.nativeOrder());if(actual.getInt(0)!=0x07230203)throw new AssertionError("SPIR-V magic");
    ByteBuffer copy=memAlloc((int)length).order(ByteOrder.nativeOrder());copy.put(actual).flip();stage("GLSL compiled on runtime: SPIR-V bytes"+length);return copy;
   }finally{shaderc_result_release(result);}
  }finally{if(options!=0)shaderc_compile_options_release(options);shaderc_compiler_release(compiler);}
 }
 private static void cycle(int cycle,boolean host) {
  ByteBuffer runtimeCode=compile(cycle);
  VkInstance instance=null;VkDevice device=null;
  long buffer=0,memory=0,shader=0,setLayout=0,pipelineLayout=0,pipeline=0,descriptorPool=0,commandPool=0,fence=0;
  boolean mapped=false,incomplete=false;
  try(MemoryStack stack=MemoryStack.stackPush()) {
   PointerBuffer ptr=stack.mallocPointer(1);LongBuffer handle=stack.mallocLong(1);IntBuffer count=stack.mallocInt(1);
   VkApplicationInfo app=VkApplicationInfo.calloc(stack).sType$Default().pApplicationName(stack.UTF8("PS5 Java Runtime Shader018")).apiVersion(VK_API_VERSION_1_1);
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
   try {
    VkShaderModuleCreateInfo sm=VkShaderModuleCreateInfo.calloc(stack).sType$Default().pCode(runtimeCode);
    stage("create shader module from runtime-compiled GLSL");check(vkCreateShaderModule(device,sm,null,handle),"vkCreateShaderModule");shader=handle.get(0);
   }finally{memFree(runtimeCode);runtimeCode=null;}
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
   if(runtimeCode!=null)memFree(runtimeCode);
   if(!incomplete && device!=null){if(fence!=0)vkDestroyFence(device,fence,null);if(commandPool!=0)vkDestroyCommandPool(device,commandPool,null);if(descriptorPool!=0)vkDestroyDescriptorPool(device,descriptorPool,null);if(pipeline!=0)vkDestroyPipeline(device,pipeline,null);if(pipelineLayout!=0)vkDestroyPipelineLayout(device,pipelineLayout,null);if(setLayout!=0)vkDestroyDescriptorSetLayout(device,setLayout,null);if(shader!=0)vkDestroyShaderModule(device,shader,null);if(mapped)vkUnmapMemory(device,memory);if(buffer!=0)vkDestroyBuffer(device,buffer,null);if(memory!=0)vkFreeMemory(device,memory,null);vkDestroyDevice(device,null);}
   if(!incomplete && instance!=null)vkDestroyInstance(instance,null);
  }
 }
 public static void main(String[] args){
  Configuration.SHADERC_LIBRARY_NAME.set(System.getProperty("ps5.test.shadercLibrary",System.mapLibraryName("ps5shaderc")));
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.VULKAN_EXPLICIT_INIT.set(true);Library.initialize();String host=System.getProperty("ps5.test.vulkanLibrary");
  if(host==null){System.loadLibrary("ps5shaderc");System.loadLibrary("ps5clientgpu");VK.create(new PS5Library(System.mapLibraryName("ps5clientgpu")));}else VK.create(new PS5Library(host));
  try{for(int i=0;i<3;i++)cycle(i,host!=null);}finally{VK.destroy();}
  stage("PASS actual runtime GLSL compiler:3 compilers/invalid diagnostic controls/SPIR-V results,18 real GPU dispatches,full output/guard checks,3 session lifecycles");
 }
}
