#!/usr/bin/env python3
"""Test actual startup option migration and original Minecraft enum codec."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args()
lock=json.loads((ROOT/'client/26.3.lock.json').read_text())
cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in lock['artifacts'])
source=r'''
import java.nio.file.*;
import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import net.minecraft.client.InactivityFpsLimit;
public class MenuPolicyCheck {
 public static void main(String[]args)throws Exception {
  Path root=Path.of(args[0]);
  String original="musicVolume:0.4\r\ninactivityFpsLimit:\"afk\"\r\ncustom_option:leave:exactly\r\n";
  Files.createDirectories(root);Files.writeString(root.resolve("options.txt"),original);
  ClientStartup25.prepareWork(root);
  String changed=Files.readString(root.resolve("options.txt"));
  if(!changed.equals(original.replace("\"afk\"","\"minimized\"")))throw new AssertionError("unrelated bytes changed");
  if(!Files.readString(root.resolve("options.before-menu063.txt")).equals(original))throw new AssertionError("backup not exact");
  ClientStartup25.prepareWork(root);
  if(!Files.readString(root.resolve("options.txt")).equals(changed))throw new AssertionError("not idempotent");
  String value=changed.lines().filter(s->s.startsWith("inactivityFpsLimit:")).findFirst().orElseThrow().split(":",2)[1];
  if(InactivityFpsLimit.CODEC.parse(JsonOps.INSTANCE,JsonParser.parseString(value)).getOrThrow()!=InactivityFpsLimit.MINIMIZED)throw new AssertionError("original Minecraft codec rejected setting");
  if(InactivityFpsLimit.CODEC.parse(JsonOps.INSTANCE,JsonParser.parseString("\"afk\"")).getOrThrow()!=InactivityFpsLimit.AFK)throw new AssertionError();
  Path fresh=root.resolve("fresh");ClientStartup25.prepareWork(fresh);
  if(!Files.readString(fresh.resolve("options.txt")).contains("inactivityFpsLimit:\"minimized\""))throw new AssertionError("fresh policy missing");
  if(Files.exists(fresh.resolve("options.before-menu063.txt")))throw new AssertionError("unnecessary backup");
  System.out.println("PASS actual option migration:only AFK setting replaced,CRLF/custom options preserved,exact backup,idempotence,new profile;original unmodified Minecraft enum CODEC accepts minimized. No Main/game hooks.");
 }
}
'''
with tempfile.TemporaryDirectory(prefix='mc-menu-policy-')as folder:
    w=Path(folder);(w/'MenuPolicyCheck.java').write_text(source)
    subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(ROOT/'client/startup/ClientStartup25.java'),str(w/'MenuPolicyCheck.java')],check=True)
    subprocess.run([str(a.java_home/'bin/java'),'-Xint','--enable-native-access=ALL-UNNAMED','-cp',str(w)+':'+cp,'MenuPolicyCheck',str(w/'profile')],check=True)
