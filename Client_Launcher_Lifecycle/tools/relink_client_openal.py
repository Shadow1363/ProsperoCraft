#!/usr/bin/env python3
"""Relink preserved client026 native inputs,optionally replacing compatible OpenAL."""
from pathlib import Path
import argparse,json,hashlib,subprocess,tempfile,shutil,os
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--lld',type=Path,required=True);p.add_argument('--objcopy',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--openal-object',type=Path);a=p.parse_args();root=Path(__file__).resolve().parent;manifest=json.loads((root/'manifest.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for row in manifest['files']:
 file=root/row['path'];assert file.is_file()and sha(file)==row['sha256'],'Relink input checksum: '+row['path']
with tempfile.TemporaryDirectory(prefix='client026-relink-')as temp:
 # LLVM dependent-library metadata uses original library basenames.
 # Recreate those names locally instead of relying on the build machine's SDK.
 library_dir=Path(temp)/'libraries';library_dir.mkdir()
 for row in manifest['files']:
  file=root/row['path']
  if file.suffix in {'.a','.so'}:
   target=library_dir/file.name.split('-',1)[1]
   try:os.link(file,target)
   except OSError:shutil.copyfile(file,target)
 replacement=None
 if a.openal_object:
  if not a.objcopy:raise ValueError('--objcopy /path/to/llvm-objcopy required with a replacement')
  replacement=Path(temp)/'embedded-ps5openal.o'
  subprocess.run([str(a.lld),'-r',str(a.openal_object.resolve()),str(root/manifest['openal_lifecycle']),*[str(root/item)for item in manifest.get('openal_extra_objects',[])],'-o',str(replacement)],check=True)
  subprocess.run([str(a.objcopy),'--redefine-sym','JNI_OnLoad=ps5_ps5openal_JNI_OnLoad',str(replacement)],check=True)
 args=[]
 for item in manifest['arguments']:
  if item=='{OUTPUT}':args.append(str(a.output.resolve()))
  elif item=='-L{LIBRARY_DIR}':args.append('-L'+str(library_dir))
  elif item==manifest['openal_group']and replacement:args.append(str(replacement))
  elif item.startswith('inputs/'):args.append(str(root/item))
  else:args.append(item)
 subprocess.run([str(a.lld),*args],check=True)
 if not replacement:assert sha(a.output)==manifest['original_elf_sha256'],'Unmodified ELF did not reproduce exactly'
 print('Rebuilt native ELF SHA256',sha(a.output),'(modified artifact;console acceptance does not transfer)'if replacement else'(exact tested ELF reproduced)')
