#!/usr/bin/env python3
"""Build the PS5 bootstrap harness with the separately maintained Java port."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--runtime-workspace',type=Path,required=True);args=parser.parse_args();runtime=args.runtime_workspace.resolve()
subprocess.run(['python3',str(ROOT/'tools/prepare_server.py'),'--runtime-workspace',str(runtime)],check=True)
subprocess.run(['python3',str(runtime/'tools/package_java25_jni.py'),'--probe-spec',str(ROOT/'build/probe-spec.json')],check=True)
dist=ROOT/'dist';dist.mkdir(exist_ok=True);package=dist/'PPSA99874.zip';shutil.copy2(runtime/'dist/PPSA99874.zip',package)
sha=hashlib.sha256(package.read_bytes()).hexdigest();(dist/'PPSA99874.sha256').write_text(sha+'  PPSA99874.zip\n')
version=json.loads((ROOT/'server/param.json').read_text())['contentVersion']
shutil.copy2(runtime/'build/native/llvm-pie.elf',ROOT/'build'/('bootstrap-'+version+'-symbols.elf'))
report={'minecraft':'26.3','title_id':'PPSA99874','app_version':json.loads((ROOT/'server/param.json').read_text())['contentVersion'],'package_sha256':sha,'console':'pending','scope':'Official artifact preflight and real server --help; no world generation, EULA acceptance or ready-server claim','runtime_repository':'https://github.com/mateo-cogeanu/ps5-java25-homebrew'}
(ROOT/'build/package-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('Ready:',package,'SHA256',sha)
