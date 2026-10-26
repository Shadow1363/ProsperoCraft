#!/usr/bin/env python3
"""Build a separate startup-only LWJGL module platform overlay;keep originals intact."""
from pathlib import Path
import argparse,hashlib,json,subprocess,urllib.request,zipfile,shutil
ROOT=Path(__file__).resolve().parents[1]
def build(java_home,offline=False):
 pin=json.loads((ROOT/'client/ports/lwjgl/modules.json').read_text());lock=json.loads((ROOT/'client/26.3.lock.json').read_text());out=ROOT/'build/client-ports/lwjgl-modules';out.mkdir(parents=True,exist_ok=True)
 sources=[];audits=[]
 for row in pin['modules']:
  record=row['source'];cache=ROOT/'.tools/client'/record['file']
  if not cache.exists():
   if offline:raise FileNotFoundError(cache)
   cache.write_bytes(urllib.request.urlopen(record['url'],timeout=60).read())
  data=cache.read_bytes();assert len(data)==record['size'] and hashlib.sha256(data).hexdigest()==record['sha256']
  with zipfile.ZipFile(cache)as z:original=z.read(row['unit']).decode()
  patch=ROOT/'client/ports/lwjgl'/('0004-'+row['name']+'-ps5-dispatch.patch')
  # Apply a reviewable source patch to a fresh copy of the pinned upstream unit.
  path=out/'sources'/row['unit'];path.parent.mkdir(parents=True,exist_ok=True);path.write_text(original)
  subprocess.run(['git','apply','--unsafe-paths','--directory='+str(out/'sources'),str(patch)],check=True)
  sources.append(path);audits.append({'module':row['name'],'unit':row['unit'],'source_archive_sha256':record['sha256'],'original_unit_sha256':hashlib.sha256(original.encode()).hexdigest(),'patched_unit_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'patch_sha256':hashlib.sha256(patch.read_bytes()).hexdigest()})
 classes=out/'classes';shutil.rmtree(classes,ignore_errors=True);classes.mkdir()
 cp=':'.join([str(ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar'),*[str(ROOT/'.tools/client'/r['file'])for r in lock['artifacts']]])
 subprocess.run([str(java_home/'bin/javac'),'--release','8','-proc:none','-cp',cp,'-d',str(classes),*[str(p)for p in sources]],check=True)
 emitted=sorted(classes.rglob('*.class'));assert emitted
 for path in emitted:assert str(path.relative_to(classes)).startswith(('org/lwjgl/vulkan/VK','org/lwjgl/openal/ALC','org/lwjgl/opengl/GL'))
 jar=out/'lwjgl-3.4.3-ps5-modules.jar'
 with zipfile.ZipFile(jar,'w',zipfile.ZIP_DEFLATED)as z:
  for path in emitted:
   info=zipfile.ZipInfo(str(path.relative_to(classes)));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,path.read_bytes())
  info=zipfile.ZipInfo('META-INF/PS5-PORT-LICENSE.txt');info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(ROOT/'client/ports/lwjgl/LICENSE.md').read_bytes())
 audit={'scope':pin['scope'],'units':audits,'classes':[str(p.relative_to(classes))for p in emitted],'output_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'game_jar_modified':False,'native_implementations_added':False,'console':'Native implementations are supplied separately;actual per-app PS5 validation required.026 module dispatch/callback/OpenAL acceptance is frozen separately.'}
 (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');print('Built startup module platform overlay',jar);return jar
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);p.add_argument('--offline',action='store_true');a=p.parse_args();build(a.java_home,a.offline)
