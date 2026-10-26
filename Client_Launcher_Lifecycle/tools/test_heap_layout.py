#!/usr/bin/env python3
"""Compare actual SerialGC promotion pressure at the console's fixed heap size.
Long-lived arrays model heap occupancy; this is not a player or PS5 latency test.
"""
from pathlib import Path
import subprocess,tempfile,re,json
r=Path(__file__).resolve().parents[1];jdk=Path('/opt/homebrew/opt/openjdk@25/bin')
source=r'''import java.lang.management.*;
public class HeapLayout {
 static volatile Object sink;static byte[][] retained;
 static long full(){long n=0;for(var gc:ManagementFactory.getGarbageCollectorMXBeans())if(gc.getName().contains("MarkSweep"))n+=gc.getCollectionCount();return n;}
 public static void main(String[]args){retained=new byte[108*128][];for(int i=0;i<retained.length;i++){retained[i]=new byte[8192];retained[i][0]=(byte)i;}
 System.gc();long before=full();for(int i=0;i<65536;i++){byte[]next=new byte[8192];next[0]=(byte)i;sink=next;}int checksum=0;for(int i=0;i<retained.length;i++)if(retained[i][0]!=(byte)i)throw new AssertionError("Live data changed");else checksum+=retained[i][0];System.out.println("HEAP_LAYOUT fullCollections="+(full()-before)+" checksum="+checksum+" maxHeap="+Runtime.getRuntime().maxMemory());}
}'''
with tempfile.TemporaryDirectory() as directory:
 w=Path(directory);(w/'HeapLayout.java').write_text(source);subprocess.run([str(jdk/'javac'),str(w/'HeapLayout.java')],check=True)
 results={}
 for ratio in [2,7]:
  result=subprocess.run([str(jdk/'java'),'-Xmixed','-XX:TieredStopAtLevel=1','-XX:CICompilerCount=1','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=16m','-Xms16m','-Xmx144m','-XX:NewRatio='+str(ratio),'-cp',str(w),'HeapLayout'],capture_output=True,text=True,timeout=120)
  if result.returncode:
   assert ratio==2 and 'OutOfMemoryError: Java heap space' in result.stderr,result.stdout+result.stderr
   results[ratio]='heapOOM';print('ratio',ratio,'heapOOM under retained108MiB plus512MiB transient allocation');continue
  count=int(re.search(r'fullCollections=(\d+)',result.stdout)[1]);results[ratio]=count;print('ratio',ratio,result.stdout.strip())
 assert results[7]<=2 and (results[2]=='heapOOM' or results[2]>results[7]),results
 (r/'build/host-heap-layout.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS: retained108MiB content preserved; actual 144MiB SerialGC churn completes with NewRatio7; ratio2 has more full collections or a real heap-OOM control; host occupancy model, not console proof')
