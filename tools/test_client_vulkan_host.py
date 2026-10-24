#!/usr/bin/env python3
"""Run unmodified LWJGL Vulkan command bindings against a real MoltenVK host GPU."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',required=True,type=Path);p.add_argument('--runtime-workspace',required=True,type=Path);p.add_argument('--shader',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--present',action='store_true');p.add_argument('--runtime-shader',action='store_true');p.add_argument('--texture',action='store_true');p.add_argument('--scene',action='store_true');a=p.parse_args()
if sum([a.shader,a.render,a.present,a.runtime_shader,a.texture,a.scene])>1:p.error('Choose one candidate')
fixture='ClientScene25' if a.scene else 'ClientTexture25' if a.texture else 'ClientRuntimeShader25' if a.runtime_shader else 'ClientPresentHost25' if a.present else 'ClientRender25' if a.render else 'ClientShader25' if a.shader else 'ClientVulkan25'
subprocess.run(['python3',str(ROOT/'tools/test_lwjgl_core.py'),'--java-home',str(a.java_home),'--runtime-workspace',str(a.runtime_workspace)],check=True)
w=ROOT/('build/scene-host-022' if a.scene else 'build/texture-host-021' if a.texture else 'build/runtime-shader-host-015' if a.runtime_shader else 'build/present-host-011' if a.present else 'build/render-host-010' if a.render else 'build/shader-host-009' if a.shader else 'build/vulkan-host-008');w.mkdir(exist_ok=True)
callback='''#include <jni.h>
#include <stdio.h>
static void note(JNIEnv*e,jclass c,jstring s){(void)c;const char*p=(*e)->GetStringUTFChars(e,s,NULL);if(p){puts(p);fflush(stdout);(*e)->ReleaseStringUTFChars(e,s,p);}}
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM*v,void*r){(void)r;JNIEnv*e=NULL;if((*v)->GetEnv(v,(void**)&e,JNI_VERSION_1_8)!=JNI_OK)return JNI_ERR;jclass c=(*e)->FindClass(e,"ClientVulkan25");if(!c)return JNI_ERR;JNINativeMethod n={"checkpoint","(Ljava/lang/String;)V",(void*)&note};return (*e)->RegisterNatives(e,c,&n,1)==JNI_OK?JNI_VERSION_1_8:JNI_ERR;}
'''
if a.render or a.present:
 callback=callback.replace('#include <stdio.h>','#include <stdio.h>\n#include <stdlib.h>')
 callback=callback.replace('JNIEXPORT jint JNICALL JNI_OnLoad','''static void publish(JNIEnv*e,jclass c,jobject b,jint width,jint height){(void)c;void*p=(*e)->GetDirectBufferAddress(e,b);jlong n=(*e)->GetDirectBufferCapacity(e,b);const char*path=getenv("PS5_RENDER_READBACK_PATH");if(!p||n<256*256*4||width!=256||height!=256||!path){(*e)->ThrowNew(e,(*e)->FindClass(e,"java/lang/IllegalArgumentException"),"Invalid host image");return;}FILE*f=fopen(path,"wb");if(!f){(*e)->ThrowNew(e,(*e)->FindClass(e,"java/io/IOException"),"Host image open failed");return;}int bad=fwrite(p,1,256*256*4,f)!=256*256*4;if(fclose(f))bad=1;if(bad)(*e)->ThrowNew(e,(*e)->FindClass(e,"java/io/IOException"),"Host image write failed");}
JNIEXPORT jint JNICALL JNI_OnLoad''')
 callback=callback.replace('JNINativeMethod n={"checkpoint","(Ljava/lang/String;)V",(void*)&note};return (*e)->RegisterNatives(e,c,&n,1)', 'JNINativeMethod n[]={{"checkpoint","(Ljava/lang/String;)V",(void*)&note},{"publishPixels","(Ljava/nio/ByteBuffer;II)V",(void*)&publish}};return (*e)->RegisterNatives(e,c,n,2)')
(w/'callback.c').write_text(callback.replace('ClientVulkan25',fixture))
(w/'RunVulkan.java').write_text('public class RunVulkan{public static void main(String[]args){System.load(args[0]);'+('System.load(args[1]);'if a.runtime_shader else '')+fixture+'.main(new String[0]);}}\n')
subprocess.run(['clang','-dynamiclib','-I'+str(a.java_home/'include'),'-I'+str(a.java_home/'include/darwin'),str(w/'callback.c'),'-o',str(w/'libcallback.dylib')],check=True)
lock=json.loads((ROOT/'client/26.3.lock.json').read_text());row=next(r for r in lock['artifacts']if r['file']=='lwjgl-vulkan-3.4.3.jar');vulkan=ROOT/'.tools/client'/row['file']
assert hashlib.sha256(vulkan.read_bytes()).hexdigest()==row['sha256']
core=ROOT/'build/lwjgl-core-test/lwjgl-host-paired.jar';cp=str(core)+':'+str(vulkan)
extra=[];properties=[]
if a.runtime_shader:
 import zipfile,shutil,platform
 from build_shaderc_native import build as build_shaderc
 lib=build_shaderc(a.runtime_workspace,host=True);hostlib=w/'libshaderc.dylib';shutil.copyfile(lib,hostlib)
 sdlhost=ROOT/'build/sdl-host-012/libhost-loader.dylib';assert sdlhost.exists()
 original=ROOT/'.tools/client/lwjgl-shaderc-3.4.3.jar';paired=w/'lwjgl-shaderc-host-paired.jar'
 resource='META-INF/macos/'+('arm64'if platform.machine()=='arm64'else'x64')+'/org/lwjgl/shaderc/libshaderc.dylib.sha1'
 with zipfile.ZipFile(original)as src,zipfile.ZipFile(paired,'w',zipfile.ZIP_DEFLATED)as out:
  assert resource in src.namelist()
  for info in src.infolist():out.writestr(info,hashlib.sha1(hostlib.read_bytes()).hexdigest().encode()if info.filename==resource else src.read(info.filename))
 cp+=':'+str(paired);extra=[str(sdlhost)];properties=['-Dps5.test.shadercLibrary='+str(hostlib)]
sources=[ROOT/'client/vulkan/ClientVulkan25.java']
if a.scene:
 from compile_client_scene import compile_scene
 # Host-only hook calls a genuine GPU blit verifier after target scene pixels
 # have passed; all original rendering/reference code stays the same.
 scene=ROOT/'client/scene/ClientScene25.java';host_scene=w/'ClientScene25.java'
 content=scene.read_text();hook='latestPixels[i]=pixels.get(i);}'
 assert hook in content
 content=content.replace(hook,'latestPixels[i]=pixels.get(i);SceneBlitHost25.verify(device,mp,cmd,queue,fence,image,buffer,memory,pixels);}')
 host_scene.write_text(content)
 sources=[host_scene,ROOT/'client/scene/SceneBlitHost25.java',compile_scene()]
elif a.texture:
 from compile_client_texture import compile_texture
 sources=[ROOT/'client/texture/ClientTexture25.java',compile_texture()]
elif a.runtime_shader:
 sources=[ROOT/'client/runtime_shader/ClientRuntimeShader25.java']
elif a.present:
 from compile_client_present import compile_present
 sources=[ROOT/'client/present/ClientPresentHost25.java',ROOT/'client/present/ClientPresent25.java',compile_present()]
elif a.render:
 from compile_client_render import compile_render
 sources=[ROOT/'client/render/ClientRender25.java',compile_render()]
elif a.shader:
 from compile_client_shader import compile_shader
 sources=[ROOT/'client/shader/ClientShader25.java',compile_shader()]
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(path)for path in sources],str(w/'RunVulkan.java')],check=True)
env=dict(os.environ,PS5_RENDER_READBACK_PATH=str(w/'readback.rgba'),UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1')
result=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED',*properties,'-Dps5.test.vulkanLibrary=/opt/homebrew/lib/libMoltenVK.dylib','-Djava.library.path='+str(ROOT/'build/client-ports/lwjgl-native/host'),'-cp',str(w)+':'+cp,'RunVulkan',str(w/'libcallback.dylib'),*extra],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
(w/'result.log').write_text(result.stdout);result.check_returncode()
for marker in ['runtime error:','WARNING in native method','FATAL ERROR in native method','Exception in thread','Failed to locate address']:assert marker not in result.stdout,marker
if a.scene:
 assert result.stdout.count('draw graphics cycle')==9
 assert result.stdout.count('all pixels/guards PASS')==3
 assert 'PASS scene/perspective/vertices:27 draws' in result.stdout
 assert 'PASS real scene RGBA->BGRA nearest scaling blit' in result.stdout
elif a.texture:
 assert result.stdout.count('draw graphics cycle')==9
 assert result.stdout.count('all pixels/guards PASS')==3
 assert 'PASS texture/depth/blend:27 draws' in result.stdout
elif a.render or a.present:
 assert result.stdout.count('draw graphics cycle')==9
 assert result.stdout.count('all pixels/guards PASS')==3
 assert 'PASS original LWJGL graphics pipeline:9 draws' in result.stdout
 data=(w/'readback.rgba').read_bytes();assert len(data)==256*256*4
 if a.present:
  converted=bytearray(data)
  for i in range(0,len(data),4):converted[i:i+4]=bytes([data[i+2],data[i+1],data[i],data[i+3]])
  data=bytes(converted)
 import struct,zlib
 def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
 png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',256,256,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(b'\0'+data[y*1024:(y+1)*1024]for y in range(256))))+chunk(b'IEND',b'')
 (w/'readback.png').write_bytes(png)
elif a.shader or a.runtime_shader:
 assert result.stdout.count('dispatch shader cycle')==18
 assert result.stdout.count('all output/guard words PASS')==3
 assert ('PASS actual runtime GLSL compiler:3 compilers'if a.runtime_shader else'PASS original LWJGL compute pipeline:18 dispatches') in result.stdout
 if a.runtime_shader:assert result.stdout.count('invalid GLSL diagnostic control PASS')==3
else:
 assert result.stdout.count('via LWJGL vkQueueSubmit')==12
 assert result.stdout.count('bindings and GPU byte checks PASS')==3
 assert 'PASS unmodified LWJGL Vulkan bindings:12 GPU transfers,3 instance/device lifecycles, VK loader cleanup'in result.stdout
assert hashlib.sha256(vulkan.read_bytes()).hexdigest()==row['sha256']
summary='Scene022 real vertex buffer/perspective UV/full readback/depth-blend controls;27draws/9images+guards/3lifecycles. SDL presentation not exercised on host' if a.scene else 'Texture021 actual uploads/combined sampler/D32 depth reject and disabled control/alpha blend and disabled control;27draws/9full256x256images+guards/3lifecycles' if a.texture else 'RuntimeShader015 actual shaderc valid/invalid compiler controls/3compilers/18GPU dispatches/full output+guards' if a.runtime_shader else 'Present011 HOST OFFSCREEN ONLY: presentation shader/BGRA output/push constants,9 draws/full pixels+guards/3lifecycles. PS5 display/surface/swapchain/acquire/present NOT EXERCISED' if a.present else '9graphics draws/full256x256 pixels+guards/3graphics lifecycles/readback image' if a.render else '18compute dispatches/1,63,64,65,1024,4096 words/full output+guards/3pipeline lifecycles' if a.shader else '12copy-fill-readbacks/full output+guards/3instance-device lifecycles/duplicate-init rejection'
print('PASS original LWJGL Vulkan3.4.3, standard command bindings:',summary,'; Java25 Xint/XcheckJNI/verify + real core UBSan + MoltenVK physical host GPU. PS5 pending.')
