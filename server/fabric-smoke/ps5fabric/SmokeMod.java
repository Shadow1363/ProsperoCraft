package ps5fabric;
import net.fabricmc.api.ModInitializer;

/** No game hooks: prove a real server mod entrypoint is executed by Fabric. */
public final class SmokeMod implements ModInitializer {
 public void onInitialize() {
  if(!"server".equals(net.fabricmc.loader.api.FabricLoader.getInstance().getEnvironmentType().name().toLowerCase(java.util.Locale.ROOT)))throw new IllegalStateException("Server-only mod loaded outside server");
  System.out.println("PS5_FABRIC_SMOKE_OK id=ps5-fabric-smoke version=1.0.0 real server mod entrypoint");
 }
}
