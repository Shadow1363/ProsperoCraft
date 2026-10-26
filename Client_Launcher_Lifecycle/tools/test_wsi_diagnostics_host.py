#!/usr/bin/env python3
"""Exercise actual bounded diagnostic helper;no native WSI/GPU emulation claim."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];w=ROOT/'build/wsi-diagnostics';s=(w/'wsi_common_videoout.c').read_text();start=s.index('extern void client_gpu_stage');end=s.index('#define VIDEOOUT_BUFFERS',start)
source=r'''
#include <stdint.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <pthread.h>
typedef int VkResult;
#define VK_SUCCESS 0
static unsigned calls;
void client_gpu_stage(const char*,int);
void client_gpu_stage(const char*message,int code){assert(strlen(message)<384&&code==INT32_MIN);__atomic_fetch_add(&calls,1,__ATOMIC_RELAXED);}
'''+s[start:end]+r'''
static void*worker(void*arg){(void)arg;for(unsigned i=0;i<100;i++)assert(videoout_probe_result("test",-3)==-3);return NULL;}
int main(void){assert(videoout_probe_result("success",0)==0&&calls==0);char long_text[2048];memset(long_text,'x',sizeof(long_text)-1);long_text[sizeof(long_text)-1]=0;videoout_probe("%s",long_text);assert(calls==1);pthread_t threads[4];for(unsigned i=0;i<4;i++)assert(pthread_create(&threads[i],NULL,worker,NULL)==0);for(unsigned i=0;i<4;i++)assert(pthread_join(threads[i],NULL)==0);assert(calls==64);puts("PASS actual WSI diagnostic helper:unchanged success/failure codes,384byte bounded format,64event cap under4threads;no GPU/OS failure-path validation");}
'''
p=w/'host-check.c';p.write_text(source);binary=w/'host-check';subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-pthread',str(p),'-o',str(binary)],check=True);subprocess.run([str(binary)],check=True)
