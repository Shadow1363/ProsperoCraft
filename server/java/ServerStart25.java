import java.io.*;
import java.lang.reflect.InvocationTargetException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

/** One bounded real server startup/save/stop attempt with PS5 report adaptation. */
public class ServerStart25 {
 private static native void checkpoint(String stage);
 private static void trace(String stage){if(Boolean.getBoolean("ps5.probe.dependencyTrace"))checkpoint("MC start: "+stage);}
 private static final class Observer extends OutputStream {
  final PrintStream console;final StringBuilder head=new StringBuilder(),tail=new StringBuilder(),errors=new StringBuilder(),line=new StringBuilder();volatile boolean ready;volatile long readyAt;volatile long gameTime=-1,timeReplies,saveReplies,serverErrors,authErrors,discoveryErrors,networkErrors,playerJoins;
  OutputStream log;long logged;
  private void persist(byte[] bytes,int offset,int length){if(log==null)return;try{int n=(int)Math.min(length,32L*1024*1024-logged);if(n>0){log.write(bytes,offset,n);logged+=n;}if(n<length){log.write("\n[Log capped at 32 MiB]\n".getBytes(StandardCharsets.UTF_8));log.close();log=null;}else log.flush();}catch(IOException e){console.println("Probe console log write failed: "+e);try{log.close();}catch(IOException ignored){}log=null;}}
  public synchronized void close()throws IOException{if(log!=null){log.close();log=null;}}
  Observer(PrintStream console){this.console=console;String path=System.getProperty("ps5.probe.serverLogPath");if(path!=null)try{log=new FileOutputStream(path);}catch(IOException e){console.println("Probe console log unavailable: "+e);}}
  public synchronized void write(int value){console.write(value);persist(new byte[]{(byte)value},0,1);record(Character.toString((char)(value&255)));}
  public synchronized void write(byte[] bytes,int offset,int length){console.write(bytes,offset,length);persist(bytes,offset,length);record(new String(bytes,offset,length,StandardCharsets.UTF_8));}
  private void record(String text){
   if(head.length()<4096)head.append(text,0,Math.min(text.length(),4096-head.length()));
   tail.append(text);
   if(!ready&&tail.indexOf("Done (")>=0&&tail.indexOf("For help, type")>=0){readyAt=System.nanoTime();ready=true;}
   if(tail.length()>4096)tail.delete(0,tail.length()-4096);
   for(int i=0;i<text.length();i++){
    char c=text.charAt(i);
    if(c=='\n'){note();line.setLength(0);}else if(line.length()<4096)line.append(c=='\t'?' ':c);
   }
  }
  private void note(){String value=line.toString().trim();
   String prefix="[Server thread/INFO]: ";int at=value.indexOf(prefix);
   String reply=at<0?"":value.substring(at+prefix.length());
   if(reply.startsWith("System chat: "))reply=reply.substring("System chat: ".length());
   if(reply.startsWith("The game time is ")) {
    int start="The game time is ".length(),end=reply.indexOf(" tick(s)",start);
    if(end>start)try{gameTime=Long.parseLong(reply.substring(start,end));timeReplies++;}catch(NumberFormatException ignored){}
   }
   if(reply.equals("Saved the game"))saveReplies++;
   if(reply.endsWith(" joined the game"))playerJoins++;
   if(value.contains("[User Authenticator ")&&value.contains("/ERROR]"))authErrors++;
   if(value.contains("[Minecraft Services Discovery/WARN]")&&(value.contains("Failed to connect")||value.contains("Services are unavailable")))discoveryErrors++;
   if(value.contains("[Netty ")&&value.contains("/ERROR]"))networkErrors++;
   if(value.contains("[Server thread/ERROR]"))serverErrors++;
   if(errors.length()<4096&&!value.startsWith("at ")&&(value.contains("ERROR")||value.contains("Exception")||value.contains("Error")||value.contains("Caused by:")))errors.append(value,0,Math.min(value.length(),4096-errors.length())).append('\n');}
  synchronized String recent(){return "ERROR HEADINGS AND CAUSES:\n"+errors+"\nFIRST OUTPUT:\n"+head+"\nRECENT OUTPUT:\n"+tail;}
 }
 private static String describe(Throwable error){StringBuilder result=new StringBuilder();for(int i=0;error!=null&&i<8;i++,error=error.getCause()){if(i>0)result.append(" | caused by: ");result.append(error);}return result.toString();}
 static Thread serverThread(){
  // Finding a thread must not request a native stack dump of every thread,
  // especially after the server has already reported allocation failure.
  ThreadGroup group=Thread.currentThread().getThreadGroup();
  while(group.getParent()!=null)group=group.getParent();
  for(int capacity=64;capacity<=4096;capacity*=2){
   Thread[] threads=new Thread[capacity];int count=group.enumerate(threads,true);
   if(count==capacity)continue; // Retry a possibly truncated enumeration.
   for(int i=0;i<count;i++)if(threads[i].isAlive()&&threads[i].getName().equals("Server thread"))return threads[i];
   return null;
  }
  throw new IllegalStateException("Server thread enumeration exceeded 4096 platform threads");
 }
 // Check the exact nofollow operation used by DirectoryValidator before loading the server.
 static void checkWorldMetadata(Path root)throws IOException {
  try {
   Files.readAttributes(root,java.nio.file.attribute.BasicFileAttributes.class,LinkOption.NOFOLLOW_LINKS);
   try{Files.readAttributes(root.resolve("world"),java.nio.file.attribute.BasicFileAttributes.class,LinkOption.NOFOLLOW_LINKS);}
   catch(NoSuchFileException absent){/* The official server creates a missing world. */}
  }catch(IOException failure){throw new IOException("World metadata preflight (NOFOLLOW_LINKS): "+failure,failure);}
 }
 static long setting(String name,long fallback,long min,long max) {
  String text=System.getProperty(name);long value=text==null?fallback:Long.parseLong(text);
  if(value<min||value>max)throw new IllegalArgumentException(name+" outside "+min+".."+max);return value;
 }
 private static void command(PipedOutputStream commands,String text)throws IOException{commands.write((text+"\n").getBytes(StandardCharsets.UTF_8));commands.flush();}
 private static void awaitReply(Observer observer,long previous,boolean save,long timeoutSeconds)throws Exception {
  long deadline=System.nanoTime()+timeoutSeconds*1_000_000_000L;
  while((save?observer.saveReplies:observer.timeReplies)<=previous) {
   if(serverThread()==null)throw new IOException("Server thread exited during endurance command");
   if(System.nanoTime()>=deadline)throw new IOException("No server acknowledgement for "+(save?"save-all flush":"time query gametime"));
   Thread.sleep(100);
  }
 }
 private static void checkOnline(Observer observer)throws IOException {
  if(observer.networkErrors>0)throw new IOException("Network packet failure during endurance; inspect server.log");
  if(!Boolean.getBoolean("ps5.mc.requireOnline"))return;
  if(observer.discoveryErrors>0)throw new IOException("Minecraft authentication discovery failed; inspect server.log and native DNS stages");
  if(observer.authErrors>0)throw new IOException("Online login failure during endurance");
 }
 private static void endurance(Observer observer,PipedOutputStream commands,long seconds)throws Exception {
  if(seconds==0)return;
  long poll=setting("ps5.mc.endurancePollSeconds",30,1,300),saveInterval=setting("ps5.mc.enduranceSaveSeconds",300,1,3600),timeout=setting("ps5.mc.enduranceReplySeconds",120,1,600);
  long begin=observer.readyAt==0?System.nanoTime():observer.readyAt,deadline=begin+seconds*1_000_000_000L,nextSave=begin+saveInterval*1_000_000_000L;
  if(System.nanoTime()-begin>poll*1_000_000_000L)throw new IOException("Endurance monitoring started too late after readiness");
  long last=-1,lastReplyAt=0,checks=0,saves=0,errors=observer.serverErrors;
  var performance=new ServerPerformance25();
  System.out.println("MC_ENDURANCE_BEGIN targetSeconds="+seconds+" pollSeconds="+poll+" saveSeconds="+saveInterval+" noPlayerAutoPause=false");
  do {
   checkOnline(observer);
   if(serverThread()==null)throw new IOException("Server exited before endurance completed");
   long before=observer.timeReplies;command(commands,"time query gametime");awaitReply(observer,before,false,timeout);
   long current=observer.gameTime;
   if(last>=0&&current<=last)throw new IOException("Game time did not advance: "+last+" -> "+current);
   long replyAt=System.nanoTime();String rate=ServerPerformance25.rate(last,current,lastReplyAt,replyAt);
   last=current;lastReplyAt=replyAt;checks++;
   if(System.nanoTime()>=nextSave) {
    before=observer.saveReplies;command(commands,"save-all flush");awaitReply(observer,before,true,timeout);saves++;
    nextSave=System.nanoTime()+saveInterval*1_000_000_000L;
   }
   if(observer.serverErrors>errors)throw new IOException("Server ERROR logged during endurance");
   Runtime memory=Runtime.getRuntime();
   System.out.println("MC_ENDURANCE_HEALTH elapsedSeconds="+((System.nanoTime()-begin)/1_000_000_000L)+" targetSeconds="+seconds+" gameTime="+current+" checks="+checks+" saves="+saves+" joins="+observer.playerJoins+" authErrors="+observer.authErrors+" discoveryErrors="+observer.discoveryErrors+" networkErrors="+observer.networkErrors+" "+rate+" "+performance.sample()+" heapUsed="+(memory.totalMemory()-memory.freeMemory())+" heapCommitted="+memory.totalMemory()+" heapMax="+memory.maxMemory());
   if(Boolean.getBoolean("ps5.mc.gameplayDiagnostics")) {
    System.out.println("MC_GAMEPLAY_SAMPLE read-only player hunger/saturation/exhaustion; replies follow in server.log");
    for(String field:new String[]{"foodLevel","foodSaturationLevel","foodExhaustionLevel"})command(commands,"execute as @a run data get entity @s "+field);
   }
   if(System.nanoTime()>=deadline)break;
   long remaining=deadline-System.nanoTime();Thread.sleep(Math.max(1,Math.min(poll*1000,remaining/1_000_000)));
  }while(true);
  // A final flushed save is required even when the requested run is shorter
  // than the periodic save interval. Stop/thread exit/file check follow.
  long before=observer.saveReplies;command(commands,"save-all flush");awaitReply(observer,before,true,timeout);
  if(observer.serverErrors>errors)throw new IOException("Server ERROR during final endurance save");
  checkOnline(observer);
  System.out.println("MC_ENDURANCE_COMPLETE elapsedSeconds="+((System.nanoTime()-begin)/1_000_000_000L)+" checks="+checks+" saves="+(saves+1)+" joins="+observer.playerJoins+" authErrors="+observer.authErrors+" discoveryErrors="+observer.discoveryErrors+" networkErrors="+observer.networkErrors);
 }
 public static void main(String[] args)throws Exception {
  long enduranceSeconds=setting("ps5.mc.enduranceSeconds",0,0,86400);
  Thread.currentThread().setContextClassLoader(ClassLoader.getSystemClassLoader());
  if(!Boolean.getBoolean("ps5.mc.eulaAccepted"))throw new IllegalStateException("Human EULA acceptance is required before this test");
  Path root=Path.of(System.getProperty("ps5.mc.workdir",System.getProperty("user.dir"))).toAbsolutePath();
  String stage="write authorized EULA and isolated flat-world configuration";trace(stage);
  Files.createDirectories(root);
  stage="verify world metadata without following final symlinks";trace(stage);
  checkWorldMetadata(root);
  Files.writeString(root.resolve("eula.txt"),"# Human accepted Minecraft EULA for this test\neula=true\n");
  Files.writeString(root.resolve("server.properties"),"level-name=world\nlevel-type=minecraft:flat\ngenerator-settings={\"biome\":\"minecraft:plains\",\"layers\":[{\"block\":\"minecraft:bedrock\",\"height\":1},{\"block\":\"minecraft:dirt\",\"height\":2},{\"block\":\"minecraft:grass_block\",\"height\":1}]}\ngenerate-structures=false\nspawn-chunk-radius=0\nview-distance=2\nsimulation-distance=2\nmax-players=1\nonline-mode=true\nserver-ip=\nserver-port=25565\nenable-query=false\nenable-rcon=false\nwhite-list=true\nmax-tick-time=-1\n");
  if(enduranceSeconds>0)Files.writeString(root.resolve("server.properties"),"pause-when-empty-seconds=0\n",StandardOpenOption.APPEND);
  PrintStream originalOut=System.out,originalErr=System.err;InputStream originalIn=System.in;
  Observer observer=new Observer(originalOut);PipedInputStream input=new PipedInputStream();PipedOutputStream commands=new PipedOutputStream(input);
  boolean stopped=false;Throwable failure=null;
  try(PrintStream captured=new PrintStream(observer,true,StandardCharsets.UTF_8)) {
   System.setOut(captured);System.setErr(captured);System.setIn(input);
   try {
    if(Boolean.getBoolean("ps5.mc.checkNetworkMemory")) {stage="verify network allocator growth";trace(stage);ServerMemory25.check();}
    if(Boolean.getBoolean("ps5.mc.requireOnline")) {
     stage="verify online DNS/HTTPS discovery, account profile and whitelist";trace(stage);
     Class.forName("ServerOnline25").getMethod("prepare",Path.class).invoke(null,root);
    }
    stage="initialize and invoke server nogui with PS5 diagnostic adaptation";trace(stage);
    Class<?> main=Class.forName("net.minecraft.server.Main",true,ClassLoader.getSystemClassLoader());
    main.getMethod("main",String[].class).invoke(null,(Object)new String[]{"--nogui","--universe",root.toString(),"--world","world"});
    stage="wait up to 10 minutes for real Done readiness message";trace(stage);
    long deadline=System.nanoTime()+600_000_000_000L;
    while(!observer.ready&&System.nanoTime()<deadline){if(serverThread()==null)break;Thread.sleep(200);}
    if(!observer.ready)throw new IOException("Server did not report ready; thread exited or deadline elapsed");
    checkOnline(observer);
    // Optional host stress fixture, absent from console launch options.
    long chunks=setting("ps5.mc.validationChunkRadius",0,0,4);
    if(chunks>0){long edge=chunks*16;command(commands,"forceload add "+(-edge)+" "+(-edge)+" "+edge+" "+edge);}
    stage="endurance: tick progress, periodic flushed saves and server liveness";trace(stage);
    endurance(observer,commands,enduranceSeconds);
    stage="send stop and await real server thread exit";trace(stage);
    commands.write("stop\n".getBytes(StandardCharsets.UTF_8));commands.flush();
    Thread thread=serverThread();if(thread!=null)thread.join(120000);
    if(serverThread()!=null)throw new IOException("Server did not stop within 120 seconds");stopped=true;
    stage="verify persisted world level.dat after stop";trace(stage);
    try(InputStream saved=Files.newInputStream(root.resolve("world/level.dat"))){if(saved.read()<0)throw new IOException("Empty saved world level.dat");}
    if(enduranceSeconds>0)originalOut.println("MC_SERVER_ENDURANCE_OK targetSeconds="+enduranceSeconds+" real tick progress, flushed saves, stop/thread exit and saved level.dat");
    originalOut.println("MC_SERVER_START_OK real Done readiness, stop, thread exit and saved level.dat");
   }catch(Throwable error){failure=error instanceof InvocationTargetException&&error.getCause()!=null?error.getCause():error;}
   finally {
    if(!stopped&&serverThread()!=null){commands.write("stop\n".getBytes(StandardCharsets.UTF_8));commands.flush();Thread thread=serverThread();if(thread!=null)thread.join(30000);}
   }
  }finally{System.setOut(originalOut);System.setErr(originalErr);System.setIn(originalIn);commands.close();input.close();}
  if(failure!=null)throw new Exception("MC server start stage "+stage+": "+describe(failure)+" | Java heap bytes: max="+Runtime.getRuntime().maxMemory()+" total="+Runtime.getRuntime().totalMemory()+" free="+Runtime.getRuntime().freeMemory()+" | output: "+observer.recent(),failure);
 }
}
