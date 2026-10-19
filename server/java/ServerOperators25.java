import com.google.gson.*;
import java.io.IOException;
import java.nio.file.*;
import java.util.*;

/** Authorized policy via vanilla ops.json; no game-thread hook or replacement. */
public final class ServerOperators25 {
 private static volatile boolean ready;
 public static void prepare(Path root)throws Exception {
  if(!Boolean.getBoolean("ps5.mc.opAll"))return;
  if(!Files.readString(root.resolve("server.properties")).contains("online-mode=true\n")||!Files.readString(root.resolve("server.properties")).contains("white-list=true\n"))throw new IOException("OP policy requires online authentication and whitelist");
  Path whitelist=root.resolve("whitelist.json"),ops=root.resolve("ops.json");
  if((Files.exists(whitelist)&&Files.size(whitelist)>262144)||(Files.exists(ops)&&Files.size(ops)>262144))throw new IOException("Policy file exceeds256KiB");
  JsonArray admitted=Files.exists(whitelist)?JsonParser.parseString(Files.readString(whitelist)).getAsJsonArray():new JsonArray();
  Map<UUID,JsonObject> entries=new LinkedHashMap<>();
  if(Files.exists(ops))for(JsonElement value:JsonParser.parseString(Files.readString(ops)).getAsJsonArray()) {
   JsonObject entry=value.getAsJsonObject();entries.put(UUID.fromString(entry.get("uuid").getAsString()),entry);
  }
  for(JsonElement value:admitted) {
   JsonObject source=value.getAsJsonObject();UUID id=UUID.fromString(source.get("uuid").getAsString());String name=source.get("name").getAsString();
   if(!name.matches("[A-Za-z0-9_]{3,16}"))throw new IOException("Invalid whitelisted player name");
   JsonObject entry=new JsonObject();entry.addProperty("uuid",id.toString());entry.addProperty("name",name);entry.addProperty("level",4);entry.addProperty("bypassesPlayerLimit",false);entries.put(id,entry);
  }
  JsonArray result=new JsonArray();entries.values().forEach(result::add);
  Path temporary=Files.createTempFile(root,".ops-policy-",".json");
  try {
   Files.writeString(temporary,new GsonBuilder().setPrettyPrinting().create().toJson(result));
   try{Files.move(temporary,ops,StandardCopyOption.REPLACE_EXISTING,StandardCopyOption.ATOMIC_MOVE);}
   catch(AtomicMoveNotSupportedException unsupported){Files.move(temporary,ops,StandardCopyOption.REPLACE_EXISTING);}
  }finally{Files.deleteIfExists(temporary);}
  ready=true;System.out.println("MC_OP_READY level4 for startup whitelist via vanilla ops.json; player-limit bypass=false");
 }
 public static void requireReady()throws Exception {
  if(Boolean.getBoolean("ps5.mc.opAll")&&!ready)throw new IOException("Vanilla ops.json was not prepared");
 }
}
