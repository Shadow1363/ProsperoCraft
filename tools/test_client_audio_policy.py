#!/usr/bin/env python3
"""Exercise actual one-time audio options migration without game hooks."""
from pathlib import Path
import argparse,json,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--java-home',type=Path,required=True);a=p.parse_args()
lock=json.loads((ROOT/'client/26.3.lock.json').read_text());cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in lock['artifacts'])
source=r'''import java.nio.file.*;
public class AudioPolicyCheck{
 public static void main(String[]args)throws Exception{
  Path root=Path.of(args[0]);Files.createDirectories(root);
  String old="soundCategory_master:0.0\r\nsoundCategory_music:0.0\r\nsoundDevice:\"No Output\"\r\ncustom:keep:this\r\n";
  Files.writeString(root.resolve("options.txt"),old);ClientStartup25.prepareAudio(root);
  String expected=old.replace("master:0.0","master:0.5").replace("music:0.0","music:0.25").replace("soundDevice:\"No Output\"","soundDevice:\"\"");
  if(!Files.readString(root.resolve("options.txt")).equals(expected))throw new AssertionError("unexpected migration");
  if(!Files.readString(root.resolve("options.before-audio067.txt")).equals(old))throw new AssertionError("backup not exact");
  Files.writeString(root.resolve("options.txt"),"soundCategory_master:0.0\nsoundCategory_music:0.0\n");
  ClientStartup25.prepareAudio(root);if(!Files.readString(root.resolve("options.txt")).contains("master:0.0"))throw new AssertionError("later mute overridden");
  Path custom=root.resolve("custom");Files.createDirectories(custom);String text="soundCategory_master:0.8\nsoundCategory_music:0.6\nsoundDevice:\"Chosen Device\"\n";Files.writeString(custom.resolve("options.txt"),text);ClientStartup25.prepareAudio(custom);
  if(!Files.readString(custom.resolve("options.txt")).equals(text)||Files.exists(custom.resolve("options.before-audio067.txt")))throw new AssertionError("custom settings lost");
  Path fresh=root.resolve("fresh");ClientStartup25.prepareWork(fresh);ClientStartup25.prepareAudio(fresh);if(!Files.readString(fresh.resolve("options.txt")).contains("master:0.5"))throw new AssertionError("new profile muted");
  System.out.println("PASS actual audio policy:legacy0master/music unmute once,obsoleteNullDevice reset,CRLF/custom values preserved,exactbackup,lateruser mute preserved,newprofile audibility defaults;no game invocation");
 }
}'''
with tempfile.TemporaryDirectory(prefix='client-audio-policy-')as folder:
 w=Path(folder);(w/'AudioPolicyCheck.java').write_text(source)
 subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/startup/ClientStartup25.java'),str(ROOT.parents[2]/'java25/tests/ps5probe/JitWarmup25.java'),str(w/'AudioPolicyCheck.java')],check=True)
 subprocess.run([str(a.java_home/'bin/java'),'-cp',str(w)+':'+cp,'AudioPolicyCheck',str(w/'profile')],check=True)
