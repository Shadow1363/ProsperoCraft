/* SPDX-License-Identifier: GPL-3.0-or-later
 * Standard Vulkan loader entry for a statically resident ICD. No fake commands.
 */
#define VK_NO_PROTOTYPES
#include <vulkan/vulkan.h>
extern PFN_vkVoidFunction vk_icdGetInstanceProcAddr(VkInstance,const char*);
VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL vkGetInstanceProcAddr(VkInstance instance,const char *name){
 return vk_icdGetInstanceProcAddr(instance,name);
}
