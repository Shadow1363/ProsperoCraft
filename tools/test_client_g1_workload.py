#!/usr/bin/env python3
"""Real G1 retained-world occupancy/churn control; no Minecraft timing claim."""
from pathlib import Path
import argparse,subprocess,tempfile,json,re
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args()
source=r'''
import java.lang.management.*;
public class G1WorldControl {
 static byte[][] retained=new byte[600][];
 static byte[][] ring=new byte[24][];
 static void verify(){for(int i=0;i<retained.length;i++)if(retained[i][0]!=(byte)i||retained[i][retained[i].length-1]!=(byte)(i+1))throw new AssertionError("retained");}
 public static void main(String[]args){
  if(ManagementFactory.getGarbageCollectorMXBeans().stream().noneMatch(gc->gc.getName().contains("G1")))throw new AssertionError("wrong collector");
  for(int i=0;i<600;i++){retained[i]=new byte[1024*1024];retained[i][0]=(byte)i;retained[i][retained[i].length-1]=(byte)(i+1);}
  for(int i=0;i<2048;i++){ring[i%24]=new byte[2*1024*1024];ring[i%24][0]=(byte)i;if(i%128==0)verify();}
  verify();for(int i=0;i<24;i++){int last=2047-((2047-i)%24);if(ring[i][0]!=(byte)last)throw new AssertionError("ring");}
  System.out.println("PASS actual G1:600MiB retained+48MiB live ring+4GiB transient churn, checked contents intact; no explicit System.gc");
 }
}
'''
with tempfile.TemporaryDirectory(prefix='client-g1-control-')as folder:
 w=Path(folder);(w/'G1WorldControl.java').write_text(source)
 subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-d',str(w),str(w/'G1WorldControl.java')],check=True)
 log=ROOT/'build/client074-g1-workload-gc.log'
 flags=['-Xmixed','-XX:TieredStopAtLevel=1','-XX:CICompilerCount=1','-XX:CompileThresholdScaling=4.0','-XX:CompileCommand=MemLimit,*.*,2M','-XX:ReservedCodeCacheSize=32m','-XX:SweeperThreshold=50.0','-Xms128m','-Xmx1536m','-XX:-UseCompressedOops','-XX:+UseCompactObjectHeaders','-XX:+UseG1GC','-XX:MaxGCPauseMillis=8','-XX:ParallelGCThreads=4','-XX:ConcGCThreads=1','-XX:G1ReservePercent=20','-XX:ActiveProcessorCount=4']
 for flag in flags:assert '"'+flag+'"' in (ROOT/'client/startup/bootstrap.cpp').read_text(),flag
 result=subprocess.run([str(a.java_home/'bin/java'),*flags,'-Xlog:gc*=debug:file='+str(log),'-cp',str(w),'G1WorldControl'],capture_output=True,text=True,timeout=120)
 assert result.returncode==0 and 'contents intact'in result.stdout,result.stdout+result.stderr
 text=log.read_text();assert 'Using G1'in text and 'Pause Young'in text and 'Concurrent Mark Cycle'in text
 full=re.findall(r'Pause Full.*?([\d.]+)ms',text)
 assert not full,'Unexpected full GC in bounded host workload; inspect before claiming control pass'
 (ROOT/'build/client074-g1-workload.json').write_text(json.dumps({'workload':'600MiBretained/48MiBring/4GiBtransient','contents':'PASS','collector':'ActualG1','concurrent_mark_cycle':True,'full_pauses':len(full),'explicit_gc':False,'scope':'Host only, notPS5timing/physicalreservation/native-pressure/Minecraftacceptance'},indent=2)+'\n')
 print(result.stdout.strip())
print('PASS real G1 mixed/concurrent-cycle control with candidate flags; PS5 GC integration pending')
