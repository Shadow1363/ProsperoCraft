import java.nio.file.*;
import java.security.MessageDigest;
import java.util.HexFormat;

/** External Fabric launcher integration; never rewrites the official game JAR. */
public final class ServerFabric25 {
 public static void prepare(Path root)throws Exception {
  Path assets=Path.of(System.getProperty("ps5.mc.assets","/app0/assets/java25"));
  Path source=assets.resolve("fabric-mods/ps5-fabric-smoke.jar");
  String expected=Files.readString(assets.resolve("fabric-mods/ps5-fabric-smoke.sha256")).trim();
  byte[] bytes=Files.readAllBytes(source);
  if(!HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes)).equals(expected))throw new SecurityException("Fabric test mod checksum mismatch");
  Files.createDirectories(root.resolve("mods"));
  Files.write(root.resolve("mods/ps5-fabric-smoke.jar"),bytes);
  System.out.println("MC_FABRIC_PREPARED hash-verified server-only smoke mod; original game artifact unchanged");
 }
 public static ClassLoader launch(String[] args)throws Exception {
  Class.forName("net.fabricmc.loader.impl.launch.knot.KnotServer").getMethod("main",String[].class).invoke(null,(Object)args);
  Object launcher=Class.forName("net.fabricmc.loader.impl.launch.FabricLauncherBase").getMethod("getLauncher").invoke(null);
  ClassLoader loader=(ClassLoader)Class.forName("net.fabricmc.loader.impl.launch.FabricLauncher").getMethod("getTargetClassLoader").invoke(launcher);
  if(loader==null||loader==ClassLoader.getSystemClassLoader())throw new IllegalStateException("Fabric target loader not established");
  Thread.currentThread().setContextClassLoader(loader);
  Class<?> game=Class.forName("net.minecraft.server.MinecraftServer",false,loader);
  if(game.getClassLoader()!=loader)throw new IllegalStateException("Game did not load through Fabric target loader");
  System.out.println("MC_FABRIC_LOADER_OK gameLoader="+loader.getClass().getName());
  return loader;
 }
}
