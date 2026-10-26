#!/usr/bin/env python3
"""Check launch policy/workdir and exercise the actual unchanged Main on host."""
from pathlib import Path
import argparse,subprocess,json,tempfile,hashlib,os
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);a=p.parse_args();lock=json.loads((ROOT/'client/26.3.lock.json').read_text())
cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in lock['artifacts'])
out=ROOT/'build/startup-host-060';out.mkdir(exist_ok=True)
(out/'StartupPolicy.java').write_text('''import java.nio.file.*;import java.util.*;public class StartupPolicy{public static void main(String[]a)throws Exception{Path w=Path.of(a[0]);ClientStartup25.prepareWork(w);String text=Files.readString(w.resolve("options.txt"));if(!text.contains("soundCategory_music:0.0"))throw new AssertionError();Files.writeString(w.resolve("options.txt"),"existing");ClientStartup25.prepareWork(w);if(!Files.readString(w.resolve("options.txt")).equals("existing"))throw new AssertionError("existing options overwritten");String[]args=ClientStartup25.launchArguments(w,Path.of(a[1]));List<String>l=Arrays.asList(args);for(String flag:new String[]{"--demo","--disableMultiplayer","--disableChat","--graphicsBackend","vulkan","--accessToken","0"})if(!l.contains(flag))throw new AssertionError(flag);if(l.contains("--quickPlayMultiplayer"))throw new AssertionError();System.out.println("PASS original-client launch policy:demo/no credentials/multiplayer disabled,writable workdir,existing options preserved;no game invocation in policy check");}}''')
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(out),str(ROOT/'client/startup/ClientStartup25.java'),str(out/'StartupPolicy.java')],check=True)
with tempfile.TemporaryDirectory(prefix='mc-startup-policy-')as temp:
 subprocess.run([str(a.java_home/'bin/java'),'-cp',str(out)+':'+cp,'StartupPolicy',str(Path(temp)/'work'),str(ROOT/'build/client-assets')],check=True)
