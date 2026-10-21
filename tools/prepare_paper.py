"""Materialize hash-pinned upstream Paper outputs using its original Paperclip."""
from pathlib import Path
import hashlib,json,shutil,subprocess,urllib.request,zipfile
USER_AGENT='ps5-minecraft-java/0.1 (https://github.com/mateo-cogeanu/ps5-minecraft-java)'
def checked(path,record):
 data=path.read_bytes()
 if len(data)!=record['size'] or hashlib.sha256(data).hexdigest()!=record['sha256']:raise ValueError('Paper artifact checksum: '+path.name)
 return data
def prepare(root,mojang,jars):
 lock=json.loads((root/'server/paper-26.3.lock.json').read_text());artifact=root/'.tools'/lock['file']
 if not artifact.exists():
  with urllib.request.urlopen(urllib.request.Request(lock['url'],headers={'User-Agent':USER_AGENT}),timeout=60) as response:artifact.write_bytes(response.read())
 checked(artifact,lock)
 # All runtime artifacts must agree with the publisher's embedded inventory.
 with zipfile.ZipFile(artifact) as archive:
  for kind in ['versions','libraries']:
   expected={row['id']:row for row in lock['jars'] if row['kind']==kind}
   lines=archive.read('META-INF/'+kind+'.list').decode().splitlines();assert len(lines)==len(expected)
   for line in lines:
    sha,identity,relative=line.split('\t');row=expected[identity];assert (sha,relative)==(row['sha256'],row['path'])
 work=root/'.tools/paper-26.3-207';(work/'cache').mkdir(parents=True,exist_ok=True)
 shutil.copyfile(mojang,work/'cache/mojang_26.3.jar')
 subprocess.run(['/opt/homebrew/opt/openjdk@25/bin/java','-Dpaperclip.patchonly=true','-jar',str(artifact.resolve())],cwd=work,check=True)
 assert len({row['file'] for row in lock['jars']})==len(lock['jars'])
 for row in lock['jars']:(jars/row['file']).write_bytes(checked(work/row['kind']/row['path'],row))
 classes=root/'build/paper-smoke-classes';shutil.rmtree(classes,ignore_errors=True);classes.mkdir()
 cp=':'.join(str(jars/row['file']) for row in lock['jars'])
 subprocess.run(['/opt/homebrew/opt/openjdk@25/bin/javac','--release','25','-cp',cp,'-d',str(classes),str(root/'server/paper-smoke/ps5paper/SmokePlugin.java')],check=True)
 plugins=jars.parent/'paper-plugins';plugins.mkdir()
 with zipfile.ZipFile(plugins/'ps5-paper-smoke.jar','w',zipfile.ZIP_DEFLATED) as out:
  for name,data in [('plugin.yml',(root/'server/paper-smoke/plugin.yml').read_bytes()),*[(str(f.relative_to(classes)),f.read_bytes())for f in sorted(classes.rglob('*.class'))]]:
   info=zipfile.ZipInfo(name);info.compress_type=zipfile.ZIP_DEFLATED;out.writestr(info,data)
 (plugins/'ps5-paper-smoke.sha256').write_text(hashlib.sha256((plugins/'ps5-paper-smoke.jar').read_bytes()).hexdigest()+'\n')
 return lock
