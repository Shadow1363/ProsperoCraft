#!/usr/bin/env python3
"""Prepare official, hash-pinned server assets locally; no game files enter Git."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import urllib.request
import zipfile
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--runtime-workspace',type=Path,required=True);args=parser.parse_args()
runtime=args.runtime_workspace.resolve();lock=json.loads((ROOT/'server/26.3.lock.json').read_text())
cache=ROOT/'.tools/server-26.3.jar';cache.parent.mkdir(exist_ok=True)
if not cache.exists():urllib.request.urlretrieve(lock['server_bundle']['url'],cache)
data=cache.read_bytes()
assert len(data)==lock['server_bundle']['size'] and hashlib.sha1(data).hexdigest()==lock['server_bundle']['sha1']
assert hashlib.sha256(data).hexdigest()==lock['server_bundle_sha256']
assets=ROOT/'build/assets';shutil.rmtree(assets,ignore_errors=True);jars=assets/'java25/jars';jars.mkdir(parents=True)
assert len({record['file'] for record in lock['jars']})==len(lock['jars'])
with zipfile.ZipFile(cache) as archive:
    for kind in ['versions','libraries']:
        expected={record['id']:record for record in lock['jars'] if record['kind']==kind}
        lines=archive.read('META-INF/'+kind+'.list').decode().splitlines();assert len(lines)==len(expected)
        for line in lines:
            sha,identity,relative=line.split('\t');record=expected[identity];assert sha==record['sha256'] and Path(relative).name==record['file']
            payload=archive.read('META-INF/'+kind+'/'+relative);assert hashlib.sha256(payload).hexdigest()==sha
            (jars/record['file']).write_bytes(payload)
inventory=''.join(record['file']+'='+record['sha256']+'\n' for record in lock['jars'])
(assets/'java25/server-inventory.properties').write_text(inventory)
shutil.copy2(ROOT/'server/config/log4j2-ps5.xml',assets/'java25/log4j2-ps5.xml')
# Put the consumer's helper classes in a JAR: the PS5 system loader already
# supports bundled JAR URLs, while loose class-directory lookup uses sandbox
# metadata operations that are not established for these fixtures.
wrapper_classes=ROOT/'build/wrapper-classes';shutil.rmtree(wrapper_classes,ignore_errors=True);wrapper_classes.mkdir()
subprocess.run(['/opt/homebrew/opt/openjdk@25/bin/javac','--release','25','-d',str(wrapper_classes),*[str(p) for p in sorted((ROOT/'server/java').glob('*.java'))]],check=True)
with zipfile.ZipFile(jars/'ps5-server-probe.jar','w',zipfile.ZIP_DEFLATED) as probe:
    config=zipfile.ZipInfo('log4j2-ps5.xml');config.compress_type=zipfile.ZIP_DEFLATED
    probe.writestr(config,(ROOT/'server/config/log4j2-ps5.xml').read_bytes())
    for path in sorted(wrapper_classes.rglob('*.class')):
        info=zipfile.ZipInfo(path.relative_to(wrapper_classes).as_posix());info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
        probe.writestr(info,path.read_bytes())
with zipfile.ZipFile(jars/'ps5-server-probe.jar') as probe:
    assert 'ServerStart25$Observer.class' in probe.namelist()
classpath='/app0/assets/java25/jars/ps5-server-probe.jar:'+':'.join('/app0/assets/java25/jars/'+record['file'] for record in lock['jars'])
(ROOT/'build/server_classpath.hpp').write_text('#pragma once\n#define SERVER_CLASSPATH_OPTION '+json.dumps('-Djava.class.path='+classpath)+'\n')
spec={'source':str(ROOT/'server/native/bootstrap.cpp'),'param':str(ROOT/'server/param.json'),'asset_dir':str(assets),'java_sources':[str(p) for p in sorted((ROOT/'server/java').glob('*.java'))],'modules':lock['modules'],'include_dirs':[str(ROOT/'build'),str(runtime/'java25/probe')]}
(ROOT/'build/probe-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
print('Prepared 40 verified official server JARs and external probe specification')