# Exercise the actual observer with live blocked/deep-stack threads, bounds and stop.
(out/'StartupObserverCheck.java').write_text(r'''import java.io.*;import java.util.*;import java.util.concurrent.*;
public class StartupObserverCheck{
 static void deep(int n,CountDownLatch ready,CountDownLatch release)throws Exception{if(n>0)deep(n-1,ready,release);else{ready.countDown();release.await();}}
 static void joinObserver()throws Exception{for(Thread t:Thread.getAllStackTraces().keySet())if(t.getName().equals("PS5 startup observer")){if(!t.isDaemon())throw new AssertionError("not daemon");t.join(5000);if(t.isAlive())throw new AssertionError("unbounded observer");}}
 public static void main(String[]a)throws Exception{
  CountDownLatch ready=new CountDownLatch(34),release=new CountDownLatch(1);
  for(int i=0;i<34;i++){Thread worker=new Thread(null,()->{try{deep(80,ready,release);}catch(Exception e){throw new RuntimeException(e);}},"Worker-Main-test"+i,256*1024,false);worker.setDaemon(true);worker.start();}
  if(!ready.await(5,TimeUnit.SECONDS))throw new AssertionError("workers");
  ByteArrayOutputStream bytes=new ByteArrayOutputStream();PrintStream console=new PrintStream(bytes,true,java.nio.charset.StandardCharsets.UTF_8);
  ClientStartup25.StartupObserver observer=new ClientStartup25.StartupObserver(console,2,10);observer.start();joinObserver();observer.close();
  ClientStartup25.StartupObserver schedule=new ClientStartup25.StartupObserver(console,240,1000,5000);
  if(schedule.intervalAfter(1)!=1000||schedule.intervalAfter(89)!=1000||schedule.intervalAfter(90)!=250||schedule.intervalAfter(169)!=250||schedule.intervalAfter(170)!=1000||schedule.intervalAfter(179)!=1000||schedule.intervalAfter(180)!=5000||schedule.intervalAfter(239)!=5000)throw new AssertionError("late schedule");schedule.close();
  String text=bytes.toString(java.nio.charset.StandardCharsets.UTF_8);
  if(!text.contains("PS5 native observer unavailable;Java snapshots continue:"))throw new AssertionError("host absent-native fallback");
  if(text.split("PS5 STARTUP SNAPSHOT ",-1).length!=3||!text.contains("MAIN")||!text.contains("StartupObserverCheck.main")||!text.contains("deep(")||!text.contains("[frame limit64]")||!text.contains("[thread limit32]")||!text.contains("heapUsed=")||!text.contains("elapsedMs=")||!text.contains("observer completed"))throw new AssertionError(text);
  bytes.reset();observer=new ClientStartup25.StartupObserver(console,90,1000);observer.start();
  long deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(5);
  while(!bytes.toString().contains("PS5 END SNAPSHOT 1")&&System.nanoTime()<deadline)Thread.sleep(5);
  if(!bytes.toString().contains("PS5 END SNAPSHOT 1"))throw new AssertionError("no first snapshot");observer.close();joinObserver();int size=bytes.size();Thread.sleep(20);if(bytes.size()!=size||bytes.toString().contains("SNAPSHOT 2"))throw new AssertionError("writes after close");
  var languageFrame=new StackTraceElement("net.minecraft.locale.Language","loadFromJson","Language.java",85);
  var reloadFrame=new StackTraceElement("net.minecraft.client.resources.language.LanguageManager","onResourceManagerReload","LanguageManager.java",75);
  var loopFrame=new StackTraceElement("net.minecraft.client.Minecraft","runTick","Minecraft.java",1240);
  if(!ClientStartup25.StartupObserver.isLanguageApply(new StackTraceElement[]{languageFrame,reloadFrame,loopFrame})||ClientStartup25.StartupObserver.isLanguageApply(new StackTraceElement[]{languageFrame})||ClientStartup25.StartupObserver.isLanguageApply(new StackTraceElement[]{languageFrame,reloadFrame})||ClientStartup25.StartupObserver.isLanguageApply(null))throw new AssertionError("transition trigger");
  bytes.reset();ClientStartup25.StartupObserver burst=new ClientStartup25.StartupObserver(console,1,1);
  java.util.concurrent.atomic.AtomicReference<Throwable> burstError=new java.util.concurrent.atomic.AtomicReference<>();
  Thread sampler=new Thread(()->{try{burst.captureMainTransitions(3,1);}catch(Throwable e){burstError.set(e);}},"host transition sampler");sampler.setDaemon(true);sampler.start();sampler.join(5000);
  if(sampler.isAlive()||burstError.get()!=null)throw new AssertionError("burst lifecycle",burstError.get());
  String captured=bytes.toString(java.nio.charset.StandardCharsets.UTF_8);
  if(captured.split("PS5 END MAIN TRANSITION ",-1).length!=4||!captured.contains("StartupObserverCheck.main")||!captured.contains("PS5 MAIN TRANSITION COMPLETE")||!captured.contains("heapUsed=")||!captured.contains("elapsedMs="))throw new AssertionError(captured);burst.close();
  bytes.reset();ClientStartup25.StartupObserver stoppedBurst=new ClientStartup25.StartupObserver(console,1,1);
  sampler=new Thread(()->{try{stoppedBurst.captureMainTransitions(500,10);}catch(Throwable e){burstError.set(e);}},"host stopped transition sampler");sampler.setDaemon(true);sampler.start();
  deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(5);while(!bytes.toString().contains("PS5 END MAIN TRANSITION 1")&&System.nanoTime()<deadline)Thread.sleep(1);
  if(!bytes.toString().contains("PS5 END MAIN TRANSITION 1"))throw new AssertionError("no transition");stoppedBurst.close();sampler.join(5000);size=bytes.size();Thread.sleep(20);
  if(sampler.isAlive()||bytes.size()!=size||bytes.toString().contains("TRANSITION COMPLETE"))throw new AssertionError("burst writes after close");
  System.out.println("PASS actual owner-only transition burst:precise language trigger,finite samples/live owner stacks,elapsed/heap records,close without later writes;host only");
  release.countDown();System.out.println("PASS actual startup observer:live Main/blocked resource stacks,heap/elapsed time,32thread/64frame bounds,finite sampling,dense and late cadence boundaries,absent-native fallback,daemon and interrupted close without later writes;host only");
 }
}''')
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',str(out)+':'+cp,'-d',str(out),str(out/'StartupObserverCheck.java')],check=True)
subprocess.run([str(a.java_home/'bin/java'),'-Xint','-cp',str(out)+':'+cp,'StartupObserverCheck'],check=True,timeout=20)
# Exercise the exact target GC/safepoint selection through the actual host JVM.
# This verifies syntax/content and bounded rollover,not PS5 collector correctness.
import re
flag=re.search(r'"(-Xlog:gc\*=debug,safepoint\*=debug,class\+load=info,class\+init=info:[^"]+)"',(ROOT/'client/startup/bootstrap.cpp').read_text()).group(1)
(out/'StartupGcCheck.java').write_text('public class StartupGcCheck{public static void main(String[]a){byte[][]keep=new byte[32][];for(int i=0;i<512;i++)keep[i%32]=new byte[1024*1024];System.gc();System.out.println("GC fixture complete");}}')
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-d',str(out),str(out/'StartupGcCheck.java')],check=True)
with tempfile.TemporaryDirectory(prefix='mc-startup-gc-')as temp:
 for rotate in (False,True):
  log=Path(temp)/('rolled.log'if rotate else 'exact.log')
  option=flag.replace('/download0/java25-gc.log',str(log))
  if rotate:option=option.replace('filesize=4M','filesize=1K')
  result=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xms16m','-Xmx256m','-XX:+UseSerialGC',option,'-cp',str(out),'StartupGcCheck'],capture_output=True,text=True,timeout=30)
  result.check_returncode();assert 'GC fixture complete'in result.stdout
  if rotate:
   assert log.with_name(log.name+'.0').is_file(),'no rolled log'
   assert set(p.name for p in Path(temp).glob('rolled.log*'))=={'rolled.log','rolled.log.0'}
  else:
   text=log.read_text();assert all(x in text for x in ('[gc,start','[gc,heap','[gc,phases','[safepoint','[class,load','[class,init','Pause Full (System.gc())')),text[-4000:]
