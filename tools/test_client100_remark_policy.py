#!/usr/bin/env python3
"""Verify scoped remark-unloading deferral and full-GC reclamation on a real JVM."""
from pathlib import Path
import argparse,subprocess,tempfile,json,re
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--java-home',type=Path,required=True);a=p.parse_args()
source=r'''
import java.lang.management.*;
import java.lang.ref.*;
import java.nio.file.*;
import java.util.*;
import com.sun.management.HotSpotDiagnosticMXBean;
public class RemarkPolicyControl {
 static class Loader extends ClassLoader {Loader(){super(null);} Class<?> define(byte[]b){return defineClass("UnloadMarker",b,0,b.length);}}
 static List<WeakReference<ClassLoader>> refs=new ArrayList<>();
 static byte[][] kept=new byte[128][];
 static void load(byte[]bytes)throws Exception{for(int i=0;i<120;i++){Loader l=new Loader();Class<?>c=l.define(bytes);if(!c.getName().equals("UnloadMarker")||c.getClassLoader()!=l)throw new AssertionError("class definition");refs.add(new WeakReference<>(l));}}
 public static void main(String[]args)throws Exception{
  var bean=ManagementFactory.getPlatformMXBean(HotSpotDiagnosticMXBean.class);
  if(!bean.getVMOption("ClassUnloading").getValue().equals("true"))throw new AssertionError("full class unloading disabled");
  if(!bean.getVMOption("ClassUnloadingWithConcurrentMark").getValue().equals(args[1]))throw new AssertionError("wrong remark flag");
  load(Files.readAllBytes(Path.of(args[0])));
  for(int i=0;i<kept.length;i++){kept[i]=new byte[524312];kept[i][0]=(byte)i;}
  for(int n=0;n<10;n++){System.gc();Thread.sleep(50);}
  long cleared=refs.stream().filter(r->r.get()==null).count();
  boolean expectCleared=Boolean.parseBoolean(args[2]);
  if(!args[2].equals("any")&&(expectCleared?cleared!=120:cleared!=0))throw new AssertionError("unexpected loader reclamation:"+cleared);
  for(int i=0;i<kept.length;i++)if(kept[i][0]!=(byte)i)throw new AssertionError("retained payload");
  System.out.println("PASS scoped remark policy:cleared="+cleared+"/120;full class unloading enabled,live payload intact");
 }
}
'''
s=(ROOT/'client/startup/bootstrap.cpp').read_text();assert '"-XX:-ClassUnloadingWithConcurrentMark"'in s
common=['-Xmixed','-XX:TieredStopAtLevel=1','-XX:CICompilerCount=1','-Xms128m','-Xmx1536m','-XX:-UseCompressedOops','-XX:+UseCompactObjectHeaders','-XX:+UseG1GC','-XX:MaxGCPauseMillis=4','-XX:+UnlockExperimentalVMOptions','-XX:G1NewSizePercent=1','-XX:G1MixedGCCountTarget=16','-XX:ParallelGCThreads=4','-XX:ConcGCThreads=1','-XX:G1ReservePercent=20','-XX:ActiveProcessorCount=4']
for flag in common:assert '"'+flag+'"'in s,flag
results={}
with tempfile.TemporaryDirectory(prefix='remark-policy-')as folder:
 w=Path(folder);(w/'RemarkPolicyControl.java').write_text(source);(w/'UnloadMarker.java').write_text('public class UnloadMarker{public static int value(){return42;}}'.replace('return42','return 42'))
 subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-d',str(w),str(w/'RemarkPolicyControl.java'),str(w/'UnloadMarker.java')],check=True)
 for label,flags,concurrent,expected in [('099-concurrent',['-XX:+ClassUnloadingWithConcurrentMark','-XX:+ExplicitGCInvokesConcurrent'],'true','any'),('100-concurrent',['-XX:-ClassUnloadingWithConcurrentMark','-XX:+ExplicitGCInvokesConcurrent'],'false','false'),('100-full',['-XX:-ClassUnloadingWithConcurrentMark'],'false','true')]:
  log=ROOT/('build/client100-host-'+label+'.log')
  run=subprocess.run([str(a.java_home/'bin/java'),*common,*flags,'-Xlog:gc=info,gc+phases=debug,class+unload=info:file='+str(log)+':uptimemillis,level,tags','-cp',str(w),'RemarkPolicyControl',str(w/'UnloadMarker.class'),concurrent,expected],capture_output=True,text=True,timeout=90)
  assert run.returncode==0 and 'PASS scoped remark policy'in run.stdout,run.stdout+run.stderr
  text=log.read_text();unloads=len(re.findall(r'unloading class UnloadMarker ',text));assert expected=='any' or unloads==(120 if expected=='true'else 0)
  if label.endswith('concurrent'):
   assert 'Pause Remark'in text and 'Pause Full'not in text
   assert ('Class Unloading'in text)==(concurrent=='true')
  else:assert 'Pause Full (System.gc())'in text
  results[label]={'contents':'PASS','unloaded_fixture_classes':unloads,'ClassUnloading':True,'ClassUnloadingWithConcurrentMark':concurrent=='true','full_GC':'Pause Full'in text,'remark':'Pause Remark'in text}
  print(label,run.stdout.strip())
results['scope']='Real host G1 flag gating/classloader retention and full-GC reclamation;not PS5 latency/memory/lifecycle acceptance. Deferral retains unused classloaders/code longer and can increase pressure/fullGC risk.'
(ROOT/'build/client100-remark-policy.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS scoped100remark deferral with full-GC unloading retained;PS5 pending')
