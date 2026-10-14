import java.io.*;
import java.nio.charset.StandardCharsets;
public class test_probe_output {
 public static void main(String[] args)throws Exception {
  Class<?> type=Class.forName("ServerStart25$Observer");var constructor=type.getDeclaredConstructor(PrintStream.class);constructor.setAccessible(true);
  OutputStream observer=(OutputStream)constructor.newInstance(new PrintStream(OutputStream.nullOutputStream()));
  observer.write("startup\njava.lang.UnsatisfiedLinkError: missing-real-symbol\n".getBytes(StandardCharsets.UTF_8));
  observer.write(("\tat framework.LongStack.method(Unknown Source)\n".repeat(1000)).getBytes(StandardCharsets.UTF_8));
  observer.write("Caused by: java.io.IOException: actual denied operation\n".getBytes(StandardCharsets.UTF_8));
  var recent=type.getDeclaredMethod("recent");recent.setAccessible(true);String text=(String)recent.invoke(observer);
  if(!text.startsWith("ERROR HEADINGS AND CAUSES:")||!text.contains("missing-real-symbol")||!text.contains("actual denied operation")||text.length()>13000)throw new AssertionError(text);
  var ready=type.getDeclaredField("ready");ready.setAccessible(true);if(ready.getBoolean(observer))throw new AssertionError("false ready");
  observer.write("Done (1.0s)! For help, type \"help\"\n".getBytes(StandardCharsets.UTF_8));if(!ready.getBoolean(observer))throw new AssertionError("missed ready");
  System.out.println("PASS: bounded head/tail, first error retained across 40KB stack, cause heading retained, real readiness predicate");
 }
}
