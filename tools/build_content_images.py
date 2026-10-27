#!/usr/bin/env python3
"""Build consumer-owned project thumbnails, pinned libwebp and STB."""
from pathlib import Path
import json,subprocess,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];LLVM=Path('/opt/homebrew/opt/llvm/bin')
def build(runtime,java_home,host=False,bindings=None,offline=False):
 port=ROOT/'client/ports/content_images';pin=json.loads((port/'sources.json').read_text());src=ROOT/'.tools/libwebp-src'
 if not src.exists() and offline:raise FileNotFoundError(src)
 if not src.exists():subprocess.run(['git','clone','--no-checkout',pin['webp']['repository'],str(src)],check=True);subprocess.run(['git','-C',str(src),'checkout','--detach',pin['webp']['commit']],check=True)
 assert subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip()==pin['webp']['commit'];subprocess.run(['git','-C',str(src),'diff','--exit-code','HEAD'],check=True)
 w=ROOT/('build/content-images-host' if host else 'build/content-images-ps5');w.mkdir(exist_ok=True)
 flags=['-DCMAKE_BUILD_TYPE=Release','-DBUILD_SHARED_LIBS=OFF','-DWEBP_ENABLE_SIMD=OFF','-DWEBP_USE_THREAD=OFF','-DWEBP_BUILD_ANIM_UTILS=OFF','-DWEBP_BUILD_CWEBP=OFF','-DWEBP_BUILD_DWEBP=OFF','-DWEBP_BUILD_GIF2WEBP=OFF','-DWEBP_BUILD_IMG2WEBP=OFF','-DWEBP_BUILD_VWEBP=OFF','-DWEBP_BUILD_WEBPINFO=OFF','-DWEBP_BUILD_LIBWEBPMUX=OFF','-DWEBP_BUILD_WEBPMUX=OFF','-DWEBP_BUILD_EXTRAS=OFF']
 sdk=runtime/'.tools/native-sdk/ps5-payload-sdk';target=[] if host else ['-target','x86_64-sie-ps5','-fvisibility-nodllstorageclass=default','-isysroot',str(sdk),'-march=x86-64','-mno-avx','-mno-avx2','-mno-fma','-fno-stack-protector','-femulated-tls']
 if not host:
  tool=w/'ps5.cmake';tool.write_text('set(CMAKE_SYSTEM_NAME FreeBSD)\nset(CMAKE_SYSTEM_PROCESSOR x86_64)\nset(CMAKE_C_COMPILER '+str(LLVM/'clang')+')\nset(CMAKE_C_COMPILER_TARGET x86_64-sie-ps5)\nset(CMAKE_AR '+str(LLVM/'llvm-ar')+')\nset(CMAKE_RANLIB '+str(LLVM/'llvm-ranlib')+')\nset(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)\n')
  flags+=['-DCMAKE_TOOLCHAIN_FILE='+str(tool),'-DCMAKE_C_FLAGS='+' '.join(target)+' -fPIC']
 else:flags+=['-DCMAKE_C_COMPILER=clang','-DCMAKE_C_FLAGS=-fPIC -fsanitize=undefined']
 subprocess.run(['cmake','-S',str(src),'-B',str(w/'webp'),'-G','Ninja',*flags],check=True);subprocess.run(['cmake','--build',str(w/'webp'),'--target','webpdecoder','-j','6'],check=True)
 stb=ROOT/'.tools/lwjgl-stb-src/stb_image.h';lock=json.loads((ROOT/'client/ports/stb/native-sources.json').read_text());row=next(p for p in lock['files']if p['file']=='stb_image.h');assert hashlib.sha256(stb.read_bytes()).hexdigest()==row['sha256']
 headers=java_home/'include' if host else runtime/'.tools/java25/openjdk/build/ps5-bootstrap/support/modules_include/java.base'
 obj=w/'decode.o';subprocess.run(['clang' if host else str(LLVM/'clang'),'-std=c11','-O2','-fPIC',*target,*(['-fsanitize=undefined'] if host else []),'-I'+str(src/'src'),'-I'+str(stb.parent),'-I'+str(headers),'-I'+str(headers/('darwin' if host else 'freebsd')),'-c',str(port/'decode.c'),'-o',str(obj)],check=True)
 if host:
  library=w/'libps5contentimages.dylib';subprocess.run(['clang','-dynamiclib','-fsanitize=undefined',str(obj),str(w/'webp/libwebpdecoder.a'),'-o',str(library)],check=True);return library
 raw=w/'raw.o';output=w/'content-images.o';subprocess.run(['/opt/homebrew/opt/lld/bin/ld.lld','-r',str(obj),'--whole-archive',str(w/'webp/libwebpdecoder.a'),'--no-whole-archive','-o',str(raw)],check=True)
 mapping=w/'bindings.txt';mapping.write_text(''.join(k+' '+v+'\n'for k,v in sorted((bindings or {}).items())))
 subprocess.run([str(LLVM/'llvm-objcopy'),'--redefine-syms='+str(mapping),str(raw),str(output)],check=True)
 sections=subprocess.check_output([str(LLVM/'llvm-readelf'),'-SW',str(output)],text=True);assert '.init_array'not in sections and '.tdata'not in sections and '.tbss'not in sections
 (w/'audit.json').write_text(json.dumps({'sources':pin,'source_sha256':hashlib.sha256((port/'decode.c').read_bytes()).hexdigest(),'object_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'scope':pin['scope'],'console':'pending'},indent=2)+'\n');return output
