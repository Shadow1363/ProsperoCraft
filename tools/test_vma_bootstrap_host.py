#!/usr/bin/env python3
"""Exercise real VMA GPU allocation/transfers through original LWJGL JNI;host only."""
from pathlib import Path
import argparse,copy,hashlib,json,os,platform,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args();w=ROOT/'build/vma-bootstrap-host-035';w.mkdir(exist_ok=True)
original=ROOT/'.tools/client/lwjgl-vma-3.4.3.jar';lock=json.loads((ROOT/'client/26.3.lock.json').read_text());pin=next(r for r in lock['artifacts']if r['file']==original.name);assert hashlib.sha256(original.read_bytes()).hexdigest()==pin['sha256']
library=ROOT/'build/lwjgl-vma-host/liblwjgl_vma.dylib';resource='META-INF/macos/'+('arm64'if platform.machine()=='arm64'else'x64')+'/org/lwjgl/vma/liblwjgl_vma.dylib.sha1';paired=w/'lwjgl-vma-host-paired.jar'
with zipfile.ZipFile(original)as src,zipfile.ZipFile(paired,'w',zipfile.ZIP_DEFLATED)as out:
 assert resource in src.namelist()
 for info in src.infolist():out.writestr(copy.copy(info),hashlib.sha1(library.read_bytes()).hexdigest().encode()if info.filename==resource else src.read(info.filename))
cp=':'.join([str(ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar'),str(ROOT/'.tools/client/lwjgl-vulkan-3.4.3.jar'),str(paired)])
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/vma_bootstrap/ClientVMA25.java'),str(ROOT/'tools/fixtures/PS5VMADispatchHost25.java')],check=True)
cmd=[str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Dps5.test.ffiCore='+str(ROOT/'build/libffi-host/liblwjglffi.dylib'),'-Dps5.test.vulkanLibrary=/opt/homebrew/lib/libMoltenVK.dylib','-Djava.library.path='+str(library.parent),'-cp',str(w)+':'+cp,'ClientVMA25']
r=subprocess.run(cmd,capture_output=True,text=True,timeout=120,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'));(w/'result.log').write_text(r.stdout+r.stderr);print(r.stdout,r.stderr);r.check_returncode();assert r.stdout.count('PASS actual VMA cycle')==3
for bad in ['WARNING in native method','FATAL ERROR in native method','runtime error:']:assert bad not in r.stdout+r.stderr,bad
print('PASS actual original VMA/JNI3cycles:12real MoltenVK GPU transfers,VMA allocate/map/flush/invalidate/free,exact output/source+guards,NEVER_ALLOCATE controls,allocator/device/loader cleanup;PS5 pending')

ported=list(cmd);ported[-1]='PS5VMADispatchHost25';r=subprocess.run(ported,capture_output=True,text=True,timeout=120,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'));(w/'ps5-dispatch.log').write_text(r.stdout+r.stderr);print(r.stdout,r.stderr);r.check_returncode();assert r.stdout.count('PASS actual VMA cycle')==3
for bad in ['WARNING in native method','FATAL ERROR in native method','runtime error:']:assert bad not in r.stdout+r.stderr,bad
print('PASS actual PS5 enum VMA JNI dispatch on real MoltenVK allocations/transfers;not a PS5 console pass')
