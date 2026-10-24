import java.nio.*;
import org.lwjgl.PointerBuffer;
import org.lwjgl.system.*;
import org.lwjgl.system.ps5.PS5Library;
import org.lwjgl.vulkan.*;
import static org.lwjgl.system.MemoryUtil.*;
import static org.lwjgl.vulkan.VK10.*;
import static org.lwjgl.vulkan.VK11.VK_API_VERSION_1_1;

/** Unmodified upstream LWJGL Vulkan structs, capability tables and command bindings. */
public final class ClientVulkan25 {
 public static native void checkpoint(String text);
 private static void check(int result,String call) {if(result!=VK_SUCCESS)throw new IllegalStateException(call+" VkResult="+result);}
 private static void stage(String text){checkpoint("LWJGL Vulkan008 @"+System.nanoTime()+"ns: "+text);}
 private static void rejected(Runnable call) {
  try{call.run();}catch(IllegalStateException expected){return;}
  throw new AssertionError("Expected duplicate VK.create rejection");
 }
 private static final class Allocation implements AutoCloseable {
  final VkDevice device;long buffer,memory;ByteBuffer bytes;boolean retained;
  Allocation(VkDevice device,VkPhysicalDeviceMemoryProperties properties,int size) {
   this.device=device;
   try(MemoryStack stack=MemoryStack.stackPush()) {
    LongBuffer pointer=stack.mallocLong(1);
    VkBufferCreateInfo info=VkBufferCreateInfo.calloc(stack).sType$Default().size(size)
     .usage(VK_BUFFER_USAGE_TRANSFER_SRC_BIT|VK_BUFFER_USAGE_TRANSFER_DST_BIT).sharingMode(VK_SHARING_MODE_EXCLUSIVE);
    check(vkCreateBuffer(device,info,null,pointer),"vkCreateBuffer");buffer=pointer.get(0);
    VkMemoryRequirements requirements=VkMemoryRequirements.malloc(stack);vkGetBufferMemoryRequirements(device,buffer,requirements);
    int type=-1;
    for(int i=0;i<properties.memoryTypeCount();i++)if((requirements.memoryTypeBits()&(1<<i))!=0&&(properties.memoryTypes(i).propertyFlags()&VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)!=0){type=i;break;}
    if(type<0)throw new AssertionError("No host visible Vulkan memory");
    VkMemoryAllocateInfo allocate=VkMemoryAllocateInfo.calloc(stack).sType$Default().allocationSize(requirements.size()).memoryTypeIndex(type);
    check(vkAllocateMemory(device,allocate,null,pointer),"vkAllocateMemory");memory=pointer.get(0);
    check(vkBindBufferMemory(device,buffer,memory,0),"vkBindBufferMemory");
    PointerBuffer mapped=stack.mallocPointer(1);check(vkMapMemory(device,memory,0,VK_WHOLE_SIZE,0,mapped),"vkMapMemory");
    bytes=memByteBuffer(mapped.get(0),size).order(ByteOrder.nativeOrder());
   }catch(Throwable e){close();throw e;}
  }
  public void close(){
   if(retained)return;
   if(bytes!=null){vkUnmapMemory(device,memory);bytes=null;}
   if(buffer!=0){vkDestroyBuffer(device,buffer,null);buffer=0;}
   if(memory!=0){vkFreeMemory(device,memory,null);memory=0;}
  }
 }
 private static void cycle(int cycle,boolean host) {
  VkInstance instance=null;VkDevice device=null;long pool=0,fence=0;boolean incomplete=false;
  try(MemoryStack stack=MemoryStack.stackPush()) {
   PointerBuffer pointer=stack.mallocPointer(1);
   VkApplicationInfo app=VkApplicationInfo.calloc(stack).sType$Default().pApplicationName(stack.UTF8("PS5 Java LWJGL Vulkan008")).apiVersion(VK_API_VERSION_1_1);
   VkInstanceCreateInfo info=VkInstanceCreateInfo.calloc(stack).sType$Default().pApplicationInfo(app);
   stage("initialize original VK10 class before native instance call");
   try {Class.forName("org.lwjgl.vulkan.VK10");}catch(ClassNotFoundException e){throw new AssertionError(e);}
   stage("VK10 class initialized; enter standard vkCreateInstance");
   check(vkCreateInstance(info,null,pointer),"vkCreateInstance");
   stage("vkCreateInstance returned; construct VkInstance capability table");
   instance=new VkInstance(pointer.get(0),info);
   stage("VkInstance capability table complete; enumerate physical devices");
   if(!instance.getCapabilities().Vulkan11)throw new AssertionError("Vulkan1.1 instance capability");
   IntBuffer count=stack.mallocInt(1);check(vkEnumeratePhysicalDevices(instance,count,null),"count physical GPUs");
   if(count.get(0)<1||count.get(0)>16)throw new AssertionError("Bounded physical GPU count");
   PointerBuffer devices=stack.mallocPointer(count.get(0));check(vkEnumeratePhysicalDevices(instance,count,devices),"enumerate physical GPUs");
   VkPhysicalDevice physical=new VkPhysicalDevice(devices.get(0),instance);
   VkPhysicalDeviceProperties properties=VkPhysicalDeviceProperties.malloc(stack);vkGetPhysicalDeviceProperties(physical,properties);stage("device "+properties.deviceNameString());
   VkPhysicalDeviceMemoryProperties memory=VkPhysicalDeviceMemoryProperties.malloc(stack);vkGetPhysicalDeviceMemoryProperties(physical,memory);
   vkGetPhysicalDeviceQueueFamilyProperties(physical,count,null);int familyCount=count.get(0);if(familyCount<1||familyCount>64)throw new AssertionError("Bounded queue count");
   VkQueueFamilyProperties.Buffer families=VkQueueFamilyProperties.malloc(familyCount,stack);vkGetPhysicalDeviceQueueFamilyProperties(physical,count,families);
   int family=-1;for(int i=0;i<familyCount;i++)if(families.get(i).queueCount()>0&&(families.get(i).queueFlags()&VK_QUEUE_GRAPHICS_BIT)!=0){family=i;break;}
   if(family<0)throw new AssertionError("No graphics transfer queue");
   VkDeviceQueueCreateInfo.Buffer queueInfo=VkDeviceQueueCreateInfo.calloc(1,stack);queueInfo.get(0).sType$Default().queueFamilyIndex(family).pQueuePriorities(stack.floats(1));
   VkDeviceCreateInfo deviceInfo=VkDeviceCreateInfo.calloc(stack).sType$Default().pQueueCreateInfos(queueInfo);
   if(host) {
    check(vkEnumerateDeviceExtensionProperties(physical,(ByteBuffer)null,count,null),"count device extensions");
    VkExtensionProperties.Buffer extensions=VkExtensionProperties.malloc(count.get(0),stack);check(vkEnumerateDeviceExtensionProperties(physical,(ByteBuffer)null,count,extensions),"enumerate device extensions");
    for(int i=0;i<count.get(0);i++)if(extensions.get(i).extensionNameString().equals("VK_KHR_portability_subset")){deviceInfo.ppEnabledExtensionNames(stack.pointers(stack.UTF8("VK_KHR_portability_subset")));break;}
   }
   stage("create device and full LWJGL device capability table");check(vkCreateDevice(physical,deviceInfo,null,pointer),"vkCreateDevice");stage("vkCreateDevice returned; construct VkDevice capability table");device=new VkDevice(pointer.get(0),physical,deviceInfo);stage("VkDevice capability table complete");
   if(device.getCapabilities().vkCmdCopyBuffer==0||device.getCapabilities().vkCmdFillBuffer==0)throw new AssertionError("Standard command table missing");
   vkGetDeviceQueue(device,family,0,pointer);VkQueue queue=new VkQueue(pointer.get(0),device);
   LongBuffer handle=stack.mallocLong(1);
   VkCommandPoolCreateInfo poolInfo=VkCommandPoolCreateInfo.calloc(stack).sType$Default().queueFamilyIndex(family).flags(VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT);
   check(vkCreateCommandPool(device,poolInfo,null,handle),"vkCreateCommandPool");pool=handle.get(0);
   VkCommandBufferAllocateInfo commands=VkCommandBufferAllocateInfo.calloc(stack).sType$Default().commandPool(pool).level(VK_COMMAND_BUFFER_LEVEL_PRIMARY).commandBufferCount(1);
   check(vkAllocateCommandBuffers(device,commands,pointer),"vkAllocateCommandBuffers");VkCommandBuffer cmd=new VkCommandBuffer(pointer.get(0),device);
   VkFenceCreateInfo fenceInfo=VkFenceCreateInfo.calloc(stack).sType$Default();check(vkCreateFence(device,fenceInfo,null,handle),"vkCreateFence");fence=handle.get(0);
   try(Allocation src=new Allocation(device,memory,65536);Allocation dst=new Allocation(device,memory,65536)) {
    for(int size:new int[]{8,256,4096,65536}) {
     int pattern=0x5a00cafe^size^cycle;
     for(int i=0;i<65536/4;i++){src.bytes.putInt(i*4,i*0x9e3779b9^pattern);dst.bytes.putInt(i*4,0x6d6d6d6d);}
     try(MemoryStack commandsStack=MemoryStack.stackPush()) {
      VkMappedMemoryRange.Buffer ranges=VkMappedMemoryRange.calloc(2,commandsStack);
      ranges.get(0).sType$Default().memory(src.memory).size(VK_WHOLE_SIZE);ranges.get(1).sType$Default().memory(dst.memory).size(VK_WHOLE_SIZE);
      check(vkFlushMappedMemoryRanges(device,ranges),"vkFlushMappedMemoryRanges");
      check(vkResetCommandBuffer(cmd,0),"vkResetCommandBuffer");
      VkCommandBufferBeginInfo begin=VkCommandBufferBeginInfo.calloc(commandsStack).sType$Default().flags(VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT);
      check(vkBeginCommandBuffer(cmd,begin),"vkBeginCommandBuffer");
      VkBufferMemoryBarrier.Buffer before=VkBufferMemoryBarrier.calloc(2,commandsStack);
      before.get(0).sType$Default().srcAccessMask(VK_ACCESS_HOST_WRITE_BIT).dstAccessMask(VK_ACCESS_TRANSFER_READ_BIT).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).buffer(src.buffer).size(VK_WHOLE_SIZE);
      before.get(1).sType$Default().srcAccessMask(VK_ACCESS_HOST_WRITE_BIT).dstAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).buffer(dst.buffer).size(VK_WHOLE_SIZE);
      vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_HOST_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,null,before,null);
      VkBufferCopy.Buffer copies=VkBufferCopy.calloc(1,commandsStack);copies.get(0).size(size/2);
      vkCmdCopyBuffer(cmd,src.buffer,dst.buffer,copies);vkCmdFillBuffer(cmd,dst.buffer,size/2,size/2,pattern);
      VkBufferMemoryBarrier.Buffer after=VkBufferMemoryBarrier.calloc(1,commandsStack);after.get(0).sType$Default().srcAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).dstAccessMask(VK_ACCESS_HOST_READ_BIT).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).buffer(dst.buffer).size(VK_WHOLE_SIZE);
      vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,null,after,null);
      check(vkEndCommandBuffer(cmd),"vkEndCommandBuffer");check(vkResetFences(device,fence),"vkResetFences");
      VkSubmitInfo.Buffer submit=VkSubmitInfo.calloc(1,commandsStack);submit.get(0).sType$Default().pCommandBuffers(commandsStack.pointers(cmd.address()));
      stage("submit GPU cycle"+cycle+" bytes"+size+" via LWJGL vkQueueSubmit");check(vkQueueSubmit(queue,submit,fence),"vkQueueSubmit");
      int wait=vkWaitForFences(device,fence,true,5_000_000_000L);
      if(wait!=VK_SUCCESS){incomplete=true;src.retained=true;dst.retained=true;throw new IllegalStateException("GPU fence incomplete VkResult="+wait+"; relaunch required");}
      VkMappedMemoryRange.Buffer invalidate=VkMappedMemoryRange.calloc(1,commandsStack);invalidate.get(0).sType$Default().memory(dst.memory).size(VK_WHOLE_SIZE);check(vkInvalidateMappedMemoryRanges(device,invalidate),"vkInvalidateMappedMemoryRanges");
      for(int i=0;i<size/4;i++){int expected=i<size/8?src.bytes.getInt(i*4):pattern;if(dst.bytes.getInt(i*4)!=expected)throw new AssertionError("LWJGL Vulkan GPU word mismatch"+i);}
      for(int i=size;i<65536;i++)if(dst.bytes.get(i)!=(byte)0x6d)throw new AssertionError("LWJGL Vulkan GPU guard mismatch"+i);
     }
    }
   }
   stage("cycle"+cycle+" twelve-path bindings and GPU byte checks PASS");
  } finally {
   if(!incomplete){if(device!=null){if(fence!=0)vkDestroyFence(device,fence,null);if(pool!=0)vkDestroyCommandPool(device,pool,null);vkDestroyDevice(device,null);}if(instance!=null)vkDestroyInstance(instance,null);}
  }
 }
 public static void main(String[] args) {
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.VULKAN_EXPLICIT_INIT.set(true);Library.initialize();
  String hostLibrary=System.getProperty("ps5.test.vulkanLibrary");
  if(hostLibrary!=null) {
   VK.create(new PS5Library(hostLibrary));
  } else {
   System.loadLibrary("ps5clientgpu");
   VK.create(new PS5Library(System.mapLibraryName("ps5clientgpu")));
  }
  try {
   rejected(()->VK.create(VK.getFunctionProvider()));
   if(VK.getInstanceVersionSupported()<VK_API_VERSION_1_1)throw new AssertionError("Vulkan1.1 loader");
   stage("Vulkan loader initialized; instance and device tables follow");
   for(int i=0;i<3;i++)cycle(i,hostLibrary!=null);
  } finally {VK.destroy();}
  VK.destroy();
  stage("PASS unmodified LWJGL Vulkan bindings:12 GPU transfers,3 instance/device lifecycles, VK loader cleanup");
 }
}
