#!/usr/bin/env python3
"""Run unmodified LWJGL Vulkan command bindings against a real MoltenVK host GPU."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',required=True,type=Path);p.add_argument('--runtime-workspace',required=True,type=Path);p.add_argument('--shader',action='store_true');p.add_argument('--render',action='store_true');a=p.parse_args()
if a.shader and a.render:p.error('Choose one candidate')
fixture='ClientRender25' if a.render else 'ClientShader25' if a.shader else 'ClientVulkan25'
subprocess.run(['python3',str(ROOT/'tools/test_lwjgl_core.py'),'--java-home',str(a.java_home),'--runtime-workspace',str(a.runtime_workspace)],check=True)
w=ROOT/('build/render-host-010' if a.render else 'build/shader-host-009' if a.shader else 'build/vulkan-host-008');w.mkdir(exist_ok=True)
callback='''#include <jni.h>
#include <stdio.h>
static void note(JNIEnv*e,jclass c,jstring s){(void)c;const char*p=(*e)->GetStringUTFChars(e,s,NULL);if(p){puts(p);fflush(stdout);(*e)->ReleaseStringUTFChars(e,s,p);}}
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM*v,void*r){(void)r;JNIEnv*e=NULL;if((*v)->GetEnv(v,(void**)&e,JNI_VERSION_1_8)!=JNI_OK)return JNI_ERR;jclass c=(*e)->FindClass(e,"ClientVulkan25");if(!c)return JNI_ERR;JNINativeMethod n={"checkpoint","(Ljava/lang/String;)V",(void*)&note};return (*e)->RegisterNatives(e,c,&n,1)==JNI_OK?JNI_VERSION_1_8:JNI_ERR;}
'''
if a.render:
 callback=callback.replace('#include <stdio.h>','#include <stdio.h>\n#include <stdlib.h>')
 callback=callback.replace('JNIEXPORT jint JNICALL JNI_OnLoad','''static void publish(JNIEnv*e,jclass c,jobject b,jint width,jint height){(void)c;void*p=(*e)->GetDirectBufferAddress(e,b);jlong n=(*e)->GetDirectBufferCapacity(e,b);const char*path=getenv("PS5_RENDER_READBACK_PATH");if(!p||n<256*256*4||width!=256||height!=256||!path){(*e)->ThrowNew(e,(*e)->FindClass(e,"java/lang/IllegalArgumentException"),"Invalid host image");return;}FILE*f=fopen(path,"wb");if(!f){(*e)->ThrowNew(e,(*e)->FindClass(e,"java/io/IOException"),"Host image open failed");return;}int bad=fwrite(p,1,256*256*4,f)!=256*256*4;if(fclose(f))bad=1;if(bad)(*e)->ThrowNew(e,(*e)->FindClass(e,"java/io/IOException"),"Host image write failed");}
JNIEXPORT jint JNICALL JNI_OnLoad''')
 callback=callback.replace('JNINativeMethod n={"checkpoint","(Ljava/lang/String;)V",(void*)&note};return (*e)->RegisterNatives(e,c,&n,1)', 'JNINativeMethod n[]={{"checkpoint","(Ljava/lang/String;)V",(void*)&note},{"publishPixels","(Ljava/nio/ByteBuffer;II)V",(void*)&publish}};return (*e)->RegisterNatives(e,c,n,2)')
(w/'callback.c').write_text(callback.replace('ClientVulkan25',fixture))
(w/'RunVulkan.java').write_text('public class RunVulkan{public static void main(String[]args){System.load(args[0]);'+fixture+'.main(new String[0]);}}\n')
subprocess.run(['clang','-dynamiclib','-I'+str(a.java_home/'include'),'-I'+str(a.java_home/'include/darwin'),str(w/'callback.c'),'-o',str(w/'libcallback.dylib')],check=True)
lock=json.loads((ROOT/'client/26.3.lock.json').read_text());row=next(r for r in lock['artifacts']if r['file']=='lwjgl-vulkan-3.4.3.jar');vulkan=ROOT/'.tools/client'/row['file']
assert hashlib.sha256(vulkan.read_bytes()).hexdigest()==row['sha256']
core=ROOT/'build/lwjgl-core-test/lwjgl-host-paired.jar';cp=str(core)+':'+str(vulkan)
sources=[ROOT/'client/vulkan/ClientVulkan25.java']
if a.render:
 from compile_client_render import compile_render
 sources=[ROOT/'client/render/ClientRender25.java',compile_render()]
elif a.shader:
 from compile_client_shader import compile_shader
 sources=[ROOT/'client/shader/ClientShader25.java',compile_shader()]
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(path)for path in sources],str(w/'RunVulkan.java')],check=True)
env=dict(os.environ,PS5_RENDER_READBACK_PATH=str(w/'readback.rgba'),UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1')
result=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Dps5.test.vulkanLibrary=/opt/homebrew/lib/libMoltenVK.dylib','-Djava.library.path='+str(ROOT/'build/client-ports/lwjgl-native/host'),'-cp',str(w)+':'+cp,'RunVulkan',str(w/'libcallback.dylib')],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
(w/'result.log').write_text(result.stdout);result.check_returncode()
for marker in ['runtime error:','WARNING in native method','FATAL ERROR in native method','Exception in thread','Failed to locate address']:assert marker not in result.stdout,marker
if a.render:
 assert result.stdout.count('draw graphics cycle')==9
 assert result.stdout.count('all pixels/guards PASS')==3
 assert 'PASS original LWJGL graphics pipeline:9 draws' in result.stdout
 data=(w/'readback.rgba').read_bytes();assert len(data)==256*256*4
 import struct,zlib
 def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
 png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',256,256,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(b'\0'+data[y*1024:(y+1)*1024]for y in range(256))))+chunk(b'IEND',b'')
 (w/'readback.png').write_bytes(png)
elif a.shader:
 assert result.stdout.count('dispatch shader cycle')==18
 assert result.stdout.count('all output/guard words PASS')==3
 assert 'PASS original LWJGL compute pipeline:18 dispatches' in result.stdout
else:
 assert result.stdout.count('via LWJGL vkQueueSubmit')==12
 assert result.stdout.count('bindings and GPU byte checks PASS')==3
 assert 'PASS unmodified LWJGL Vulkan bindings:12 GPU transfers,3 instance/device lifecycles, VK loader cleanup'in result.stdout
assert hashlib.sha256(vulkan.read_bytes()).hexdigest()==row['sha256']
summary='9graphics draws/full256x256 pixels+guards/3graphics lifecycles/readback image' if a.render else '18compute dispatches/1,63,64,65,1024,4096 words/full output+guards/3pipeline lifecycles' if a.shader else '12copy-fill-readbacks/full output+guards/3instance-device lifecycles/duplicate-init rejection'
print('PASS original LWJGL Vulkan3.4.3, standard command bindings:',summary,'; Java25 Xint/XcheckJNI/verify + real core UBSan + MoltenVK physical host GPU. PS5 pending.')
