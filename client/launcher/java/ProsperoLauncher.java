import java.nio.file.Path;
import java.util.*;

/** Controller UI state + in-memory account session. No token persistence. */
public final class ProsperoLauncher {
 interface Menu {boolean show();}
 private static ProsperoLauncher current;
 private final ProsperoAuth auth;
 private int selected=0,page=0,generation=0;
 private boolean busy=false,launch=false,demo=false;
 private String message="Pick your instance. Make it your world.",code="",uri="";
 private ProsperoAuth.Session session;
 private Thread worker;
 private String[] cached;
 ProsperoLauncher(ProsperoAuth auth){this.auth=auth;}
 static String[] run(Menu menu)throws Exception {
  current=new ProsperoLauncher(new ProsperoAuth());
  if(!menu.show()){current.cancel();throw new IllegalStateException("Launcher display handoff failed;game not started");}
  synchronized(current){if(!current.launch)throw new IllegalStateException("Launcher did not select a launch");}
  return current.arguments(Path.of("/download0/mc-client"),Path.of("/app0/assets/java25/game-assets"));
 }
 public static String[] nativeTick(int buttons){return current.tick(buttons);}
 synchronized void cancel(){generation++;busy=false;code="";uri="";if(worker!=null)worker.interrupt();worker=null;cached=null;}
 private synchronized void signIn(){
  if(busy)return;cancel();busy=true;message="Connecting to Microsoft";final int attempt=generation;
  worker=new Thread(()->{
   try{
    ProsperoAuth.Session result=auth.signIn(new ProsperoAuth.View(){
     public void stage(String text){synchronized(ProsperoLauncher.this){if(generation==attempt){message=text;cached=null;}}}
     public void code(String value,String address){synchronized(ProsperoLauncher.this){if(generation==attempt){code=value;uri=address;cached=null;}}}
    },()->{synchronized(ProsperoLauncher.this){return generation!=attempt;}});
    synchronized(ProsperoLauncher.this){if(generation==attempt){session=result;busy=false;code="";uri="";message="Welcome, "+result.name+". Your world is ready.";cached=null;}}
   }catch(ProsperoAuth.Failure failure){synchronized(ProsperoLauncher.this){if(generation==attempt){busy=false;code="";uri="";message=failure.getMessage();cached=null;}}}
  },"ProsperoCraft account sign-in");worker.setDaemon(true);worker.start();
 }
 synchronized String[] tick(int buttons){
  if((buttons&0x10)!=0){selected=(selected+4)%5;cached=null;}
  if((buttons&0x40)!=0){selected=(selected+1)%5;cached=null;}
  if((buttons&0x2000)!=0){cancel();page=0;message="Back home. Ready when you are.";}
  if((buttons&0x1000)!=0){cancel();session=null;message="Signed out on this console.";}
  if((buttons&0x8000)!=0){cancel();demo=true;launch=true;}
  if((buttons&0x4000)!=0){
   if(selected==4){cancel();demo=true;launch=true;}
   else if(selected==0){if(session!=null&&session.valid(System.currentTimeMillis())){launch=true;demo=false;}else signIn();}
   else if(selected==2){if(session==null||!session.valid(System.currentTimeMillis()))signIn();page=2;cached=null;}
   else{page=selected;cached=null;}
  }
  if(cached==null)cached=new String[]{
   "Your next world.","Starts right here.",message,code,uri,
   session==null?"Not signed in":session.name,
   session==null?"SIGN IN & PLAY":"PLAY JAVA 26.3",
   busy?"CIRCLE  Cancel sign-in":"SQUARE  Play demo     TRIANGLE  Sign out",
   busy?"SIGNING IN":session==null?"MICROSOFT ACCOUNT":"CONNECTED",
   Integer.toString(selected),launch?"LAUNCH":"WAIT",Integer.toString(page)
  };
  if(launch)cached[10]="LAUNCH";
  return cached;
 }
 synchronized String[] arguments(Path work,Path assets)throws Exception {
  if(!launch)throw new IllegalStateException("No launch selected");
  if(!demo&&(session==null||!session.valid(System.currentTimeMillis())))throw new IllegalStateException("Minecraft account session expired; sign in again");
  List<String> args=new ArrayList<>();
  if(demo)Collections.addAll(args,"--demo","--disableMultiplayer","--disableChat","--username","PS5Probe","--uuid",UUID.nameUUIDFromBytes("OfflinePlayer:PS5Probe".getBytes(java.nio.charset.StandardCharsets.UTF_8)).toString(),"--accessToken","0");
  else Collections.addAll(args,"--username",session.name,"--uuid",session.id,"--accessToken",session.accessToken(),"--clientId",ProsperoAuth.CLIENT_ID);
  Collections.addAll(args,"--version","26.3","--versionType","release","--gameDir",work.toString(),"--assetsDir",assets.toString(),"--assetIndex","34","--graphicsBackend","vulkan","--width","1280","--height","720");
  return args.toArray(String[]::new);
 }
 @Override public String toString(){return "ProsperoCraft launcher [credentials redacted]";}
}
