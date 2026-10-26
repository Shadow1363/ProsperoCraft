#!/usr/bin/env python3
"""Build pinned upstream LWJGL core/memory/JNI units for PS5 or host validation."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.request
ROOT=Path(__file__).resolve().parents[1]

def build(runtime,java_home,host=False,offline=False):
 port=ROOT/'client/ports/lwjgl';lock=json.loads((port/'native-sources.json').read_text());cache=ROOT/'.tools/lwjgl-native-src';cache.mkdir(parents=True,exist_ok=True)
 out=ROOT/'build/client-ports/lwjgl-native'/('host'if host else'ps5');out.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='lwjgl-native-',dir=out)as folder:
  source=Path(folder)
  for row in lock['files']:
   path=cache/row['file']
   if not path.exists():
    if offline:raise FileNotFoundError('Offline native source: '+row['file'])
    with urllib.request.urlopen(row['url'],timeout=60)as response:data=response.read()
    if len(data)!=row['size']or hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('Native source download checksum: '+row['file'])
    path.write_bytes(data)
   data=path.read_bytes()
   if len(data)!=row['size']or hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('Native source cache checksum: '+row['file'])
   (source/row['file']).write_bytes(data)
  subprocess.run(['git','apply','--unsafe-paths','--directory='+str(source),str(port/'0002-native-core-ps5.patch')],check=True)
  shutil.copyfile(port/'PS5Config.h',source/'PS5Config.h')
  if host:
   compiler='clang';flags=['-DLWJGL_MACOS','-I'+str(java_home/'include'),'-I'+str(java_home/'include/darwin'),'-fsanitize=undefined','-g']
  else:
   compiler='/opt/homebrew/opt/llvm/bin/clang';sdk=runtime/'.tools/native-sdk/ps5-payload-sdk';headers=runtime/'.tools/java25/openjdk/build/ps5-bootstrap/support/modules_include/java.base'
   flags=['-target','x86_64-sie-ps5','-march=x86-64','-msse2','-mno-avx','-mno-avx2','-mno-fma','-DLWJGL_PS5','-fvisibility-nodllstorageclass=default','-isysroot',str(sdk),'-I'+str(headers),'-I'+str(headers/'freebsd')]
  objects=[]
  for name in lock['compile_units']:
   obj=out/(name+'.o')
   subprocess.run([compiler,'-std=c11','-D_GNU_SOURCE','-O2','-fPIC','-I'+str(source),*flags,'-c',str(source/name),'-o',str(obj)],check=True);objects.append(obj)
  obj=out/'lwjgl_resident.o'
  subprocess.run([compiler,'-std=c11','-D_GNU_SOURCE','-O2','-fPIC',*flags,'-c',str(ROOT/'client/native/lwjgl_resident.c'),'-o',str(obj)],check=True);objects.append(obj)
  if host:
   subprocess.run(['clang','-dynamiclib','-fsanitize=undefined',*[str(p)for p in objects],'-o',str(out/'liblwjgl.dylib')],check=True)
 audit={'upstream_commit':lock['commit'],'source_sha256':{row['file']:row['sha256']for row in lock['files']},'objects_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in objects},'scope':lock['scope'],'target':'host validation'if host else'PS5 x86_64','compile_profile':'host validation'if host else'x86-64/SSE2; AVX/AVX2/FMA disabled', 'adaptations_sha256':{name:hashlib.sha256(path.read_bytes()).hexdigest()for name,path in [('native_patch',port/'0002-native-core-ps5.patch'),('PS5Config.h',port/'PS5Config.h'),('resident_provider',ROOT/'client/native/lwjgl_resident.c')]},'console':'pending'}
 (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');print('Built LWJGL native core subset:',out);return objects

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);p.add_argument('--java-home',type=Path,required=True);p.add_argument('--host',action='store_true');p.add_argument('--offline',action='store_true');a=p.parse_args();build(a.runtime_workspace.resolve(),a.java_home,a.host,a.offline)
