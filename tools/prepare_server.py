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
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--runtime-workspace',type=Path,required=True);parser.add_argument('--flavor',choices=['vanilla','fabric','paper'],default='vanilla');args=parser.parse_args()
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
extra=[]
paper=None
if args.flavor=='paper':
    from prepare_paper import prepare
    for path in jars.iterdir():path.unlink()
    paper=prepare(ROOT,cache,jars)
    lock={**lock,'jars':paper['jars'],'modules':[*lock['modules'],'jdk.security.auth','java.net.http']}
if args.flavor=='fabric':
    fabric=json.loads((ROOT/'server/fabric-26.3.lock.json').read_text());extra=fabric['jars']
    for record in extra:
        path=ROOT/'.tools'/record['file']
        if not path.exists():urllib.request.urlretrieve(record['url'],path)
        payload=path.read_bytes()
        assert len(payload)==record['size'] and hashlib.sha256(payload).hexdigest()==record['sha256'],record['file']
        (jars/record['file']).write_bytes(payload)
    mod_classes=ROOT/'build/fabric-smoke-classes';shutil.rmtree(mod_classes,ignore_errors=True);mod_classes.mkdir()
    loader=jars/next(x['file'] for x in extra if x['id'].startswith('net.fabricmc:fabric-loader:'))
    subprocess.run(['/opt/homebrew/opt/openjdk@25/bin/javac','--release','25','-cp',str(loader),'-d',str(mod_classes),str(ROOT/'server/fabric-smoke/ps5fabric/SmokeMod.java')],check=True)
    mods=assets/'java25/fabric-mods';mods.mkdir()
    with zipfile.ZipFile(mods/'ps5-fabric-smoke.jar','w',zipfile.ZIP_DEFLATED) as mod:
        for name,data in [('fabric.mod.json',(ROOT/'server/fabric-smoke/fabric.mod.json').read_bytes()),('ps5fabric/SmokeMod.class',(mod_classes/'ps5fabric/SmokeMod.class').read_bytes())]:
            info=zipfile.ZipInfo(name);info.compress_type=zipfile.ZIP_DEFLATED;mod.writestr(info,data)
    (mods/'ps5-fabric-smoke.sha256').write_text(hashlib.sha256((mods/'ps5-fabric-smoke.jar').read_bytes()).hexdigest()+'\n')
inventory=''.join(record['file']+'='+record['sha256']+'\n' for record in lock['jars']+extra)
(assets/'java25/server-inventory.properties').write_text(inventory)
log_config=ROOT/('server/config/log4j2-paper-ps5.xml' if paper else 'server/config/log4j2-ps5.xml')
shutil.copy2(log_config,assets/'java25/log4j2-ps5.xml')
# Put the consumer's helper classes in a JAR: the PS5 system loader already
# supports bundled JAR URLs, while loose class-directory lookup uses sandbox
# metadata operations that are not established for these fixtures.
java_sources=sorted((ROOT/'server/java').glob('*.java'))+[runtime/'java25/tests/ps5probe/JitWarmup25.java']
wrapper_classes=ROOT/'build/wrapper-classes';shutil.rmtree(wrapper_classes,ignore_errors=True);wrapper_classes.mkdir()
subprocess.run(['/opt/homebrew/opt/openjdk@25/bin/javac','--release','25','-cp',str(next(jars/r['file'] for r in lock['jars'] if r['id'].startswith('com.google.code.gson:gson:'))),'-d',str(wrapper_classes),*[str(p) for p in java_sources]],check=True)
# Execute the hash-verified original server JAR. No transformations/signature stripping.
assert not (jars/'ps5-platform-diagnostics.jar').exists()
execution=json.loads((ROOT/'server/execution.json').read_text())
execution['flavor']=args.flavor
execution['loader']=fabric['loader'] if args.flavor=='fabric' else 'Paper upstream build207' if paper else None
execution['external_loader_transformations']='Fabric standard class loading/Mixin; no project game-JAR rewrites' if args.flavor=='fabric' else None
if paper:
    execution={'flavor':'paper','upstream_distribution':'Paper26.3 build207','upstream_paperclip_sha256':paper['sha256'],'server_sha256':next(row['sha256'] for row in paper['jars'] if row['kind']=='versions'),'active_game_transformations':[],'replacement_game_classes':[],'project_game_transformations':[],'note':'Executes pinned upstream Paper server, not unmodified Mojang server; only upstream Paperclip applies publisher patches on host.'}
else:
    server=next(record for record in lock['jars'] if record['file']=='server-26.3.jar')
    assert execution['server_sha256']==server['sha256'] and execution['active_game_transformations']==[] and execution['replacement_game_classes']==[]
(assets/'java25/execution-audit.json').write_text(json.dumps(execution,indent=2)+'\n')
with zipfile.ZipFile(jars/'ps5-server-probe.jar','w',zipfile.ZIP_DEFLATED) as probe:
    config=zipfile.ZipInfo('log4j2-ps5.xml');config.compress_type=zipfile.ZIP_DEFLATED
    probe.writestr(config,log_config.read_bytes())
    for path in sorted(wrapper_classes.rglob('*.class')):
        info=zipfile.ZipInfo(path.relative_to(wrapper_classes).as_posix());info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
        probe.writestr(info,path.read_bytes())
with zipfile.ZipFile(jars/'ps5-server-probe.jar') as probe:
    assert 'ServerStart25$Observer.class' in probe.namelist()
classpath='/app0/assets/java25/jars/ps5-server-probe.jar:'+':'.join('/app0/assets/java25/jars/'+record['file'] for record in lock['jars']+extra)
(ROOT/'build/server_classpath.hpp').write_text('#pragma once\n#define SERVER_CLASSPATH_OPTION '+json.dumps('-Djava.class.path='+classpath)+'\n#define SERVER_FLAVOR_OPTION '+json.dumps('-Dps5.mc.serverFlavor='+args.flavor)+'\n#define SERVER_HEAP_OPTION '+json.dumps('-Xmx384m' if paper else '-Xmx224m')+'\n#define SERVER_IS_PAPER '+str(int(paper is not None))+'\n#define SERVER_FLAVOR_LABEL '+json.dumps('Fabric '+fabric['loader'] if args.flavor=='fabric' else 'Paper 26.3 build207' if paper else 'Vanilla')+'\n')
spec={'menu_audio':False,'source':str(ROOT/'server/native/bootstrap.cpp'),'param':str(ROOT/'server/param.json'),'asset_dir':str(assets),'java_sources':[str(p) for p in java_sources],'modules':lock['modules'],'java_compile_classpath':[str(next(jars/r['file'] for r in lock['jars'] if r['id'].startswith('com.google.code.gson:gson:')))],'include_dirs':[str(ROOT/'build'),str(runtime/'java25/probe')]}
(ROOT/'build/probe-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
print('Prepared',len(lock['jars']),'verified upstream runtime JARs and',len(extra),'loader JARs; flavor',args.flavor)
