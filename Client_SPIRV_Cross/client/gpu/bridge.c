/* SPDX-License-Identifier: GPL-3.0-or-later
 * Consumer JNI bridge: real Vulkan offscreen transfer, with no game/SDL hooks.
 */
#define VK_NO_PROTOTYPES
#include <vulkan/vulkan.h>
#include <jni.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#define I_COMMANDS(X) X(DestroyInstance) X(EnumeratePhysicalDevices) X(GetPhysicalDeviceProperties) X(GetPhysicalDeviceQueueFamilyProperties) X(GetPhysicalDeviceMemoryProperties) X(EnumerateDeviceExtensionProperties) X(CreateDevice) X(GetDeviceProcAddr)
#define D_COMMANDS(X) X(DestroyDevice) X(GetDeviceQueue) X(CreateCommandPool) X(DestroyCommandPool) X(AllocateCommandBuffers) X(ResetCommandBuffer) X(BeginCommandBuffer) X(EndCommandBuffer) X(CreateFence) X(DestroyFence) X(ResetFences) X(WaitForFences) X(QueueSubmit) X(CreateBuffer) X(DestroyBuffer) X(GetBufferMemoryRequirements) X(AllocateMemory) X(FreeMemory) X(BindBufferMemory) X(MapMemory) X(UnmapMemory) X(FlushMappedMemoryRanges) X(InvalidateMappedMemoryRanges) X(CmdCopyBuffer) X(CmdFillBuffer) X(CmdPipelineBarrier)
#define DECLARE(n) static PFN_vk##n vk##n;
I_COMMANDS(DECLARE)
D_COMMANDS(DECLARE)
#undef DECLARE
#ifdef PS5_GPU_HOST
extern PFN_vkVoidFunction vkGetInstanceProcAddr(VkInstance,const char*);
#define GET_PROC vkGetInstanceProcAddr
static void stage(const char *s,int code){fprintf(stderr,"[gpu004] %s: %d\n",s,code);}
#else
extern PFN_vkVoidFunction vk_icdGetInstanceProcAddr(VkInstance,const char*);
extern void client_gpu_stage(const char*,int);
#define GET_PROC vk_icdGetInstanceProcAddr
static void stage(const char *s,int code){client_gpu_stage(s,code);}
extern void clientgpu_ps5_fp_ieee(void);
typedef void (*Initializer)(void);
extern Initializer __client_gpu_init_start[],__client_gpu_init_end[];
#endif
static VkInstance instance;
static VkDevice device;
static VkPhysicalDevice physical;
static VkQueue queue;
static VkCommandPool pool;
static VkCommandBuffer cmd;
static VkFence fence;
static VkPhysicalDeviceMemoryProperties memory_properties;
static pthread_t owner;
static jlong serial,handle,last_closed;
static int poisoned;
static void fail(JNIEnv *e,const char *type,const char *text){
 jclass c=(*e)->FindClass(e,type);if(c){(*e)->ThrowNew(e,c,text);(*e)->DeleteLocalRef(e,c);}
}
static int vk_ok(JNIEnv *e,VkResult result,const char *call){
 stage(call,(int)result);if(result==VK_SUCCESS)return 1;
 char msg[256];snprintf(msg,sizeof(msg),"%s returned VkResult %d",call,(int)result);
 fail(e,"java/lang/IllegalStateException",msg);return 0;
}
#define CALL(expr) (stage(#expr,INT32_MIN),vk_ok(e,(expr),#expr))
static int valid(JNIEnv *e,jlong value){
 if(!handle||value!=handle){fail(e,"java/lang/IllegalStateException","Closed or unknown GPU session");return 0;}
 if(!pthread_equal(owner,pthread_self())){fail(e,"java/lang/IllegalStateException","GPU session belongs to its opening thread");return 0;}
 if(poisoned){fail(e,"java/lang/IllegalStateException","GPU submission incomplete; relaunch instead of freeing in-flight resources");return 0;}
 return 1;
}
static void destroy_context(void){
 if(fence&&vkDestroyFence)vkDestroyFence(device,fence,NULL);
 if(pool&&vkDestroyCommandPool)vkDestroyCommandPool(device,pool,NULL);
 if(device&&vkDestroyDevice)vkDestroyDevice(device,NULL);
 if(instance&&vkDestroyInstance)vkDestroyInstance(instance,NULL);
 fence=VK_NULL_HANDLE;pool=VK_NULL_HANDLE;device=VK_NULL_HANDLE;instance=VK_NULL_HANDLE;cmd=VK_NULL_HANDLE;
}
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM *vm,void *reserved){
 (void)vm;(void)reserved;
#ifndef PS5_GPU_HOST
 static int initialized;
 if(!initialized){
  clientgpu_ps5_fp_ieee();
  stage("Running explicit GPU constructors after VM creation",INT32_MIN);
  for(Initializer *p=__client_gpu_init_start;p!=__client_gpu_init_end;p++)if(*p)(*p)();
  initialized=1;stage("GPU constructors complete",0);
 }
#endif
 return JNI_VERSION_1_8;
}
JNIEXPORT jlong JNICALL Java_ClientGpu25_open(JNIEnv *e,jclass klass){
 (void)klass;if(handle){fail(e,"java/lang/IllegalStateException","GPU session already open");return 0;}
 PFN_vkCreateInstance create=(PFN_vkCreateInstance)GET_PROC(VK_NULL_HANDLE,"vkCreateInstance");
 if(!create){fail(e,"java/lang/IllegalStateException","Missing Vulkan instance entry point");return 0;}
 const VkApplicationInfo app={.sType=VK_STRUCTURE_TYPE_APPLICATION_INFO,.pApplicationName="PS5 Java GPU004",.apiVersion=VK_API_VERSION_1_2};
 VkInstanceCreateInfo ci={.sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,.pApplicationInfo=&app};
 if(!CALL(create(&ci,NULL,&instance)))return 0;
#define LOAD(n) vk##n=(PFN_vk##n)GET_PROC(instance,"vk"#n);if(!vk##n){fail(e,"java/lang/IllegalStateException","Missing vk"#n);goto failed;}
 I_COMMANDS(LOAD)
#undef LOAD
 uint32_t count=1;
 if(!CALL(vkEnumeratePhysicalDevices(instance,&count,&physical)))goto failed;
 if(count!=1){fail(e,"java/lang/IllegalStateException","Expected one physical GPU");goto failed;}
 VkPhysicalDeviceProperties properties;vkGetPhysicalDeviceProperties(physical,&properties);stage(properties.deviceName,0);
 if(properties.apiVersion<VK_API_VERSION_1_2){fail(e,"java/lang/IllegalStateException","Vulkan1.2 unavailable");goto failed;}
 VkQueueFamilyProperties families[32];count=32;vkGetPhysicalDeviceQueueFamilyProperties(physical,&count,families);
 uint32_t family=UINT32_MAX;
 for(uint32_t i=0;i<count&&i<32;i++)if(families[i].queueCount&&(families[i].queueFlags&VK_QUEUE_GRAPHICS_BIT)){family=i;break;}
 if(family==UINT32_MAX){fail(e,"java/lang/IllegalStateException","No graphics/transfer queue");goto failed;}
 vkGetPhysicalDeviceMemoryProperties(physical,&memory_properties);
 const float priority=1;const VkDeviceQueueCreateInfo qi={.sType=VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,.queueFamilyIndex=family,.queueCount=1,.pQueuePriorities=&priority};
 VkDeviceCreateInfo di={.sType=VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO,.queueCreateInfoCount=1,.pQueueCreateInfos=&qi};
#ifdef PS5_GPU_HOST
 VkExtensionProperties extensions[512];count=512;
 if(!CALL(vkEnumerateDeviceExtensionProperties(physical,NULL,&count,extensions)))goto failed;
 const char *device_extensions[]={"VK_KHR_portability_subset"};
 for(uint32_t i=0;i<count&&i<512;i++)if(!strcmp(extensions[i].extensionName,device_extensions[0])){di.enabledExtensionCount=1;di.ppEnabledExtensionNames=device_extensions;break;}
#endif
 if(!CALL(vkCreateDevice(physical,&di,NULL,&device)))goto failed;
#define LOAD(n) vk##n=(PFN_vk##n)vkGetDeviceProcAddr(device,"vk"#n);if(!vk##n){fail(e,"java/lang/IllegalStateException","Missing vk"#n);goto failed;}
 D_COMMANDS(LOAD)
#undef LOAD
 vkGetDeviceQueue(device,family,0,&queue);
 const VkCommandPoolCreateInfo pi={.sType=VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO,.flags=VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT,.queueFamilyIndex=family};
 if(!CALL(vkCreateCommandPool(device,&pi,NULL,&pool)))goto failed;
 const VkCommandBufferAllocateInfo ca={.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO,.commandPool=pool,.level=VK_COMMAND_BUFFER_LEVEL_PRIMARY,.commandBufferCount=1};
 if(!CALL(vkAllocateCommandBuffers(device,&ca,&cmd)))goto failed;
 const VkFenceCreateInfo fi={.sType=VK_STRUCTURE_TYPE_FENCE_CREATE_INFO};
 if(!CALL(vkCreateFence(device,&fi,NULL,&fence)))goto failed;
 owner=pthread_self();handle=++serial;poisoned=0;return handle;
failed: destroy_context();return 0;
}
struct Buffer {VkBuffer buffer;VkDeviceMemory memory;void *map;};
static void destroy_buffer(struct Buffer *b){
 if(b->map)vkUnmapMemory(device,b->memory);
 if(b->buffer)vkDestroyBuffer(device,b->buffer,NULL);
 if(b->memory)vkFreeMemory(device,b->memory,NULL);
 memset(b,0,sizeof(*b));
}
static int make_buffer(JNIEnv *e,struct Buffer *b,VkDeviceSize bytes){
 const VkBufferCreateInfo bi={.sType=VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO,.size=bytes,.usage=VK_BUFFER_USAGE_TRANSFER_SRC_BIT|VK_BUFFER_USAGE_TRANSFER_DST_BIT,.sharingMode=VK_SHARING_MODE_EXCLUSIVE};
 if(!CALL(vkCreateBuffer(device,&bi,NULL,&b->buffer)))return 0;
 VkMemoryRequirements req;vkGetBufferMemoryRequirements(device,b->buffer,&req);
 uint32_t type=UINT32_MAX;
 for(uint32_t i=0;i<memory_properties.memoryTypeCount;i++)if((req.memoryTypeBits&(1u<<i))&&(memory_properties.memoryTypes[i].propertyFlags&VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)){type=i;break;}
 if(type==UINT32_MAX){fail(e,"java/lang/IllegalStateException","No host-visible transfer memory");return 0;}
 const VkMemoryAllocateInfo ma={.sType=VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO,.allocationSize=req.size,.memoryTypeIndex=type};
 return CALL(vkAllocateMemory(device,&ma,NULL,&b->memory))&&CALL(vkBindBufferMemory(device,b->buffer,b->memory,0))&&CALL(vkMapMemory(device,b->memory,0,VK_WHOLE_SIZE,0,&b->map));
}
JNIEXPORT void JNICALL Java_ClientGpu25_transfer(JNIEnv *e,jclass klass,jlong value,jobject input,jobject output,jint bytes,jint pattern){
 (void)klass;if(!valid(e,value))return;
 void *in=input?(*e)->GetDirectBufferAddress(e,input):NULL;void *out=output?(*e)->GetDirectBufferAddress(e,output):NULL;
 jlong in_size=input?(*e)->GetDirectBufferCapacity(e,input):-1; jlong out_size=output?(*e)->GetDirectBufferCapacity(e,output):-1;
 if(!in||!out||in==out||bytes<8||bytes>65536||(bytes&7)||in_size<bytes||out_size<bytes){fail(e,"java/lang/IllegalArgumentException","Distinct direct buffers with capacity for8..65536 bytes, multiple of8 required");return;}
 struct Buffer src={0},dst={0};
 if(!make_buffer(e,&src,(VkDeviceSize)bytes)||!make_buffer(e,&dst,(VkDeviceSize)bytes))goto cleanup;
 memcpy(src.map,in,(size_t)bytes);
 const VkMappedMemoryRange flush={.sType=VK_STRUCTURE_TYPE_MAPPED_MEMORY_RANGE,.memory=src.memory,.size=VK_WHOLE_SIZE};
 if(!CALL(vkFlushMappedMemoryRanges(device,1,&flush))||!CALL(vkResetCommandBuffer(cmd,0)))goto cleanup;
 const VkCommandBufferBeginInfo begin={.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO,.flags=VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT};
 if(!CALL(vkBeginCommandBuffer(cmd,&begin)))goto cleanup;
 const VkBufferMemoryBarrier host={.sType=VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER,.srcAccessMask=VK_ACCESS_HOST_WRITE_BIT,.dstAccessMask=VK_ACCESS_TRANSFER_READ_BIT,.srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,.dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,.buffer=src.buffer,.size=VK_WHOLE_SIZE};
 vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_HOST_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,0,NULL,1,&host,0,NULL);
 const VkBufferCopy copy={0,0,(VkDeviceSize)bytes/2};vkCmdCopyBuffer(cmd,src.buffer,dst.buffer,1,&copy);
 vkCmdFillBuffer(cmd,dst.buffer,(VkDeviceSize)bytes/2,(VkDeviceSize)bytes/2,(uint32_t)pattern);
 const VkBufferMemoryBarrier gpu={.sType=VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER,.srcAccessMask=VK_ACCESS_TRANSFER_WRITE_BIT,.dstAccessMask=VK_ACCESS_HOST_READ_BIT,.srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,.dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,.buffer=dst.buffer,.size=VK_WHOLE_SIZE};
 vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,0,NULL,1,&gpu,0,NULL);
 if(!CALL(vkEndCommandBuffer(cmd))||!CALL(vkResetFences(device,1,&fence)))goto cleanup;
 const VkSubmitInfo submit={.sType=VK_STRUCTURE_TYPE_SUBMIT_INFO,.commandBufferCount=1,.pCommandBuffers=&cmd};
 if(!CALL(vkQueueSubmit(queue,1,&submit,fence)))goto cleanup;
 if(!CALL(vkWaitForFences(device,1,&fence,VK_TRUE,UINT64_C(5000000000)))){
  poisoned=1;stage("Keeping possibly in-flight Vulkan resources; relaunch required",-1);return;
 }
 const VkMappedMemoryRange invalidate={.sType=VK_STRUCTURE_TYPE_MAPPED_MEMORY_RANGE,.memory=dst.memory,.size=VK_WHOLE_SIZE};
 if(!CALL(vkInvalidateMappedMemoryRanges(device,1,&invalidate)))goto cleanup;
 memcpy(out,dst.map,(size_t)bytes);
cleanup:destroy_buffer(&dst);destroy_buffer(&src);
}
JNIEXPORT void JNICALL Java_ClientGpu25_close(JNIEnv *e,jclass klass,jlong value){
 (void)klass;if(value&&value==last_closed)return;
 if(!valid(e,value))return;
 destroy_context();last_closed=handle;handle=0;stage("GPU session explicitly destroyed",0);
}
#ifdef PS5_GPU_HOST
JNIEXPORT void JNICALL Java_ClientGpu25_checkpoint(JNIEnv *e,jclass c,jstring s){
 (void)c;const char *p=(*e)->GetStringUTFChars(e,s,NULL);if(p){stage(p,0);(*e)->ReleaseStringUTFChars(e,s,p);}
}
#endif
