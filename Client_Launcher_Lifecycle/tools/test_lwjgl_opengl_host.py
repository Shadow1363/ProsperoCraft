#!/usr/bin/env python3
"""Real CGL GPU/JNI regression for original generated bindings;PS5 provider pending."""
from pathlib import Path
import argparse,subprocess,json,zipfile,hashlib,platform,os,copy
ROOT=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args();w=ROOT/'build/opengl-bindings-host-028';w.mkdir(exist_ok=True)
original=ROOT/'.tools/client/lwjgl-opengl-3.4.3.jar';lock=json.loads((ROOT/'client/26.3.lock.json').read_text());pin=next(r for r in lock['artifacts']if r['file']==original.name);assert hashlib.sha256(original.read_bytes()).hexdigest()==pin['sha256'];library=ROOT/'build/lwjgl-opengl-host/liblwjgl_opengl.dylib';paired=w/'lwjgl-opengl-host-paired.jar';resource='META-INF/macos/'+('arm64'if platform.machine()=='arm64'else'x64')+'/org/lwjgl/opengl/liblwjgl_opengl.dylib.sha1'
with zipfile.ZipFile(original)as src,zipfile.ZipFile(paired,'w',zipfile.ZIP_DEFLATED)as out:
 assert resource in src.namelist()
 for info in src.infolist():out.writestr(copy.copy(info),hashlib.sha1(library.read_bytes()).hexdigest().encode()if info.filename==resource else src.read(info.filename))
cp=':'.join([str(ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar'),str(paired)])
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'tools/fixtures/OpenGLBindingsHost25.java')],check=True)
r=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Djava.library.path='+str(library.parent),'-cp',str(w)+':'+cp,'OpenGLBindingsHost25',str(ROOT/'build/libffi-host/liblwjglffi.dylib'),str(ROOT/'build/sdl-host-012/libhost-loader.dylib')],capture_output=True,text=True,timeout=120,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'));(w/'result.log').write_text(r.stdout+r.stderr);print(r.stdout,r.stderr);r.check_returncode();assert r.stdout.count('PASS actual original OpenGL JNI/host GPU cycle')==3
for bad in ['WARNING in native method','FATAL ERROR in native method','runtime error:']:assert bad not in r.stdout+r.stderr,bad
print('PASS actual generated OpenGL JNI dispatch with real host GPU3contexts/192pixels/384guard bytes;no PS5 GL provider or context pass')
