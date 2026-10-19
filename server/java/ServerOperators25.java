import com.google.gson.*;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;

/** Explicit user policy: level-4 OP for authenticated, whitelisted players. */
public final class ServerOperators25 {
 private static final boolean ENABLED=Boolean.getBoolean("ps5.mc.opAll");
 private static volatile boolean ready;private static volatile String failure;
 private static int steps;
 private static Method getList,getPlayers,getProfile,isOp,isAllowed,op,permissions;
 private static Constructor<?> fromProfile,fromIdentity;
 private static Object list;
 private static void grant(Object server,Object identity,boolean force)throws Exception {
  if(!(boolean)isAllowed.invoke(list,identity))throw new IllegalStateException("OP policy refused non-whitelisted identity");
  if(force||!(boolean)isOp.invoke(list,identity)){
   op.invoke(list,identity,Optional.of(permissions.invoke(server)),Optional.of(false));
   if(!(boolean)isOp.invoke(list,identity))throw new IllegalStateException("Vanilla OP grant did not persist");
   System.out.println("MC_OP_GRANTED whitelisted identity; configured permission level; player-limit bypass=false");
  }
 }
 public static void tick(Object server){
  if(!ENABLED||failure!=null)return;
  try{
   if(!ready){
    Class<?> serverClass=Class.forName("net.minecraft.server.MinecraftServer"),listClass=Class.forName("net.minecraft.server.players.PlayerList"),identity=Class.forName("net.minecraft.server.players.NameAndId");
    if(!(boolean)serverClass.getMethod("usesAuthentication").invoke(server))throw new IllegalStateException("OP policy requires online authentication");
    getList=serverClass.getMethod("getPlayerList");list=getList.invoke(server);
    if(!(boolean)listClass.getMethod("isUsingWhitelist").invoke(list))throw new IllegalStateException("OP policy requires whitelist");
    isAllowed=listClass.getMethod("isWhiteListed",identity);isOp=listClass.getMethod("isOp",identity);
    op=listClass.getMethod("op",identity,Optional.class,Optional.class);permissions=serverClass.getMethod("operatorUserPermissions");
    getPlayers=listClass.getMethod("getPlayers");getProfile=Class.forName("net.minecraft.world.entity.player.Player").getMethod("getGameProfile");
    fromProfile=identity.getConstructor(Class.forName("com.mojang.authlib.GameProfile"));fromIdentity=identity.getConstructor(UUID.class,String.class);
    Path file=Path.of(System.getProperty("ps5.mc.workdir",System.getProperty("user.dir"))).resolve("whitelist.json");
    if(Files.exists(file)){
     if(Files.size(file)>262144)throw new IllegalStateException("Whitelist exceeds256KiB");
     JsonArray entries=JsonParser.parseString(Files.readString(file)).getAsJsonArray();
     for(JsonElement value:entries){JsonObject entry=value.getAsJsonObject();grant(server,fromIdentity.newInstance(UUID.fromString(entry.get("uuid").getAsString()),entry.get("name").getAsString()),true);}
    }
    ready=true;System.out.println("MC_OP_READY level4 policy for online whitelisted players; vanilla APIs/persistence");
   }
   if(++steps%20!=0)return;
   for(Object player:(List<?>)getPlayers.invoke(list))grant(server,fromProfile.newInstance(getProfile.invoke(player)),false);
  }catch(Throwable error){failure=error.toString();System.out.println("MC_OP_POLICY_FAILED "+failure);}
 }
 public static void requireReady()throws Exception{
  if(!ENABLED)return;long deadline=System.nanoTime()+5_000_000_000L;
  while(!ready&&failure==null&&System.nanoTime()<deadline)Thread.sleep(25);
  if(!ready||failure!=null)throw new IllegalStateException("Operator policy unavailable: "+failure);
 }
}
