#!/usr/bin/env python3
"""Actual JNI buffer bridge in a real host JVM with checked JNI and UBSan."""
import argparse
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);args=p.parse_args()
w=ROOT/'build/client-bridge-test';w.mkdir(parents=True,exist_ok=True)
(w/'bridge.cpp').write_text('''
#include "buffer_bridge.hpp"
static void note(JNIEnv*env,jclass,jstring text){const char*p=env->GetStringUTFChars(text,nullptr);if(p){puts(p);env->ReleaseStringUTFChars(text,p);}}
extern "C" JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM*vm,void*){
 JNIEnv*env=nullptr;if(vm->GetEnv(reinterpret_cast<void**>(&env),JNI_VERSION_1_8)!=JNI_OK)return JNI_ERR;
 jclass c=env->FindClass("ClientBridge25");if(!c)return JNI_ERR;
 JNINativeMethod methods[]={
 {const_cast<char*>("pageSize"),const_cast<char*>("()J"),reinterpret_cast<void*>(&client_bridge_page_size)},
 {const_cast<char*>("fill"),const_cast<char*>("(Ljava/nio/ByteBuffer;J)J"),reinterpret_cast<void*>(&client_bridge_fill)},
 {const_cast<char*>("checkpoint"),const_cast<char*>("(Ljava/lang/String;)V"),reinterpret_cast<void*>(&note)}};
 return env->RegisterNatives(c,methods,3)==JNI_OK?JNI_VERSION_1_8:JNI_ERR;
}
'''.replace('#include "buffer_bridge.hpp"','#include <cstdio>\n#include "buffer_bridge.hpp"'))
(w/'RunClientBridge.java').write_text('public class RunClientBridge{public static void main(String[]args){System.load(args[0]);ClientBridge25.main(new String[0]);}}')
subprocess.run(['clang++','-std=c++17','-O1','-g','-dynamiclib','-fsanitize=undefined','-I'+str(args.java_home/'include'),'-I'+str(args.java_home/'include/darwin'),'-I'+str(ROOT/'client/native'),str(w/'bridge.cpp'),'-o',str(w/'libbridge.dylib')],check=True)
subprocess.run([str(args.java_home/'bin/javac'),'--release','25','-d',str(w),str(ROOT/'client/java/ClientBridge25.java'),str(w/'RunClientBridge.java')],check=True)
subprocess.run([str(args.java_home/'bin/java'),'-Xcheck:jni','-Xverify:all','-cp',str(w),'RunClientBridge',str(w/'libbridge.dylib')],check=True)
print('PASS actual JNI direct buffer writes including zero/slices/guard bytes/checksums/heap/null/readonly errors; host only, PS5 pending')
