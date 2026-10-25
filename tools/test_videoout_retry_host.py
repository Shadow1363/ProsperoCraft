#!/usr/bin/env python3
"""Test the exact patched output-open state machine with controlled OS responses."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];w=ROOT/'build/wsi-diagnostics';s=(w/'wsi_common_videoout.c').read_text();start=s.index('static unsigned videoout_open_attempts;');end=s.index('PUBLIC int wsi_videoout_set_flip_rate',start)
source=r'''
#include <stdint.h>
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <assert.h>
#define PS5_VIDEO_OUT_USER_SYSTEM 255
#define PS5_VIDEO_OUT_MODE_HIGH_FRAME_RATE 15
#define PS5_VIDEO_OUT_MODE_RESTORE 1
#define VIDEOOUT_HIGH_REFRESH_LIMIT_NS UINT64_C(12500000)
struct wsi_videoout_output{bool opened,high_frame_rate;int handle;void*current;unsigned set_count;};
static struct wsi_videoout_output videoout_output;
static uint64_t clock_ns;static int results[2];static unsigned calls;static char last_message[384];
static uint64_t os_time_get_nano(void){return clock_ns;}
static int sceVideoOutOpen(int user,int bus,int index,const void*param){assert(user==255&&bus==0&&index==0&&!param&&calls<2);return results[calls++];}
static bool videoout_title_declares_high_frame_rate(void){return false;}
static int sceVideoOutIsOutputSupported(int h,unsigned m,const void*a,const void*b,const void*c){(void)h;(void)m;(void)a;(void)b;(void)c;return 0;}
static int sceVideoOutConfigureOutput(int h,unsigned m,const void*a,const void*b,const void*c){(void)h;(void)m;(void)a;(void)b;(void)c;return 0;}
static uint64_t videoout_vblank_period_ns(int h){(void)h;return 16666667;}
static void videoout_probe(const char*format,...){va_list a;va_start(a,format);vsnprintf(last_message,sizeof(last_message),format,a);va_end(a);}
'''+s[start:end]+r'''
static void reset(int first,int second){videoout_output=(struct wsi_videoout_output){.handle=-1};clock_ns=0;calls=0;videoout_open_attempts=0;videoout_open_retry_ns=0;results[0]=first;results[1]=second;last_message[0]=0;}
int main(void){reset(-7,9);assert(!videoout_open_locked()&&!videoout_output.opened&&calls==1&&strstr(last_message,"fffffff9"));clock_ns=1999999999;assert(!videoout_open_locked()&&calls==1);clock_ns=2000000000;assert(videoout_open_locked()&&videoout_output.opened&&videoout_output.handle==9&&calls==2);for(unsigned i=0;i<100;i++)assert(videoout_open_locked()&&calls==2);
reset(-7,-8);assert(!videoout_open_locked());clock_ns=2000000000;assert(!videoout_open_locked()&&!videoout_output.opened&&calls==2&&strstr(last_message,"fffffff8"));clock_ns=9000000000;for(unsigned i=0;i<100;i++)assert(!videoout_open_locked()&&calls==2);
reset(0,9);assert(videoout_open_locked()&&videoout_output.handle==0&&videoout_output.opened&&calls==1);assert(videoout_open_locked()&&calls==1);
reset(-7,9);assert(!videoout_open_locked());clock_ns=3000000000;videoout_output.current=(void*)1;assert(!videoout_open_locked()&&calls==1);videoout_output.current=NULL;videoout_output.set_count=1;assert(!videoout_open_locked()&&calls==1);
puts("PASS exact VideoOut open function:negative first result logged/not cached as success,no early retry,one retry at2s,success/zero handles retained,max2 failures,no retry with existing swapchain/buffers;synthetic OS responses only,PS5 pending");}
'''
p=w/'retry-host-check.c';p.write_text(source);binary=w/'retry-host-check';subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',str(binary)],check=True);subprocess.run([str(binary)],check=True)
