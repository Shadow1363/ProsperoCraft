#!/usr/bin/env python3
"""Run actual LWJGL/libffi upcalls and OpenAL mixer on host;no PS5 pass inference."""
from pathlib import Path
import argparse,subprocess,json,os
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args();w=ROOT/'build/native-bootstrap-host-026';w.mkdir(exist_ok=True)
(w/'callback.c').write_text('''#include <jni.h>\n#include <stdio.h>\nstatic void note(JNIEnv*e,jclass c,jstring s){(void)c;const char*p=(*e)->GetStringUTFChars(e,s,NULL);if(p){puts(p);fflush(stdout);(*e)->ReleaseStringUTFChars(e,s,p);}}\nJNIEXPORT jint JNICALL JNI_OnLoad(JavaVM*v,void*r){(void)r;JNIEnv*e=NULL;if((*v)->GetEnv(v,(void**)&e,JNI_VERSION_1_8)!=JNI_OK)return JNI_ERR;jclass c=(*e)->FindClass(e,"ClientNativeBootstrap25");if(!c)return JNI_ERR;JNINativeMethod m={"checkpoint","(Ljava/lang/String;)V",(void*)&note};return (*e)->RegisterNatives(e,c,&m,1)==JNI_OK?JNI_VERSION_1_8:JNI_ERR;}''')
helper=w/'libcallback.dylib';subprocess.run(['clang','-dynamiclib','-fsanitize=undefined','-I'+str(a.java_home/'include'),'-I'+str(a.java_home/'include/darwin'),str(w/'callback.c'),str(ROOT/'client/native_bootstrap/callback_probe.c'),'-o',str(helper)],check=True)
lock=json.loads((ROOT/'client/26.3.lock.json').read_text());cp=':'.join([str(ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar'),*[str(ROOT/'.tools/client'/r['file'])for r in lock['artifacts']]])
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/native_bootstrap/ClientNativeBootstrap25.java'),str(ROOT/'tools/fixtures/PS5DispatchHost25.java')],check=True)
cmd=[str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Dps5.test.ffiCore='+str(ROOT/'build/libffi-host/liblwjglffi.dylib'),'-Dps5.test.callbackHelper='+str(helper),'-Dps5.test.hostLoader='+str(ROOT/'build/sdl-host-012/libhost-loader.dylib'),'-Dps5.test.openal='+str(ROOT/'build/openal-host/libopenal.dylib'),'-cp',str(w)+':'+cp,'ClientNativeBootstrap25']
r=subprocess.run(cmd,text=True,capture_output=True,timeout=120,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'));(w/'result.log').write_text(r.stdout+r.stderr);print(r.stdout,r.stderr);r.check_returncode()
for marker in ['WARNING in native method','FATAL ERROR in native method','runtime error:']:assert marker not in r.stdout+r.stderr,marker
assert r.stdout.count('PASS genuine libffi/LWJGL callback cycle')==3 and r.stdout.count('PASS real OpenAL Soft loopback cycle')==3

# Actual patched PS5 enum dispatch using real host native providers.
ported=list(cmd);ported[ported.index('-cp')+1]=str(w)+':'+str(ROOT/'build/client-ports/lwjgl-modules/lwjgl-3.4.3-ps5-modules.jar')+':'+cp;ported[-1]='PS5DispatchHost25'
r=subprocess.run(ported,text=True,capture_output=True,timeout=120,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'));(w/'ps5-dispatch.log').write_text(r.stdout+r.stderr);print(r.stdout,r.stderr);r.check_returncode()
for marker in ['WARNING in native method','FATAL ERROR in native method','runtime error:']:assert marker not in r.stdout+r.stderr,marker
assert r.stdout.count('PASS genuine libffi/LWJGL callback cycle')==3 and r.stdout.count('PASS real OpenAL Soft loopback cycle')==3
