#!/usr/bin/env python3
"""Build the PS5 bootstrap harness with the separately maintained Java port."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import re
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--runtime-workspace',type=Path,required=True);parser.add_argument('--join-player',required=True,help='Online account to provision in the local package, not source Git');parser.add_argument('--flavor',choices=['vanilla','fabric','paper'],default='vanilla');args=parser.parse_args()
if not re.fullmatch(r'[A-Za-z0-9_]{3,16}',args.join_player):parser.error('Join player must be one Minecraft account name')
runtime=args.runtime_workspace.resolve()
subprocess.run(['python3',str(ROOT/'tools/prepare_server.py'),'--runtime-workspace',str(runtime),'--flavor',args.flavor],check=True)
(ROOT/'build/assets/java25/join-player.txt').write_text(args.join_player+'\n')
subprocess.run(['python3',str(runtime/'tools/package_java25_jni.py'),'--probe-spec',str(ROOT/'build/probe-spec.json')],check=True)
from apply_branding import apply_package
apply_package(runtime/'dist/PPSA99874.zip',runtime/'dist/PPSA99874')
dist=ROOT/'dist';dist.mkdir(exist_ok=True);package=dist/'PPSA99874.zip';shutil.copy2(runtime/'dist/PPSA99874.zip',package)
sha=hashlib.sha256(package.read_bytes()).hexdigest();(dist/'PPSA99874.sha256').write_text(sha+'  PPSA99874.zip\n')
version=json.loads((ROOT/'server/param.json').read_text())['contentVersion']
shutil.copy2(runtime/'build/native/llvm-pie.elf',ROOT/'build'/('bootstrap-'+version+'-symbols.elf'))
report={'minecraft':'26.3','title_id':'PPSA99874','app_version':json.loads((ROOT/'server/param.json').read_text())['contentVersion'],'package_sha256':sha,'console':'pending','server_flavor':args.flavor,'scope':'Development server start probe: authorized EULA, normal world,20-player configured limit and explicit OP-all admitted-player policy; real readiness/save/stop; console pending','runtime_repository':'https://github.com/mateo-cogeanu/ps5-java25-homebrew'}
(ROOT/'build/package-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('Ready:',package,'SHA256',sha)
