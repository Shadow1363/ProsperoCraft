#!/usr/bin/env python3
"""Compare098/099G1 policies on retained/churn host controls;not PS5 timing proof."""
from pathlib import Path
import argparse,subprocess,tempfile,json,re,statistics
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--java-home',type=Path,required=True);a=p.parse_args()
source=r'''
import java.lang.management.*;
import com.sun.management.HotSpotDiagnosticMXBean;
public class G1FrameControl {
 static byte[][] retained=new byte[1000][], ring=new byte[2048][];
 static void verify(){for(int i=0;i<retained.length;i++)if(retained[i][0]!=(byte)i||retained[i][retained[i].length-1]!=(byte)(i+1))throw new AssertionError("retained contents");}
 public static void main(String[]args){
  var bean=ManagementFactory.getPlatformMXBean(HotSpotDiagnosticMXBean.class);
  String[] names={"MaxGCPauseMillis","G1NewSizePercent","G1MixedGCCountTarget"};
  for(int i=0;i<names.length;i++)if(!bean.getVMOption(names[i]).getValue().equals(args[i]))throw new AssertionError("wrong effective flag:"+names[i]);
  if(ManagementFactory.getGarbageCollectorMXBeans().stream().noneMatch(gc->gc.getName().contains("G1")))throw new AssertionError("wrong collector");
  for(int i=0;i<retained.length;i++){retained[i]=new byte[524312];retained[i][0]=(byte)i;retained[i][524311]=(byte)(i+1);}
  for(int i=0;i<262144;i++){int n=16384+(i%7)*16;ring[i%ring.length]=new byte[n];ring[i%ring.length][0]=(byte)i;ring[i%ring.length][n-1]=(byte)(i+1);if(i%8192==0)verify();}
  verify();for(int i=0;i<ring.length;i++){int last=262143-((262143-i)%ring.length);byte[] b=ring[i];if(b[0]!=(byte)last||b[b.length-1]!=(byte)(last+1))throw new AssertionError("ring contents");}
  System.out.println("PASS G1 effective flags,500MiB retained524312-byte arrays plus32MiB small-object ring/4GiB churn with checked contents");
 }
}
'''
s=(ROOT/'client/startup/bootstrap.cpp').read_text()
common=['-Xmixed','-XX:TieredStopAtLevel=1','-XX:CICompilerCount=1','-XX:CompileThresholdScaling=4.0','-XX:CompileCommand=MemLimit,*.*,2M','-XX:ReservedCodeCacheSize=32m','-XX:SweeperThreshold=50.0','-Xms128m','-Xmx1536m','-XX:-UseCompressedOops','-XX:+UseCompactObjectHeaders','-XX:+UseG1GC','-XX:ParallelGCThreads=4','-XX:ConcGCThreads=1','-XX:G1ReservePercent=20','-XX:ActiveProcessorCount=4']
new=['-XX:MaxGCPauseMillis=4','-XX:+UnlockExperimentalVMOptions','-XX:G1NewSizePercent=1','-XX:G1MixedGCCountTarget=16']
for flag in common+new:assert '"'+flag+'"'in s,flag
results={}
with tempfile.TemporaryDirectory(prefix='g1-frame-policy-')as folder:
 w=Path(folder);(w/'G1FrameControl.java').write_text(source)
 subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-d',str(w),str(w/'G1FrameControl.java')],check=True)
 for label,flags,expected in [('098',['-XX:+UnlockExperimentalVMOptions','-XX:MaxGCPauseMillis=8'],['8','5','8']),('099',new,['4','1','16'])]:
  log=ROOT/('build/client099-host-policy-'+label+'.log')
  run=subprocess.run([str(a.java_home/'bin/java'),*common,*flags,'-Xlog:gc=info,safepoint=info:file='+str(log)+':uptimemillis,level,tags','-cp',str(w),'G1FrameControl',*expected],capture_output=True,text=True,timeout=120)
  assert run.returncode==0 and 'PASS G1 effective flags'in run.stdout,run.stdout+run.stderr
  text=log.read_text();assert 'Pause Young'in text and 'Using G1'in text
  pauses=[float(m[1])for m in re.finditer(r'Pause (?:Young|Remark|Cleanup).* ([\d.]+)ms',text)]
  results[label]={'contents':'PASS','effective_flags':dict(zip(['MaxGCPauseMillis','G1NewSizePercent','G1MixedGCCountTarget'],expected)),'pause_count':len(pauses),'median_ms':statistics.median(pauses),'max_ms':max(pauses),'full_GC':'Pause Full'in text}
  assert not results[label]['full_GC'],'Unexpected fullGC in host control'
  print(label,json.dumps(results[label]))
results['scope']='Host effective flags,allocation/content/collector integration only. Synthetic workloads and host pause timing do not establish PS5 frame times,stutter improvement,actual native headroom or game stability.'
(ROOT/'build/client099-host-policy.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS actual098/099G1 host policy comparison;PS5 outcome pending')
