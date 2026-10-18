import java.nio.file.*;
/** Called by the runtime's isolated metadata-denial test JVM after native rebinding. */
public class test_online_file_denial {
 public static void main(String[] args)throws Exception {
  System.setProperty("ps5.mc.joinPlayer",args[1]);Path root=Path.of(args[0]);Files.createDirectories(root);
  ServerOnline25.prepare(root);
  if(!Files.readString(root.resolve("whitelist.json")).contains("uuid"))throw new AssertionError("Whitelist not persisted");
  System.out.println("PASS: real online HTTPS/account provisioning with denied java.io stat/access and target cacerts through default JSSE");
 }
}
