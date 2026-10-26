#!/usr/bin/env python3
"""Verify read-only options diagnostics and absence of active distance migration."""
from pathlib import Path
import argparse,json,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args()
cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in json.loads((ROOT/'client/26.3.lock.json').read_text())['artifacts'])
source=r'''
import java.nio.file.*;
public class ConfigurationCheck {
 public static void main(String[]args)throws Exception {
  System.clearProperty("ps5.startupObserver");if(ClientStartup25.startupObserverEnabled())throw new AssertionError("observer enabled by default");
  System.setProperty("ps5.startupObserver","true");if(!ClientStartup25.startupObserverEnabled())throw new AssertionError("observer override unavailable");System.clearProperty("ps5.startupObserver");
  Path w=Path.of(args[0]);Files.createDirectories(w);
  String text="version:123\r\ngraphicsPreset:\"fancy\"\r\nrenderDistance:16\r\nsimulationDistance:12\r\nother:private-value\r\n";
  Files.writeString(w.resolve("options.txt"),text);
  String report=ClientStartup25.configurationSummary(w);
  for(String expected:new String[]{"PS5_OPTIONS_BEFORE_MAIN","version=123","graphicsPreset=\"fancy\"","renderDistance=16","simulationDistance=12","migration070=false","distancePolicy=preserve-existing/no-new-cap"})if(!report.contains(expected))throw new AssertionError(expected);
  if(report.contains("private-value")||!Files.readString(w.resolve("options.txt")).equals(text)||Files.list(w).count()!=1)throw new AssertionError("mutation or excess field");
  Files.writeString(w.resolve("options.txt"),"renderDistance:"+"9".repeat(200)+"\n");
  Files.writeString(w.resolve("distances-enabled-070.txt"),"previous marker");
  report=ClientStartup25.configurationSummary(w);
  if(!report.contains("simulationDistance=<missing>")||!report.contains("migration070=true")||report.contains("9".repeat(65)))throw new AssertionError("bounds/missing/marker");
  System.out.println("PASS read-only selected options summary:high settings preserved,CRLF,private fields excluded,64char bounds,missing/070marker explicit");
 }
}
'''
with tempfile.TemporaryDirectory(prefix='client-configuration-')as folder:
 w=Path(folder);(w/'ConfigurationCheck.java').write_text(source)
 subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/startup/ClientStartup25.java'),str(ROOT.parents[2]/'java25/tests/ps5probe/JitWarmup25.java'),str(w/'ConfigurationCheck.java')],check=True)
 subprocess.run([str(a.java_home/'bin/java'),'-cp',str(w)+':'+cp,'ConfigurationCheck',str(w/'cases')],check=True)
 code=subprocess.check_output([str(a.java_home/'bin/javap'),'-classpath',str(w),'-c','ClientStartup25'],text=True)
 main=code.split('public static void main(java.lang.String[])',1)[1]
 assert 'Method prepareDistances:' not in main and 'Method configurationSummary:' in main
print('PASS actual Main bytecode logs selected configuration without invoking the070distance migration')
