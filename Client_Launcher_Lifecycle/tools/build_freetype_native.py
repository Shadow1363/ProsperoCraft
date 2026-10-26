#!/usr/bin/env python3
"""Build pinned real FreeType;PS5 resident exports or host UBSan library."""
from pathlib import Path
import argparse,hashlib,json,subprocess,tarfile,urllib.request,shutil
ROOT=Path(__file__).resolve().parents[1];LLVM=Path('/opt/homebrew/opt/llvm/bin')
def build(runtime,host=False,offline=False):
 pin=json.loads((ROOT/'client/ports/freetype/sources.json').read_text())
 for row in pin['files']:
  path=ROOT/'.tools'/row['file']
  if not path.exists():
   if offline:raise FileNotFoundError(path)
   path.write_bytes(urllib.request.urlopen(row['url'],timeout=60).read())
  assert path.stat().st_size==row['size'] and hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],path
 source=ROOT/'build/freetype-source'
 if not source.exists():
  temporary=ROOT/'build/freetype-extract';temporary.mkdir(exist_ok=True)
  with tarfile.open(ROOT/'.tools/freetype-source.tar.gz')as archive:archive.extractall(temporary,filter='data')
  shutil.move(str(temporary/('freetype-'+pin['commit'])),source);temporary.rmdir()
 # Refuse a modified extracted source tree;the tarball remains the authority.
 with tarfile.open(ROOT/'.tools/freetype-source.tar.gz')as archive:
  for member in archive.getmembers():
   if member.isfile():
    relative=Path(member.name).relative_to('freetype-'+pin['commit']);assert (source/relative).read_bytes()==archive.extractfile(member).read(),relative
 out=ROOT/('build/freetype-host'if host else'build/freetype-ps5');out.mkdir(exist_ok=True)
 flags=['-DCMAKE_BUILD_TYPE=Release','-DFT_DISABLE_ZLIB=ON','-DFT_DISABLE_BZIP2=ON','-DFT_DISABLE_PNG=ON','-DFT_DISABLE_HARFBUZZ=ON','-DFT_DISABLE_BROTLI=ON','-DCMAKE_POSITION_INDEPENDENT_CODE=ON']
 if host:flags+=['-DBUILD_SHARED_LIBS=ON','-DCMAKE_C_FLAGS=-fsanitize=undefined','-DCMAKE_SHARED_LINKER_FLAGS=-fsanitize=undefined']
 else:
  sdk=runtime/'.tools/native-sdk/ps5-payload-sdk'
  flags+=['-DBUILD_SHARED_LIBS=OFF','-DCMAKE_SYSTEM_NAME=FreeBSD','-DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY','-DCMAKE_C_COMPILER='+str(LLVM/'clang'),'-DCMAKE_C_COMPILER_TARGET=x86_64-sie-ps5','-DCMAKE_SYSROOT='+str(sdk),'-DCMAKE_AR='+str(LLVM/'llvm-ar'),'-DCMAKE_RANLIB='+str(LLVM/'llvm-ranlib'),'-DCMAKE_C_FLAGS=-fvisibility-nodllstorageclass=default -march=x86-64 -msse2 -mno-avx -mno-avx2 -mno-fma -fno-stack-protector -femulated-tls']
 subprocess.run(['cmake','-S',str(source),'-B',str(out),'-G','Ninja',*flags],check=True);subprocess.run(['cmake','--build',str(out),'-j','4'],check=True)
 if host:return out/'libfreetype.dylib'
 raw=out/'freetype-raw.o';subprocess.run(['/opt/homebrew/opt/lld/bin/ld.lld','-r','--whole-archive',str(out/'libfreetype.a'),'--no-whole-archive','-o',str(raw)],check=True)
 result=out/'freetype.o';subprocess.run([str(LLVM/'llvm-objcopy'),'--redefine-syms='+str(ROOT/'build/client-gpu/sdl-bindings.txt'),str(raw),str(result)],check=True)
 defined=subprocess.check_output([str(LLVM/'llvm-nm'),'--extern-only','--defined-only',str(result)],text=True);symbols=[line.split()[-1]for line in defined.splitlines()if len(line.split())==3];exports=[n for n in symbols if n.startswith('FT_')];assert 'FT_Init_FreeType'in exports and 'FT_Render_Glyph'in exports
 sections=subprocess.check_output([str(LLVM/'llvm-readelf'),'-SW',str(result)],text=True);assert '.tdata'not in sections and '.tbss'not in sections
 audit={'source':pin,'object_sha256':hashlib.sha256(result.read_bytes()).hexdigest(),'exports':len(exports),'optional_dependencies':'zlib,bzip2,png,harfbuzz,brotli disabled;built-in font drivers/rasterizers enabled','allocator':'Existing scoped graphics heap/file providers;JVM global wrappers unchanged','console':'PS5 acceptance pending','scope':'Real original FreeType implementation;original LWJGL Java downcalls via existing JNI/libffi;not a game/font-feature completeness claim'}
 (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');print('PASS real target FreeType',len(exports),'exports',audit['object_sha256']);return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);p.add_argument('--host',action='store_true');p.add_argument('--offline',action='store_true');a=p.parse_args();print(build(a.runtime_workspace,a.host,a.offline))
