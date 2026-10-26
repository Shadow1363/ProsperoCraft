#!/usr/bin/env python3
"""Stage hash-verified original assets from the already pinned publisher index."""
from pathlib import Path
import argparse,hashlib,json,concurrent.futures,urllib.request,shutil,time
ROOT=Path(__file__).resolve().parents[1]
def prepare(offline=False):
 lock=json.loads((ROOT/'client/26.3.lock.json').read_text());pin=lock['asset_index'];index=ROOT/'.tools/client'/pin['file'];data=index.read_bytes()
 for algorithm in ['sha1','sha256']:
  if algorithm in pin:assert hashlib.new(algorithm,data).hexdigest()==pin[algorithm]
 assert len(data)==pin['size']
 objects=json.loads(data)['objects'];unique={v['hash']:v['size']for v in objects.values()};cache=ROOT/'.tools/client-assets/objects';dest=ROOT/'build/client-assets';cache.mkdir(parents=True,exist_ok=True)
 def fetch(row):
  digest,size=row;assert len(digest)==40 and all(c in '0123456789abcdef'for c in digest)
  path=cache/digest[:2]/digest;path.parent.mkdir(exist_ok=True)
  def valid():return path.exists()and path.stat().st_size==size and hashlib.sha1(path.read_bytes()).hexdigest()==digest
  if not valid():
   if offline:raise FileNotFoundError('Missing verified asset '+digest)
   for attempt in range(3):
    try:
     with urllib.request.urlopen('https://resources.download.minecraft.net/'+digest[:2]+'/'+digest,timeout=45)as response:blob=response.read()
     assert len(blob)==size and hashlib.sha1(blob).hexdigest()==digest
     temporary=path.with_suffix('.part');temporary.write_bytes(blob);temporary.replace(path);break
    except Exception:
     if attempt==2:raise
   assert valid()
  target=dest/'objects'/digest[:2]/digest;target.parent.mkdir(parents=True,exist_ok=True)
  if not target.exists()or target.stat().st_size!=size or hashlib.sha1(target.read_bytes()).hexdigest()!=digest:shutil.copyfile(path,target)
  return size
 with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
  count=0;total=0
  for size in pool.map(fetch,sorted(unique.items())):
   count+=1;total+=size
   if count%500==0:print('Verified assets',count,'/',len(unique),'bytes',total,flush=True)
 (dest/'indexes').mkdir(parents=True,exist_ok=True);shutil.copyfile(index,dest/'indexes'/(pin['id']+'.json'))
 audit={'asset_index':pin,'logical_objects':len(objects),'unique_objects':len(unique),'unique_bytes':sum(unique.values()),'verification':'Every original object matches publisher index SHA1 and size;all objects staged,including sounds. No transformed/replacement assets.','console':'Asset preparation is not startup/menu validation.'};(dest/'asset-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print('PASS all pinned original assets staged',len(unique),sum(unique.values()),flush=True)
 return dest
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--offline',action='store_true');a=p.parse_args();prepare(a.offline)
