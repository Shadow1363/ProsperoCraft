import java.lang.reflect.Method;
import java.util.List;

/** Read-only server-thread samples. Never changes inventory, food or use state. */
public final class ServerGameplay25 {
 private static final boolean ENABLED=Boolean.getBoolean("ps5.mc.gameplayDiagnostics");
 private static boolean failed,wasUsing;
 private static Object previousPlayer;
 private static long started,previousTickAt,gapTotal,gapMax;
 private static int gapSamples,slowGaps;
 private static int startTick,lastCount=-1,lastFood=-1;
 private static Method playerList,players,tick,using,remaining,use,main,off,food,foodLevel,saturation,count,item;
 private static Method method(String owner,String name)throws Exception{return Class.forName(owner).getMethod(name);}
 private static void initialize()throws Exception {
  playerList=method("net.minecraft.server.MinecraftServer","getPlayerList");tick=method("net.minecraft.server.MinecraftServer","getTickCount");
  players=method("net.minecraft.server.players.PlayerList","getPlayers");
  String living="net.minecraft.world.entity.LivingEntity";
  using=method(living,"isUsingItem");remaining=method(living,"getUseItemRemainingTicks");use=method(living,"getUseItem");main=method(living,"getMainHandItem");off=method(living,"getOffhandItem");
  food=method("net.minecraft.world.entity.player.Player","getFoodData");foodLevel=method("net.minecraft.world.food.FoodData","getFoodLevel");saturation=method("net.minecraft.world.food.FoodData","getSaturationLevel");
  count=method("net.minecraft.world.item.ItemStack","getCount");item=method("net.minecraft.world.item.ItemStack","getItem");
  System.out.println("MC_ITEM_USE_READY read-only server-thread hook");
 }
 private static String stack(Object stack)throws Exception{return item.invoke(stack)+"x"+count.invoke(stack);}
 private static void sampleTickGap() {
  long now=System.nanoTime();
  if(previousTickAt!=0){long gap=now-previousTickAt;gapTotal+=gap;gapMax=Math.max(gapMax,gap);if(gap>100_000_000L)slowGaps++;
   if(++gapSamples==100){System.out.println("MC_TICK_GAP samples="+gapSamples+" meanMicros="+(gapTotal/gapSamples/1000)+" maxMillis="+(gapMax/1_000_000)+" over100Millis="+slowGaps);gapSamples=slowGaps=0;gapTotal=gapMax=0;}
  }
  previousTickAt=now;
 }
 public static void tick(Object server) {
  ServerOperators25.tick(server);
  if(!ENABLED||failed)return;
  try {
   sampleTickGap();
   if(playerList==null)initialize();
   List<?> list=(List<?>)players.invoke(playerList.invoke(server));
   if(list.isEmpty()){previousPlayer=null;wasUsing=false;return;}
   Object player=list.get(0); // Sample one player to bound diagnostic overhead; OP policy checks every admitted player.
   if(player!=previousPlayer){previousPlayer=player;wasUsing=false;lastCount=-1;lastFood=-1;}
   boolean active=(boolean)using.invoke(player);int now=(int)tick.invoke(server);
   boolean transition=active!=wasUsing;
   if(active&&!wasUsing){started=System.nanoTime();startTick=now;}
   if(transition||(active?now%8==0:now%20==0)) {
    Object data=food.invoke(player),held=main.invoke(player);int level=(int)foodLevel.invoke(data),amount=(int)count.invoke(held);
    if(active||transition||amount!=lastCount||level!=lastFood)System.out.println("MC_ITEM_USE tick="+now+" using="+active+" remaining="+remaining.invoke(player)+" use="+stack(use.invoke(player))+" main="+stack(held)+" off="+stack(off.invoke(player))+" food="+level+" saturation="+saturation.invoke(data)+" use_ticks="+(started==0?0:now-startTick)+" use_ms="+(started==0?0:(System.nanoTime()-started)/1_000_000));
    lastCount=amount;lastFood=level;
   }
   wasUsing=active;
  }catch(Throwable error){failed=true;System.out.println("MC_ITEM_USE_UNAVAILABLE "+error);}
 }
}
