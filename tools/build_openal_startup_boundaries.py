#!/usr/bin/env python3
"""Recompile only private pinned alc.cpp with bounded native scope observations."""
from pathlib import Path
import hashlib
import json
import re
import shlex
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
LLVM=Path('/opt/homebrew/opt/llvm/bin')
LLD=Path('/opt/homebrew/opt/lld/bin/ld.lld')
MEMBER='CMakeFiles/OpenAL.dir/alc/alc.cpp.o'
ANCHORS=[
 ('alcGetError','ALC_API ALCenum ALC_APIENTRY alcGetError(ALCdevice *device) noexcept\n{','device'),
 ('alcGetString','ALC_API auto ALC_APIENTRY alcGetString(ALCdevice *Device, ALCenum param) noexcept -> const ALCchar*\ntry {','Device'),
 ('alcGetIntegerv','ALC_API void ALC_APIENTRY alcGetIntegerv(ALCdevice *device, ALCenum param, ALCsizei size,\n    ALCint *values) noexcept\ntry {','device'),
 ('alcCreateContext','ALC_API auto ALC_APIENTRY alcCreateContext(ALCdevice *device, const ALCint *attrList) noexcept\n    -> ALCcontext*\ntry {','device'),
 ('alcMakeContextCurrent','ALC_API auto ALC_APIENTRY alcMakeContextCurrent(ALCcontext *context) noexcept -> ALCboolean\ntry {','context'),
]
def sha(path):return hashlib.file_digest(path.open('rb'),'sha256').hexdigest()
def command(line):
 args=shlex.split(line)
 if '&&'in args:args=args[args.index('&&')+1:];args=args[:args.index('&&')]if'&&'in args else args
 return args
def build(host=False):
 source=ROOT/'.tools/openal-soft-src';pin=json.loads((ROOT/'client/ports/openal/sources.json').read_text())
 assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==pin['commit']
 subprocess.run(['git','-C',str(source),'diff','--exit-code','HEAD'],check=True)
 base=ROOT/('build/openal-host'if host else'build/openal-ps5')
 out=ROOT/('build/openal-startup-boundary-host'if host else'build/openal-startup-boundary-ps5');out.mkdir(exist_ok=True)
 original=source/'alc/alc.cpp';text=original.read_text()
 for name,anchor,value in ANCHORS:
  assert text.count(anchor)==1,name
  text=text.replace(anchor,anchor+'\n    client_openal_boundary::Scope startup_scope{"'+name+'", '+value+'};')
 patched=out/'alc.cpp';patched.write_text(text)
 header=ROOT/'client/ports/openal/startup_boundary.hpp';obj=out/'alc.cpp.o'
 lines=subprocess.check_output(['ninja','-C',str(base),'-t','commands',MEMBER],text=True).splitlines();args=command(lines[-1])
 args[args.index('-o')+1]=str(obj);args[args.index('-c')+1]=str(patched)
 if '-MF'in args:args[args.index('-MF')+1]=str(out/'alc.cpp.o.d')
 args+=['-iquote',str(source/'alc'),'-include',str(header)]
 subprocess.run(args,cwd=base,check=True)
 audit={'pin':pin,'original_source_sha256':sha(original),'patched_source_sha256':sha(patched),'header_sha256':sha(header),'unit_object_sha256':sha(obj),'functions':[x[0]for x in ANCHORS],'scope':'At most128native API body scopes/256records,errno preserved;scope-exit includes exception unwinding,not success/return proof','game_jar_modified':False}
 if host:
  lines=subprocess.check_output(['ninja','-C',str(base),'-t','commands','OpenAL'],text=True).splitlines()
  args=command(next(line for line in lines if '-dynamiclib'in line));library=out/'libopenal-boundary.dylib'
  args[args.index('-o')+1]=str(library);args[args.index(MEMBER)]=str(obj)
  subprocess.run(args,cwd=base,check=True);result=library
 else:
  original_archive=base/'libopenal.a';before=sha(original_archive);archive=out/'libopenal-boundary.a';shutil.copy2(original_archive,archive)
  assert subprocess.check_output([str(LLVM/'llvm-ar'),'t',str(archive)],text=True).splitlines().count('alc.cpp.o')==1
  subprocess.run([str(LLVM/'llvm-ar'),'r',str(archive),str(obj)],check=True)
  raw=out/'openal-raw.o';subprocess.run([str(LLD),'-r','--whole-archive',str(archive),'--no-whole-archive','-o',str(raw)],check=True)
  result=out/'openal.o';subprocess.run([str(LLVM/'llvm-objcopy'),'--redefine-syms='+str(base/'provider-bindings.txt'),str(raw),str(result)],check=True)
  sections=subprocess.check_output([str(LLVM/'llvm-readelf'),'-SW',str(result)],text=True);ctors=sorted(set(re.findall(r'\]\s+(\.(?:init_array|ctors)(?:\.\S+)?)\s',sections)));opts=[]
  for name in ctors:
   suffix=name.rsplit('.',1)[-1];priority=(65535-int(suffix)if name.startswith('.ctors.')else int(suffix))if suffix.isdigit()else 65535
   opts+=['--rename-section',name+'=.data.rel.ro.clientopenal.init_array.'+f'{priority:05d}'+name]
  if opts:subprocess.run([str(LLVM/'llvm-objcopy'),*opts,str(result)],check=True)
  assert sha(original_archive)==before
  audit.update(original_archive_sha256=before,private_archive_sha256=sha(archive),original_archive_unchanged=True,constructor_sections=ctors,replaced_member='alc.cpp.o')
 audit['output_sha256']=sha(result);(out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
 return result,audit
