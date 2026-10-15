#!/usr/bin/env python3
"""Run real server readiness/save/stop in a temporary host directory."""
from pathlib import Path
import argparse,json,subprocess,tempfile,re
ROOT=Path(__file__).resolve().parents[1]
JDK=Path('/opt/homebrew/opt/openjdk@25/libexec/openjdk.jdk/Contents/Home')
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--heap-mib',type=int,default=192,choices=[128,160,192,256]);args=parser.parse_args()
assets=ROOT/'build/assets/java25';lock=json.loads((ROOT/'server/26.3.lock.json').read_text())
# Run entirely from the prepared probe JAR; no loose-class directory fallback.
cp=str(assets/'jars/ps5-server-probe.jar')+':'+str(assets/'jars/ps5-platform-diagnostics.jar')+':'+':'.join(str(assets/'jars'/r['file']) for r in lock['jars'] if r['file']!='server-26.3.jar')
with tempfile.TemporaryDirectory(prefix='ps5-mc-start-') as directory:
 result=subprocess.run([str(JDK/'bin/java'),'-Xint',f'-Xmx{args.heap_mib}m','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=8m','-XX:+PrintCodeCache','-XX:ActiveProcessorCount=2','-Dps5.probe.serverLogPath='+str(Path(directory)/'server-console.log'),'-Dps5.mc.eulaAccepted=true','-Dps5.mc.workdir='+directory,'-Duser.dir='+directory,'-Dlog4j2.disableJmx=true','-Dlog4j2.configurationFile=jar:'+ (assets/'jars/ps5-server-probe.jar').as_uri()+'!/log4j2-ps5.xml','--limit-modules',','.join(lock['modules']),'-cp',cp,'ServerStart25'],cwd=directory,capture_output=True,text=True,timeout=780)
 output=result.stdout+result.stderr;(ROOT/'build/host-ServerStart25.log').write_text(output)
 assert result.returncode==0 and 'MC_SERVER_START_OK' in output,output[-12000:]
 assert (Path(directory)/'world/level.dat').stat().st_size>0
 assert 'Done (' in (Path(directory)/'server-console.log').read_text()
 print(f'PASS: real server Done readiness, clean stop, saved level.dat at {args.heap_mib} MiB / interpreter mode')
