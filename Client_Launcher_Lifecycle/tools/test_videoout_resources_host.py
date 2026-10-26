#!/usr/bin/env python3
"""Exercise exact read-only resource helper with controlled kernel query results."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];w=ROOT/'build/wsi-diagnostics';s=(w/'wsi_common_videoout.c').read_text();start=s.index('/* Read-only resource evidence;');end=s.index('static bool\nvideoout_open_locked',start)
source=r'''
#include <assert.h>
#include <errno.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#define __PROSPERO__ 1
#define PS5_KERNEL_DIRECT_ALIGNMENT 65536
static unsigned calls;static int failure;static int64_t total=4096;static char message[384];
static int sceKernelConfiguredFlexibleMemorySize(size_t*n){++calls;errno=7;if(failure)return -2;*n=100;return 0;}
static int sceKernelAvailableFlexibleMemorySize(size_t*n){++calls;errno=8;if(failure)return -3;*n=42;return 0;}
static int64_t sceKernelGetDirectMemorySize(void){++calls;errno=9;return total;}
static int sceKernelAvailableDirectMemorySize(int64_t lo,int64_t hi,size_t align,int64_t*start,size_t*n){assert(lo==0&&hi==total&&align==65536);++calls;errno=10;if(failure)return -4;*start=512;*n=1024;return 0;}
static void videoout_probe(const char*format,...){va_list a;va_start(a,format);vsnprintf(message,sizeof(message),format,a);va_end(a);errno=11;}
'''+s[start:end]+r'''
int main(void){errno=123;videoout_probe_memory("before-open");assert(errno==123&&calls==4&&strstr(message,"configured100 flexibleRc0x00000000 flexible42")&&strstr(message,"directLargest1024 directStart512"));
failure=1;calls=0;errno=124;videoout_probe_memory("after-open");assert(errno==124&&calls==4&&strstr(message,"configuredRc0xfffffffe configured0")&&strstr(message,"flexibleRc0xfffffffd flexible0")&&strstr(message,"directRc0xfffffffc directLargest0 directStart-1"));
total=-5;calls=0;videoout_probe_memory("bad-total");assert(errno==124&&calls==3&&strstr(message,"directTotal-5 directRc0xffffffff"));puts("PASS exact WSI resource helper:read-only query arguments/statuses/values,failed-query sentinels,invalid-total skips range query,errno preserved;synthetic kernel results only,PS5 pending");}
'''
p=w/'resources-host-check.c';p.write_text(source);binary=w/'resources-host-check';subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',str(binary)],check=True);subprocess.run([str(binary)],check=True)
