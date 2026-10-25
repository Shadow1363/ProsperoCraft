#!/usr/bin/env python3
"""Exercise exact patched flip worker with controlled fence/OS responses."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];w=ROOT/'build/wsi-diagnostics';s=(w/'wsi_common_videoout.c').read_text();a=s.index('static unsigned videoout_flip_probe_count;');b=s.index('/* --- VK_KHR_display',a)
source=r'''
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <setjmp.h>
#define ARRAY_SIZE(a) (sizeof(a)/sizeof((a)[0]))
#define VK_TRUE 1
#define VK_SUCCESS 0
#define PS5_VIDEO_OUT_FLIP_VSYNC 1
 typedef int VkResult;
struct wsi_device{VkResult(*WaitForFences)(int,unsigned,const uint64_t*,int,uint64_t);};
struct wsi_videoout_swapchain{struct{const struct wsi_device*wsi;int device;}base;unsigned in_flight;};
struct wsi_videoout_present{struct wsi_videoout_swapchain*chain;unsigned buffer;uint64_t fence;};
struct wsi_videoout_output{int lock,changed,handle;int64_t flip_argument;struct{int64_t argument;bool pending;}buffer[5];struct wsi_videoout_present queue[10];unsigned queue_head,queue_count;};
static struct wsi_videoout_output videoout_output;
static jmp_buf done;static unsigned locks,wait_calls,flip_calls,event_count;static int wait_result,flip_result,phase;
static char events[8][384];
static void videoout_probe(const char*format,...){assert(event_count<8);va_list a;va_start(a,format);vsnprintf(events[event_count++],384,format,a);va_end(a);}
static void mtx_lock(int*unused){(void)unused;assert(locks==0);locks=1;}
static void mtx_unlock(int*unused){(void)unused;assert(locks==1);locks=0;}
static void cnd_wait(int*a,int*b){(void)a;(void)b;assert(!"unexpected wait on empty queue");}
static void cnd_broadcast(int*unused){(void)unused;assert(locks==1&&phase==2);longjmp(done,1);}
static VkResult wait_fence(int device,unsigned count,const uint64_t*fence,int all,uint64_t timeout){assert(locks==0&&phase==0&&device==6&&count==1&&*fence==42&&all==1&&timeout==UINT64_MAX);phase=1;++wait_calls;return wait_result;}
static int sceVideoOutSubmitFlip(int h,int buffer,unsigned mode,int64_t arg){assert(locks==1&&phase==1&&h==7&&buffer==2&&mode==1&&arg==10);phase=2;++flip_calls;return flip_result;}
'''+s[a:b]+r'''
static struct wsi_device device={wait_fence};static struct wsi_videoout_swapchain chain;
static void run(int wait,int flip,unsigned previous){wait_result=wait;flip_result=flip;phase=0;locks=wait_calls=flip_calls=event_count=0;videoout_flip_probe_count=previous;videoout_present_probe_count=0;memset(events,0,sizeof(events));memset(&videoout_output,0,sizeof(videoout_output));
 chain=(struct wsi_videoout_swapchain){.base={&device,6},.in_flight=1};videoout_output.handle=7;videoout_output.flip_argument=9;videoout_output.queue_count=1;videoout_output.queue[0]=(struct wsi_videoout_present){&chain,2,42};videoout_output.buffer[2].pending=true;
 if(!setjmp(done))(void)videoout_flip_thread(NULL);
 assert(wait_calls==1&&flip_calls==1&&locks==1&&videoout_output.queue_head==1&&videoout_output.queue_count==0&&chain.in_flight==0&&!videoout_output.buffer[2].pending);
 assert(videoout_output.flip_argument==(flip==0?10:9));assert(videoout_output.buffer[2].argument==(flip==0?10:0));}
int main(void){run(0,0,0);assert(event_count==3&&strstr(events[0],"fence begin")&&strstr(events[1],"fence result0")&&strstr(events[2],"submit result0x00000000"));run(0,0,8);assert(event_count==0);run(-4,0,8);assert(event_count==1&&strstr(events[0],"fence result-4"));run(0,-9,8);assert(event_count==1&&strstr(events[0],"submit result0xfffffff7"));run(-4,-9,0);assert(event_count==3);puts("PASS exact flip worker:ordered fence/OS calls and unchanged queue/buffer/argument behavior,first8 progress cap and raw error logging;failed-fence existing behavior retained,synthetic OS only,PS5 pending");}
'''
p=w/'present-host-check.c';p.write_text(source);binary=w/'present-host-check';subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-Wno-unused-parameter','-fsanitize=address,undefined',str(p),'-o',str(binary)],check=True);subprocess.run([str(binary)],check=True)
