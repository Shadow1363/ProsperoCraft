/* SPDX-License-Identifier: Zlib
 * Consumer SDL endpoint for Controlify's quad-channel DualSense haptic stream.
 * Channels 0/1 are discarded; channels 2/3 feed the real type-10 actuator port.
 * Game speaker playback remains owned by OpenAL's separate main port.
 */
#include "SDL_internal.h"
#ifdef SDL_AUDIO_DRIVER_PS5
#include "audio/SDL_audiodev_c.h"
#include "audio/SDL_sysaudio.h"
#include "ps5_haptic_pcm.h"

extern int sceAudioOutInit(void);
extern int sceAudioOutOpen(int,int,int,unsigned,unsigned,unsigned);
extern int sceAudioOutOutput(int,const void *);
extern int sceAudioOutClose(int);
extern int sceUserServiceGetInitialUser(int *);
extern int scePadGetHandle(int,int,int);
extern int scePadSetVibrationMode(int,int);
extern void client_sdl_diagnostic(const char *);

#define PS5_HAPTIC_FRAMES 256
typedef struct { int user,pad; } PS5_HapticDevice;
struct SDL_PrivateAudioData {
    int port,pad;bool healthy;
    Uint8 *buffer;
    Sint16 *pcm;
};

static void PS5AUDIO_Report(const char *phase,int result)
{
    char text[160];SDL_snprintf(text,sizeof(text),"PS5_HAPTIC phase=%s result=0x%x",phase,(unsigned)result);client_sdl_diagnostic(text);
}

static int retained_port=-1,retained_user=-1;
int prospero_haptic_reserve(void)
{
    int user=-1;if(sceUserServiceGetInitialUser(&user)<0)return -1;
    if(retained_port>=0&&retained_user==user)return retained_port;
    if(retained_port>=0){(void)sceAudioOutClose(retained_port);retained_port=-1;}
    retained_port=sceAudioOutOpen(user,10,0,PS5_HAPTIC_FRAMES,48000,1);retained_user=user;
    PS5AUDIO_Report("reserve-port",retained_port);return retained_port;
}
static void PS5AUDIO_DetectDevices(SDL_AudioDevice **playback,SDL_AudioDevice **recording)
{
    (void)recording;
    int user=-1;
    if(sceUserServiceGetInitialUser(&user)<0)return;
    int pad=scePadGetHandle(user,0,0);if(pad<0)return;
    int init=sceAudioOutInit();PS5AUDIO_Report("init",init);
    if(init<0&&(Uint32)init!=0x8026000eu&&(Uint32)init!=0x80260002u)return;
    int port=prospero_haptic_reserve();PS5AUDIO_Report("probe-port",port);
    if(port<0)return;
    int mode=scePadSetVibrationMode(pad,1);PS5AUDIO_Report("probe-advanced",mode);
    int restore=scePadSetVibrationMode(pad,2);
    if(mode<0||restore<0){(void)sceAudioOutClose(port);retained_port=-1;return;}
    PS5_HapticDevice *handle=SDL_malloc(sizeof(*handle));if(!handle)return;
    *handle=(PS5_HapticDevice){user,pad};
    SDL_AudioSpec spec={SDL_AUDIO_F32,4,48000};
    *playback=SDL_AddAudioDevice(false,"DualSense PS5 Haptics",&spec,handle);
    if(!*playback)SDL_free(handle);
}

static bool PS5AUDIO_OpenDevice(SDL_AudioDevice *device)
{
    if(device->recording||!device->handle)return SDL_Unsupported();
    const PS5_HapticDevice *handle=device->handle;
    struct SDL_PrivateAudioData *data=SDL_calloc(1,sizeof(*data));if(!data)return false;
    device->hidden=data;data->port=-1;data->pad=handle->pad;data->healthy=true;
    device->spec=(SDL_AudioSpec){SDL_AUDIO_F32,4,48000};device->sample_frames=PS5_HAPTIC_FRAMES;
    SDL_UpdatedAudioDeviceFormat(device);
    data->buffer=SDL_aligned_alloc(64,device->buffer_size);
    data->pcm=SDL_aligned_alloc(64,PS5_HAPTIC_FRAMES*2*sizeof(Sint16));
    if(!data->buffer||!data->pcm)return false;
    SDL_memset(data->buffer,0,device->buffer_size);SDL_memset(data->pcm,0,PS5_HAPTIC_FRAMES*2*sizeof(Sint16));
    if(retained_port>=0&&retained_user==handle->user){data->port=retained_port;retained_port=-1;}
    else data->port=sceAudioOutOpen(handle->user,10,0,PS5_HAPTIC_FRAMES,48000,1);PS5AUDIO_Report("open-port",data->port);
    if(data->port<0)return SDL_SetError("PS5 DualSense haptic audio port unavailable");
    int mode=scePadSetVibrationMode(handle->pad,1);PS5AUDIO_Report("advanced",mode);
    if(mode<0){data->healthy=false;return SDL_SetError("PS5 DualSense advanced vibration mode unavailable");}
    return true;
}

static bool PS5AUDIO_PlayDevice(SDL_AudioDevice *device,const Uint8 *buffer,int size)
{
    if(size!=PS5_HAPTIC_FRAMES*4*(int)sizeof(float))return SDL_SetError("Unexpected PS5 haptic buffer size");
    struct SDL_PrivateAudioData *data=device->hidden;
    prospero_haptic_pcm((const float *)buffer,data->pcm,PS5_HAPTIC_FRAMES);
    int result=sceAudioOutOutput(data->port,data->pcm);
    if(result<0){data->healthy=false;PS5AUDIO_Report("output-failed",result);return SDL_SetError("PS5 haptic output failed");}
    return true;
}
static bool PS5AUDIO_WaitDevice(SDL_AudioDevice *device){(void)device;return true;} /* Output paces playback. */
static Uint8 *PS5AUDIO_GetDeviceBuf(SDL_AudioDevice *device,int *size){*size=device->buffer_size;return device->hidden->buffer;}
static void PS5AUDIO_CloseDevice(SDL_AudioDevice *device)
{
    struct SDL_PrivateAudioData *data=device->hidden;if(!data)return;
    if(data->port>=0){int drained=sceAudioOutOutput(data->port,NULL);(void)scePadSetVibrationMode(data->pad,2);
        if(data->healthy&&drained>=0&&retained_port<0){retained_port=data->port;retained_user=((PS5_HapticDevice *)device->handle)->user;PS5AUDIO_Report("retain-port",retained_port);}
        else PS5AUDIO_Report("close-port",sceAudioOutClose(data->port));}
    SDL_aligned_free(data->buffer);SDL_aligned_free(data->pcm);SDL_free(data);device->hidden=NULL;
}
static void PS5AUDIO_FreeDeviceHandle(SDL_AudioDevice *device){SDL_free(device->handle);device->handle=NULL;}
static bool PS5AUDIO_Init(SDL_AudioDriverImpl *impl)
{
    impl->DetectDevices=PS5AUDIO_DetectDevices;impl->OpenDevice=PS5AUDIO_OpenDevice;
    impl->PlayDevice=PS5AUDIO_PlayDevice;impl->WaitDevice=PS5AUDIO_WaitDevice;
    impl->GetDeviceBuf=PS5AUDIO_GetDeviceBuf;impl->CloseDevice=PS5AUDIO_CloseDevice;
    impl->FreeDeviceHandle=PS5AUDIO_FreeDeviceHandle;
    return true;
}
AudioBootStrap PS5AUDIO_bootstrap={"ps5","PS5 DualSense actuator audio",PS5AUDIO_Init,false,false};
#endif
