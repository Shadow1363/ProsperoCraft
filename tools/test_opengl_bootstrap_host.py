#!/usr/bin/env python3
"""Real pinned Mesa softpipe/LWJGL context and readback acceptance;host only."""
from pathlib import Path
import argparse,subprocess,json,zipfile,hashlib,platform,os,copy
ROOT=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args();w=ROOT/'build/opengl-bootstrap-host-028';w.mkdir(exist_ok=True)
provider=ROOT/'build/osmesa-host/libOSMesa.dylib';java_include=a.java_home/'include';helper=provider.parent/'context.o'
subprocess.run(['clang','-fPIC','-fsanitize=undefined','-I'+str(java_include),'-I'+str(java_include/'darwin'),'-I'+str(ROOT/'build/mesa-osmesa-source/include'),'-c',str(ROOT/'client/opengl_bootstrap/context.c'),'-o',str(helper)],check=True)
(w/'notes.cpp').write_text('#include <stdio.h>\nextern "C" void client_gpu_stage(const char*s,int code){(void)code;puts(s);fflush(stdout); }\n')
# SPIRV-Tools is an optional host Meson auto-detection;use its actual dependency.
subprocess.run(['clang++','-dynamiclib','-fsanitize=undefined','-Wl,-u,_OSMesaGetProcAddress',str(helper),str(w/'notes.cpp'),str(provider.parent/'src/gallium/targets/osmesa/libOSMesa.a'),'-L/opt/homebrew/lib','-lSPIRV-Tools',str(provider.parent/'subprojects/zlib-1.3.1/libz.a'),'-o',str(provider)],check=True)
original=ROOT/'.tools/client/lwjgl-opengl-3.4.3.jar';lock=json.loads((ROOT/'client/26.3.lock.json').read_text());pin=next(r for r in lock['artifacts']if r['file']==original.name);assert hashlib.sha256(original.read_bytes()).hexdigest()==pin['sha256'];library=ROOT/'build/lwjgl-opengl-host/liblwjgl_opengl.dylib';paired=w/'lwjgl-opengl-host-paired.jar';resource='META-INF/macos/'+('arm64'if platform.machine()=='arm64'else'x64')+'/org/lwjgl/opengl/liblwjgl_opengl.dylib.sha1'
with zipfile.ZipFile(original)as src,zipfile.ZipFile(paired,'w',zipfile.ZIP_DEFLATED)as out:
 assert resource in src.namelist()
 for info in src.infolist():out.writestr(copy.copy(info),hashlib.sha1(library.read_bytes()).hexdigest().encode()if info.filename==resource else src.read(info.filename))
cp=':'.join([str(ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar'),str(paired)])
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/opengl_bootstrap/ClientOpenGL25.java')],check=True)
r=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Dps5.test.ffiCore='+str(ROOT/'build/libffi-host/liblwjglffi.dylib'),'-Dps5.test.hostLoader='+str(ROOT/'build/sdl-host-012/libhost-loader.dylib'),'-Dps5.test.osmesa='+str(provider),'-Djava.library.path='+str(library.parent),'-cp',str(w)+':'+cp,'ClientOpenGL25',str(ROOT/'build/libffi-host/liblwjglffi.dylib'),str(ROOT/'build/sdl-host-012/libhost-loader.dylib'),str(provider)],capture_output=True,text=True,timeout=120,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'));(w/'result.log').write_text(r.stdout+r.stderr);print(r.stdout,r.stderr);r.check_returncode();assert r.stdout.count('PASS actual Mesa/LWJGL cycle')==3
for bad in ['WARNING in native method','FATAL ERROR in native method','runtime error:']:assert bad not in r.stdout+r.stderr,bad
print('PASS actual Mesa softpipe/OpenGL JNI:3contexts,192pixels,768guard bytes;PS5 integration/console pending')
