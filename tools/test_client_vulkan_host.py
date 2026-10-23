#!/usr/bin/env python3
"""Run unmodified LWJGL Vulkan command bindings against a real MoltenVK host GPU."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',required=True,type=Path);p.add_argument('--runtime-workspace',required=True,type=Path);a=p.parse_args()
subprocess.run(['python3',str(ROOT/'tools/test_lwjgl_core.py'),'--java-home',str(a.java_home),'--runtime-workspace',str(a.runtime_workspace)],check=True)
w=ROOT/'build/vulkan-host-005';w.mkdir(exist_ok=True)
(w/'callback.c').write_text('''#include <jni.h>
#include <stdio.h>
static void note(JNIEnv*e,jclass c,jstring s){(void)c;const char*p=(*e)->GetStringUTFChars(e,s,NULL);if(p){puts(p);fflush(stdout);(*e)->ReleaseStringUTFChars(e,s,p);}}
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM*v,void*r){(void)r;JNIEnv*e=NULL;if((*v)->GetEnv(v,(void**)&e,JNI_VERSION_1_8)!=JNI_OK)return JNI_ERR;jclass c=(*e)->FindClass(e,"ClientVulkan25");if(!c)return JNI_ERR;JNINativeMethod n={"checkpoint","(Ljava/lang/String;)V",(void*)&note};return (*e)->RegisterNatives(e,c,&n,1)==JNI_OK?JNI_VERSION_1_8:JNI_ERR;}
''')
(w/'RunVulkan.java').write_text('public class RunVulkan{public static void main(String[]args){System.load(args[0]);ClientVulkan25.main(new String[0]);}}\n')
subprocess.run(['clang','-dynamiclib','-I'+str(a.java_home/'include'),'-I'+str(a.java_home/'include/darwin'),str(w/'callback.c'),'-o',str(w/'libcallback.dylib')],check=True)
lock=json.loads((ROOT/'client/26.3.lock.json').read_text());row=next(r for r in lock['artifacts']if r['file']=='lwjgl-vulkan-3.4.3.jar');vulkan=ROOT/'.tools/client'/row['file']
assert hashlib.sha256(vulkan.read_bytes()).hexdigest()==row['sha256']
core=ROOT/'build/lwjgl-core-test/lwjgl-host-paired.jar';cp=str(core)+':'+str(vulkan)
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/vulkan/ClientVulkan25.java'),str(w/'RunVulkan.java')],check=True)
env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1')
result=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Dps5.test.vulkanLibrary=/opt/homebrew/lib/libMoltenVK.dylib','-Djava.library.path='+str(ROOT/'build/client-ports/lwjgl-native/host'),'-cp',str(w)+':'+cp,'RunVulkan',str(w/'libcallback.dylib')],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
(w/'result.log').write_text(result.stdout);result.check_returncode()
for marker in ['runtime error:','WARNING in native method','FATAL ERROR in native method','Exception in thread','Failed to locate address']:assert marker not in result.stdout,marker
assert result.stdout.count('via LWJGL vkQueueSubmit')==12
assert result.stdout.count('bindings and GPU byte checks PASS')==3
assert 'PASS unmodified LWJGL Vulkan bindings:12 GPU transfers,3 instance/device lifecycles, VK loader cleanup'in result.stdout
assert hashlib.sha256(vulkan.read_bytes()).hexdigest()==row['sha256']
print('PASS original LWJGL Vulkan3.4.3 JAR with standard VK.create provider/VkInstance/VkDevice tables/structs/commands,12real GPU copy-fill-readbacks8..65536,full word+guard checks,3create/destroy cycles,duplicate-init rejection and loader cleanup; Java25 Xint/XcheckJNI/verify + real core UBSan + MoltenVK physical host GPU. PS5 pending.')
