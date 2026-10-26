#!/usr/bin/env python3
"""Verify exact early WSI entry shares the retained output with later opens."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];w=ROOT/'build/wsi-diagnostics';s=(w/'wsi_common_videoout.c').read_text();base=(w/'retry-host-check.c').read_text().split('static void reset(')[0];base=base.replace('#include <stdint.h>','#include <stdint.h>\n#include <pthread.h>');base=base.replace('struct wsi_videoout_output{','struct wsi_videoout_output{int lock;')
a=s.index('/* Startup uses the real WSI owner');b=s.index('static void\nvideoout_settle_modes',a)
source=base+r'''
#define PUBLIC
static pthread_once_t videoout_once=PTHREAD_ONCE_INIT;
static pthread_mutex_t test_lock=PTHREAD_MUTEX_INITIALIZER;
static unsigned initializations;
static void videoout_output_init_once(void){++initializations;}
static void call_once(pthread_once_t*once,void(*fn)(void)){assert(pthread_once(once,fn)==0);}
static void mtx_lock(int*lock){(void)lock;assert(pthread_mutex_lock(&test_lock)==0);}
static void mtx_unlock(int*lock){(void)lock;assert(pthread_mutex_unlock(&test_lock)==0);}
'''+s[a:b]+r'''
static void*prepare(void*arg){(void)arg;assert(client_wsi_videoout_prepare()==0);return NULL;}
int main(int argc,char**argv){(void)argv;results[0]=argc==1?7:argc==2?0:-7;results[1]=-8;videoout_output.handle=-1;
if(argc<=2){pthread_t threads[4];for(unsigned i=0;i<4;++i)assert(pthread_create(&threads[i],NULL,prepare,NULL)==0);for(unsigned i=0;i<4;++i)assert(pthread_join(threads[i],NULL)==0);assert(calls==1&&initializations==1&&videoout_output.opened&&videoout_output.handle==results[0]);for(unsigned i=0;i<100;++i)assert(videoout_open_locked()&&calls==1);assert(!videoout_output.current&&!videoout_output.set_count);}
else{assert(client_wsi_videoout_prepare()==-7&&!videoout_output.opened&&calls==1);assert(client_wsi_videoout_prepare()==-7&&calls==1);clock_ns=2000000000;assert(client_wsi_videoout_prepare()==-8&&!videoout_output.opened&&calls==2);assert(client_wsi_videoout_prepare()==-8&&calls==2);}
puts("PASS exact early WSI entry:shared lock/once,concurrent retention,positive/zero handle reused by later opens,no buffers,raw failure/delayed retry preserved;synthetic OS only,PS5 pending");}
'''
p=w/'early-owner-host-check.c';p.write_text(source);binary=w/'early-owner-host-check';subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-pthread',str(p),'-o',str(binary)],check=True)
for args in [[],['zero'],['fail','twice']]:subprocess.run([str(binary),*args],check=True)
