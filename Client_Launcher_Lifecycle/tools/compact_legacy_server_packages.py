#!/usr/bin/env python3
"""Compact private historical runtime server ZIP outputs;active consumer packages stay intact."""
from pathlib import Path
import hashlib,json,subprocess,tarfile
import argparse
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--runtime-workspace',type=Path,required=True);args=parser.parse_args();root=args.runtime_workspace.resolve();source=root/'build/java25';dest=Path(__file__).resolve().parents[1]/'dist/archives';archive=dest/'legacy-server-packages.tar.zst';manifest=dest/'legacy-server-packages.json'
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert not archive.exists()and not manifest.exists();files=sorted(source.glob('PPSA99874-*-full-local.zip'));assert len(files)>20
record={'scope':'Private historical server ZIP outputs;originals restored to runtime build/java25','files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)}for p in files}}
proc=subprocess.Popen(['zstd','--long=30','-T2','-10','-q','-o',str(archive.with_suffix('.partial'))],stdin=subprocess.PIPE)
try:
 with tarfile.open(fileobj=proc.stdin,mode='w|')as t:
  for p in files:t.add(p,arcname=p.name)
finally:proc.stdin.close()
assert proc.wait()==0;archive.with_suffix('.partial').rename(archive);record['archive_sha256']=sha(archive);record['archive_bytes']=archive.stat().st_size;record['original_bytes']=sum(r['bytes']for r in record['files'].values());manifest.write_text(json.dumps(record,indent=2)+'\n')
proc=subprocess.Popen(['zstd','-d','--long=30','-q','-c',str(archive)],stdout=subprocess.PIPE);seen=set()
try:
 with tarfile.open(fileobj=proc.stdout,mode='r|')as t:
  for m in t:
   assert m.isfile()and m.name in record['files'];r=record['files'][m.name];assert m.size==r['bytes']and hashlib.file_digest(t.extractfile(m),'sha256').hexdigest()==r['sha256'];seen.add(m.name)
finally:proc.stdout.close()
assert proc.wait()==0 and seen==set(record['files'])
for p in files:assert sha(p)==record['files'][p.name]['sha256']
for p in files:p.unlink()
print('VERIFIED',len(files),'historical server ZIPs;compacted',record['original_bytes'],'to',record['archive_bytes'],'bytes. Exact restore manifest:',manifest,flush=True)
