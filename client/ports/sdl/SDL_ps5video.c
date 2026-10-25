/*
 * Dusklight for the PlayStation 5 - SDL3's video driver for the console.
 *
 * The console has one output and no windows: this gives SDL one display and
 * lets it keep its window bookkeeping (size, flags, events) for a window that
 * is the whole screen. Nothing is drawn through SDL; the title's renderer
 * presents through VK_KHR_display on its own.
 *
 * Altered for the PS5 Java probe: actual Vulkan display query and static ICD
 * surface/presentation hooks replace preset dimensions and external surfaces.
 *
 * SPDX-License-Identifier: Zlib
 */
#include "SDL_internal.h"

#ifdef SDL_VIDEO_DRIVER_PS5

#include "video/SDL_sysvideo.h"
#include "events/SDL_events_c.h"

/* Use the same public resident loader as LWJGL. Minecraft checks pointer identity.
 * The public entry delegates to the real static ICD;all returned commands stay real. */
#include "video/SDL_vulkan_internal.h"
extern PFN_vkVoidFunction vkGetInstanceProcAddr(VkInstance,const char*);
static bool PS5_Vulkan_LoadLibrary(SDL_VideoDevice *_this,const char *path)
{
    if(path && *path)return SDL_SetError("PS5 uses its statically resident Vulkan ICD; explicit library path unsupported");
    PFN_vkVoidFunction enumerate=vkGetInstanceProcAddr(VK_NULL_HANDLE,"vkEnumerateInstanceExtensionProperties");
    if(!enumerate)return SDL_SetError("Resident ICD missing extension enumeration");
    _this->vulkan_config.vkGetInstanceProcAddr=(SDL_FunctionPointer)vkGetInstanceProcAddr;
    _this->vulkan_config.vkEnumerateInstanceExtensionProperties=(SDL_FunctionPointer)enumerate;
    _this->vulkan_config.loader_handle=NULL; /* A genuine static provider, no fabricated dlopen handle. */
    _this->vulkan_config.loader_path[0]=0;
    return true;
}
static void PS5_Vulkan_UnloadLibrary(SDL_VideoDevice *_this)
{
    _this->vulkan_config.vkGetInstanceProcAddr=NULL;
    _this->vulkan_config.vkEnumerateInstanceExtensionProperties=NULL;
}
static char const *const *PS5_Vulkan_GetInstanceExtensions(SDL_VideoDevice *_this,Uint32 *count)
{
    static const char *const extensions[]={VK_KHR_SURFACE_EXTENSION_NAME,VK_KHR_DISPLAY_EXTENSION_NAME};
    *count=SDL_arraysize(extensions);return extensions;
}
static bool PS5_Vulkan_CreateSurface(SDL_VideoDevice *_this,SDL_Window *window,VkInstance instance,const VkAllocationCallbacks *allocator,VkSurfaceKHR *surface)
{
    return SDL_Vulkan_Display_CreateSurface((void*)_this->vulkan_config.vkGetInstanceProcAddr,instance,allocator,surface);
}
static void PS5_Vulkan_DestroySurface(SDL_VideoDevice *_this,VkInstance instance,VkSurfaceKHR surface,const VkAllocationCallbacks *allocator)
{
    SDL_Vulkan_DestroySurface_Internal((void*)_this->vulkan_config.vkGetInstanceProcAddr,instance,surface,allocator);
}
static bool PS5_Vulkan_GetPresentationSupport(SDL_VideoDevice *_this,VkInstance instance,VkPhysicalDevice physical,Uint32 family)
{
    VkSurfaceKHR surface=VK_NULL_HANDLE;VkBool32 supported=VK_FALSE;
    if(!PS5_Vulkan_CreateSurface(_this,NULL,instance,NULL,&surface))return false;
    PFN_vkGetPhysicalDeviceSurfaceSupportKHR query=(PFN_vkGetPhysicalDeviceSurfaceSupportKHR)vkGetInstanceProcAddr(instance,"vkGetPhysicalDeviceSurfaceSupportKHR");
    VkResult result=query?query(physical,family,surface,&supported):VK_ERROR_EXTENSION_NOT_PRESENT;
    PS5_Vulkan_DestroySurface(_this,instance,surface,NULL);
    if(result!=VK_SUCCESS)return SDL_SetError("PS5 Vulkan presentation query failed: %d",result);
    return supported==VK_TRUE;
}
static bool PS5_QueryDisplay(SDL_DisplayMode *mode)
{
    const char *extensions[]={VK_KHR_SURFACE_EXTENSION_NAME,VK_KHR_DISPLAY_EXTENSION_NAME};
    VkApplicationInfo app={.sType=VK_STRUCTURE_TYPE_APPLICATION_INFO,.pApplicationName="SDL PS5 display query",.apiVersion=VK_API_VERSION_1_1};
    VkInstanceCreateInfo ci={.sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,.pApplicationInfo=&app,.enabledExtensionCount=2,.ppEnabledExtensionNames=extensions};
    PFN_vkCreateInstance create=(PFN_vkCreateInstance)vkGetInstanceProcAddr(VK_NULL_HANDLE,"vkCreateInstance");VkInstance instance=VK_NULL_HANDLE;
    VkResult result=create?create(&ci,NULL,&instance):VK_ERROR_INITIALIZATION_FAILED;
    if(result!=VK_SUCCESS)return SDL_SetError("SDL PS5 display instance failed: %d",result);
#define LOAD(name) PFN_vk##name name=(PFN_vk##name)vkGetInstanceProcAddr(instance,"vk"#name)
    LOAD(DestroyInstance);LOAD(EnumeratePhysicalDevices);LOAD(GetPhysicalDeviceDisplayPropertiesKHR);LOAD(GetDisplayModePropertiesKHR);
#undef LOAD
    bool ok=false;uint32_t count=16;VkPhysicalDevice devices[16];
    if(!DestroyInstance||!EnumeratePhysicalDevices||!GetPhysicalDeviceDisplayPropertiesKHR||!GetDisplayModePropertiesKHR)goto done;
    if(EnumeratePhysicalDevices(instance,&count,devices)!=VK_SUCCESS||count<1||count>16)goto done;
    VkDisplayPropertiesKHR displays[16];count=16;
    if(GetPhysicalDeviceDisplayPropertiesKHR(devices[0],&count,displays)!=VK_SUCCESS||count<1||count>16)goto done;
    VkDisplayModePropertiesKHR modes[32];count=32;
    if(GetDisplayModePropertiesKHR(devices[0],displays[0].display,&count,modes)!=VK_SUCCESS||count<1||count>32)goto done;
    int selected=-1;
    for(uint32_t i=0;i<count;i++)if(modes[i].parameters.visibleRegion.width==displays[0].physicalResolution.width&&modes[i].parameters.visibleRegion.height==displays[0].physicalResolution.height){if(selected<0||modes[i].parameters.refreshRate>modes[selected].parameters.refreshRate)selected=(int)i;}
    if(selected<0)selected=0;
    if(modes[selected].parameters.visibleRegion.width<640||modes[selected].parameters.visibleRegion.width>3840||modes[selected].parameters.visibleRegion.height<480||modes[selected].parameters.visibleRegion.height>2160)goto done;
    SDL_zero(*mode);mode->format=SDL_PIXELFORMAT_BGRA32;mode->w=(int)modes[selected].parameters.visibleRegion.width;mode->h=(int)modes[selected].parameters.visibleRegion.height;mode->refresh_rate=modes[selected].parameters.refreshRate/1000.0f;ok=true;
done:
    if(DestroyInstance)DestroyInstance(instance,NULL);
    if(!ok)return SDL_SetError("SDL PS5 display inventory/mode query failed");
    return true;
}

