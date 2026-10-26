#!/usr/bin/env python3
"""Build/sign native-only client003 using the isolated pinned RADV SDK. No JVM rebuild."""
from pathlib import Path
import subprocess,os,json,re,hashlib,shutil,zipfile
import argparse
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args()
R=Path(__file__).resolve().parents[1];W=a.runtime_workspace.resolve();S=R/'.tools/graphics-sdk';U=R/'.tools/ps5-vulkan';B=R/'build/client-graphics';B.mkdir(exist_ok=True)
LLVM=Path('/opt/homebrew/opt/llvm/bin');env=dict(os.environ,LLVM_CONFIG=str(LLVM/'llvm-config'))
from prepare_client_graphics import LOCK
# Reject dependency changes rather than packaging a different, unrecorded driver.
for key,path in [('driver',U),('mesa',R/'.tools/PS5_Mesa')]:
 assert subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()==LOCK[key]['commit']
 subprocess.run(['git','-C',str(path),'diff','--exit-code','HEAD'],check=True)
assert json.loads((S/'.client-graphics-sdk.json').read_text())['fork_commit']==LOCK['sdk']['commit']
for row in LOCK['compiler_rt']['files']+[LOCK['compiler_rt']['license']]:
 path=R/'build'/('graphics-cpu-model.c'if row.get('file')=='x86.c'else row.get('file','graphics-LLVM-LICENSE.txt'))
 assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],path.name

def run(*args,**kw):subprocess.run(list(map(str,args)),check=True,env=env,**kw)
flags=['-target','x86_64-sie-ps5','-isysroot',str(S),'-fvisibility-nodllstorageclass=default','-fno-stack-protector','-fno-plt','-femulated-tls','-march=x86-64','-msse2','-mno-avx','-mno-avx2','-mno-fma','-fdenormal-fp-math=ieee','-O2','-ffunction-sections','-fdata-sections']
objects=[]
for name,source,cxx,extra in [
 ('presentation',R/'client/graphics/presentation.c',False,['-I'+str(R/'.tools/PS5_Mesa/include')]),
 ('bootstrap',R/'client/graphics/bootstrap.cpp',True,['-I'+str(W/'java25/probe'),'-I'+str(W/'src')]),
 ('crt',U/'tooling/native/app_crt.cpp',True,[]),
 ('cpp_runtime',U/'tooling/native/app_cpp_runtime.cpp',True,[]),
 ('cpu_model',R/'build/graphics-cpu-model.c',False,['-I'+str(R/'build')])]:
 obj=B/(name+'.o');run(LLVM/('clang++'if cxx else'clang'),*flags,*(['-std=c++20','-fno-exceptions','-fno-rtti','-isystem',str(S/'target/include/c++/v1')]if cxx else['-std=c11']),'-isystem',str(S/'target/include'),'-Wall','-Wextra','-Werror',*extra,'-c',source,'-o',obj);objects.append(obj)
# compiler-rt's actual target emulated-TLS object is supplied by the verified SDK.
run(LLVM/'llvm-ar','x',S/'target/lib/libc.a','emutls.o',cwd=B)
rt=B/'libgraphics-builtins.a';run(LLVM/'llvm-ar','rcs',rt,B/'emutls.o')
# Keep upstream dependency checkout intact. Adapt only the host-specific builtins
# archive path in a generated copy of its recipe; symbol/heap/thread flags stay upstream.
recipe=(U/'tools/radv-link.sh').read_text();pattern=r'    builtins=".*?\n'
recipe,n=re.subn(pattern,'    builtins="'+str(rt)+'"\n',recipe,count=1);assert n==1
(B/'radv-link-host.sh').write_text(recipe)
stubs=[]
for lib,src in [('libSceAgc','agc_canary_link_stub.c'),('libSceAgcDriver','agc_driver_canary_link_stub.c')]:
 obj=B/(lib+'.o');so=B/(lib+'.so');run(LLVM/'clang',*flags,'-c',U/'vendor/ps5/sdk/stubs'/src,'-o',obj)
 run('bash',S/'bin/prospero-lld','--shared','-soname',lib+'.prx','-o',so,obj);stubs.append(so)
