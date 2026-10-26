/* SPDX-License-Identifier: GPL-3.0-or-later
 * Layerless Vulkan loader for the statically resident ICD. No fake GPU commands.
 * Layer discovery belongs to the loader, not the ICD. No layers are bundled.
 */
#define VK_NO_PROTOTYPES
#include <vulkan/vulkan.h>
#include <string.h>
extern PFN_vkVoidFunction vk_icdGetInstanceProcAddr(VkInstance,const char*);
VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL vkGetInstanceProcAddr(VkInstance,const char*);

static VKAPI_ATTR VkResult VKAPI_CALL resident_layers(uint32_t *count,VkLayerProperties *properties){
 (void)properties;
 *count=0;
 return VK_SUCCESS;
}
static VKAPI_ATTR VkResult VKAPI_CALL resident_extensions(const char *layer,uint32_t *count,VkExtensionProperties *properties){
 if(layer)return VK_ERROR_LAYER_NOT_PRESENT;
 PFN_vkEnumerateInstanceExtensionProperties query=(PFN_vkEnumerateInstanceExtensionProperties)vk_icdGetInstanceProcAddr(VK_NULL_HANDLE,"vkEnumerateInstanceExtensionProperties");
 return query(layer,count,properties);
}
static VKAPI_ATTR VkResult VKAPI_CALL resident_create(const VkInstanceCreateInfo *info,const VkAllocationCallbacks *allocator,VkInstance *instance){
 if(info->enabledLayerCount){*instance=VK_NULL_HANDLE;return VK_ERROR_LAYER_NOT_PRESENT;}
 PFN_vkCreateInstance create=(PFN_vkCreateInstance)vk_icdGetInstanceProcAddr(VK_NULL_HANDLE,"vkCreateInstance");
 return create(info,allocator,instance);
}
VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL vkGetInstanceProcAddr(VkInstance instance,const char *name){
 if(!name)return NULL;
 if(!strcmp(name,"vkGetInstanceProcAddr"))return (PFN_vkVoidFunction)vkGetInstanceProcAddr;
 if(!strcmp(name,"vkEnumerateInstanceLayerProperties"))return (PFN_vkVoidFunction)resident_layers;
 if(!strcmp(name,"vkEnumerateInstanceExtensionProperties"))return (PFN_vkVoidFunction)resident_extensions;
 if(!strcmp(name,"vkCreateInstance"))return (PFN_vkVoidFunction)resident_create;
 return vk_icdGetInstanceProcAddr(instance,name);
}
