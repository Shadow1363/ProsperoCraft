import java.io.*;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.UUID;
import org.lwjgl.system.Configuration;
import org.lwjgl.system.MemoryUtil;

/** Invokes the original client entry point; no game class replacement/hooks. */
public final class ClientStartup25 {
 public static native void checkpoint(String text);
 public static native void nativeSnapshot(long elapsedMillis,int phase);
 private static void stage(String text){checkpoint("MC Startup074: "+text);}
 public static String[] launchArguments(Path work,Path assets){
  String name="PS5Probe",uuid=UUID.nameUUIDFromBytes(("OfflinePlayer:"+name).getBytes(StandardCharsets.UTF_8)).toString();
  return new String[]{"--demo","--disableMultiplayer","--disableChat","--username",name,"--uuid",uuid,"--accessToken","0","--version","26.3","--versionType","release","--gameDir",work.toString(),"--assetsDir",assets.toString(),"--assetIndex","34","--graphicsBackend","vulkan","--width","1280","--height","720"};
 }
 public static void prepareWork(Path work)throws IOException{
  Files.createDirectories(work);Files.createDirectories(work.resolve("native-cache"));Files.createDirectories(work.resolve("resourcepacks"));
  Path options=work.resolve("options.txt");
  if(!Files.exists(options))Files.writeString(options,"soundCategory_master:0.0\nsoundCategory_music:0.0\ninactivityFpsLimit:\"minimized\"\n",StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW);
  else {
   String original=Files.readString(options,StandardCharsets.UTF_8);
   String desired=original.replaceAll("(?m)^inactivityFpsLimit:[^\\r\\n]*","inactivityFpsLimit:\"minimized\"");
   if(desired.equals(original)&&!original.lines().anyMatch(line->line.startsWith("inactivityFpsLimit:")))
    desired=original+(original.isEmpty()||original.endsWith("\n")?"":"\n")+"inactivityFpsLimit:\"minimized\"\n";
   if(!desired.equals(original)) {
    Path backup=work.resolve("options.before-menu063.txt");
    if(!Files.exists(backup))Files.copy(options,backup);
    Path temporary=work.resolve("options.menu063.tmp");
    Files.writeString(temporary,desired,StandardCharsets.UTF_8);
    Files.move(temporary,options,StandardCopyOption.REPLACE_EXISTING);
   }
  }
 }
 public static boolean startupObserverEnabled(){return Boolean.getBoolean("ps5.startupObserver");}
 public static String configurationSummary(Path work)throws IOException{
  StringBuilder result=new StringBuilder("PS5_OPTIONS_BEFORE_MAIN");
  String text=Files.readString(work.resolve("options.txt"),StandardCharsets.UTF_8);
  for(String key:new String[]{"version","graphicsPreset","renderDistance","simulationDistance"}){
   String value=text.lines().filter(line->line.startsWith(key+":")).map(line->line.substring(key.length()+1)).findFirst().orElse("<missing>");
   result.append(" ").append(key).append("=").append(value.substring(0,Math.min(value.length(),64)));
  }
  result.append(" migration070=").append(Files.exists(work.resolve("distances-enabled-070.txt")));
  result.append(" distancePolicy=preserve-existing/no-new-cap");return result.toString();
 }
 public static void prepareDistances(Path work)throws IOException{
  Path marker=work.resolve("distances-enabled-070.txt");if(Files.exists(marker))return;
  Path options=work.resolve("options.txt");String original=Files.readString(options,StandardCharsets.UTF_8),desired=original;
  for(String key:new String[]{"renderDistance","simulationDistance"}){
   int limit=key.equals("renderDistance")?6:5;
   var pattern=java.util.regex.Pattern.compile("(?m)^"+key+":([0-9]+)(?=\r?$)");
   var matcher=pattern.matcher(desired);StringBuffer changed=new StringBuffer();boolean found=false;
   while(matcher.find()){
    found=true;String value=matcher.group(1);boolean above;
    try{above=Integer.parseInt(value)>limit;}catch(NumberFormatException error){above=true;}
    matcher.appendReplacement(changed,java.util.regex.Matcher.quoteReplacement(above?key+":"+limit:matcher.group()));
   }
   matcher.appendTail(changed);desired=changed.toString();
   if(!found && !desired.lines().anyMatch(line->line.startsWith(key+":")))desired+=(desired.endsWith("\n")?"":"\n")+key+":"+limit+"\n";
  }
  if(!desired.equals(original)){
   Path backup=work.resolve("options.before-distances070.txt");if(!Files.exists(backup))Files.copy(options,backup);
   Path temporary=work.resolve("options.distances070.tmp");Files.writeString(temporary,desired,StandardCharsets.UTF_8);
   Files.move(temporary,options,StandardCopyOption.REPLACE_EXISTING);
  }
  Files.writeString(marker,"070:initial view<=6/simulation<=5;backup options.before-distances070.txt. Later user edits preserved.\n",StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW);
 }
 public static void prepareAudio(Path work)throws IOException{
  Path marker=work.resolve("audio-enabled-067.txt");if(Files.exists(marker))return;
  Path options=work.resolve("options.txt");String original=Files.readString(options,StandardCharsets.UTF_8);
  String desired=original.replaceAll("(?m)^soundCategory_master:0(?:\\.0+)?$","soundCategory_master:0.5")
   .replaceAll("(?m)^soundCategory_music:0(?:\\.0+)?$","soundCategory_music:0.25");
  if(!original.lines().anyMatch(line->line.startsWith("soundCategory_master:")))desired+=(desired.endsWith("\n")?"":"\n")+"soundCategory_master:0.5\n";
  if(!original.lines().anyMatch(line->line.startsWith("soundCategory_music:")))desired+=(desired.endsWith("\n")?"":"\n")+"soundCategory_music:0.25\n";
  // Remove only the obsolete project null-backend device selection,if persisted.
  desired=desired.replaceAll("(?m)^soundDevice:\"No Output\"$","soundDevice:\"\"");
  if(!desired.equals(original)){
   Path backup=work.resolve("options.before-audio067.txt");if(!Files.exists(backup))Files.copy(options,backup);
   Path temporary=work.resolve("options.audio067.tmp");Files.writeString(temporary,desired,StandardCharsets.UTF_8);
   Files.move(temporary,options,StandardCopyOption.REPLACE_EXISTING);
  }
  Files.writeString(marker,"AudioOut speaker candidate067:legacy zero master/music unmuted once;backup options.before-audio067.txt. Later user volume changes preserved.\n",StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW);
 }
 /** Real LWJGL system allocator,including paired grow/free and alignment. */
 public static String verifyNativeAllocation(){
  var allocator=MemoryUtil.getAllocator();long[] pointers=new long[3];long aligned=0,zeroed=0;int bytes=4*1024*1024;
  try{
   for(int i=0;i<pointers.length;i++){
    pointers[i]=allocator.malloc(bytes);if(pointers[i]==0)throw new OutOfMemoryError("LWJGL native preflight4MiB allocation"+i);
    MemoryUtil.memSet(pointers[i],0x35+i,bytes);
   }
   long grown=allocator.realloc(pointers[0],bytes*2L);if(grown==0)throw new OutOfMemoryError("LWJGL native preflight grow8MiB");pointers[0]=grown;
   for(int i=0;i<pointers.length;i++)for(int offset=0;offset<bytes;offset+=4096)if(MemoryUtil.memGetByte(pointers[i]+offset)!=(byte)(0x35+i))throw new AssertionError("Native allocation/grow contents");
   if(MemoryUtil.memGetByte(grown+bytes-1)!=0x35)throw new AssertionError("Native grow tail");MemoryUtil.memSet(grown+bytes,0x6a,bytes);if(MemoryUtil.memGetByte(grown+bytes*2L-1)!=0x6a)throw new AssertionError("Native grown extent");
   zeroed=allocator.calloc(1,65536);if(zeroed==0)throw new OutOfMemoryError("Native calloc");for(int i=0;i<65536;i++)if(MemoryUtil.memGetByte(zeroed+i)!=0)throw new AssertionError("Native calloc zeroing");
   aligned=allocator.aligned_alloc(4096,bytes);if(aligned==0||(aligned&4095)!=0)throw new AssertionError("Native4096 alignment");MemoryUtil.memSet(aligned,0x5c,bytes);if(MemoryUtil.memGetByte(aligned+bytes-1)!=0x5c)throw new AssertionError("Native aligned extent");
  }finally{if(aligned!=0)allocator.aligned_free(aligned);if(zeroed!=0)allocator.free(zeroed);for(long pointer:pointers)if(pointer!=0)allocator.free(pointer);}
  return "PASS real LWJGL system allocator:3x4MiB,grow8MiB/preserved pages,new extent,calloc64KiB zeroes,4096-aligned4MiB and paired cleanup";
 }
 /** Diagnostic only: one daemon, finite sampling, no changes to game threads. */
 static final class StartupObserver implements AutoCloseable {
  private final PrintStream console;
  private final Thread owner,worker;
  private final int samples;
  private final long intervalMillis,laterIntervalMillis;
  private final long startedNanos=System.nanoTime();
  private volatile boolean running=true;
  private boolean nativeSampling=true;
  StartupObserver(PrintStream console,int samples,long intervalMillis){this(console,samples,intervalMillis,intervalMillis);}
  StartupObserver(PrintStream console,int samples,long intervalMillis,long laterIntervalMillis){
   this.console=console;this.samples=samples;this.intervalMillis=intervalMillis;this.laterIntervalMillis=laterIntervalMillis;owner=Thread.currentThread();
   worker=new Thread(null,this::run,"PS5 startup observer",256*1024,false);worker.setDaemon(true);
  }
  long intervalAfter(int sample){
   if(sample>=180)return laterIntervalMillis;
   if(sample>=90&&sample<170)return Math.max(1,intervalMillis/4);
   return intervalMillis;
  }
  static boolean isLanguageApply(StackTraceElement[] frames){
   boolean language=false,reload=false,mainLoop=false;
   if(frames!=null)for(var frame:frames){
    if(frame.getClassName().equals("net.minecraft.locale.Language")&&frame.getMethodName().equals("loadFromJson"))language=true;
    if(frame.getClassName().equals("net.minecraft.client.resources.language.LanguageManager")&&frame.getMethodName().equals("onResourceManagerReload"))reload=true;
    if(frame.getClassName().equals("net.minecraft.client.Minecraft")&&frame.getMethodName().equals("runTick"))mainLoop=true;
   }
   return language&&reload&&mainLoop;
  }
  // One bounded burst on this same daemon,triggered by an observed original
  // language-apply stack. No game calls/hooks,extra thread or native query loop.
  void captureMainTransitions(int count,long pauseMillis)throws InterruptedException{
   StackTraceElement[] previous=null;int previousSample=0;
   synchronized(console){if(running)console.println("PS5 MAIN TRANSITION BEGIN samples="+count+" intervalMs="+pauseMillis);}
   for(int sample=1;running&&sample<=count;sample++){
    var frames=owner.getStackTrace();Runtime heap=Runtime.getRuntime();
    boolean unchanged=java.util.Arrays.equals(previous,frames);
    StringBuilder text=new StringBuilder(4096);
    text.append("PS5 MAIN TRANSITION ").append(sample).append(" elapsedMs=").append((System.nanoTime()-startedNanos)/1_000_000).append(" heapUsed=").append(heap.totalMemory()-heap.freeMemory()).append(" state=").append(owner.getState()).append(" frames=").append(frames.length).append('\n');
    if(unchanged)text.append("  unchangedFromTransition=").append(previousSample).append('\n');
    else{
     for(int frame=0;frame<Math.min(frames.length,64);frame++)text.append("  at ").append(frames[frame]).append('\n');
     if(frames.length>64)text.append("  [frame limit64]\n");
     previous=frames;previousSample=sample;
    }
    text.append("PS5 END MAIN TRANSITION ").append(sample).append('\n');
    synchronized(console){if(running){console.print(text);console.flush();}}
    if(sample<count)Thread.sleep(pauseMillis);
   }
   synchronized(console){if(running)console.println("PS5 MAIN TRANSITION COMPLETE;bounded diagnostic only");}
  }
  private void observeNative(int phase){
   synchronized(console){
    if(!running||!nativeSampling)return;
    try{nativeSnapshot((System.nanoTime()-startedNanos)/1_000_000,phase);}
    catch(Throwable unavailable){nativeSampling=false;console.println("PS5 native observer unavailable;Java snapshots continue: "+unavailable);}
   }
  }
  void start(){worker.start();}
  private void run(){
   try{
    boolean transitionCaptured=false;
    for(int sample=1;running&&sample<=samples;sample++){
     observeNative(0);
     var traces=Thread.getAllStackTraces();
     var threads=new java.util.ArrayList<>(traces.keySet());
     // Always include the invoking Main/render thread before bounded other threads.
     threads.sort(java.util.Comparator.<Thread>comparingInt(t->t==owner?0:t.getName().startsWith("Worker-Main")?1:2).thenComparingLong(Thread::threadId));
     Runtime heap=Runtime.getRuntime();StringBuilder text=new StringBuilder(8192);
     text.append("PS5 STARTUP SNAPSHOT ").append(sample).append(" elapsedMs=").append((System.nanoTime()-startedNanos)/1_000_000).append(" heapUsed=").append(heap.totalMemory()-heap.freeMemory()).append(" heapCommitted=").append(heap.totalMemory()).append(" heapMax=").append(heap.maxMemory()).append(" threads=").append(threads.size()).append('\n');
     int count=0;
     for(Thread thread:threads){
      if(thread==worker)continue;
      if(count++==32){text.append("  [thread limit32]\n");break;}
      text.append("THREAD ").append(thread.threadId()).append(' ').append(thread.getName()).append(" state=").append(thread.getState()).append(thread==owner?" MAIN":"").append('\n');
      StackTraceElement[] frames=traces.get(thread);
      for(int frame=0;frame<Math.min(frames.length,64);frame++)text.append("  at ").append(frames[frame]).append('\n');
      if(frames.length>64)text.append("  [frame limit64]\n");
     }
     text.append("PS5 END SNAPSHOT ").append(sample).append('\n');
     synchronized(console){if(running){console.print(text);console.flush();}}
     observeNative(1);
     if(!transitionCaptured&&isLanguageApply(traces.get(owner))){transitionCaptured=true;captureMainTransitions(500,10);}
     if(sample<samples)Thread.sleep(intervalAfter(sample));
    }
   }catch(InterruptedException stopped){Thread.currentThread().interrupt();}
   catch(Throwable failure){synchronized(console){if(running)console.println("PS5 startup observer stopped: "+failure);}}
   finally{synchronized(console){if(running)console.println("PS5 startup observer completed;bounded diagnostic only");}running=false;}
  }
  public void close(){synchronized(console){running=false;}worker.interrupt();}
 }
 public static void main(String[] args)throws Throwable{
  Path work=Path.of("/download0/mc-client"),assets=Path.of("/app0/assets/java25/game-assets");prepareWork(work);prepareAudio(work);
  if(!Files.isRegularFile(assets.resolve("indexes/34.json")))throw new IOException("Packaged original asset index missing");
  PrintStream previousOut=System.out,previousErr=System.err;
  PrintStream console=new PrintStream(new FileOutputStream(Path.of("/download0/java25-exceptions.log").toFile(),false),true,StandardCharsets.UTF_8);
  System.setOut(console);System.setErr(console);
  StartupObserver observer=null;
  try{
   console.println(configurationSummary(work));
   System.setProperty("user.dir",work.toString());System.setProperty("user.home",work.toString());System.setProperty("java.io.tmpdir",work.resolve("native-cache").toString());
   for(String key:new String[]{"jna.tmpdir","io.netty.native.workdir"})System.setProperty(key,work.resolve("native-cache").toString());
   System.setProperty("jna.nosys","true");
   Configuration.OPENGL_CONTEXT_API.set("OSMesa");Configuration.OPENGL_OSMESA_LIBRARY_NAME.set(System.mapLibraryName("ps5clientgl"));
   Configuration.SPVC_LIBRARY_NAME.set(System.mapLibraryName("ps5spvc"));
   Configuration.MEMORY_ALLOCATOR.set("system");Configuration.OPENAL_LIBRARY_NAME.set(System.mapLibraryName("ps5openal"));Configuration.SDL_LIBRARY_NAME.set(System.mapLibraryName("ps5sdl"));Configuration.VULKAN_LIBRARY_NAME.set(System.mapLibraryName("ps5clientgpu"));Configuration.SHADERC_LIBRARY_NAME.set(System.mapLibraryName("ps5shaderc"));Configuration.SHARED_LIBRARY_EXTRACT_PATH.set(work.resolve("native-cache").toString());
   stage("configure validated036 SPIRV-Cross,035 VMA,033 FreeType,031 STB and029 real OSMesa/OpenGL plus026 libffi/OpenAL and resident SDL/Vulkan/shaderc;other native bindings remain incomplete");
   System.loadLibrary("ps5clientgpu");System.loadLibrary("ps5clientgl");System.loadLibrary("ps5shaderc");System.loadLibrary("ps5sdl");System.loadLibrary("ps5openal");
   boolean controls=org.lwjgl.sdl.SDLHints.SDL_SetHint("PS5_TEMPORARY_CONTROLS",System.getProperty("ps5.temporaryControls","1"));
   stage("Temporary SDL controls hint="+org.lwjgl.sdl.SDLHints.SDL_GetHint("PS5_TEMPORARY_CONTROLS")+" accepted="+controls+";D-pad/left stick=menu arrows,X=select,Circle=back,Triangle=Tab,Square=Backspace;gamepad subsystem hands off to future mods");
   stage("Menu inactivity FPS policy=minimized;other options retained,original backed up when migrated");
   stage("Guarded C1 warmup:checking actual level1 compiled integer kernel before original Main");
   ps5probe.JitWarmup25.check();
   stage("PASS current-run C1 level1 kernel compiled and verified;performance/world stability still pending");
   stage(verifyNativeAllocation());
   Runtime heap=Runtime.getRuntime();stage("heap maxMiB="+(heap.maxMemory()/1048576)+" committedMiB="+(heap.totalMemory()/1048576)+" usedMiB="+((heap.totalMemory()-heap.freeMemory())/1048576));
   stage("original Main class lookup;offline demo arguments,no credentials or multiplayer");
   Class<?> main=Class.forName("net.minecraft.client.main.Main",false,ClassLoader.getSystemClassLoader());Method method=main.getMethod("main",String[].class);
   stage("ENTER original net.minecraft.client.main.Main.main;menu/world not yet validated");
   console.println("Original Minecraft26.3 Main entry;offline demo test. Native dependency coverage remains incomplete.");
   if(startupObserverEnabled()){
    try{observer=new StartupObserver(console,390,1000,5000);observer.start();}
    catch(Throwable unavailable){console.println("PS5 startup observer unavailable;continuing original Main: "+unavailable);observer=null;}
   }else console.println("PS5 startup observer disabled for performance run;enable ps5.startupObserver explicitly for stack sampling");
   try{method.invoke(null,(Object)launchArguments(work,assets));}
   catch(InvocationTargetException failure){throw failure.getCause();}
   stage("Original Main returned;this alone does not establish menu or gameplay success");
   throw new IllegalStateException("Original game main returned;inspect exceptions.log/latest.log and actual visible state;no automatic menu PASS");
  }catch(Throwable failure){failure.printStackTrace(console);stage("Original startup stopped: "+failure);throw failure;}
  finally{if(observer!=null)observer.close();console.flush();System.setOut(previousOut);System.setErr(previousErr);console.close();}
 }
}
