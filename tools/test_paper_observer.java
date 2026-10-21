import java.io.*;
import java.lang.reflect.*;
public class test_paper_observer {
 public static void main(String[]args)throws Exception {
  System.setProperty("ps5.mc.serverFlavor","paper");
  Class<?> type=Class.forName("ServerStart25$Observer");var constructor=type.getDeclaredConstructor(PrintStream.class);constructor.setAccessible(true);
  var out=(OutputStream)constructor.newInstance(new PrintStream(OutputStream.nullOutputStream()));
  out.write("[Server thread/INFO]: PS5_PAPER_PLUGIN_ENABLED version=1.0.0\n[Server thread/INFO]: PS5_PAPER_SCHEDULER_OK tick=20\n[Server thread/INFO]: PS5_PAPER_COMMAND_OK tick=21\n".getBytes());
  for(String name:new String[]{"paperPluginReady","paperSchedulerReady","paperCommandReady"}){var field=type.getDeclaredField(name);field.setAccessible(true);if(!field.getBoolean(out))throw new AssertionError(name);}
  var gate=ServerStart25.class.getDeclaredMethod("checkOnline",type);gate.setAccessible(true);gate.invoke(null,out);
  out.write("[Paper Common Worker #0/ERROR]: Java heap space\n".getBytes());
  try{gate.invoke(null,out);throw new AssertionError("Paper worker error ignored");}catch(InvocationTargetException e){if(!(e.getCause() instanceof IOException))throw e;}
  System.out.println("PASS: actual observer plugin enable/scheduler/command markers and Paper worker ERROR failure gate");
 }
}
