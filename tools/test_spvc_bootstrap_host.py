#!/usr/bin/env python3
"""Exercise real SPIRV-Cross translation/reflection through original LWJGL downcalls;host only."""
from pathlib import Path
import argparse,copy,hashlib,json,os,platform,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args();w=ROOT/'build/spvc-bootstrap-host-036';w.mkdir(exist_ok=True)
from compile_client_shader import compile_shader
compile_shader()
original=ROOT/'.tools/client/lwjgl-spvc-3.4.3.jar';lock=json.loads((ROOT/'client/26.3.lock.json').read_text());pin=next(r for r in lock['artifacts']if r['file']==original.name);assert hashlib.sha256(original.read_bytes()).hexdigest()==pin['sha256']
library=ROOT/'build/spvc-host/libspirv-cross-c-shared.dylib';resource='META-INF/macos/'+('arm64'if platform.machine()=='arm64'else'x64')+'/org/lwjgl/spvc/libspirv-cross.dylib.sha1';paired=w/'lwjgl-spvc-host-paired.jar'
with zipfile.ZipFile(original)as src,zipfile.ZipFile(paired,'w',zipfile.ZIP_DEFLATED)as out:
 assert resource in src.namelist()
 for info in src.infolist():out.writestr(copy.copy(info),hashlib.sha1(library.read_bytes()).hexdigest().encode()if info.filename==resource else src.read(info.filename))
cp=':'.join([str(ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar'),str(paired)])
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/spvc_bootstrap/ClientSPVC25.java'),str(ROOT/'tools/fixtures/PS5SPVCDispatchHost25.java'),str(ROOT/'build/client-shader/ClientShaderCode25.java')],check=True)
cmd=[str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Dps5.test.ffiCore='+str(ROOT/'build/libffi-host/liblwjglffi.dylib'),'-Djava.library.path='+str(library.parent),'-Dps5.test.hostLoader='+str(ROOT/'build/sdl-host-012/libhost-loader.dylib'),'-Dps5.test.spvc='+str(library),'-Dps5.test.spvcOutput='+str(w),'-cp',str(w)+':'+cp,'ClientSPVC25']
r=subprocess.run(cmd,capture_output=True,text=True,timeout=120,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'));(w/'result.log').write_text(r.stdout+r.stderr);print(r.stdout,r.stderr);r.check_returncode();assert r.stdout.count('PASS actual SPIRV-Cross cycle')==3
for bad in ['WARNING in native method','FATAL ERROR in native method','runtime error:']:assert bad not in r.stdout+r.stderr,bad
print('PASS actual SPIRV-Cross3contexts:9GLSL/HLSL/MSL translations,reflection/version,malformed SPIR-V controls,384guards and allocation/context cleanup;PS5 pending')

ported=list(cmd);ported[-1]='PS5SPVCDispatchHost25';r=subprocess.run(ported,capture_output=True,text=True,timeout=120,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'));(w/'ps5-dispatch.log').write_text(r.stdout+r.stderr);print(r.stdout,r.stderr);r.check_returncode();assert r.stdout.count('PASS actual SPIRV-Cross cycle')==3
for bad in ['WARNING in native method','FATAL ERROR in native method','runtime error:']:assert bad not in r.stdout+r.stderr,bad
print('PASS actual PS5 enum SPIRV-Cross downcalls on real host translators;not a PS5 console pass')

# Compile translated GLSL/HLSL through an independent compiler and validate SPIR-V.
for source in sorted([*w.glob('cycle*.comp'),*w.glob('cycle*.hlsl')]):
 output=source.with_suffix(source.suffix+'.spv');subprocess.run(['/opt/homebrew/bin/glslangValidator','-V','--target-env','vulkan1.1','-S','comp',*(['-D','-e','main']if source.suffix=='.hlsl'else[]),'-o',str(output),str(source)],check=True);subprocess.run(['/opt/homebrew/bin/spirv-val','--target-env','vulkan1.1',str(output)],check=True)
print('PASS translated GLSL/HLSL independently recompiled and spirv-val validated;MSL compiler/execution and target GPU translation execution not tested')
