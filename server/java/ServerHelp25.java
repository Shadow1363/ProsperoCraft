import java.io.*;
import java.nio.charset.StandardCharsets;

public class ServerHelp25 {
 private static native void checkpoint(String stage);
 private static void trace(String stage){if(Boolean.getBoolean("ps5.probe.dependencyTrace"))checkpoint("MC help: "+stage);}
 private static String describe(Throwable error){StringBuilder text=new StringBuilder();for(int i=0;error!=null&&i<8;i++){if(i>0)text.append(" | cause: ");text.append(error);error=error.getCause();}return text.toString();}
 public static void main(String[] args) throws Exception {
  String stage="capture real server help output";
  PrintStream originalOut=System.out,originalErr=System.err;
  ByteArrayOutputStream buffer=new ByteArrayOutputStream();
  try(PrintStream captured=new PrintStream(buffer,true,StandardCharsets.UTF_8)) {
   System.setOut(captured);System.setErr(captured);
   stage="initialize official server main";trace(stage);
   Class<?> main=Class.forName("net.minecraft.server.Main",true,ClassLoader.getSystemClassLoader());
   stage="invoke official main --help";trace(stage);
   main.getMethod("main",String[].class).invoke(null,(Object)new String[]{"--help"});
   String output=buffer.toString(StandardCharsets.UTF_8);
   stage="verify server option parser help result";trace(stage);
   if(!output.contains("nogui")||!output.contains("port")||!output.contains("universe"))throw new AssertionError("Expected server help options missing: "+output.substring(0,Math.min(output.length(),1000)));
   originalOut.println(output);originalOut.println("MC_SERVER_HELP_OK official 26.3 entry point; no world or EULA acceptance");
  }catch(Throwable error){throw new Exception("MC server help stage "+stage+": "+describe(error),error);}
  finally{System.setOut(originalOut);System.setErr(originalErr);}
 }
}