script=B/'link.sh';script.write_text('''#!/bin/bash
set -euo pipefail
source "$1"
radv_link_recipe "$2" "$3" "$4"
shift 4
"$1/bin/prospero-lld" "${radv_linker_script[@]}" --eh-frame-hdr "${radv_link_flags[@]}" \\
 --version-script "$2/tooling/native/app-symbols.map" --exclude-libs=ALL -e _start -o "$3/llvm-pie.elf" \\
 "$3/crt.o" "$3/cpp_runtime.o" "$3/bootstrap.o" "$3/presentation.o" "$3/cpu_model.o" \\
 "$3/libSceAgc.so" "$3/libSceAgcDriver.so" "${radv_link_inputs[@]}" --as-needed "$1"/target/lib/*.so
''')
run('bash',script,B/'radv-link-host.sh',U,S,R/'build/graphics-radv/src/amd/vulkan/libvulkan_radeon.a',S,U,B)
tool=W/'build/native/host/ps5-native-tool'
run(tool,'link','--in',B/'llvm-pie.elf','--out',B/'eboot.elf','--stub-dir',S/'target/lib',*sum([['--stub',str(s)]for s in stubs],[]),'--module-sdk','0x02000009','--companion-sdk','0x08050001','--file-name','eboot.elf')
app=B/'PPSA99874';(app/'sce_sys').mkdir(parents=True,exist_ok=True);(app/'sce_module').mkdir(exist_ok=True)
run(tool,'self','--sign','--in',B/'eboot.elf','--out',app/'eboot.bin','--magic','0x1D3D154F')
shutil.copyfile(R/'client/graphics/param.json',app/'sce_sys/param.json');shutil.copyfile(W/'sce_sys/icon0.png',app/'sce_sys/icon0.png');shutil.copyfile(W/'build/native/libc.prx',app/'sce_module/libc.prx')
from apply_branding import apply_app
apply_app(app)
licenses=app/'licenses';licenses.mkdir(exist_ok=True)
for src,name in [(U/'LICENSE','PS5-Vulkan-GPL-3.0.txt'),(R/'build/graphics-sdk-source/LICENSE','PS5-PayloadSDK-GPL-3.0.txt'),(R/'.tools/PS5_Mesa/licenses/MIT','Mesa-MIT.txt'),(R/'.tools/PS5_Mesa/licenses/Apache-2.0','Mesa-Apache-2.0.txt'),(R/'build/graphics-LLVM-LICENSE.txt','LLVM-LICENSE.txt')]:
 shutil.copyfile(src,licenses/name)
shutil.copytree(R/'.tools/PS5_Mesa/licenses',licenses/'Mesa',dirs_exist_ok=True)
# Retain per-source leading copyright/license notices from the pinned Mesa,
# SDK and installed SDK headers, alongside the full component license texts.
notices=[];seen=set()
for tree,label in [(R/'.tools/PS5_Mesa','Mesa'),(R/'build/graphics-sdk-source','SDK-fork'),(S/'target/include','SDK-headers')]:
 for path in sorted(tree.rglob('*')):
  if not path.is_file()or path.suffix not in {'.c','.h','.cpp','.hpp','.cc'}:continue
  data=path.read_bytes()[:32768].decode('utf-8',errors='replace');pos=0;blocks=[]
  while True:
   m=re.match(r'\s*(/\*.*?\*/|//[^\n]*(?:\n|$))',data[pos:],re.S)
   if not m:break
   blocks.append(m.group(1));pos+=m.end()
  notice='\n'.join(blocks).strip()
  if notice and any(word in notice.lower()for word in ['copyright','spdx','permission'])and notice not in seen:
   seen.add(notice);notices.append(label+'/'+str(path.relative_to(tree))+'\n'+notice+'\n')
(licenses/'UPSTREAM-NOTICES.txt').write_text('\n'.join(notices))
shutil.copyfile(R/'.tools/PS5_Mesa/docs/license.rst',licenses/'Mesa-license-guide.rst')
shutil.copyfile(R/'build/graphics-sdk-source/platform/src/regex/COPYRIGHT.musl',licenses/'musl-regex-COPYRIGHT.txt')
(licenses/'SOURCES.txt').write_text('Native-only client003. Source pins: client/graphics/sources.json in https://github.com/mateo-cogeanu/ProsperoCraft .\nDriver CRT/recipe/import declarations: mihawk-99/PS5_Vulkan GPL-3.0-or-later; Mesa/RADV/ACO/NIR and its component licenses; PS5 payload SDK v0.42 and pinned fork/platform; LLVM compiler-rt22.1.7 Apache-2.0 WITH LLVM-exception. No Java or game JARs in this app.\n')
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
audit={'source_pins':json.loads((R/'client/graphics/sources.json').read_text()),'scope':'Native-only; no Java, SDL, audio, Minecraft, shader pipeline or lifecycle teardown validation','radv_archive_sha256':sha(R/'build/graphics-radv/src/amd/vulkan/libvulkan_radeon.a'),'platform_archive_sha256':sha(S/'target/lib/libps5platform.a'),'host_recipe_sha256':sha(B/'radv-link-host.sh'),'objects_sha256':{p.name:sha(p)for p in objects},'stub_policy':'AGC stub .so files are import declarations consumed by native converter, never shipped/executed','runtime_sdk_replaced':False,'console':'pending'}
assets=app/'assets';assets.mkdir(exist_ok=True);(assets/'graphics-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
for p in [app/'eboot.bin',app/'sce_module/libc.prx']:run(tool,'self','--inspect','--file',p)
D=R/'dist/client-graphics';D.mkdir(exist_ok=True)
with zipfile.ZipFile(D/'PPSA99874.zip','w',compression=zipfile.ZIP_DEFLATED)as z:
 for p in sorted(app.rglob('*')):
  if p.is_file():
   info=zipfile.ZipInfo(str(p.relative_to(B)));info.external_attr=0o100777<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
shutil.copyfile(D/'PPSA99874.zip',W/'dist/PPSA99874.zip')
print('SHA256',hashlib.sha256((D/'PPSA99874.zip').read_bytes()).hexdigest())
(D/'SHA256SUMS').write_text(hashlib.sha256((D/'PPSA99874.zip').read_bytes()).hexdigest()+'  PPSA99874.zip\n')
