#!/usr/bin/env python3
"""Check launch policy/workdir and exercise the actual unchanged Main on host."""
from pathlib import Path
import argparse,subprocess,json,tempfile,hashlib
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args();lock=json.loads((ROOT/'client/26.3.lock.json').read_text())
cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in lock['artifacts'])
out=ROOT/'build/startup-host-030';out.mkdir(exist_ok=True)
(out/'StartupPolicy.java').write_text('''import java.nio.file.*;import java.util.*;public class StartupPolicy{public static void main(String[]a)throws Exception{Path w=Path.of(a[0]);ClientStartup25.prepareWork(w);String text=Files.readString(w.resolve("options.txt"));if(!text.contains("soundCategory_music:0.0"))throw new AssertionError();Files.writeString(w.resolve("options.txt"),"existing");ClientStartup25.prepareWork(w);if(!Files.readString(w.resolve("options.txt")).equals("existing"))throw new AssertionError("existing options overwritten");String[]args=ClientStartup25.launchArguments(w,Path.of(a[1]));List<String>l=Arrays.asList(args);for(String flag:new String[]{"--demo","--disableMultiplayer","--disableChat","--graphicsBackend","vulkan","--accessToken","0"})if(!l.contains(flag))throw new AssertionError(flag);if(l.contains("--quickPlayMultiplayer"))throw new AssertionError();System.out.println("PASS original-client launch policy:demo/no credentials/multiplayer disabled,writable workdir,existing options preserved;no game invocation in policy check");}}''')
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(out),str(ROOT/'client/startup/ClientStartup25.java'),str(out/'StartupPolicy.java')],check=True)
with tempfile.TemporaryDirectory(prefix='mc-startup-policy-')as temp:
 subprocess.run([str(a.java_home/'bin/java'),'-cp',str(out)+':'+cp,'StartupPolicy',str(Path(temp)/'work'),str(ROOT/'build/client-assets')],check=True)
# Run original upstream Main in a separate process so its System.exit is real.
with tempfile.TemporaryDirectory(prefix='mc-original-main-')as temp:
 args=['--demo','--disableMultiplayer','--disableChat','--username','PS5Probe','--uuid','00000000-0000-3000-8000-000000000000','--accessToken','0','--version','26.3','--versionType','release','--gameDir',temp,'--assetsDir',str(ROOT/'build/client-assets'),'--assetIndex','34','--graphicsBackend','vulkan','--width','1280','--height','720']
 command=[str(a.java_home/'bin/java'),'-Xint','-Xmx128m','--enable-native-access=ALL-UNNAMED','-cp',cp,'net.minecraft.client.main.Main',*args]
 try:result=subprocess.run(command,cwd=temp,capture_output=True,text=True,timeout=60)
 except subprocess.TimeoutExpired as error:raise RuntimeError('Original host startup exceeded60s;inspect rather than claim pass')from error
 text=result.stdout+result.stderr;(out/'original-main.log').write_text(text)
 assert result.returncode!=0,'Unexpected host menu/run result;review explicitly'
 assert 'NativeLibrariesBootstrap' in text and ('UnsatisfiedLinkError' in text or 'Failed to locate' in text or 'Failed to load' in text),text[-4000:]
 assert 'Missing required option' not in text and 'not a valid value' not in text,text[-4000:]
 print('PASS actual unmodified host Main executed and reached native-library bootstrap;expected unprovided host-native failure captured,exit',result.returncode,';no host menu or PS5 startup pass')
client=ROOT/'.tools/client/client-26.3.jar';assert hashlib.sha256(client.read_bytes()).hexdigest()==lock['artifacts'][0]['sha256'];print('PASS original client JAR unchanged')
