#!/usr/bin/env python3
"""Build pinned original SPIRV-Cross C API/backends for resident PS5 or host UBSan."""
from pathlib import Path
import argparse,json,hashlib,subprocess,tarfile,urllib.request,shutil,os
ROOT=Path(__file__).resolve().parents[1];LLVM=Path('/opt/homebrew/opt/llvm/bin')
def build(runtime,host=False,offline=False):
 pin=json.loads((ROOT/'client/ports/spvc/sources.json').read_text());archive=ROOT/'.tools'/pin['file']
 if not archive.exists():
  if offline:raise FileNotFoundError(archive)
  archive.write_bytes(urllib.request.urlopen(pin['url'],timeout=60).read())
 assert archive.stat().st_size==pin['size']and hashlib.sha256(archive.read_bytes()).hexdigest()==pin['sha256']
 source=ROOT/'build/spvc-source'
 if not source.exists():
  temporary=ROOT/'build/spvc-extract';temporary.mkdir(exist_ok=True)
  with tarfile.open(archive)as t:t.extractall(temporary,filter='data')
  shutil.move(str(temporary/('SPIRV-Cross-'+pin['commit'])),source)
 with tarfile.open(archive)as t:
  for member in t.getmembers():
   if member.isfile():
    p=Path(member.name).relative_to('SPIRV-Cross-'+pin['commit']);assert (source/p).read_bytes()==t.extractfile(member).read(),p
 out=ROOT/('build/spvc-host'if host else'build/spvc-ps5');out.mkdir(exist_ok=True)
 adapted=out/'source';marker=adapted/'.ps5-patch-sha256';patch=ROOT/'client/ports/spvc/0001-ps5-native-localeconv.patch';patch_sha=hashlib.sha256(patch.read_bytes()).hexdigest()
 if not marker.exists()or marker.read_text()!=patch_sha:
  shutil.rmtree(adapted,ignore_errors=True);shutil.copytree(source,adapted);subprocess.run(['git','apply','--unsafe-paths','--directory='+str(adapted),str(patch)],check=True);marker.write_text(patch_sha)
 configured=out/'cmake'
 args=['-DCMAKE_BUILD_TYPE=Release','-DCMAKE_POSITION_INDEPENDENT_CODE=ON','-DSPIRV_CROSS_CLI=OFF','-DSPIRV_CROSS_ENABLE_TESTS=OFF','-DSPIRV_CROSS_SKIP_INSTALL=ON','-DSPIRV_CROSS_EXCEPTIONS_TO_ASSERTIONS=OFF','-DSPIRV_CROSS_NAMESPACE_OVERRIDE=clientspvc','-DCMAKE_DISABLE_FIND_PACKAGE_Git=TRUE','-DSPIRV_CROSS_SHARED='+('ON'if host else'OFF'),'-DSPIRV_CROSS_STATIC='+('OFF'if host else'ON')]
 if host:args+=['-DSPIRV_CROSS_SANITIZE_UNDEFINED=ON','-DCMAKE_SHARED_LINKER_FLAGS=-fsanitize=undefined','-DCMAKE_CXX_FLAGS=-DSPIRV_CROSS_PS5_LOCALECONV']
 else:
  sdk=ROOT/'.tools/graphics-sdk';flags='-fvisibility-nodllstorageclass=default -march=x86-64 -msse2 -mno-avx -mno-avx2 -mno-fma -fno-stack-protector -femulated-tls'
  args+=['-DCMAKE_SYSTEM_NAME=FreeBSD','-DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY','-DCMAKE_C_COMPILER='+str(LLVM/'clang'),'-DCMAKE_CXX_COMPILER='+str(LLVM/'clang++'),'-DCMAKE_C_COMPILER_TARGET=x86_64-sie-ps5','-DCMAKE_CXX_COMPILER_TARGET=x86_64-sie-ps5','-DCMAKE_SYSROOT='+str(sdk),'-DCMAKE_AR='+str(LLVM/'llvm-ar'),'-DCMAKE_RANLIB='+str(LLVM/'llvm-ranlib'),'-DCMAKE_C_FLAGS='+flags,'-DCMAKE_CXX_FLAGS='+flags+' -isystem '+str(sdk/'target/include/c++/v1')+' -isystem '+str(sdk/'target/include')+' -fexceptions -frtti -DSPIRV_CROSS_PS5_LOCALECONV']
 env=dict(os.environ,SOURCE_DATE_EPOCH='0');subprocess.run(['cmake','-S',str(adapted),'-B',str(configured),'-G','Ninja',*args],check=True,env=env);subprocess.run(['cmake','--build',str(configured),'-j','4'],check=True,env=env)
 if host:
  library=out/'libspirv-cross-c-shared.dylib';shutil.copyfile(configured/library.name,library);return library
 archives=sorted(configured.glob('libspirv-cross-*.a'));assert len(archives)>=6
 raw=out/'spvc-raw.o';subprocess.run(['/opt/homebrew/opt/lld/bin/ld.lld','-r','--whole-archive',*map(str,archives),'--no-whole-archive','-o',str(raw)],check=True)
 obj=out/'spvc.o';subprocess.run([str(LLVM/'llvm-objcopy'),'--redefine-syms='+str(ROOT/'build/client-gpu/sdl-bindings.txt'),str(raw),str(obj)],check=True)
 sections=subprocess.check_output([str(LLVM/'llvm-readelf'),'-SW',str(obj)],text=True);assert '.tdata'not in sections and '.tbss'not in sections
 names=subprocess.check_output([str(LLVM/'llvm-nm'),'--extern-only','--defined-only',str(obj)],text=True);exports=[l.split()[-1]for l in names.splitlines()if len(l.split())==3 and l.split()[-1].startswith('spvc_')];assert len(exports)>150
 audit={'source':pin,'locale_patch_sha256':patch_sha,'locale':'PS5 uses actual localeconv() decimal separator through supported native libc;host tests select same code branch;no constant/stub;concurrent locale changes not validated','object_sha256':hashlib.sha256(obj.read_bytes()).hexdigest(),'c_api_exports':len(exports),'backends':'GLSL,HLSL,MSL,CPP,JSON reflection and core enabled;C API0.68.0','namespace':'Supported SPIRV_CROSS_NAMESPACE_OVERRIDE=clientspvc;C API unchanged','exceptions':'Real C++ exceptions/RTTI enabled;invalid input returns actual C API errors,not assertion substitutes','build_metadata':'SOURCE_DATE_EPOCH=0;CMake Git discovery disabled to avoid consumer-parent repository identity','allocator':'Existing scoped graphics C++/thread/heap providers;JVM globals unchanged','scope':'Real original SPIRV-Cross C API/backends;PS5 shader translation/reflection/error controls pending'};(out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');print('PASS real target SPIRV-Cross',len(exports),'exports',audit['object_sha256']);return obj
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);p.add_argument('--host',action='store_true');p.add_argument('--offline',action='store_true');a=p.parse_args();print(build(a.runtime_workspace,a.host,a.offline))
