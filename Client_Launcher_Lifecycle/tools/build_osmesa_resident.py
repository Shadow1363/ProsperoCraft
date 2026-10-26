#!/usr/bin/env python3
"""Isolate genuine Mesa symbols and stage constructors for the PS5 resident registry."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
from build_osmesa_native import build, ROOT
LLVM=Path('/opt/homebrew/opt/llvm/bin')
def prepare(runtime,offline=False):
 out=build(offline=offline);raw=out/'osmesa-raw.o'
 nm=subprocess.check_output([str(LLVM/'llvm-nm'),'--defined-only','--extern-only',str(raw)],text=True)
 names={r.split()[-1]for r in nm.splitlines()if len(r.split())==3}
 # Preserve the actual OSMesa API;all other definitions belong to this private
 # Mesa instance,including TLS descriptors and C++ template instantiations.
 mapping={name:'clientgl_'+name for name in names if not name.startswith('OSMesa')}
 bindings=json.loads((ROOT/'build/client-gpu/audit.json').read_text())['graphics_bindings']
 mapping.update({k:v for k,v in bindings.items()if k not in names})
 rename=out/'resident-bindings.txt';rename.write_text(''.join(k+' '+v+'\n'for k,v in sorted(mapping.items())))
 obj=out/'osmesa-resident.o';subprocess.run([str(LLVM/'llvm-objcopy'),'--redefine-syms='+str(rename),str(raw),str(obj)],check=True)
 undefined=subprocess.check_output([str(LLVM/'llvm-nm'),'--undefined-only',str(raw)],text=True)
 assert '_ZTH18_glapi_tls_Context'not in undefined,'Unexpected C++ TLS initializer for constant-initialized C slot'
 sections=subprocess.check_output([str(LLVM/'llvm-readelf'),'-SW',str(obj)],text=True)
 ctors=sorted(set(re.findall(r'\]\s+(\.(?:init_array|ctors)(?:\.\S+)?)\s',sections)));options=[]
 for name in ctors:
  suffix=name.rsplit('.',1)[-1];priority=(65535-int(suffix)if name.startswith('.ctors.')else int(suffix))if suffix.isdigit()else 65535
  options+=['--rename-section',name+'=.data.rel.ro.clientgl.init_array.'+f'{priority:05d}'+name]
 if options:subprocess.run([str(LLVM/'llvm-objcopy'),*options,str(obj)],check=True)
 headers=runtime/'.tools/java25/openjdk/build/ps5-bootstrap/support/modules_include/java.base'
 flags=['-target','x86_64-sie-ps5','-O2','-fPIC','-fvisibility-nodllstorageclass=default','-isysroot',str(ROOT/'.tools/graphics-sdk'),'-I'+str(headers),'-I'+str(headers/'freebsd'),'-I'+str(ROOT/'build/mesa-osmesa-source/include')]
 objects=[obj]
 for name,src in [('lifecycle',ROOT/'client/ports/opengl/lifecycle.c'),('context',ROOT/'client/opengl_bootstrap/context.c')]:
  output=out/(name+'-resident.o');subprocess.run([str(LLVM/'clang'),*flags,'-c',str(src),'-o',str(output)],check=True);objects.append(output)
 audit={'component':json.loads((out/'audit.json').read_text()),'private_definitions':len(names)-len([n for n in names if n.startswith('OSMesa')]),'renames':mapping,'constructor_sections':ctors,'objects_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in objects},'scope':'Genuine OSMesa private symbols;existing graphics providers;explicit OnLoad constructors','tls':'Compiler-managed emulated __thread for constant-initialized GL slots;no optional C++ thunk','console':'pending actual PS5 acceptance'}
 (out/'resident-audit.json').write_text(json.dumps(audit,indent=2)+'\n');return objects,audit
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);p.add_argument('--offline',action='store_true');a=p.parse_args();prepare(a.runtime_workspace,a.offline)