static bool PS5_VideoInit(SDL_VideoDevice *_this)
{
    SDL_DisplayMode mode;
    if(!PS5_QueryDisplay(&mode))return false;
    return SDL_AddBasicVideoDisplay(&mode)!=0;
}

static void PS5_VideoQuit(SDL_VideoDevice *_this)
{
}

static void PS5_PumpEvents(SDL_VideoDevice *_this)
{
}

static bool PS5_CreateWindow(SDL_VideoDevice *_this, SDL_Window *window, SDL_PropertiesID props)
{
    /* The window is the screen, and always has the pad's focus */
    SDL_SetKeyboardFocus(window);
    return true;
}

static bool PS5_SetWindowPosition(SDL_VideoDevice *_this, SDL_Window *window)
{
    return true;
}

static void PS5_SetWindowSize(SDL_VideoDevice *_this, SDL_Window *window)
{
    /* The size stays the display's */
}

static SDL_FullscreenResult PS5_SetWindowFullscreen(SDL_VideoDevice *_this, SDL_Window *window, SDL_VideoDisplay *display, SDL_FullscreenOp fullscreen)
{
    return SDL_FULLSCREEN_SUCCEEDED;
}

static void PS5_DeleteDevice(SDL_VideoDevice *device)
{
    SDL_free(device);
}

static SDL_VideoDevice *PS5_CreateDevice(void)
{
    SDL_VideoDevice *device = (SDL_VideoDevice *)SDL_calloc(1, sizeof(SDL_VideoDevice));
    if (!device) {
        return NULL;
    }
    device->Vulkan_LoadLibrary=PS5_Vulkan_LoadLibrary;
    device->Vulkan_UnloadLibrary=PS5_Vulkan_UnloadLibrary;
    device->Vulkan_GetInstanceExtensions=PS5_Vulkan_GetInstanceExtensions;
    device->Vulkan_CreateSurface=PS5_Vulkan_CreateSurface;
    device->Vulkan_DestroySurface=PS5_Vulkan_DestroySurface;
    device->Vulkan_GetPresentationSupport=PS5_Vulkan_GetPresentationSupport;
    device->VideoInit = PS5_VideoInit;
    device->VideoQuit = PS5_VideoQuit;
    device->PumpEvents = PS5_PumpEvents;
    device->CreateSDLWindow = PS5_CreateWindow;
    device->SetWindowPosition = PS5_SetWindowPosition;
    device->SetWindowSize = PS5_SetWindowSize;
    device->SetWindowFullscreen = PS5_SetWindowFullscreen;
    device->free = PS5_DeleteDevice;
    device->device_caps = VIDEO_DEVICE_CAPS_FULLSCREEN_ONLY;
    return device;
}

VideoBootStrap PS5_bootstrap = {
    "ps5", "PlayStation 5 video driver",
    PS5_CreateDevice,
    NULL, // no ShowMessageBox implementation
    false
};

#endif // SDL_VIDEO_DRIVER_PS5
