#!/usr/bin/env python3
"""Compare real SerialGC layouts under a retained-data/transient-ring workload.

This models the captured ~330MiB live set; it is not Minecraft or a PS5 timing
benchmark. Preserve contents and compare collections, not machine-dependent ms.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--java-home', type=Path, required=True)
a = p.parse_args()
source = r'''
public class ClientGcLayout {
 static byte[][] retained = new byte[330][];
 static byte[][] ring = new byte[12][];
 public static void main(String[] args) {
  for(int i=0;i<retained.length;i++) {
   retained[i]=new byte[1024*1024];
   retained[i][0]=(byte)i;retained[i][retained[i].length-1]=(byte)(i+1);
  }
  System.gc(); // Deliberate common setup; excluded from pressure GC counts.
  for(int i=0;i<512;i++) {
   ring[i%ring.length]=new byte[4*1024*1024];
   ring[i%ring.length][0]=(byte)i;
  }
  for(int i=0;i<retained.length;i++)
   if(retained[i][0]!=(byte)i || retained[i][retained[i].length-1]!=(byte)(i+1))
    throw new AssertionError("retained data changed");
  for(int i=0;i<ring.length;i++) {
   int last=511-((511-i)%ring.length);
   if(ring[i][0]!=(byte)last)throw new AssertionError("ring data changed");
  }
  System.out.println("PASS retained330MiB +48MiB live ring +2GiB transient churn; contents preserved");
 }
}
'''
with tempfile.TemporaryDirectory(prefix='client-gc-layout-') as folder:
    w = Path(folder)
    (w/'ClientGcLayout.java').write_text(source)
    subprocess.run([str(a.java_home/'bin/javac'), '--release', '25', '-d', str(w), str(w/'ClientGcLayout.java')], check=True)
    results = {}
    for name, extra in [('067', []), ('068', ['-XX:NewRatio=7'])]:
        log = w/(name+'.log')
        command = [str(a.java_home/'bin/java'), '-Xmixed', '-XX:TieredStopAtLevel=1',
                   '-XX:CICompilerCount=1', '-XX:CompileThresholdScaling=4.0',
                   '-XX:CompileCommand=MemLimit,*.*,2M', '-XX:+UseSerialGC',
                   '-XX:+UseCompactObjectHeaders', '-XX:-UseCompressedOops',
                   '-Xms16m', '-Xmx512m', *extra,
                   '-Xlog:gc*,gc+heap=debug:file='+str(log), '-cp', str(w), 'ClientGcLayout']
        r = subprocess.run(command, capture_output=True, text=True, timeout=60)
        assert r.returncode == 0 and 'contents preserved' in r.stdout, r.stdout+r.stderr
        text = log.read_text()
        pressure = re.findall(r'Pause Full \(Allocation Failure\).*? ([\d.]+)ms', text)
        young = re.findall(r'Pause Young \(Allocation Failure\).*? ([\d.]+)ms', text)
        old = [int(n) for n in re.findall(r'Tenured\s+total (\d+)K', text)]
        results[name] = {'full_allocation_pauses': len(pressure), 'young_pauses': len(young),
                         'maximum_old_capacity_kib': max(old), 'contents_preserved': True}
        (ROOT/'build'/('client068-layout-'+name+'.log')).write_text(text)
    assert results['068']['maximum_old_capacity_kib'] > results['067']['maximum_old_capacity_kib']
    assert results['068']['full_allocation_pauses'] < results['067']['full_allocation_pauses'], results
    (ROOT/'build/client068-gc-layout.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))
print('PASS actual SerialGC layout comparison; host occupancy model only, not PS5 frame-time acceptance')
