#!/usr/bin/env python3
"""Exercise real private WSI high-refresh admission with controlled VideoOut calls."""
from pathlib import Path
import json, subprocess, tempfile
r=Path(__file__).resolve().parents[1]
s=(r/'build/wsi-diagnostics/wsi_common_videoout.c').read_text()
parser=s[s.index('static bool\nvideoout_title_declares_high_frame_rate'):s.index('/* Opens VideoOut once per process')]
opening=s[s.index('static unsigned videoout_open_attempts;'):s.index('PUBLIC int wsi_videoout_set_flip_rate')]
source=r'''
#define _POSIX_C_SOURCE 200809L
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#define VIDEOOUT_ATTRIBUTE3_HIGH_FRAME_RATE 0x40u
#define VIDEOOUT_PERIOD_INTERVALS 6
#define VIDEOOUT_HIGH_REFRESH_LIMIT_NS UINT64_C(12500000)
#define PS5_VIDEO_OUT_USER_SYSTEM 255
#define PS5_VIDEO_OUT_MODE_HIGH_FRAME_RATE 15
#define PS5_VIDEO_OUT_MODE_RESTORE 1
struct wsi_videoout_output{bool opened,high_frame_rate;int handle;void*current;unsigned set_count;};
static struct wsi_videoout_output videoout_output;
static int support,configuration,wait_error,restore_calls,support_calls,configure_calls,open_calls;
static uint64_t clock_ns,period_ns;
static uint64_t os_time_get_nano(void){return clock_ns;}
static int sceVideoOutWaitVblank(int h){assert(h==7);clock_ns+=period_ns;return wait_error;}
static int sceVideoOutOpen(int u,int b,int i,const void*p){assert(u==255&&b==0&&i==0&&!p);++open_calls;return 7;}
static int sceVideoOutIsOutputSupported(int h,unsigned m,const void*a,const void*b,const void*c){assert(h==7&&m==15&&!a&&!b&&!c);++support_calls;return support;}
static int sceVideoOutConfigureOutput(int h,unsigned m,const void*a,const void*b,const void*c){assert(h==7&&!a&&!b&&!c);if(m==1){++restore_calls;return 0;}assert(m==15);++configure_calls;return configuration;}
static void videoout_probe(const char*fmt,...){(void)fmt;}
'''+parser+opening+r'''
static void reset(void){videoout_output=(struct wsi_videoout_output){.handle=-1};videoout_open_attempts=0;videoout_open_retry_ns=0;clock_ns=0;support=1;configuration=wait_error=restore_calls=support_calls=configure_calls=open_calls=0;period_ns=8341675;}
int main(int argc,char**argv){assert(argc==3);assert(setenv("PS5_VIDEOOUT_PARAM_JSON",argv[1],1)==0);
reset();assert(videoout_title_declares_high_frame_rate());assert(videoout_open_locked()&&videoout_output.high_frame_rate&&configure_calls==1&&!restore_calls);assert(videoout_open_locked()&&open_calls==1&&configure_calls==1);
reset();support=0;assert(videoout_open_locked()&&!videoout_output.high_frame_rate&&support_calls==1&&!configure_calls);
reset();support=-7;assert(videoout_open_locked()&&!videoout_output.high_frame_rate&&!configure_calls);
reset();configuration=-8;assert(videoout_open_locked()&&!videoout_output.high_frame_rate&&configure_calls==1&&!restore_calls);
reset();period_ns=16683350;assert(videoout_open_locked()&&!videoout_output.high_frame_rate&&restore_calls==1);
reset();wait_error=-1;assert(videoout_open_locked()&&!videoout_output.high_frame_rate&&restore_calls==1);
assert(setenv("PS5_VIDEOOUT_PARAM_JSON",argv[2],1)==0);reset();assert(!videoout_title_declares_high_frame_rate());assert(videoout_open_locked()&&!videoout_output.high_frame_rate&&!support_calls&&!configure_calls);
puts("PASS real WSI manifest parser/high-refresh admission/vblank measurement:120Hz success/retention,unsupported/error/configure refusal/60Hz measurement/wait failure fallback,legacy manifest;synthetic OS responses,PS5 pending");}
'''
assert json.loads((r/'client/startup/param.json').read_text())['attribute3']&0x40
with tempfile.TemporaryDirectory(prefix='videoout-refresh-') as d:
 w=Path(d);unit=w/'check.c';unit.write_text(source);binary=w/'check'
 low=w/'60.json';low.write_text('{"attribute3":0}')
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(unit),'-o',str(binary)],check=True)
 subprocess.run([str(binary),str(r/'client/startup/param.json'),str(low)],check=True)
