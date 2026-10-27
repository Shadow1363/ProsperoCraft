#!/usr/bin/env python3
"""Build the pinned OSHI dependency port, leaving original OSHI/game JARs intact."""
from pathlib import Path
import argparse,hashlib,json,subprocess,urllib.request,zipfile,shutil
ROOT=Path(__file__).resolve().parents[1]
def build(java_home,offline=False):
 source=ROOT/'client/ports/oshi';spec=json.loads((source/'sources.json').read_text());archive=ROOT/'.tools/oshi-core-6.9.0-sources.jar';pin=spec['source']
 if not archive.exists():
  if offline:raise RuntimeError('Missing pinned OSHI source archive')
  urllib.request.urlretrieve(pin['url'],archive)
 assert archive.stat().st_size==pin['size'] and hashlib.sha256(archive.read_bytes()).hexdigest()==pin['sha256']
 assert hashlib.sha256((source/'LICENSE').read_bytes()).hexdigest()==spec['license']['sha256']
 work=ROOT/'build/client-ports/oshi';work.mkdir(parents=True,exist_ok=True);src=work/'src';shutil.rmtree(src,ignore_errors=True);(src/'oshi').mkdir(parents=True)
 with zipfile.ZipFile(archive) as z:(src/'oshi/SystemInfo.java').write_bytes(z.read('oshi/SystemInfo.java'))
 subprocess.run(['patch','-s','-p1','-i',str(source/'0001-ps5-cpu-provider.patch')],cwd=src,check=True)
 shutil.copytree(source/'java',src,dirs_exist_ok=True);classes=work/'classes';shutil.rmtree(classes,ignore_errors=True);classes.mkdir()
 cp=':'.join(str(ROOT/'.tools/client'/n) for n in ('oshi-core-6.9.0.jar','jna-5.17.0.jar','slf4j-api-2.0.17.jar'))
 subprocess.run([str(java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(classes),*[str(p) for p in sorted(src.rglob('*.java'))]],check=True)
 output=work/'oshi-6.9.0-ps5-platform.jar'
 with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(classes.rglob('*.class')):
   info=zipfile.ZipInfo(p.relative_to(classes).as_posix());info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
  z.writestr(zipfile.ZipInfo('META-INF/OSHI-LICENSE.txt'),(source/'LICENSE').read_bytes())
 audit={'scope':spec['scope'],'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'upstream_source':pin,'source_sha256':{p.relative_to(source).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source.rglob('*')) if p.is_file()},'game_jar_modified':False,'console':'pending'}
 (work/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');print('PASS OSHI CPU platform overlay',audit['output_sha256']);return output
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);p.add_argument('--offline',action='store_true');a=p.parse_args();build(a.java_home,a.offline)
