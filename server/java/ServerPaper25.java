import java.nio.file.*;
import java.security.MessageDigest;
import java.util.HexFormat;
/** Executes publisher-prepared Paper byte-for-byte; no project game rewrites. */
public final class ServerPaper25 {
 static void configureJavaPolicy() {
  int feature=Runtime.version().feature();
  if(feature!=25)throw new IllegalStateException("Paper probe requires actual Java25; feature="+feature);
  String version=System.getProperty("java.version","");
  if(version.contains("-")){
   System.setProperty("Paper.IgnoreJavaVersion","true");
   System.out.println("MC_PAPER_EXPERIMENTAL_JAVA version="+version+" feature="+feature+" upstream opt-in enabled; runtime is experimental, not an official GA build");
  }
 }
 public static void prepare(Path root)throws Exception {
  configureJavaPolicy();
  Path assets=Path.of(System.getProperty("ps5.mc.assets","/app0/assets/java25"));
  byte[] bytes=Files.readAllBytes(assets.resolve("paper-plugins/ps5-paper-smoke.jar"));
  String expected=Files.readString(assets.resolve("paper-plugins/ps5-paper-smoke.sha256")).trim();
  if(!HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes)).equals(expected))throw new SecurityException("Paper test plugin checksum mismatch");
  Files.createDirectories(root.resolve("plugins"));Files.write(root.resolve("plugins/ps5-paper-smoke.jar"),bytes);
  Files.createDirectories(root.resolve("config"));Path config=root.resolve("config/paper-global.yml");
  if(!Files.exists(config))Files.writeString(config,"spark:\n  enabled: false\n");
  Files.deleteIfExists(root.resolve("paper-stop-ready.txt"));
  System.setProperty("paper.disableStartupVersionCheck","true");
  System.out.println("MC_PAPER_PREPARED upstream build207; separate hash-verified plugin; spark disabled in initial config");
 }
 public static ClassLoader launch(Path root,String world)throws Exception {
  ClassLoader loader=ClassLoader.getSystemClassLoader();
  Class.forName("org.bukkit.craftbukkit.Main",true,loader).getMethod("main",String[].class).invoke(null,(Object)new String[]{"--nogui","--nojline","--universe",root.toString(),"--world",world,"--config",root.resolve("server.properties").toString(),"--plugins",root.resolve("plugins").toString(),"--paper-settings-directory",root.resolve("config").toString()});
  System.out.println("MC_PAPER_LOADER_OK upstream org.bukkit.craftbukkit.Main");return loader;
 }
 public static void armStop(Path root)throws Exception {
  Files.writeString(root.resolve("paper-stop-ready.txt"),"MC_PAPER_EXPECT_EXIT0 "+System.getProperty("ps5.probe.runId","host")+"\n");
  System.out.println("MC_PAPER_EXPECT_EXIT0 checks complete; stop will exit JVM normally; reopen app for reports");
 }
}
