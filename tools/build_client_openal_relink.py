#!/usr/bin/env python3
"""Preserve exact native link inputs and OpenAL source for a frozen LGPL-linked app."""
from pathlib import Path
import argparse,json,subprocess,shutil,hashlib,zipfile,tarfile,io
ROOT=Path(__file__).resolve().parents[1]
def build(runtime,output):
 output.mkdir(parents=True,exist_ok=True);work=ROOT/'build/client-native_bootstrap-probe';sdk=runtime/'.tools/native-sdk/ps5-payload-sdk';native=runtime/'.tools/native-app/tooling/native';kit=output/'relink-kit';kit.mkdir(exist_ok=True)
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();files={};entries=[]
 def keep(p):
  p=Path(p).resolve()
  if str(p)in files:return files[str(p)]
  rel='inputs/'+f'{len(files):03d}-'+p.name;target=kit/rel;target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target);files[str(p)]=rel;entries.append({'path':rel,'sha256':sha(target),'bytes':target.stat().st_size});return rel
 flags=[json.loads(line)for line in (work/'combined-link.rsp').read_text().splitlines()]
 # Reproduce the SDK driver's actual ld.lld arguments without a host-specific SDK wrapper.
 args=['-m','elf_x86_64','-pie','--eh-frame-hdr','-z','max-page-size=0x4000','-mllvm','-emulated-tls','-T',keep(work/'gpu-probe.ld'),'--eh-frame-hdr','--version-script',keep(native/'app-symbols.map'),'--version-script',keep(work/'gpu-abi-local.map'),'-e','_start','-o','{OUTPUT}']
 for name in ['main.o','renderer.o','crt.o','cpp_runtime.o']:args.append(keep(work/name))
 args+=[keep(ROOT/'build/client-graphics/libSceAgc.so'),keep(ROOT/'build/client-graphics/libSceAgcDriver.so')]
 for token in flags:args.append(token if token.startswith('-')else keep(token))
 args+=['--as-needed',*[keep(p)for p in sorted((sdk/'target/lib').glob('*.so'))],'--hash-style=gnu']
 openal_group=keep(runtime/'build/java25/embedded-ps5openal.o');life=keep(ROOT/'build/openal-ps5/lifecycle.o')
 manifest={'app_version':'01.000.026','tested_source_commit':'4191ea21b7206367fd0749762f4fff89cf6f9e43','original_elf_sha256':sha(work/'bootstrap-01.000.026-symbols.elf'),'arguments':args,'openal_group':openal_group,'openal_lifecycle':life,'files':entries,'llvm':'22.1.7','scope':'Exact relocatable native application/runtime/dependency objects and SDK import declarations;no game JARs or asset objects. Use a compatible scoped OpenAL object from build_openal_native.py for replacement.'}
 (kit/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 shutil.copyfile(ROOT/'tools/relink_client_openal.py',kit/'relink.py')
 shutil.copyfile(ROOT/'tools/build_client_openal_replacement.py',kit/'build_openal_replacement.py')
 shutil.copyfile(ROOT/'build/openal-ps5/provider-bindings.txt',kit/'provider-bindings.txt')
 sourcepin=json.loads((ROOT/'client/ports/openal/sources.json').read_text());data=subprocess.check_output(['git','-C',str(ROOT/'.tools/openal-soft-src'),'archive','--format=tar',sourcepin['commit']]);(kit/'openal-soft-1.25.2-source.tar').write_bytes(data)
 for path in ['client/ports/openal/sources.json','client/ports/openal/lifecycle.c','tools/build_openal_native.py']:
  dest=kit/'consumer-source'/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,dest)
 # Include the exact build-time target headers for rebuilding the LGPL library.
 with tarfile.open(kit/'ps5-sdk-headers.tar','w')as tar:tar.add(ROOT/'.tools/graphics-sdk/target/include',arcname='target/include')
 (kit/'README.txt').write_text('''Client026 OpenAL corresponding-source/relink kit\n\nUnzip this kit. Python3 and LLVM/LLD22.1.7 are needed.\nRun: python3 relink.py --lld /path/to/ld.lld --output rebuilt-symbols.elf\nThis reproduces the tested native ELF from the included exact link objects.\nAll manifest input SHA256s are checked;the unmodified relink must match the recorded ELF.\n\nTo replace the LGPL OpenAL library:extract openal-soft-1.25.2-source.tar,edit it,\nand build a compatible PS5 OpenAL object using build_openal_replacement.py:\npython3 build_openal_replacement.py --source /path/to/edited/source --build-dir /path/to/build --llvm-bin /path/to/llvm/bin --lld /path/to/ld.lld\nThis helper accepts an edited source tree without a pristine-check restriction.\nThe recipe needs the pinned project SDK/scoped graphics provider bindings;the SDK\nheaders are included. The full frozen consumer source and pins are in the release\ntag at https://github.com/mateo-cogeanu/ps5-minecraft-java.\nBuild-time staging renames .ctors to retained .data.rel.ro.clientopenal.init_array.*\nand binds libc/thread references to the same real scoped graphics providers.\nThe compatible replacement object must preserve the public OpenAL ABI and this\nconstructor contract. Invoke relink.py --openal-object /path/to/new/openal.o.\nThe helper combines it with the included lifecycle object,renames JNI_OnLoad,\nand substitutes only the embedded OpenAL group. All other native inputs stay intact.\n\nConvert the resulting ELF to eboot.bin using the pinned PS5 native packaging tool\nfrom https://github.com/mateo-cogeanu/ps5-java25-homebrew and the frozen packaging\nsource. This remains normal homebrew packaging;no private signing key is needed.\nUse the public app-only ZIP and its provision helper to add your exact original\nclient/Java JARs. No game JARs are in this kit. Source edits/relinks invalidate\nthe console validation of the original026 artifact.\n\nThe original OpenAL COPYING,LICENSE-pffft,BSD-3Clause and bundled MIT/BSD license\nfiles are in the source tar. OpenAL Soft is LGPL-2.0-or-later. Relink objects\nretain their upstream licenses;runtime/dependency pins and notices are in the\nfrozen source and app. This kit does not grant rights to unrelated game data.\n''')
 archive=output/'client026-openal-source-relink.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED)as z:
  for p in sorted(kit.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(kit))
 return kit,archive
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(build(a.runtime_workspace,a.output))
