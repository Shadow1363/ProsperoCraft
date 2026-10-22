#!/usr/bin/env python3
"""Run actual upstream LWJGL memory APIs against the built native core subset."""
import argparse
import os
from pathlib import Path
import subprocess
import hashlib
import platform
import zipfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args()
subprocess.run(['python3',str(ROOT/'tools/build_lwjgl_native.py'),'--runtime-workspace',str(a.runtime_workspace),'--java-home',str(a.java_home),'--host','--offline'],check=True)
w=ROOT/'build/lwjgl-core-test';w.mkdir(parents=True,exist_ok=True)
(w/'callback.c').write_text('''
#include <jni.h>
#include <stdio.h>
static void note(JNIEnv*e,jclass c,jstring s){(void)c;const char*p=(*e)->GetStringUTFChars(e,s,NULL);if(p){puts(p);(*e)->ReleaseStringUTFChars(e,s,p);}}
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM*v,void*r){(void)r;JNIEnv*e=NULL;if((*v)->GetEnv(v,(void**)&e,JNI_VERSION_1_8)!=JNI_OK)return JNI_ERR;jclass c=(*e)->FindClass(e,"ClientLwjglCore25");if(!c)return JNI_ERR;JNINativeMethod n={"checkpoint","(Ljava/lang/String;)V",(void*)&note};return (*e)->RegisterNatives(e,c,&n,1)==JNI_OK?JNI_VERSION_1_8:JNI_ERR;}
''')
(w/'RunLwjglCore.java').write_text('public class RunLwjglCore{public static void main(String[]a){System.load(a[0]);ClientLwjglCore25.main(new String[0]);}}')
subprocess.run(['clang','-dynamiclib','-I'+str(a.java_home/'include'),'-I'+str(a.java_home/'include/darwin'),str(w/'callback.c'),'-o',str(w/'libcallback.dylib')],check=True)
jar=ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar'
# This is a locally rebuilt native binary, so its paired host-test JAR must
# carry its actual digest rather than the upstream desktop binary's digest.
arch={'arm64':'arm64','aarch64':'arm64','x86_64':'x64'}[platform.machine().lower()]
resource='META-INF/macos/'+arch+'/org/lwjgl/liblwjgl.dylib.sha1'
paired=w/'lwjgl-host-paired.jar';native=ROOT/'build/client-ports/lwjgl-native/host/liblwjgl.dylib'
with zipfile.ZipFile(jar)as original,zipfile.ZipFile(paired,'w',zipfile.ZIP_DEFLATED)as output:
 assert resource in original.namelist(),resource
 for info in original.infolist():
  data=hashlib.sha1(native.read_bytes()).hexdigest().encode() if info.filename==resource else original.read(info.filename)
  output.writestr(info,data)
jar=paired

subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',str(jar),'-d',str(w),str(ROOT/'client/java/ClientLwjglCore25.java'),str(w/'RunLwjglCore.java')],check=True)
env=dict(os.environ);env['UBSAN_OPTIONS']='handle_segv=0:handle_sigbus=0:handle_sigfpe=0'
subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Dps5.test.coreLibrary='+str(native),'-Djava.library.path='+str(ROOT/'build/client-ports/lwjgl-native/host'),'-cp',str(w)+':'+str(jar),'RunLwjglCore',str(w/'libcallback.dylib')],env=env,check=True)
print('PASS actual upstream LWJGL Library/Pointer/MemoryUtil/MemoryStack JNI: allocate/realloc/calloc/alignment/free, typed memory/copy, Unicode, Java25Unsafe backend; host, not PS5 graphics')
