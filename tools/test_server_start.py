#!/usr/bin/env python3
"""Run real server readiness/save/stop in a temporary host directory."""
from pathlib import Path
import argparse,json,subprocess,tempfile,re
ROOT=Path(__file__).resolve().parents[1]
JDK=Path('/opt/homebrew/opt/openjdk@25/libexec/openjdk.jdk/Contents/Home')
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--heap-mib',type=int,default=192,choices=[128,160,192,256]);args=parser.parse_args()
classes=ROOT/'build/host-classes';classes.mkdir(exist_ok=True)
subprocess.run([str(JDK/'bin/javac'),'--release','25','-d',str(classes),str(ROOT/'server/java/ServerStart25.java')],check=True)
assets=ROOT/'build/assets/java25';lock=json.loads((ROOT/'server/26.3.lock.json').read_text())
cp=str(classes)+':'+':'.join(str(assets/'jars'/r['file']) for r in lock['jars'])
with tempfile.TemporaryDirectory(prefix='ps5-mc-start-') as directory:
 result=subprocess.run([str(JDK/'bin/java'),'-Xint',f'-Xmx{args.heap_mib}m','-XX:+UseSerialGC','-XX:ActiveProcessorCount=2','-Dps5.mc.eulaAccepted=true','-Dps5.mc.workdir='+directory,'-Duser.dir='+directory,'-Dlog4j2.disableJmx=true','--limit-modules',','.join(lock['modules']),'-cp',cp,'ServerStart25'],cwd=directory,capture_output=True,text=True,timeout=780)
 output=result.stdout+result.stderr;(ROOT/'build/host-ServerStart25.log').write_text(output)
 assert result.returncode==0 and 'MC_SERVER_START_OK' in output,output[-12000:]
 assert (Path(directory)/'world/level.dat').stat().st_size>0
 print(f'PASS: real vanilla Done readiness, clean stop, saved level.dat at {args.heap_mib} MiB / interpreter mode')
