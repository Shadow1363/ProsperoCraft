#!/usr/bin/env python3
"""Real JVM System.loadLibrary and scoped dynamic symbol calls, XcheckJNI/UBSan."""
import argparse
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);args=p.parse_args()
w=ROOT/'build/client-library-test';w.mkdir(parents=True,exist_ok=True)
subprocess.run(['clang','-std=c11','-O1','-g','-dynamiclib','-fsanitize=undefined','-I'+str(args.java_home/'include'),'-I'+str(args.java_home/'include/darwin'),str(ROOT/'client/native/resident_library.c'),'-o',str(w/'libps5clientbridge.dylib')],check=True)
(w/'RunClientLibrary.java').write_text('''
public class RunClientLibrary {
 public static void main(String[] args) throws Exception {
  ClientLibrary25.main(new String[0]);
 }
}
''')
# The checkpoint alone is registered as the probe UI callback, as on PS5.
(w/'callback.c').write_text('''
#include <jni.h>
#include <stdio.h>
static void checkpoint(JNIEnv*e,jclass c,jstring s){(void)c;const char*p=(*e)->GetStringUTFChars(e,s,NULL);if(p){puts(p);(*e)->ReleaseStringUTFChars(e,s,p);}}
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM*v,void*r){(void)r;JNIEnv*e=NULL;if((*v)->GetEnv(v,(void**)&e,JNI_VERSION_1_8)!=JNI_OK)return JNI_ERR;jclass c=(*e)->FindClass(e,"ClientLibrary25");if(!c)return JNI_ERR;JNINativeMethod m={"checkpoint","(Ljava/lang/String;)V",(void*)&checkpoint};return (*e)->RegisterNatives(e,c,&m,1)==JNI_OK?JNI_VERSION_1_8:JNI_ERR;}
''')
subprocess.run(['clang','-dynamiclib','-I'+str(args.java_home/'include'),'-I'+str(args.java_home/'include/darwin'),str(w/'callback.c'),'-o',str(w/'libcallback.dylib')],check=True)
(w/'RunClientLibrary.java').write_text('public class RunClientLibrary{public static void main(String[]args){System.load(args[0]);ClientLibrary25.main(new String[0]);}}')
subprocess.run([str(args.java_home/'bin/javac'),'--release','25','-d',str(w),str(ROOT/'client/java/ClientLibrary25.java'),str(w/'RunClientLibrary.java')],check=True)
subprocess.run([str(args.java_home/'bin/java'),'-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','-Djava.library.path='+str(w),'-cp',str(w),'RunClientLibrary',str(w/'libcallback.dylib')],check=True)
print('PASS actual System.loadLibrary/JNI_OnLoad once, ordinary JNI native lookup, scoped dlopen/dlsym/function invocation/repeated closes and missing/wrong-ABI/heap/null/unknown-library errors; PS5 resident path pending')
