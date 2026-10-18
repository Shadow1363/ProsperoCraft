import java.io.*;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
public class test_endurance {
 static long field(Class<?> c,Object o,String name)throws Exception {var f=c.getDeclaredField(name);f.setAccessible(true);return f.getLong(o);}
 static void failed(Method m,Object...args)throws Exception {try{m.invoke(null,args);throw new AssertionError("Accepted invalid condition");}catch(InvocationTargetException expected){if(!(expected.getCause() instanceof IOException))throw expected;}}
 public static void main(String[] args)throws Exception {
  Class<?> c=Class.forName("ServerStart25$Observer");var ctor=c.getDeclaredConstructor(PrintStream.class);ctor.setAccessible(true);Object o=ctor.newInstance(new PrintStream(OutputStream.nullOutputStream()));OutputStream stream=(OutputStream)o;
  stream.write("[00:00:00] [Other/INFO]: The game time is 99 tick(s)\n[00:00:00] [Server thread/INFO]: The game time is nonsense tick(s)\n".getBytes(StandardCharsets.UTF_8));
  if(field(c,o,"timeReplies")!=0)throw new AssertionError("false reply");
  stream.write("[00:00:00] [Server thread/INFO]: System chat: The game ".getBytes(StandardCharsets.UTF_8));stream.write("time is 123 tick(s)\n".getBytes(StandardCharsets.UTF_8));
  if(field(c,o,"timeReplies")!=1||field(c,o,"gameTime")!=123)throw new AssertionError("split reply");
  stream.write("[00:00:00] [Server thread/INFO]: Saving the game (this may take a moment!)\n".getBytes(StandardCharsets.UTF_8));
  if(field(c,o,"saveReplies")!=0)throw new AssertionError("premature save");
  stream.write("[00:00:00] [Server thread/INFO]: System chat: Saved the game\n[00:00:00] [Server thread/ERROR]: Actual failure\n".getBytes(StandardCharsets.UTF_8));
  if(field(c,o,"saveReplies")!=1||field(c,o,"serverErrors")!=1)throw new AssertionError("ack/error");
  var await=ServerStart25.class.getDeclaredMethod("awaitReply",c,long.class,boolean.class,long.class);await.setAccessible(true);
  await.invoke(null,o,0L,false,1L);failed(await,o,1L,false,1L); // dead thread cannot pass
  Thread thread=new Thread(()->{try{Thread.sleep(5000);}catch(InterruptedException ignored){}},"Server thread");thread.start();
  try{failed(await,o,1L,false,1L);}finally{thread.interrupt();thread.join();} // live but unresponsive fails
  System.setProperty("ps5.mc.endurancePollSeconds","1");System.setProperty("ps5.mc.enduranceSaveSeconds","300");System.setProperty("ps5.mc.enduranceReplySeconds","1");
  var input=new PipedInputStream();var commands=new PipedOutputStream(input);
  Thread stalled=new Thread(()->{try(var reader=new BufferedReader(new InputStreamReader(input,StandardCharsets.UTF_8))){for(String command;(command=reader.readLine())!=null;){stream.write("[00:00:00] [Server thread/INFO]: System chat: The game time is 123 tick(s)\n".getBytes(StandardCharsets.UTF_8));}}catch(IOException ignored){}},"Server thread");
  var endurance=ServerStart25.class.getDeclaredMethod("endurance",c,PipedOutputStream.class,long.class);endurance.setAccessible(true);
  stalled.start();try{failed(endurance,o,commands,1L);}finally{commands.close();stalled.join(2000);if(stalled.isAlive())throw new AssertionError("test command reader stuck");}
  var errors=c.getDeclaredField("authErrors");errors.setAccessible(true);errors.setLong(o,1);System.setProperty("ps5.mc.requireOnline","true");
  var fakeCommands=new PipedOutputStream();failed(endurance,o,fakeCommands,1L);fakeCommands.close();System.clearProperty("ps5.mc.requireOnline");
  var checkOnline=ServerStart25.class.getDeclaredMethod("checkOnline",c);checkOnline.setAccessible(true);
  errors.setLong(o,0);System.setProperty("ps5.mc.requireOnline","true");checkOnline.invoke(null,o);
  stream.write("[00:00:00] [Other/WARN]: Failed to connect\n".getBytes(StandardCharsets.UTF_8));checkOnline.invoke(null,o);
  stream.write("[00:00:00] [Minecraft Services Discovery/WARN]: Failed to connect\n".getBytes(StandardCharsets.UTF_8));
  if(field(c,o,"discoveryErrors")!=1)throw new AssertionError("missed actual discovery failure");failed(checkOnline,o);
  failed(endurance,o,new PipedOutputStream(),1L);System.clearProperty("ps5.mc.requireOnline");checkOnline.invoke(null,o);
  stream.write("[00:00:00] [Netty NIO IO #2/ERROR]: Error sending packet clientbound/minecraft:update_tags\n".getBytes(StandardCharsets.UTF_8));
  if(field(c,o,"networkErrors")!=1)throw new AssertionError("missed packet encoder failure");failed(checkOnline,o);
  var readyAt=c.getDeclaredField("readyAt");readyAt.setAccessible(true);readyAt.setLong(o,System.nanoTime()-3_000_000_000L);failed(endurance,o,new PipedOutputStream(),1L);readyAt.setLong(o,0L);
  System.setProperty("ps5.mc.testSetting","0");if(ServerStart25.setting("ps5.mc.testSetting",4,0,10)!=0)throw new AssertionError();
  System.setProperty("ps5.mc.testSetting","-1");try{ServerStart25.setting("ps5.mc.testSetting",4,0,10);throw new AssertionError();}catch(IllegalArgumentException expected){}
  stream.close();System.out.println("PASS: real observer split replies/malformed/unrelated lines, saved acknowledgement vs saving, error count; command gate dead/unresponsive and repeated game-time, packet/authentication/discovery-error and late-monitor failures; config bounds");
 }
}
