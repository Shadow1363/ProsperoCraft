import java.nio.file.*;
import java.util.*;

/** Controller model. Native UI is independent; downloads and authentication use workers. */
public final class ProsperoLauncher {
 static final int FIELD_COUNT=80;
 interface Menu {boolean show();}
 private static ProsperoLauncher current;
 private final ProsperoAuth auth;private final ProsperoLibrary library;private final ProsperoInstall installer;
 private int selected=0,page=0,tab=0,row=0,generation=0,versionChoice=0,draftIcon=1,key=0,keyboardReturn=1;
 private boolean top=false,busy=false,launch=false,lowercase=false,customName=false;private String task="",message="",code="",uri="",draftName="",keyboard="",originalText="";
 private List<ProsperoInstall.Version> versions=List.of();private ProsperoLibrary.Instance detail;
 private ProsperoAuth.Session session;private Thread worker;private long completed,total,lastProgress;private String[] cached;
 private ProsperoInstall.Receipt receipt;private java.net.URLClassLoader loader;
 ProsperoLauncher(ProsperoAuth auth)throws Exception{this(auth,Path.of(System.getProperty("ps5.launcher.root","/download0/ProsperoCraft")),null);}
 ProsperoLauncher(ProsperoAuth auth,Path root,ProsperoInstall.Source source)throws Exception{this.auth=auth;library=new ProsperoLibrary(root);installer=source==null?new ProsperoInstall(root.resolve("cache")):new ProsperoInstall(root.resolve("cache"),source);if(library.settings().showIntro&&!Boolean.getBoolean("ps5.launcher.resume")){page=7;row=1;}}
 static String[] run(Menu menu)throws Exception {
  current=new ProsperoLauncher(new ProsperoAuth());
  if(!menu.show()){current.cancel();throw new IllegalStateException("Launcher display handoff failed;game not started");}
  synchronized(current){if(!current.launch)throw new IllegalStateException("No launch selected");}
  return current.arguments(null,null);
 }
 static Path selectedWork(){return current.library.game(current.detail);}
 static ClassLoader gameLoader(){return current.loader;}
 static boolean verifySelected()throws Exception{current.installer.verify(current.receipt);return true;}
 public static String[] nativeTick(int buttons){return current.tick(buttons);}
 synchronized void cancel(){generation++;code="";uri="";if(worker!=null&&worker.isAlive()){worker.interrupt();busy=true;task="STOPPING";}else{busy=false;task="";}cached=null;}
 private void runTask(String kind,Job job){if(busy){message="A task is running. Circle cancels it.";return;}busy=true;task=kind;int attempt=++generation;worker=new Thread(()->{try{job.run(attempt);}catch(Exception failure){synchronized(this){if(generation==attempt){message=failure instanceof ProsperoAuth.Failure?failure.getMessage():friendly(failure);System.err.println("PS5_LAUNCHER task="+kind+" result=FAILED storageCode="+(failure instanceof java.io.IOException io?ProsperoStorage.code(io):"NONE"));}}}finally{synchronized(this){if(generation==attempt||worker==Thread.currentThread()){busy=false;task="";code="";uri="";cached=null;}}}},"ProsperoCraft "+kind);worker.setDaemon(true);worker.start();}
 interface Job{void run(int attempt)throws Exception;}
 private static String friendly(Exception error){if(error instanceof java.io.IOException io&&java.util.Set.of("ENOSPC","QUOTA").contains(ProsperoStorage.code(io)))return "App storage is full. Refresh the loader metadata and relaunch; this build requests4GiB.";if(error instanceof IllegalArgumentException)return "Use1-40 letters, numbers, spaces or ._()!+-";if(error instanceof java.io.IOException)return error.getMessage()==null?"Storage or download error. Retry when ready.":error.getMessage();return "This action could not finish. Your worlds are kept. Try again.";}
 private synchronized boolean cancelled(int attempt){return attempt!=generation;}
 private String defaultName(String version){String base="Vanilla "+version;if(base.length()>34)base=base.substring(0,34);String name=base;int n=2;var existing=library.instances().stream().map(i->i.name).toList();while(existing.contains(name))name=base+" ("+(n++)+")";return name;}
 private void catalog(){message="Getting available26.x versions";runTask("CATALOG",attempt->{var result=installer.catalog(library.settings().snapshots,()->cancelled(attempt));synchronized(this){if(!cancelled(attempt)){versions=result;versionChoice=0;if(draftName.isEmpty()&&!versions.isEmpty())draftName=defaultName(versions.get(0).id());message="Choose a version, name and icon.";cached=null;}}});}
 private void signIn(){if(busy)return;message="Connecting to Microsoft";runTask("AUTH",attempt->{var result=auth.signIn(new ProsperoAuth.View(){public void stage(String text){synchronized(ProsperoLauncher.this){if(!cancelled(attempt)){message=text;cached=null;}}}public void code(String value,String address){synchronized(ProsperoLauncher.this){if(!cancelled(attempt)){code=value;uri=address;cached=null;}}}},()->cancelled(attempt));synchronized(this){if(!cancelled(attempt)){session=result;message="Connected. Demo instances keep their demo rules.";cached=null;}}});}
 private void install(boolean play){if(detail==null||busy)return;var instance=detail;message="Preparing "+instance.version;completed=0;total=1;runTask("DOWNLOAD",attempt->{
  ProsperoInstall.Version version=versions.stream().filter(v->v.id().equals(instance.version)).findFirst().orElse(null);
  if(version==null)version=installer.catalog(true,()->cancelled(attempt)).stream().filter(v->v.id().equals(instance.version)).findFirst().orElseThrow(()->new java.io.IOException("This version is not in the publisher catalog"));
  var installed=installer.install(version,library.settings().workers,(text,done,size)->{synchronized(this){if(!cancelled(attempt)){completed=done;total=size;long now=System.currentTimeMillis();if(now-lastProgress>100||done==size){message=text;lastProgress=now;cached=null;}}}},()->cancelled(attempt));
  synchronized(this){if(!cancelled(attempt)){library.ready(instance,true);message="Download complete. Ready for your next world.";if(play)prepareLaunch(instance,installed);cached=null;}}
 });}
 private void prepareLaunch(ProsperoLibrary.Instance instance,ProsperoInstall.Receipt installed)throws Exception {
  if(!supported(instance.version)||!"SDL".equals(installed.window)){message="Launch not available yet for this version. Native support is still being developed. Downloads are kept.";return;}
  installer.verify(installed);receipt=installed;loader=installer.loader(installed);detail=instance;launch=true;message="Starting "+instance.name;
 }
 static boolean supported(String version){return version.equals("26.3");}
 private void play(){if(detail==null||busy)return;if(!supported(detail.version)){message="Cannot launch this version yet. Only26.3 demo is currently supported.";return;}if(!detail.ready){install(true);return;}var instance=detail;runTask("VERIFY",attempt->{var installed=installer.receipt(instance.version);installer.verify(installed);synchronized(this){if(!cancelled(attempt))prepareLaunch(instance,installed);}});}
 private void beginName(int back){keyboardReturn=back;page=6;keyboard=back==5?detail.name:draftName;originalText=keyboard;key=0;}
 private void keyboard(int buttons)throws Exception {
  final String chars=lowercase?"abcdefghijklmnopqrstuvwxyz0123456789 ._-":"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ._-";
  if((buttons&0x100)!=0)lowercase=!lowercase;
  if((buttons&0x200)!=0&&keyboard.length()<40)keyboard+=" ";
  if((buttons&0x8)!=0)keyboard="";
  if((buttons&0x80)!=0)key=(key+39)%40;if((buttons&0x20)!=0)key=(key+1)%40;if((buttons&0x10)!=0)key=(key+30)%40;if((buttons&0x40)!=0)key=(key+10)%40;
  if((buttons&0x4000)!=0&&keyboard.length()<40)keyboard+=chars.charAt(key);
  if((buttons&0x1000)!=0&&!keyboard.isEmpty())keyboard=keyboard.substring(0,keyboard.length()-1);
  if((buttons&0x8000)!=0){if(keyboardReturn==5)library.rename(detail,keyboard);else{draftName=ProsperoLibrary.clean(keyboard);customName=true;}page=keyboardReturn;}
  if((buttons&0x2000)!=0){keyboard=originalText;page=keyboardReturn;}
 }
 synchronized String[] tick(int buttons){
  try{
   if(page==7){if((buttons&0x80)!=0)row=1;if((buttons&0x20)!=0)row=0;if((buttons&0x4000)!=0){if(row==0){library.settings().showIntro=!library.settings().showIntro;library.save();}else{page=0;row=0;}}if(buttons!=0)cached=null;return state();}
   if(page==8){if((buttons&0x2008)!=0){page=0;cached=null;}return state();}
   if(page==6){keyboard(buttons);if(buttons!=0)cached=null;return state();}
   if((buttons&0x8)!=0){page=8;cached=null;return state();}
   if((buttons&0x400)!=0||(buttons&0x800)!=0){tab=Math.floorMod(tab+((buttons&0x800)!=0?1:-1),3);top=true;page=0;row=0;cached=null;}
   if((buttons&0x2000)!=0){if(busy){cancel();message="Cancelled. Verified downloads are kept for retry.";}page=0;top=false;row=0;cached=null;}
   if(top&&(buttons&0xa0)!=0){tab=Math.floorMod(tab+((buttons&0x20)!=0?1:-1),3);cached=null;}
   if(page==0&&!top&&library.instances().isEmpty()&&(buttons&0x10)!=0){top=true;cached=null;}
   else if((buttons&0x40)!=0&&top){top=false;cached=null;}
   else if(page==0&&!top){int count=library.instances().size();if(count>0){if((buttons&0x80)!=0)selected=Math.max(0,selected-1);if((buttons&0x20)!=0)selected=Math.min(count-1,selected+1);if((buttons&0x10)!=0){if(selected<4)top=true;else selected-=4;}if((buttons&0x40)!=0)selected=Math.min(count-1,selected+4);}}
   else if(!top){if((buttons&0x10)!=0)row=Math.max(0,row-1);if((buttons&0x40)!=0)row=Math.min(page==1?3:page==2?4:page==3?1:page==4?2:2,row+1);}
   int direction=(buttons&0x80)!=0?-1:(buttons&0x20)!=0?1:0;
   if(!top&&page==1&&direction!=0&&!busy){if(row==0&&!versions.isEmpty()){versionChoice=Math.floorMod(versionChoice+direction,versions.size());if(!customName)draftName=defaultName(versions.get(versionChoice).id());}if(row==2)draftIcon=Math.floorMod(draftIcon+direction,ProsperoLibrary.ICONS.length);}
   if(!top&&page==5&&row==1&&direction!=0)library.icon(detail,Math.floorMod(detail.icon+direction,ProsperoLibrary.ICONS.length));
   if(!top&&page==2&&direction!=0){var settings=library.settings();if(row==0)message="Game resolution is locked to1080p for aligned pointer clicks.";if(row==1)settings.workers=Math.max(1,Math.min(6,settings.workers+direction));if(row==2)settings.reducedMotion=!settings.reducedMotion;if(row==3){settings.snapshots=!settings.snapshots;versions=List.of();}if(row==4)settings.showIntro=!settings.showIntro;library.save();}
   if((buttons&0x4000)!=0){
    if(top){page=tab+1;top=false;row=0;if(page==1&&versions.isEmpty()&&!busy)catalog();}
    else if(page==0){if(library.instances().isEmpty()){page=1;tab=0;row=0;if(versions.isEmpty()&&!busy)catalog();}else{detail=library.instances().get(selected);page=4;row=0;}}
    else if(page==1&&!busy){if(row==0){if(versions.isEmpty())catalog();else{versionChoice=(versionChoice+1)%versions.size();if(!customName)draftName=defaultName(versions.get(versionChoice).id());}}if(row==1)beginName(1);if(row==2)draftIcon=(draftIcon+1)%ProsperoLibrary.ICONS.length;if(row==3){if(versions.isEmpty())throw new java.io.IOException("Choose a version first");detail=library.add(draftName,versions.get(versionChoice).id(),draftIcon);selected=library.instances().size()-1;page=4;row=0;install(false);customName=false;draftName=defaultName(versions.get(versionChoice).id());}}
    else if(page==2){var settings=library.settings();if(row==0)message="Game resolution is locked to1080p for aligned pointer clicks.";if(row==1)settings.workers=settings.workers%6+1;if(row==2)settings.reducedMotion=!settings.reducedMotion;if(row==3){settings.snapshots=!settings.snapshots;versions=List.of();}if(row==4)settings.showIntro=!settings.showIntro;library.save();}
    else if(page==3){if(row==0)signIn();else{cancel();session=null;message="Signed out on this console.";}}
    else if(page==4){if(row==0)play();if(row==1){page=5;row=0;}else if(row==2)install(false);}
    else if(page==5){if(row==0)beginName(5);if(row==1)library.icon(detail,(detail.icon+1)%ProsperoLibrary.ICONS.length);if(row==2){page=4;row=0;}}
   }
   if(buttons!=0)cached=null;
  }catch(Exception error){message=friendly(error);cached=null;}
  return state();
 }
 private String[] state(){
  if(cached!=null)return cached;String[] f=new String[FIELD_COUNT];Arrays.fill(f,"");
  f[0]="Instances";f[1]="";f[2]=message;f[3]=code;f[4]=uri;f[5]=session==null?"Not signed in":session.name;f[6]=detail!=null&&!supported(detail.version)?"LAUNCH NOT AVAILABLE YET":detail!=null&&detail.ready?"PLAY DEMO":"DOWNLOAD & PLAY";f[7]=page==7?"D-PAD / STICK LEFT / RIGHT  Choose     X  Select / toggle":page==8?"CIRCLE / OPTIONS  Back":busy?"CIRCLE  Cancel task":"L1 / R1  Top bar     D-PAD / STICK  Navigate     X  Select     CIRCLE  Back     OPTIONS  Controls";f[8]=busy?task:session==null?"MICROSOFT ACCOUNT":"CONNECTED";f[9]=""+selected;f[10]=launch?"LAUNCH":"WAIT";f[11]=""+page;f[12]=""+tab;f[13]=""+library.instances().size();f[14]=""+(selected/8*8);f[15]=""+row;f[16]=detail==null?"":detail.name;f[17]=detail==null?"":detail.version;f[18]=""+(detail==null?1:detail.icon);f[19]=detail==null?"":detail.ready?"READY":"NOT DOWNLOADED";f[20]=""+(total==0?0:Math.min(1000,completed*1000/total));f[21]=total>1?String.format(java.util.Locale.ROOT,"%.0f / %.0f MB",completed/1048576.0,total/1048576.0):"";f[22]=draftName;f[23]=versions.isEmpty()?"Select to refresh versions":versions.get(versionChoice).id();f[24]=""+draftIcon;f[25]="1920 x 1080 (locked)";f[26]=""+library.settings().workers;f[27]=library.settings().snapshots?"ON":"OFF";f[28]=top?"TOP":"CONTENT";f[29]=keyboard;f[30]=library.settings().reducedMotion?"ON":"OFF";f[31]=""+key;
  var all=library.instances();int start=selected/8*8;for(int i=0;i<8&&start+i<all.size();i++){var instance=all.get(start+i);int at=32+i*4;f[at]=instance.name;f[at+1]=instance.version;f[at+2]=""+instance.icon;f[at+3]=!supported(instance.version)?"NOT YET":instance.ready?"READY":"DOWNLOAD";}
  f[69]=detail!=null&&supported(detail.version)?"SUPPORTED":"PENDING";f[70]=versions.isEmpty()?"":supported(versions.get(versionChoice).id())?"26.3 demo can launch on this build.":"Download available. This version cannot launch yet.";f[68]=library.settings().showIntro?"ON":"OFF";f[67]="Data and downloads: "+library.root;f[66]=lowercase?"LOWER":"UPPER";f[64]=busy?"BUSY":"IDLE";f[65]=detail!=null&&!supported(detail.version)?"Download available. Launch support is not ready yet.":"26.3 demo / native SDL gameplay";return cached=f;
 }
 synchronized String[] arguments(Path ignoredWork,Path ignoredAssets)throws Exception {
  if(!launch||detail==null||receipt==null)throw new IllegalStateException("No installed instance selected");
  java.util.List<String> args=new java.util.ArrayList<>(java.util.List.of("--demo","--disableMultiplayer","--disableChat","--username","PS5Demo","--uuid",UUID.nameUUIDFromBytes("OfflinePlayer:PS5Demo".getBytes(java.nio.charset.StandardCharsets.UTF_8)).toString(),"--accessToken","0","--version",detail.version,"--versionType","release","--gameDir",library.game(detail).toString(),"--assetsDir",library.root.resolve("cache/assets").toString(),"--assetIndex",receipt.assetIndex,"--width",""+ProsperoLibrary.GAME_WIDTH,"--height",""+ProsperoLibrary.GAME_HEIGHT));if("SDL".equals(receipt.window))java.util.Collections.addAll(args,"--graphicsBackend","vulkan");return args.toArray(String[]::new);
 }
 @Override public String toString(){return "ProsperoCraft launcher [credentials redacted]";}
}
