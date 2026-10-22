#!/usr/bin/env python3
"""Actual patched LWJGL PS5 TLS initialization failure and key-zero teardown."""
import argparse
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args()
port=ROOT/'client/ports/lwjgl';cache=ROOT/'.tools/lwjgl-native-src'
with tempfile.TemporaryDirectory(prefix='lwjgl-tls-')as folder:
 w=Path(folder).resolve()
 for name in ['common_tools.h','common_tools.c','org_lwjgl_system_MemoryUtil.c']:(w/name).write_bytes((cache/name).read_bytes())
 subprocess.run(['git','apply','--unsafe-paths','--directory='+str(w),str(port/'0002-native-core-ps5.patch')],check=True)
 (w/'PS5Config.h').write_bytes((port/'PS5Config.h').read_bytes())
 (w/'test.c').write_text('''
#include <assert.h>
#include <errno.h>
#define LWJGL_PS5
#define pthread_key_create test_key_create
#define pthread_key_delete test_key_delete
#include "common_tools.c"
static int injected,deleted;static pthread_key_t assigned;
int test_key_create(pthread_key_t* key,void(*destroy)(void*)){(void)destroy;if(injected)return injected;*key=assigned;return 0;}
int test_key_delete(pthread_key_t key){assert(key==assigned);deleted++;return 0;}
int main(void){
 assigned=0;assert(JNI_OnLoad(NULL,NULL)==JNI_VERSION_1_6);JNI_OnUnload(NULL,NULL);assert(deleted==1);JNI_OnUnload(NULL,NULL);assert(deleted==1);
 injected=EAGAIN;assert(JNI_OnLoad(NULL,NULL)==JNI_ERR);JNI_OnUnload(NULL,NULL);assert(deleted==1);
 injected=0;assigned=17;assert(JNI_OnLoad(NULL,NULL)==JNI_VERSION_1_6);JNI_OnUnload(NULL,NULL);assert(deleted==2);
 puts("PASS actual PS5 LWJGL TLS patch: key zero is valid/deleted exactly once, EAGAIN propagates JNI_ERR without deletion, subsequent valid load/unload");
}
''')
 subprocess.run(['clang','-std=c11','-O1','-g','-fsanitize=address,undefined','-I'+str(a.java_home/'include'),'-I'+str(a.java_home/'include/darwin'),'-I'+str(w),str(w/'test.c'),'-o',str(w/'test')],check=True)
 subprocess.run([str(w/'test')],check=True)