print('PASS exact startup GC/safepoint/class-load/class-init JVM logging option,actual SerialGC phases/heap/full pause and one-file rollover;host only')
# Exercise the same native allocation preflight with actual upstream JNI on host.
(out/'StartupAllocation.java').write_text('public class StartupAllocation{public static void main(String[]args){org.lwjgl.system.Configuration.MEMORY_ALLOCATOR.set("system");System.out.println(ClientStartup25.verifyNativeAllocation());}}')
subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',str(out)+':'+cp,'-d',str(out),str(out/'StartupAllocation.java')],check=True)
result=subprocess.run([str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','--enable-native-access=ALL-UNNAMED','-Dorg.lwjgl.librarypath='+str(ROOT/'build/client-ports/lwjgl-native/host'),'-cp',str(out)+':'+cp,'StartupAllocation'],capture_output=True,text=True,timeout=30,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'))
(out/'allocation.log').write_text(result.stdout+result.stderr);result.check_returncode();assert 'PASS real LWJGL system allocator:3x4MiB' in result.stdout
assert not any(marker in result.stdout+result.stderr for marker in ['WARNING in native method','FATAL ERROR in native method','runtime error:'])
print(result.stdout.strip());print('Host uses real upstream JNI and host libc;PS5 scoped heap mapping checked separately,console pending')
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
