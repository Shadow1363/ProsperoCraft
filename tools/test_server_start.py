#!/usr/bin/env python3
"""Run real server readiness/save/stop in a temporary host directory."""
from pathlib import Path
import argparse,json,subprocess,tempfile,re
ROOT=Path(__file__).resolve().parents[1]
JDK=Path('/opt/homebrew/opt/openjdk@25/libexec/openjdk.jdk/Contents/Home')
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--heap-mib',type=int,default=144,choices=[128,144,160,192,256]);parser.add_argument("--worker-runner",type=Path,help="Native JNI worker fixture runner from the Java runtime tests");parser.add_argument('--endurance-seconds',type=int,default=0);parser.add_argument('--online-player');parser.add_argument('--chunk-radius',type=int,default=0,choices=range(5));args=parser.parse_args();assert 0<=args.endurance_seconds<=86400
assets=ROOT/'build/assets/java25';lock=json.loads((ROOT/'server/26.3.lock.json').read_text())
# Run entirely from the prepared probe JAR; no loose-class directory fallback.
cp=str(assets/'jars/ps5-server-probe.jar')+':'+str(assets/'jars/ps5-platform-diagnostics.jar')+':'+':'.join(str(assets/'jars'/r['file']) for r in lock['jars'] if r['file']!='server-26.3.jar')
with tempfile.TemporaryDirectory(prefix='ps5-mc-start-') as directory:
 command=[str(JDK/'bin/java'),'-Xint','-Xss512k',f'-Xmx{args.heap_mib}m','-Dio.netty.allocator.type=unpooled','-Dps5.mc.checkNetworkMemory=true',f'-Dps5.mc.validationChunkRadius={args.chunk_radius}','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=8m','-XX:+PrintCodeCache','-XX:ActiveProcessorCount=2','-Dps5.probe.serverLogPath='+str(Path(directory)/'server-console.log'),'-Dps5.mc.eulaAccepted=true',*(['-Dps5.mc.requireOnline=true','-Dps5.mc.joinPlayer='+args.online_player] if args.online_player else []),f'-Dps5.mc.enduranceSeconds={args.endurance_seconds}','-Dps5.mc.endurancePollSeconds=2','-Dps5.mc.enduranceSaveSeconds=4','-Dps5.mc.enduranceReplySeconds=120','-Dps5.mc.workdir='+directory,'-Duser.dir='+directory,'-Dlog4j2.disableJmx=true','-Dlog4j2.configurationFile=jar:'+ (assets/'jars/ps5-server-probe.jar').as_uri()+'!/log4j2-ps5.xml','--limit-modules',','.join(lock['modules']),'-cp',cp,'ServerStart25']
 if args.worker_runner:
  # JNI invocation takes VM properties, not launcher -cp arguments.
  options=command[1:-3]
  index=options.index('--limit-modules');options[index:index+2]=['--limit-modules='+options[index+1]]
  command=[str(args.worker_runner.resolve()),'ServerStart25',*options,'-Djava.class.path='+cp]
 result=subprocess.run(command,cwd=directory,capture_output=True,text=True,timeout=780+args.endurance_seconds)
 output=result.stdout+result.stderr;(ROOT/'build/host-ServerStart25.log').write_text(output)
 assert result.returncode==0 and 'MC_SERVER_START_OK' in output,output[-12000:]
 if args.endurance_seconds:
  assert 'MC_SERVER_ENDURANCE_OK' in output and 'MC_ENDURANCE_COMPLETE' in output,output[-12000:]
  health=re.findall(r'MC_ENDURANCE_HEALTH elapsedSeconds=(\d+).*?gameTime=(\d+).*?checks=(\d+).*?saves=(\d+)',output)
  assert len(health)>=2 and int(health[-1][0])>=args.endurance_seconds and int(health[-1][1])>int(health[0][1]),health
  assert 'pause-when-empty-seconds=0' in (Path(directory)/'server.properties').read_text()
  assert 'Saved the game' in output,output[-12000:]
 if args.online_player:
  assert 'MC_ONLINE_PREFLIGHT_OK' in output,output[-12000:]
  assert any(v['name'].lower()==args.online_player.lower() for v in json.loads((Path(directory)/'whitelist.json').read_text()))
 assert 'MC_NETWORK_MEMORY_OK' in output,output[-12000:]
 if args.chunk_radius:
  assert 'Marked '+str((2*args.chunk_radius+1)**2)+' chunks' in output,output[-12000:]
  assert any(p.stat().st_size>8192 for p in Path(directory).rglob('*.mca')),'No persisted region data'
 assert 'No key layers' not in output, output[-12000:]
 assert (Path(directory)/'world/level.dat').stat().st_size>0
 assert 'Done (' in (Path(directory)/'server-console.log').read_text()
 print(f'PASS: real server Done readiness, clean stop, saved level.dat at {args.heap_mib} MiB / interpreter mode')
