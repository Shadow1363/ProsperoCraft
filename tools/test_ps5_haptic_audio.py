#!/usr/bin/env python3
"""Exercise the actual actuator backend with sanitized native-call fixtures."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
header=r'''
#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <math.h>
#include <assert.h>
typedef uint8_t Uint8;typedef uint32_t Uint32;typedef int16_t Sint16;
#define SDL_AUDIO_DRIVER_PS5 1
#define SDL_AUDIO_F32 1
#define SDL_malloc malloc
#define SDL_calloc calloc
#define SDL_free free
#define SDL_aligned_free free
#define SDL_memset memset
#define SDL_snprintf snprintf
static int alloc_fail;
static void *SDL_aligned_alloc(size_t a,size_t b){void*p=NULL;if(alloc_fail)return NULL;assert(!posix_memalign(&p,a,b));return p;}
static bool SDL_SetError(const char*s,...){(void)s;return false;}
static bool SDL_Unsupported(void){return false;}
typedef struct {int format,channels,freq;} SDL_AudioSpec;
struct SDL_PrivateAudioData;
typedef struct {bool recording;void *handle;struct SDL_PrivateAudioData *hidden;SDL_AudioSpec spec;int sample_frames,buffer_size;} SDL_AudioDevice;
typedef struct {
 void (*DetectDevices)(SDL_AudioDevice**,SDL_AudioDevice**);
 bool (*OpenDevice)(SDL_AudioDevice*);bool (*PlayDevice)(SDL_AudioDevice*,const Uint8*,int);bool (*WaitDevice)(SDL_AudioDevice*);
 Uint8 *(*GetDeviceBuf)(SDL_AudioDevice*,int*);void (*CloseDevice)(SDL_AudioDevice*);void (*FreeDeviceHandle)(SDL_AudioDevice*);
} SDL_AudioDriverImpl;
typedef struct {const char*name,*description;bool (*init)(SDL_AudioDriverImpl*);bool a,b;} AudioBootStrap;
static SDL_AudioDevice physical;
static SDL_AudioDevice *SDL_AddAudioDevice(bool recording,const char*name,const SDL_AudioSpec*spec,void*handle){assert(!recording&&strstr(name,"DualSense")&&spec->channels==4);physical=(SDL_AudioDevice){.handle=handle,.spec=*spec};return &physical;}
static void SDL_UpdatedAudioDeviceFormat(SDL_AudioDevice*d){d->buffer_size=d->sample_frames*d->spec.channels*4;}
'''
source=r'''
#include "SDL_internal.h"
static int fail_port,fail_mode,fail_output,opened,closed,advanced,compatible,outputs;
static int16_t last[512];
int sceAudioOutInit(void){return (int)0x8026000e;}
int sceAudioOutOpen(int user,int type,int index,unsigned frames,unsigned rate,unsigned format){assert(user==42&&type==10&&index==0&&frames==256&&rate==48000&&format==1);if(fail_port)return -1;opened++;return 99;}
int sceAudioOutClose(int port){assert(port==99);closed++;return 0;}
int sceAudioOutOutput(int port,const void *pcm){assert(port==99);if(pcm){outputs++;memcpy(last,pcm,sizeof(last));}return fail_output?-1:0;}
int sceUserServiceGetInitialUser(int *u){*u=42;return 0;}
int scePadGetHandle(int user,int type,int index){assert(user==42&&type==0&&index==0);return 7;}
int prospero_pad_set_vibration_mode(int pad,int mode){assert(pad==7);if(mode==1){advanced++;return fail_mode?-1:0;}assert(mode==2);compatible++;return 0;}
void client_sdl_diagnostic(const char *text){assert(strstr(text,"PS5_HAPTIC"));}
#include "SDL_ps5audio.c"
int main(void){
 SDL_AudioDriverImpl impl={0};assert(PS5AUDIO_bootstrap.init(&impl));SDL_AudioDevice *playback=NULL,*recording=NULL;
 fail_port=1;impl.DetectDevices(&playback,&recording);assert(!playback&&opened==closed);
 fail_port=0;fail_mode=1;impl.DetectDevices(&playback,&recording);assert(!playback&&opened==closed&&compatible==1);
 fail_mode=0;impl.DetectDevices(&playback,&recording);assert(playback&&opened==closed+1&&playback->spec.channels==4);
 assert(impl.OpenDevice(playback));int size=0;float *buffer=(float *)impl.GetDeviceBuf(playback,&size);assert(size==4096&&playback->spec.freq==48000);
 for(int n=0;n<256;n++){buffer[4*n]=100.0f;buffer[4*n+1]=-100.0f;buffer[4*n+2]=0.25f;buffer[4*n+3]=-0.5f;}
 buffer[2]=INFINITY;buffer[3]=NAN;buffer[6]=2.0f;buffer[7]=-2.0f;
 assert(impl.PlayDevice(playback,(const Uint8 *)buffer,size)&&outputs==1);
 assert(last[0]==0&&last[1]==0&&last[2]==32767&&last[3]==-32768&&last[4]==8191&&last[5]==-16383);
 assert(!impl.PlayDevice(playback,(const Uint8 *)buffer,size-4)&&outputs==1);
 fail_output=1;assert(!impl.PlayDevice(playback,(const Uint8 *)buffer,size));fail_output=0;
 impl.CloseDevice(playback);assert(!playback->hidden&&opened==closed);
 fail_mode=1;assert(!impl.OpenDevice(playback));impl.CloseDevice(playback);assert(opened==closed);fail_mode=0;
 alloc_fail=1;assert(!impl.OpenDevice(playback));impl.CloseDevice(playback);assert(opened==closed);alloc_fail=0;
 assert(impl.OpenDevice(playback));impl.CloseDevice(playback);assert(opened==closed+1);assert(prospero_haptic_reserve()==99&&opened==closed+1);assert(impl.OpenDevice(playback));impl.CloseDevice(playback);assert(opened==closed+1);
 impl.FreeDeviceHandle(playback);assert(!playback->handle);assert(sceAudioOutClose(retained_port)==0);retained_port=-1;assert(opened==closed);
 puts("PASS actual PS5 haptic SDL backend: advertise only after real port/mode probe;quad channels2/3 to paced stereo type10 port;finite/clamp/channel isolation;open/output/allocation/mode failures and close/reopen balanced under ASan/UBSan. Native-call fixtures,not hardware acceptance.");
}
'''
with tempfile.TemporaryDirectory(prefix='ps5-haptic-test-')as folder:
 w=Path(folder);(w/'audio').mkdir();(w/'SDL_internal.h').write_text(header)
 for f in ['SDL_audiodev_c.h','SDL_sysaudio.h']:(w/'audio'/f).write_text('')
 (w/'test.c').write_text(source)
 subprocess.run(['clang','-std=c11','-fsanitize=address,undefined','-I'+str(w),'-I'+str(ROOT/'client/ports/sdl'),str(w/'test.c'),'-o',str(w/'test')],check=True)
 subprocess.run([str(w/'test')],check=True)
