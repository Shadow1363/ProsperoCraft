#!/usr/bin/env python3
"""Build pinned real libffi and original LWJGL FFI/upcall JNI;PS5 closure W->X adapter."""
from pathlib import Path
import argparse,subprocess,json,hashlib,os,shutil,tarfile,io,urllib.request
ROOT=Path(__file__).resolve().parents[1];LLVM=Path('/opt/homebrew/opt/llvm/bin')
def build(runtime,java_home,host=False,offline=False):
 port=ROOT/'client/ports/libffi';lock=json.loads((port/'sources.json').read_text());cache=ROOT/'.tools/libffi-src'
 if not cache.exists():
  if offline:raise FileNotFoundError(cache)
  subprocess.run(['git','clone','--depth','1','--branch',lock['tag'],lock['repository'],str(cache)],check=True)
 if subprocess.run(['git','-C',str(cache),'cat-file','-e',lock['commit']],capture_output=True).returncode:
  if offline:raise FileNotFoundError('Missing pinned libffi revision')
  subprocess.run(['git','-C',str(cache),'fetch','--depth','1',lock['repository'],lock['commit']],check=True)
 subprocess.run(['git','-C',str(cache),'diff','--exit-code','HEAD'],check=True)
 out=ROOT/('build/libffi-host'if host else'build/libffi-ps5');out.mkdir(exist_ok=True);source=out/'source'
 marker=source/'.ps5-source-commit'
 if not (source/'configure').exists() or not marker.exists() or marker.read_text().strip()!=lock['commit']:
  shutil.rmtree(source,ignore_errors=True);source.mkdir()
  with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','-C',str(cache),'archive',lock['commit']])))as t:t.extractall(source,filter='data')
  subprocess.run(['sh','autogen.sh'],cwd=source,check=True);marker.write_text(lock['commit']+'\n')
 target=out/'target';target.mkdir(exist_ok=True);sdk=ROOT/'.tools/graphics-sdk'
 base=f'-isysroot {sdk} -isystem {sdk}/target/include -fvisibility-nodllstorageclass=default -march=x86-64 -msse2 -mno-avx -mno-avx2 -mno-fma -fno-stack-protector -fPIC'
 env=dict(os.environ,CC='clang'if host else str(LLVM/'clang'),AR='ar'if host else str(LLVM/'llvm-ar'),RANLIB='ranlib'if host else str(LLVM/'llvm-ranlib'))
 args=[str(source/'configure'),'--disable-shared','--enable-static','--disable-multi-os-directory','--disable-docs','--disable-exec-static-tramp']
 if not host:
  # Autoconf link checks use the same clang SysV FreeBSD ABI and actual SDK
  # import declarations;no unresolved-symbol success override or target execution.
  env.update(CFLAGS='-target x86_64-unknown-freebsd9 '+base,LDFLAGS=f'-nostdlib -fuse-ld=/opt/homebrew/opt/lld/bin/ld.lld -Wl,-e,main -L{sdk}/target/lib',LIBS='-lSceLibcInternal -lkernel');args+=['--host=x86_64-unknown-freebsd']
 else:env['CFLAGS']='-O2 -fPIC'
 subprocess.run(args,cwd=target,env=env,check=True)
 objects=[]
 if host:
  subprocess.run(['make','-j4'],cwd=target,env=env,check=True);archive=target/'.libs/libffi.a'
 else:
  adapted=out/'adapted';path=adapted/'src/x86/ffi64.c';path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/'src/x86/ffi64.c',path)
  subprocess.run(['git','apply','--unsafe-paths','--directory='+str(adapted),str(port/'0001-ps5-unix64-only.patch')],check=True);patched=path
  units=['prep_cif.c','types.c','raw_api.c','java_raw_api.c','x86/ffi64.c','x86/unix64.S']
  for unit in units:
   obj=out/(unit.replace('/','-')+'.o');subprocess.run([str(LLVM/'clang'),'-target','x86_64-sie-ps5',*base.split(),'-O2','-DHAVE_CONFIG_H','-DFFI_PS5_UNIX64_ONLY','-I'+str(source/'src/x86'),'-I'+str(target),'-I'+str(target/'include'),'-I'+str(source/'include'),'-I'+str(source/'src'),'-c',str(patched if unit=='x86/ffi64.c'else source/'src'/unit),'-o',str(obj)],check=True);objects.append(obj)
  raw=out/'ffi-raw.o';subprocess.run(['/opt/homebrew/opt/lld/bin/ld.lld','-r',*map(str,objects),'-o',str(raw)],check=True)
  obj=out/'ffi-core.o';subprocess.run([str(LLVM/'llvm-objcopy'),'--redefine-sym','ffi_prep_closure_loc=ps5ffi_prep_closure_loc_impl',str(raw),str(obj)],check=True);objects=[obj]
  obj=out/'closures-wx.o';subprocess.run([str(LLVM/'clang'),'-target','x86_64-sie-ps5',*base.split(),'-std=c11','-O2','-I'+str(target/'include'),'-c',str(port/'closures_wx.c'),'-o',str(obj)],check=True);objects.append(obj)
 # Original LWJGL generated JNI layout/constants and callback handler.
 natives=ROOT/'.tools/lwjgl-native-src';jni=[]
 for row in lock['lwjgl_files']:
  path=natives/row['file']
  if not path.exists():
   if offline:raise FileNotFoundError(path)
   path.write_bytes(urllib.request.urlopen(row['url'],timeout=60).read())
  data=path.read_bytes();assert len(data)==row['size'] and hashlib.sha256(data).hexdigest()==row['sha256']
  obj=out/(row['file']+'.o');headers=java_home/'include'if host else runtime/'.tools/java25/openjdk/build/ps5-bootstrap/support/modules_include/java.base'
  flags=['-DLWJGL_MACOS','-fsanitize=undefined','-g']if host else ['-target','x86_64-sie-ps5',*base.split(),'-DLWJGL_PS5','-DHAS_FFI_UNIX64=1','-include',str(port.parent/'lwjgl/PS5Config.h')]
  if host:flags+=['-DHAS_FFI_SYSV=1']
  # PS5Config is only needed for the target branch of common_tools.h.
  shutil.copyfile(ROOT/'client/ports/lwjgl/PS5Config.h',natives/'PS5Config.h')
  subprocess.run(['clang'if host else str(LLVM/'clang'),'-std=c11','-O2','-fPIC','-I'+str(natives),'-I'+str(target/'include'),'-I'+str(source/'include'),'-I'+str(headers),'-I'+str(headers/('darwin'if host else'freebsd')),*flags,'-c',str(path),'-o',str(obj)],check=True);jni.append(obj)
 if host:
  core=ROOT/'build/client-ports/lwjgl-native/host';library=out/'liblwjglffi.dylib'
  subprocess.run(['clang','-dynamiclib','-fsanitize=undefined',*[str(core/(u+'.o'))for u in json.loads((ROOT/'client/ports/lwjgl/native-sources.json').read_text())['compile_units']],str(core/'lwjgl_resident.o'),*map(str,jni),str(archive),'-o',str(library)],check=True);return library
 combined=out/'lwjgl-ffi.o';subprocess.run(['/opt/homebrew/opt/lld/bin/ld.lld','-r',*map(str,[*objects,*jni]),'-o',str(combined)],check=True)
 audit={'sources':lock,'abi_patch_sha256':hashlib.sha256((port/'0001-ps5-unix64-only.patch').read_bytes()).hexdigest(),'closure_allocator_sha256':hashlib.sha256((port/'closures_wx.c').read_bytes()).hexdigest(),'object_sha256':hashlib.sha256(combined.read_bytes()).hexdigest(),'target':'x86_64-sie-ps5/SysV/SSE2;configure probes against actual SDK imports','closure_policy':'One bounded mapping per closure,RW preparation then RX execution;munmap on free;failure remains real','console':'pending actual PS5 callback invocation/native-thread attachment/cleanup'};(out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');return combined,audit
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);p.add_argument('--java-home',type=Path,required=True);p.add_argument('--host',action='store_true');p.add_argument('--offline',action='store_true');a=p.parse_args();print(build(a.runtime_workspace,a.java_home,a.host,a.offline))
