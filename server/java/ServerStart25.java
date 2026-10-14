import java.io.*;
import java.lang.reflect.InvocationTargetException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

/** One bounded real vanilla startup/save/stop attempt; no simulated server. */
public class ServerStart25 {
 private static native void checkpoint(String stage);
 private static void trace(String stage){if(Boolean.getBoolean("ps5.probe.dependencyTrace"))checkpoint("MC start: "+stage);}
 private static final class Observer extends OutputStream {
  final PrintStream console;final StringBuilder tail=new StringBuilder();volatile boolean ready;
  Observer(PrintStream console){this.console=console;}
  public synchronized void write(int value){console.write(value);tail.append((char)(value&255));trim();}
  public synchronized void write(byte[] bytes,int offset,int length){console.write(bytes,offset,length);tail.append(new String(bytes,offset,length,StandardCharsets.UTF_8));trim();}
  private void trim(){if(tail.indexOf("Done (")>=0&&tail.indexOf("For help, type")>=0)ready=true;if(tail.length()>16000)tail.delete(0,tail.length()-16000);}
  synchronized String recent(){return tail.toString();}
 }
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
    if(!observer.ready)throw new IOException("Server did not report ready. Recent output: "+observer.recent());
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
  if(failure!=null)throw new Exception("MC server start stage "+stage+": "+failure+" | output: "+observer.recent(),failure);
 }
}
