#!/usr/bin/env python3
"""Losslessly archive inactive failed-client packages locally;never uploads game JARs."""
from pathlib import Path
import argparse,hashlib,json,subprocess,tarfile,shutil,os,re
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'dist/failures';FOLDER=ROOT/'dist/archives';ARCHIVE=FOLDER/'failed-client-builds.tar.zst';MANIFEST=FOLDER/'failed-client-builds.json'
def digest(path):
 with path.open('rb')as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def verify(record):
 proc=subprocess.Popen(['zstd','-d','--long=30','-q','-c',str(ARCHIVE)],stdout=subprocess.PIPE);seen=set()
 try:
  with tarfile.open(fileobj=proc.stdout,mode='r|')as archive:
   for member in archive:
    if not member.isfile():continue
    row=record['files'].get(member.name)
    if row is None:raise ValueError('Unexpected archive member: '+member.name)
    stream=archive.extractfile(member);actual=hashlib.file_digest(stream,'sha256').hexdigest()
    if actual!=row['sha256']or member.size!=row['bytes']:raise ValueError('Archive member mismatch: '+member.name)
    seen.add(member.name)
 finally:proc.stdout.close()
 if proc.wait()!=0 or seen!=set(record['files']):raise ValueError('Incomplete/corrupt archive')
 print('Verified exact archived bytes for',len(seen),'files',flush=True)
def main():
 global ARCHIVE,MANIFEST
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['pack','verify','restore']);p.add_argument('--batch',help='New archive suffix, preserving all earlier archives');a=p.parse_args();FOLDER.mkdir(exist_ok=True)
 if a.batch:
  if not re.fullmatch(r'[A-Za-z0-9_-]+',a.batch):raise ValueError('Invalid batch name')
  ARCHIVE=FOLDER/('failed-client-builds-'+a.batch+'.tar.zst');MANIFEST=FOLDER/('failed-client-builds-'+a.batch+'.json')
 if a.action=='pack':
  if ARCHIVE.exists()or MANIFEST.exists():raise ValueError('Archive already exists;verify/restore instead')
  files={}
  for path in sorted(SOURCE.rglob('*')):
   if path.is_symlink():raise ValueError('Unexpected symlink')
   if path.is_file():files[path.relative_to(ROOT/'dist').as_posix()]={'bytes':path.stat().st_size,'sha256':digest(path)}
  if not files:raise ValueError('No failures to archive')
  record={'scope':'Private exact failed-client packages/symbols;no game JAR upload','files':files,'original_bytes':sum(r['bytes']for r in files.values())};temporary=ARCHIVE.with_suffix('.partial')
  compressor=subprocess.Popen(['zstd','--long=30','-T2','-10','-q','-o',str(temporary)],stdin=subprocess.PIPE)
  try:
   with tarfile.open(fileobj=compressor.stdin,mode='w|')as archive:archive.add(SOURCE,arcname='failures',recursive=True)
  finally:compressor.stdin.close()
  if compressor.wait()!=0:raise RuntimeError('Compression failed;originals kept')
  temporary.rename(ARCHIVE);record['archive_sha256']=digest(ARCHIVE);record['archive_bytes']=ARCHIVE.stat().st_size;MANIFEST.write_text(json.dumps(record,indent=2)+'\n');verify(record)
  # Recheck originals after verification before deleting inactive expanded copies.
  for name,row in files.items():
   if digest(ROOT/'dist'/name)!=row['sha256']:raise ValueError('Original changed during archive: '+name)
  shutil.rmtree(SOURCE)
  print('Compacted',record['original_bytes'],'bytes to',record['archive_bytes'],'bytes;manifest',MANIFEST,flush=True)
 else:
  record=json.loads(MANIFEST.read_text())
  if digest(ARCHIVE)!=record['archive_sha256']:raise ValueError('Archive checksum mismatch')
  verify(record)
  if a.action=='restore':
   if SOURCE.exists():raise ValueError('Restore refuses to overwrite existing failures')
   proc=subprocess.Popen(['zstd','-d','--long=30','-q','-c',str(ARCHIVE)],stdout=subprocess.PIPE)
   try:
    with tarfile.open(fileobj=proc.stdout,mode='r|')as archive:archive.extractall(ROOT/'dist',filter='data')
   finally:proc.stdout.close()
   if proc.wait()!=0:raise RuntimeError('Restore decompression failed')
   for name,row in record['files'].items():
    if digest(ROOT/'dist'/name)!=row['sha256']:raise ValueError('Restored checksum mismatch: '+name)
   print('Restored exact failed-client packages;compact archive retained')
if __name__=='__main__':main()
