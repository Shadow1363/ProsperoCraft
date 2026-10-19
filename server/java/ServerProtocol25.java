/** Exercise the real gameplay protocol's cold metadata path after readiness. */
public final class ServerProtocol25 {
 public static void check()throws Exception {
  Class<?> protocols=Class.forName("net.minecraft.network.protocol.game.GameProtocols",true,ClassLoader.getSystemClassLoader());
  for(String field:new String[]{"SERVERBOUND_TEMPLATE","CLIENTBOUND_TEMPLATE"})if(protocols.getField(field).get(null)==null)throw new IllegalStateException("Missing real gameplay protocol template: "+field);
  System.out.println("MC_GAME_PROTOCOL_OK actual serverbound/clientbound templates initialized; no client admission claimed");
 }
}
