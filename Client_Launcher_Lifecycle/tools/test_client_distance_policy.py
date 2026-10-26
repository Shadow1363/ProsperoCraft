#!/usr/bin/env python3
"""Exercise the actual one-time chunk-distance configuration migration."""
from pathlib import Path
import argparse,json,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args()
cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in json.loads((ROOT/'client/26.3.lock.json').read_text())['artifacts'])
source=r'''
import java.nio.file.*;
public class DistancePolicyCheck {
 static void check(Path root,String name,String original,String expected,boolean backup)throws Exception {
  Path w=root.resolve(name);Files.createDirectories(w);Files.writeString(w.resolve("options.txt"),original);
  ClientStartup25.prepareDistances(w);
  if(!Files.readString(w.resolve("options.txt")).equals(expected))throw new AssertionError(name+":"+Files.readString(w.resolve("options.txt")));
  if(Files.exists(w.resolve("options.before-distances070.txt"))!=backup)throw new AssertionError("backup presence:"+name);
  if(backup&&!Files.readString(w.resolve("options.before-distances070.txt")).equals(original))throw new AssertionError("backup bytes:"+name);
  Files.writeString(w.resolve("options.txt"),"renderDistance:20\nsimulationDistance:12\n");
  ClientStartup25.prepareDistances(w);
  if(!Files.readString(w.resolve("options.txt")).equals("renderDistance:20\nsimulationDistance:12\n"))throw new AssertionError("later choice lost");
 }
 public static void main(String[]args)throws Exception {
  Path root=Path.of(args[0]);
  check(root,"large","renderDistance:16\nsimulationDistance:12\nsoundCategory_master:0.5\n","renderDistance:6\nsimulationDistance:5\nsoundCategory_master:0.5\n",true);
  check(root,"crlf","renderDistance:16\r\nsimulationDistance:12\r\nfoo:bar\r\n","renderDistance:6\r\nsimulationDistance:5\r\nfoo:bar\r\n",true);
  check(root,"smaller","renderDistance:2\nsimulationDistance:3\n","renderDistance:2\nsimulationDistance:3\n",false);
  check(root,"missing","foo:bar","foo:bar\nrenderDistance:6\nsimulationDistance:5\n",true);
  check(root,"invalid","renderDistance:invalid\nsimulationDistance:-1\n","renderDistance:invalid\nsimulationDistance:-1\n",false);
  check(root,"huge","renderDistance:9999999999999999999\nsimulationDistance:5","renderDistance:6\nsimulationDistance:5",true);
  System.out.println("PASS actual distance migration:16/12->6/5, exact backup, CRLF and other bytes, lower values, missing keys, invalid keys, large integer, once-only later edits preserved");
 }
}
'''
with tempfile.TemporaryDirectory(prefix='client-distance-policy-')as folder:
 w=Path(folder);(w/'DistancePolicyCheck.java').write_text(source)
 subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/startup/ClientStartup25.java'),*[str(p)for p in sorted((ROOT/'client/launcher/java').glob('*.java'))],str(ROOT.parents[2]/'java25/tests/ps5probe/JitWarmup25.java'),str(w/'DistancePolicyCheck.java')],check=True)
 subprocess.run([str(a.java_home/'bin/java'),'-cp',str(w)+':'+cp,'DistancePolicyCheck',str(w/'cases')],check=True)
