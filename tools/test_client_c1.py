#!/usr/bin/env python3
"""Actual guarded client C1 gate and interpreter/stale-log controls on host."""
from pathlib import Path
import argparse,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args()
with tempfile.TemporaryDirectory(prefix='client-c1-check-')as folder:
 w=Path(folder);log=w/'jit.log'
 subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-d',str(w),str(a.runtime_workspace/'java25/tests/ps5probe/JitWarmup25.java')],check=True)
 common=[str(a.java_home/'bin/java'),'-Xms128m','-Xmx1536m','-XX:-UseCompressedOops','-XX:+UseCompactObjectHeaders','-XX:+UseG1GC','-XX:MaxGCPauseMillis=8','-XX:ParallelGCThreads=4','-XX:ConcGCThreads=1','-XX:G1ReservePercent=20','-XX:ActiveProcessorCount=4','-XX:ReservedCodeCacheSize=32m','-XX:SweeperThreshold=50.0','-Dps5.probe.jitLog='+str(log),'-cp',str(w)]
 flags=['-Xmixed','-XX:TieredStopAtLevel=1','-XX:CICompilerCount=1','-XX:CompileThresholdScaling=4.0','-XX:CompileCommand=MemLimit,*.*,2M']
 logflag='-Xlog:jit+compilation=debug,codecache=info:file='+str(log)+':uptime,level,tags:filecount=1,filesize=4M'
 result=subprocess.run(common+flags+[logflag,'ps5probe.JitWarmup25'],capture_output=True,text=True,timeout=60)
 assert result.returncode==0 and 'JIT_WARMUP_OK level=1' in result.stdout,result.stdout+result.stderr
 assert 'ps5probe.JitWarmup25::kernel' in log.read_text()
 print(result.stdout.strip())
 result=subprocess.run(common+flags+['ps5probe.JitWarmup25'],capture_output=True,text=True,timeout=60)
 assert result.returncode and 'require fresh VM/session' in result.stderr,result.stdout+result.stderr
 result=subprocess.run(common+['-Xint','ps5probe.JitWarmup25'],capture_output=True,text=True,timeout=30)
 assert result.returncode and 'C1 gate requires' in result.stderr,result.stdout+result.stderr
 log.unlink()
 result=subprocess.run(common+flags+['ps5probe.JitWarmup25'],capture_output=True,text=True,timeout=60)
 assert result.returncode and 'No current-run level-1' in result.stderr,result.stdout+result.stderr
print('PASS actual client1536MiB/G1/uncompressed guardedC1 flags:level1compile andpostcompilechecksum;stale/interpreter/missinglogrefusal. Hostonly,noPS5speed/stabilityclaim')
