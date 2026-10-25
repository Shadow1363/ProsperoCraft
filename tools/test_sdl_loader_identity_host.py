#!/usr/bin/env python3
"""Exercise the actual PS5 SDL loader hook and public wrapper against real MoltenVK."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];work=ROOT/'build/sdl-loader-identity-host';work.mkdir(exist_ok=True)
source=(ROOT/'client/ports/sdl/SDL_ps5video.c').read_text();start=source.index('static bool PS5_Vulkan_LoadLibrary(');end=source.index('static void PS5_Vulkan_UnloadLibrary(',start);hook=source[start:end]
header='''#include <vulkan/vulkan.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>
typedef void(*SDL_FunctionPointer)(void);
typedef struct { struct {SDL_FunctionPointer vkGetInstanceProcAddr;SDL_FunctionPointer vkEnumerateInstanceExtensionProperties;void*loader_handle;char loader_path[256];}vulkan_config;}SDL_VideoDevice;
static bool SDL_SetError(const char*fmt,...){(void)fmt;return false;}
extern PFN_vkVoidFunction ps5_test_public_loader(VkInstance,const char*);
'''
main='''
#undef vkGetInstanceProcAddr
int main(void){SDL_VideoDevice driver={0};if(PS5_Vulkan_LoadLibrary(&driver,"not-a-resident-provider"))return 1;if(!PS5_Vulkan_LoadLibrary(&driver,NULL))return 2;
PFN_vkGetInstanceProcAddr public_entry=ps5_test_public_loader,from_sdl=(PFN_vkGetInstanceProcAddr)driver.vulkan_config.vkGetInstanceProcAddr;
if(from_sdl!=public_entry){puts("CONTROL pointer mismatch detected");return 10;}
PFN_vkEnumerateInstanceExtensionProperties query=(PFN_vkEnumerateInstanceExtensionProperties)driver.vulkan_config.vkEnumerateInstanceExtensionProperties;uint32_t count=0;if(query(NULL,&count,NULL)!=VK_SUCCESS||!count)return 3;
PFN_vkCreateInstance create=(PFN_vkCreateInstance)from_sdl(NULL,"vkCreateInstance");if(!create)return 4;
VkApplicationInfo app={.sType=VK_STRUCTURE_TYPE_APPLICATION_INFO,.apiVersion=VK_API_VERSION_1_1};VkInstanceCreateInfo info={.sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,.pApplicationInfo=&app};VkInstance instance=VK_NULL_HANDLE;if(create(&info,NULL,&instance)!=VK_SUCCESS||!instance)return 5;
PFN_vkEnumeratePhysicalDevices devices=(PFN_vkEnumeratePhysicalDevices)from_sdl(instance,"vkEnumeratePhysicalDevices");count=0;if(!devices||devices(instance,&count,NULL)!=VK_SUCCESS||!count)return 6;
PFN_vkDestroyInstance destroy=(PFN_vkDestroyInstance)from_sdl(instance,"vkDestroyInstance");if(!destroy)return 7;destroy(instance,NULL);puts("PASS actual PS5 SDL hook/public loader pointer identity,real MoltenVK extension query/instance/physical-device lookup/destroy;explicit-path rejection");return 0;}
'''
# Compile the exact consumer wrapper with only host symbol names adapted:it
# delegates to MoltenVK's actual Vulkan loader entry rather than a mock ICD.
loader=work/'loader.c';loader.write_text((ROOT/'client/vulkan/loader.c').read_text().replace('vkGetInstanceProcAddr(','ps5_test_public_loader(').replace('vk_icdGetInstanceProcAddr','vkGetInstanceProcAddr'))
includes=['-I'+str(ROOT/'.tools/lwjgl-vma-src')];base=['clang','-std=c11','-O2','-fsanitize=undefined',*includes,str(loader),'-L/opt/homebrew/lib','-lMoltenVK']
for control in [False,True]:
 unit=work/('control.c'if control else'check.c');body=hook.replace('(SDL_FunctionPointer)vkGetInstanceProcAddr','(SDL_FunctionPointer)vk_icdGetInstanceProcAddr')if control else hook
 # The negative control exposes the real underlying loader address as038did.
 body=body.replace('(SDL_FunctionPointer)vkGetInstanceProcAddr','(SDL_FunctionPointer)ps5_test_public_loader').replace('=vkGetInstanceProcAddr(','=ps5_test_public_loader(')
 unit.write_text(header+('extern PFN_vkVoidFunction vk_icdGetInstanceProcAddr(VkInstance,const char*) __asm__("_vkGetInstanceProcAddr");\n'if control else'')+body+main);binary=unit.with_suffix('');subprocess.run([*base,str(unit),'-o',str(binary)],check=True);r=subprocess.run([str(binary)],capture_output=True,text=True,timeout=30);print(r.stdout,r.stderr);assert r.returncode==(10 if control else 0)
print('PASS038pointer mismatch reproduced and corrected using real driver functions;PS5 console integration pending')
