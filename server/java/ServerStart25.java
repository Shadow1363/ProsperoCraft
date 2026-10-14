import java.io.*;
import java.lang.reflect.InvocationTargetException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

/** One bounded real vanilla startup/save/stop attempt; no simulated server. */
public class ServerStart25 {
 private static native void checkpoint(String stage);
 private static void trace(String stage){if(Boolean.getBoolean("ps5.probe.dependencyTrace"))checkpoint("MC start: "+stage);}
 private static final class Observer extends OutputStream {
  final PrintStream console;final StringBuilder head=new StringBuilder(),tail=new StringBuilder(),errors=new StringBuilder(),line=new StringBuilder();volatile boolean ready;
  Observer(PrintStream console){this.console=console;}
  public synchronized void write(int value){console.write(value);record(Character.toString((char)(value&255)));}
  public synchronized void write(byte[] bytes,int offset,int length){console.write(bytes,offset,length);record(new String(bytes,offset,length,StandardCharsets.UTF_8));}
  private void record(String text){
   if(head.length()<4096)head.append(text,0,Math.min(text.length(),4096-head.length()));
   tail.append(text);
   if(tail.indexOf("Done (")>=0&&tail.indexOf("For help, type")>=0)ready=true;
   if(tail.length()>4096)tail.delete(0,tail.length()-4096);
   for(int i=0;i<text.length();i++){
    char c=text.charAt(i);
    if(c=='\n'){note();line.setLength(0);}else if(line.length()<4096)line.append(c=='\t'?' ':c);
   }
  }
  private void note(){String value=line.toString().trim();if(errors.length()<4096&&!value.startsWith("at ")&&(value.contains("ERROR")||value.contains("Exception")||value.contains("Error")||value.contains("Caused by:")))errors.append(value,0,Math.min(value.length(),4096-errors.length())).append('\n');}
  synchronized String recent(){return "ERROR HEADINGS AND CAUSES:\n"+errors+"\nFIRST OUTPUT:\n"+head+"\nRECENT OUTPUT:\n"+tail;}
 }
 private static String describe(Throwable error){StringBuilder result=new StringBuilder();for(int i=0;error!=null&&i<8;i++,error=error.getCause()){if(i>0)result.append(" | caused by: ");result.append(error);}return result.toString();}
 private static Thread serverThread(){for(Thread thread:Thread.getAllStackTraces().keySet())if(thread.isAlive()&&thread.getName().equals("Server thread"))return thread;return null;}
 public static void main(String[] args)throws Exception {
  if(!Boolean.getBoolean("ps5.mc.eulaAccepted"))throw new IllegalStateException("Human EULA acceptance is required before this test");
  Path root=Path.of(System.getProperty("ps5.mc.workdir",System.getProperty("user.dir"))).toAbsolutePath();
  String stage="write authorized EULA and isolated flat-world configuration";trace(stage);
  Files.createDirectories(root);
  Files.writeString(root.resolve("eula.txt"),"# Human accepted Minecraft EULA for this test\neula=true\n");
  Files.writeString(root.resolve("server.properties"),"level-name=world\nlevel-type=minecraft:flat\ngenerate-structures=false\nspawn-chunk-radius=0\nview-distance=2\nsimulation-distance=2\nmax-players=1\nonline-mode=true\nserver-ip=\nserver-port=25565\nenable-query=false\nenable-rcon=false\nwhite-list=true\nmax-tick-time=-1\n");
  PrintStream originalOut=System.out,originalErr=System.err;InputStream originalIn=System.in;
  Observer observer=new Observer(originalOut);PipedInputStream input=new PipedInputStream();PipedOutputStream commands=new PipedOutputStream(input);
  boolean stopped=false;Throwable failure=null;
  try(PrintStream captured=new PrintStream(observer,true,StandardCharsets.UTF_8)) {
   System.setOut(captured);System.setErr(captured);System.setIn(input);
   try {
    stage="initialize and invoke official vanilla server nogui";trace(stage);
    Class<?> main=Class.forName("net.minecraft.server.Main",true,ClassLoader.getSystemClassLoader());
    main.getMethod("main",String[].class).invoke(null,(Object)new String[]{"--nogui","--universe",root.toString(),"--world","world"});
    stage="wait up to 10 minutes for real Done readiness message";trace(stage);
    long deadline=System.nanoTime()+600_000_000_000L;
    while(!observer.ready&&System.nanoTime()<deadline){if(serverThread()==null)break;Thread.sleep(200);}
    if(!observer.ready)throw new IOException("Server did not report ready; thread exited or deadline elapsed");
    stage="send stop and await real server thread exit";trace(stage);
    commands.write("stop\n".getBytes(StandardCharsets.UTF_8));commands.flush();
    Thread thread=serverThread();if(thread!=null)thread.join(120000);
    if(serverThread()!=null)throw new IOException("Server did not stop within 120 seconds");stopped=true;
    stage="verify persisted world level.dat after stop";trace(stage);
    try(InputStream saved=Files.newInputStream(root.resolve("world/level.dat"))){if(saved.read()<0)throw new IOException("Empty saved world level.dat");}
    originalOut.println("MC_SERVER_START_OK real Done readiness, stop, thread exit and saved level.dat");
   }catch(Throwable error){failure=error instanceof InvocationTargetException&&error.getCause()!=null?error.getCause():error;}
   finally {
    if(!stopped&&serverThread()!=null){commands.write("stop\n".getBytes(StandardCharsets.UTF_8));commands.flush();Thread thread=serverThread();if(thread!=null)thread.join(30000);}
   }
  }finally{System.setOut(originalOut);System.setErr(originalErr);System.setIn(originalIn);commands.close();input.close();}
  if(failure!=null)throw new Exception("MC server start stage "+stage+": "+describe(failure)+" | Java heap bytes: max="+Runtime.getRuntime().maxMemory()+" total="+Runtime.getRuntime().totalMemory()+" free="+Runtime.getRuntime().freeMemory()+" | output: "+observer.recent(),failure);
 }
}
