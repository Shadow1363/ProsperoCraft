#!/usr/bin/env python3
"""Build a user-edited OpenAL source tree into the compatible scoped PS5 object."""
from pathlib import Path
import argparse,subprocess,tarfile,re,shutil
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True,help='Edited extracted OpenAL source tree');p.add_argument('--build-dir',type=Path,required=True);p.add_argument('--llvm-bin',type=Path,required=True);p.add_argument('--lld',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parent;out=a.build_dir.resolve();out.mkdir(parents=True,exist_ok=True);sdk=out/'sdk'
if not (sdk/'target/include').exists():
 sdk.mkdir(exist_ok=True)
 with tarfile.open(root/'ps5-sdk-headers.tar')as tar:tar.extractall(sdk,filter='data')
source=a.source.resolve();toolchain=out/'toolchain.cmake';llvm=a.llvm_bin.resolve()
toolchain.write_text('set(CMAKE_SYSTEM_NAME FreeBSD)\nset(CMAKE_SYSTEM_VERSION 9)\nset(CMAKE_SYSTEM_PROCESSOR x86_64)\nset(CMAKE_CROSSCOMPILING TRUE)\nset(CMAKE_C_COMPILER '+str(llvm/'clang')+')\nset(CMAKE_CXX_COMPILER '+str(llvm/'clang++')+')\nset(CMAKE_C_COMPILER_TARGET x86_64-sie-ps5)\nset(CMAKE_CXX_COMPILER_TARGET x86_64-sie-ps5)\nset(CMAKE_AR '+str(llvm/'llvm-ar')+')\nset(CMAKE_RANLIB '+str(llvm/'llvm-ranlib')+')\nset(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)\n')
flags=f'-isysroot {sdk} -isystem {sdk}/target/include -fvisibility-nodllstorageclass=default -march=x86-64 -msse2 -mno-avx -mno-avx2 -mno-fma -fno-stack-protector -femulated-tls -fPIC'
args=['cmake','-S',str(source),'-B',str(out),'-G','Ninja','-DCMAKE_BUILD_TYPE=Release','-DCMAKE_TOOLCHAIN_FILE='+str(toolchain),'-DCMAKE_C_FLAGS='+flags,'-DCMAKE_CXX_FLAGS=-isystem '+str(sdk/'target/include/c++/v1')+' '+flags+' -fexceptions -frtti','-DLIBTYPE=STATIC','-DALSOFT_ENABLE_MODULES=OFF','-DALSOFT_UTILS=OFF','-DALSOFT_EXAMPLES=OFF','-DALSOFT_TESTS=OFF','-DALSOFT_EAX=OFF','-DALSOFT_EMBED_HRTF_DATA=OFF','-DALSOFT_BACKEND_WAVE=OFF','-DALSOFT_INSTALL=OFF','-DALSOFT_CPUEXT_SSE3=OFF','-DALSOFT_CPUEXT_SSE4_1=OFF','-DCMAKE_DISABLE_FIND_PACKAGE_PkgConfig=TRUE','-DCMAKE_DISABLE_FIND_PACKAGE_DBus1=TRUE']
for backend in ['PIPEWIRE','PULSEAUDIO','ALSA','OSS','SOLARIS','SNDIO','WASAPI','DSOUND','WINMM','PORTAUDIO','JACK','COREAUDIO','OBOE','OPENSL','SDL2','SDL3']:args+=['-DALSOFT_BACKEND_'+backend+'=OFF']
subprocess.run(args,check=True);subprocess.run(['cmake','--build',str(out),'--target','OpenAL','-j','4'],check=True)
raw=out/'openal-raw.o';obj=out/'openal.o';subprocess.run([str(a.lld),'-r','--whole-archive',str(out/'libopenal.a'),'--no-whole-archive','-o',str(raw)],check=True)
subprocess.run([str(llvm/'llvm-objcopy'),'--redefine-syms='+str(root/'provider-bindings.txt'),str(raw),str(obj)],check=True)
text=subprocess.check_output([str(llvm/'llvm-readelf'),'-SW',str(obj)],text=True);ctors=sorted(set(re.findall(r'\]\s+(\.(?:init_array|ctors)(?:\.\S+)?)\s',text)));options=[]
for name in ctors:
 suffix=name.rsplit('.',1)[-1];priority=(65535-int(suffix)if name.startswith('.ctors.')else int(suffix))if suffix.isdigit()else 65535
 options+=['--rename-section',name+'=.data.rel.ro.clientopenal.init_array.'+f'{priority:05d}'+name]
if options:subprocess.run([str(llvm/'llvm-objcopy'),*options,str(obj)],check=True)
print('Compatible replacement OpenAL object:',obj,';now use relink.py --openal-object with this path')
