#!/usr/bin/env python3
"""Real native module-discovery/open/read/close adapter with deterministic OS APIs."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];w=ROOT/'build/input105-native-api';w.mkdir(exist_ok=True)
source=r'''
#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "ps5_hid.h"
static int loads,opens,reads,closes,loaded[2];static int missing;
int sceSysmoduleLoadModule(uint16_t id){assert(id==0x0106||id==0x00a9);loaded[id==0x00a9]=1;loads++;return 0;}
int sceKernelGetModuleList(int*h,size_t count,size_t*actual){assert(count==512);h[0]=10;h[1]=20;*actual=2;return 0;}
int sceKernelGetModuleInfo(int h,void*p){struct info{uint64_t size;char name[256];unsigned char rest[1024];};struct info*i=p;if(i->size!=0x1a8)return -1;snprintf(i->name,256,"%s",h==10?"libSceKeyboard":"libSceMouse");return 0;}
static int init(void){return 0;}
static int open_hid(int user,int type,int index,const void*param){assert(user==42&&type==0&&index<4&&*(const uint64_t*)param==0);opens++;return index+100;}
static int read_hid(int handle,void*packets,int count){assert(handle>=100&&packets&&count>0);reads++;return 0;}
static int close_hid(int handle){assert(handle>=100);closes++;return 0;}
int sceKeyboardInit(void){return init();}int sceMouseInit(void){return init();}
int sceKeyboardOpen(int u,int t,int i,const void*p){return open_hid(u,t,i,p);}
int sceMouseOpen(int u,int t,int i,const void*p){return open_hid(u,t,i,p);}
int sceKeyboardRead(int h,void*p,int n){return read_hid(h,p,n);}
int sceMouseRead(int h,void*p,int n){return read_hid(h,p,n);}
int sceKeyboardClose(int h){return close_hid(h);}int sceMouseClose(int h){return close_hid(h);}
int sceKernelDlsym(int h,const char*name,void**fn){if(missing&&strstr(name,"Mouse")){*fn=NULL;return -1;}if(strstr(name,"Init"))*fn=(void*)init;else if(strstr(name,"Open"))*fn=(void*)open_hid;else if(strstr(name,"Read"))*fn=(void*)read_hid;else if(strstr(name,"Close"))*fn=(void*)close_hid;else return -1;return 0;}
int sceUserServiceGetInitialUser(int32_t*u){*u=42;return 0;}
int main(int argc,char**argv){missing=argc>1;prospero_hid_preload();prospero_hid_preload();assert(loads==2&&loaded[0]&&loaded[1]);int keyboard=prospero_hid_open(0,1),mouse=prospero_hid_open(1,0);assert(keyboard==101);if(missing)assert(mouse<0);else assert(mouse==100);struct prospero_keyboard_packet p={0};assert(prospero_hid_read(0,keyboard,&p,1)==0);prospero_hid_close(0,keyboard);assert(reads==1&&closes==1);assert(prospero_hid_open(2,0)<0&&prospero_hid_open(0,4)<0&&prospero_hid_read(0,-1,&p,1)<0);puts("PASS actual optional system HID discovery/module sizes/dlsym/user binding/idempotence/open/read/close and missing-mouse behavior;no arbitrary code loader");}
'''
(w/'test.c').write_text(source)
subprocess.run(['clang','-DPROSPERO_HID_LOOKUP_ONLY','-std=c11','-O1','-g','-fsanitize=address,undefined','-I'+str(ROOT/'client/ports/sdl'),str(w/'test.c'),str(ROOT/'client/ports/sdl/ps5_hid_native.c'),'-o',str(w/'test')],check=True)
for args in [[],['missing-mouse']]:subprocess.run([str(w/'test'),*args],check=True,timeout=20)

# Direct imports remain usable when the title cannot enumerate system modules.
src=source.replace('missing=argc>1;','missing=0;').replace('h[0]=10;h[1]=20;*actual=2;return 0;','*actual=0;return -1;').replace('int keyboard=prospero_hid_open','assert(opens==8);int keyboard=prospero_hid_open')
(w/'direct.c').write_text(src)
subprocess.run(['clang','-std=c11','-O1','-g','-fsanitize=address,undefined','-I'+str(ROOT/'client/ports/sdl'),str(w/'direct.c'),str(ROOT/'client/ports/sdl/ps5_hid_native.c'),'-o',str(w/'direct')],check=True)
subprocess.run([str(w/'direct')],check=True,timeout=20)
