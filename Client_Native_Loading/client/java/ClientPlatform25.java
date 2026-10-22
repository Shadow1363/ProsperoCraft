import org.lwjgl.system.Platform;
import org.lwjgl.system.APIUtil;
public final class ClientPlatform25 {
 public static native void checkpoint(String text);
 public static void main(String[] args) {
  if(!"PS5".equals(System.getProperty("os.name")))throw new AssertionError("Expected real PS5 VM identity");
  if(Platform.get()!=Platform.PS5||Platform.getArchitecture()!=Platform.Architecture.X64)throw new AssertionError("PS5/x64 platform selection");
  try{APIUtil.apiCreateLibrary("native-port-not-built");throw new AssertionError("native resolver falsely succeeded");}
  catch(UnsatisfiedLinkError expected){if(!expected.getMessage().contains("PS5 LWJGL native function resolver is not ported"))throw expected;}
  checkpoint("MC_CLIENT_PLATFORM_OK explicit PS5/x64 dependency port; native loader remains unavailable; no desktop fallback");
 }
}
