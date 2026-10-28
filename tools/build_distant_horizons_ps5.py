#!/usr/bin/env python3
"""Build the explicit PS5 Distant Horizons source variant; never patch an installed JAR."""
from pathlib import Path
import argparse,subprocess,json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];UPSTREAM='eb1007cb6cc3e0419effe2b40ab485cf24e55b43';CORE='64410621767ee697e8bc175c2a3ebe4c5e2ce520';VERSION='3.3.4+ps5.112'
def build(java_home):
 source=ROOT/'.tools/distant-horizons-3.3.4';patch=ROOT/'client/ports/distant_horizons/0001-explicit-ps5-platform.patch'
 if not source.exists():subprocess.run(['git','clone','--depth','1','--branch','3.3.4','https://gitlab.com/distant-horizons-team/distant-horizons.git',str(source)],check=True)
 assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==UPSTREAM
 subprocess.run(['git','-C',str(source),'submodule','update','--init','--depth','1'],check=True)
 core=source/'coreSubProjects';assert subprocess.check_output(['git','-C',str(core),'rev-parse','HEAD'],text=True).strip()==CORE
 changed=subprocess.check_output(['git','-C',str(core),'diff','--name-only'],text=True).splitlines();assert set(changed)<= {'core/src/main/java/com/seibel/distanthorizons/core/jar/EPlatform.java'},'Unexpected source edits;preserved'
 applied=subprocess.run(['git','-C',str(core),'apply','--reverse','--check',str(patch)],capture_output=True).returncode==0
 if not applied:subprocess.run(['git','-C',str(core),'apply',str(patch)],check=True)
 import os
 subprocess.run([str(source/'gradlew'),'-p',str(source),'-PmcVer=26.3.0','-Pbuilds_for=fabric','-Pmod_version='+VERSION,':fabric:build','--no-daemon'],env=dict(os.environ,JAVA_HOME=str(java_home)),check=True)
 jar=source/'fabric/build/libs'/('DistantHorizons-fabric-'+VERSION+'-26.3.jar');out=ROOT/'dist/candidates/DistantHorizons-PS5-112';out.mkdir(parents=True,exist_ok=True);target=out/jar.name;shutil.copy2(jar,target)
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();record={'upstream':UPSTREAM,'core':CORE,'patch_sha256':sha(patch),'version':VERSION,'artifact':target.name,'sha256':sha(target),'game_version':'26.3','loader':'fabric','runtime':'Requires ProsperoCraft112 native Zstd/SQLite integration','console':'pending;source build and host checks do not establish rendering or world persistence'}
 (out/'build.json').write_text(json.dumps(record,indent=2)+'\n');(out/'SHA256SUMS').write_text(sha(target)+'  '+target.name+'\n')
 shutil.copy2(source/'LICENSE.txt',out/'LICENSE.txt');shutil.copy2(source/'LICENSE.LESSER.txt',out/'LICENSE.LESSER.txt');return target
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args();print(build(a.java_home))
