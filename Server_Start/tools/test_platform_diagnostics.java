import java.lang.reflect.*;
public class test_platform_diagnostics {
 public static void main(String[] args)throws Exception {
  Class.forName("net.minecraft.SharedConstants").getMethod("tryDetectVersion").invoke(null);
  String old=System.getProperty("os.name");System.setProperty("os.name","PS5");
  Class<?> type=Class.forName("net.minecraft.SystemReport");Object report=type.getConstructor().newInstance();
  String text=(String)type.getMethod("toLineSeparatedString").invoke(report);
  if(!text.contains("Unavailable on PS5: no supported OSHI backend")||text.contains("ERR")||!text.contains("Memory (heap)")||!text.contains("JVM Flags"))throw new AssertionError(text);
  if(!type.getProtectionDomain().getCodeSource().getLocation().toString().endsWith("ps5-platform-diagnostics.jar"))throw new AssertionError("Adapter not loaded");
  // Confirm the original desktop methods survive in the class for non-PS5 use.
  type.getDeclaredMethod("ps5$putHardware",Class.forName("oshi.SystemInfo"));type.getDeclaredMethod("ps5$putSoftware",Class.forName("oshi.SystemInfo"));
  System.setProperty("os.name",old);
  System.out.println("PASS: PS5 diagnostic adaptation, truthful unsupported telemetry, real JVM heap/flags, retained desktop methods");
 }
}
