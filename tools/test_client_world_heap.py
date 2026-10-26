#!/usr/bin/env python3
"""Actual SerialGC occupancy control for client+integrated-server heap headroom.

Arrays approximate the observed224MiB live occupancy; not Minecraft, PS5 mapping,
world timing, native-memory pressure or a promise that512MiB is sufficient.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args()
source=r'''
import java.lang.management.*;
public class ClientWorldHeap {
 static byte[][] live; static volatile Object sink;
 public static void main(String[]args){
  live=new byte[224][];
  for(int i=0;i<live.length;i++){live[i]=new byte[1024*1024];live[i][0]=(byte)i;live[i][live[i].length-1]=(byte)(i+1);}
  System.gc();
  for(int n=0;n<16;n++){sink=new byte[32*1024*1024];}
  for(int i=0;i<live.length;i++)if(live[i][0]!=(byte)i||live[i][live[i].length-1]!=(byte)(i+1))throw new AssertionError("retained data changed");
  System.out.println("PASS retained224MiB plus512MiB transient churn,contents preserved,maxHeap="+Runtime.getRuntime().maxMemory());
 }
}
'''
with tempfile.TemporaryDirectory(prefix='client-world-heap-')as folder:
    w=Path(folder);(w/'ClientWorldHeap.java').write_text(source)
    subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-d',str(w),str(w/'ClientWorldHeap.java')],check=True)
    results={}
    for heap in [256,512]:
        r=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-XX:+UseSerialGC','-XX:+UseCompactObjectHeaders','-Xms16m','-Xmx'+str(heap)+'m',*(['-XX:-UseCompressedOops'] if heap==512 else []),'-cp',str(w),'ClientWorldHeap'],capture_output=True,text=True,timeout=60)
        if heap==256:
            assert r.returncode and 'OutOfMemoryError: Java heap space' in r.stderr,r.stdout+r.stderr
            results[str(heap)]='Real Java heap OOM in the occupancy control'
        else:
            assert r.returncode==0 and 'contents preserved' in r.stdout,r.stdout+r.stderr
            results[str(heap)]=r.stdout.strip()
        print(heap,'MiB:',results[str(heap)])
    (ROOT/'build/client065-heap-model.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS actual heap headroom control;host occupancy model only,not target reservation/world performance or sufficiency proof')
