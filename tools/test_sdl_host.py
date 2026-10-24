#!/usr/bin/env python3
"""Test original SDL Java APIs against real macOS SDL, with explicit virtual inputs."""
from pathlib import Path
import argparse,subprocess,json,hashlib,zipfile,os,platform
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--java-home',required=True,type=Path);p.add_argument('--runtime-workspace',required=True,type=Path);a=p.parse_args()
subprocess.run(['python3',str(ROOT/'tools/test_lwjgl_core.py'),'--java-home',str(a.java_home),'--runtime-workspace',str(a.runtime_workspace)],check=True)
w=ROOT/'build/sdl-host-012';w.mkdir(exist_ok=True)
record=json.loads((ROOT/'client/ports/sdl/host-loader-source.json').read_text());source=ROOT/'.tools/lwjgl-native-src'/record['file'];assert hashlib.sha256(source.read_bytes()).hexdigest()==record['sha256']
(w/'virtual.c').write_text('''#include <jni.h>
#include <SDL3/SDL.h>
JNIEXPORT jint JNICALL Java_SDLHost25_attachVirtual(JNIEnv*e,jclass c){(void)e;(void)c;SDL_VirtualJoystickDesc d;SDL_INIT_INTERFACE(&d);d.type=SDL_JOYSTICK_TYPE_GAMEPAD;d.naxes=6;d.nbuttons=SDL_GAMEPAD_BUTTON_COUNT;d.axis_mask=0x3f;d.button_mask=(1u<<SDL_GAMEPAD_BUTTON_COUNT)-1;d.name="Host-only virtual canary";return (jint)SDL_AttachVirtualJoystick(&d);}
''')
subprocess.run(['clang','-dynamiclib','-fsanitize=undefined','-DLWJGL_MACOS','-I'+str(ROOT/'.tools/lwjgl-native-src'),'-I'+str(a.java_home/'include'),'-I'+str(a.java_home/'include/darwin'),'-I/opt/homebrew/include',str(source),str(w/'virtual.c'),'-L/opt/homebrew/lib','-lSDL3','-o',str(w/'libhost-loader.dylib')],check=True)
lock=json.loads((ROOT/'client/26.3.lock.json').read_text());row=next(r for r in lock['artifacts']if r['file']=='lwjgl-sdl-3.4.3.jar');original=ROOT/'.tools/client'/row['file'];assert hashlib.sha256(original.read_bytes()).hexdigest()==row['sha256']
lib=Path('/opt/homebrew/lib/libSDL3.dylib').resolve();resource='META-INF/macos/'+('arm64'if platform.machine()=='arm64'else'x64')+'/org/lwjgl/sdl/libSDL3.dylib.sha1';paired=w/'lwjgl-sdl-host-paired.jar'
with zipfile.ZipFile(original)as src,zipfile.ZipFile(paired,'w',zipfile.ZIP_DEFLATED)as out:
 assert resource in src.namelist()
 for info in src.infolist():out.writestr(info,hashlib.sha1(lib.read_bytes()).hexdigest().encode()if info.filename==resource else src.read(info.filename))
cp=str(ROOT/'build/lwjgl-core-test/lwjgl-host-paired.jar')+':'+str(paired)
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/sdl/SDLHost25.java')],check=True)
result=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Djava.library.path='+str(ROOT/'build/client-ports/lwjgl-native/host'),'-cp',str(w)+':'+cp,'SDLHost25',str(w/'libhost-loader.dylib'),str(lib)],env=dict(os.environ,UBSAN_OPTIONS='halt_on_error=1:handle_segv=0:handle_sigbus=0:handle_sigfpe=0'),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
(w/'result.log').write_text(result.stdout);result.check_returncode();assert 'PASS original SDL Java bindings'in result.stdout
for error in ['runtime error:','WARNING in native method','FATAL ERROR in native method','Exception in thread','Incompatible Java and native library']:assert error not in result.stdout,error
print(result.stdout.strip())
