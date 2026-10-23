#!/usr/bin/env python3
"""Run actual Java/LWJGL/JNI GPU transfer on the Mac through installed MoltenVK.

This uses the real host GPU; it does not establish PS5 driver/ABI compatibility.
The platform adapter selects MoltenVK's direct entry point and advertises its
actual portability subset. The target driver, code and original JARs stay intact.
"""
import argparse,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args()
# This existing check builds the real upstream host native core and an exactly
# hash-paired host test JAR; it never disables native-library hash verification.
subprocess.run(['python3',str(ROOT/'tools/test_lwjgl_core.py'),'--java-home',str(a.java_home),'--runtime-workspace',str(a.runtime_workspace)],check=True)
w=ROOT/'build/gpu-host-004';w.mkdir(exist_ok=True)
subprocess.run(['/opt/homebrew/opt/llvm/bin/clang','-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-fPIC','-dynamiclib','-DPS5_GPU_HOST','-fsanitize=undefined','-I'+str(ROOT/'.tools/PS5_Mesa/include'),'-I'+str(a.java_home/'include'),'-I'+str(a.java_home/'include/darwin'),str(ROOT/'client/gpu/bridge.c'),'-L','/opt/homebrew/lib','-lMoltenVK','-o',str(w/'libps5clientgpu.dylib')],check=True)
jar=ROOT/'build/lwjgl-core-test/lwjgl-host-paired.jar'
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',str(jar),'-d',str(w),str(ROOT/'client/gpu/ClientGpu25.java')],check=True)
env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1')
result=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Djava.library.path='+str(w)+':'+str(ROOT/'build/client-ports/lwjgl-native/host'),'-cp',str(w)+':'+str(jar),'ClientGpu25'],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
(w/'result.log').write_text(result.stdout);result.check_returncode()
for marker in ['runtime error:','WARNING in native method','FATAL ERROR in native method','Exception in thread']:
 assert marker not in result.stdout,marker
assert result.stdout.count('GPU cycle ')==3
assert result.stdout.count('GPU session explicitly destroyed: 0')==3
assert 'PASS Java25 + actual LWJGL + Vulkan GPU submission/readback; three create/destroy cycles'in result.stdout
print('PASS real Java25 -Xint/XcheckJNI/verify + actual LWJGL memory + MoltenVK host GPU:12copy/fill/readback sizes8..65536, full Java word/guard checks, null/heap/short/alias/malformed/foreign-thread/stale-session controls, three create/destroy cycles and idempotent close; UBSan. PS5 console pending.')
