#!/usr/bin/env python3
"""Run verified official preflight and server help in an isolated host directory."""
import json
import argparse
import re
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
JDK=Path('/opt/homebrew/opt/openjdk@25/libexec/openjdk.jdk/Contents/Home')
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--runtime-image',type=Path,help='Restrict host test to modules present in the target image');args=parser.parse_args()
module_options=[]
if args.runtime_image:
    names=re.search(r'^MODULES="([^"]+)"',(args.runtime_image/'release').read_text(),re.M).group(1).split()
    module_options=['--limit-modules',','.join(names)]
classes=ROOT/'build/host-classes';classes.mkdir(exist_ok=True)
subprocess.run([str(JDK/'bin/javac'),'--release','25','-d',str(classes),*[str(p) for p in sorted((ROOT/'server/java').glob('*.java'))]],check=True)
assets=ROOT/'build/assets/java25';lock=json.loads((ROOT/'server/26.3.lock.json').read_text());cp=str(classes)+':'+':'.join(str(assets/'jars'/record['file']) for record in lock['jars'])
with tempfile.TemporaryDirectory() as directory:
    for fixture,marker in [('ServerPreflight25','MC_PREFLIGHT_OK'),('ServerHelp25','MC_SERVER_HELP_OK')]:
        result=subprocess.run([str(JDK/'bin/java'),'-Xint','-Xmx512m',*module_options,'-Dlog4j2.disableJmx=true','-Dps5.mc.assets='+str(assets),'-cp',cp,fixture],cwd=directory,capture_output=True,text=True,timeout=90)
        output=result.stdout+result.stderr;(ROOT/'build'/('host-'+fixture+'.log')).write_text(output)
        assert result.returncode==0 and marker in output,output[-5000:]
        print('PASS:',fixture,marker)
    assert not (Path(directory)/'eula.txt').exists() and not (Path(directory)/'world').exists()
    print('PASS: official --help returns without EULA acceptance or world creation')
