import java.nio.file.*;
import java.util.*;

/** Controller model. Native UI is independent; downloads and authentication use workers. */
public final class ProsperoLauncher {
 static final int FIELD_COUNT=96;
 private int feedbackSerial;private String feedbackCue="";
 private void feedback(String cue){feedbackCue=cue;feedbackSerial=feedbackSerial==Integer.MAX_VALUE?1:feedbackSerial+1;cached=null;}
 static final String[] BACKGROUNDS={"Gradient","Aurora","Grid","Stars","Waves","Bokeh","Phosphor","Paper","Dots","Vista"};
 interface Menu {boolean show();}
 private static ProsperoLauncher current;
 private final ProsperoAuth auth;private final ProsperoLibrary library;private final ProsperoInstall installer;
 private int dropdownKind,dropdownChoice,dropdownReturn,dropdownRow;
 private int selected=0,page=12,tab=0,row=0,generation=0,versionChoice=0,draftIcon=1,key=0,keyboardReturn=1;
 private boolean launchPrepared=false,awaitingTutorial=false;
 private boolean top=false,busy=false,launch=false,lowercase=false,customName=false;private String task="",message="",code="",uri="",draftName="",keyboard="",originalText="";
 private List<ProsperoInstall.Version> versions=List.of();private ProsperoLibrary.Instance detail;
 private int guideReturn=12,guideTab=0,guideSection=0;private boolean guideTop=false;private List<ProsperoDestinations.Entry> destinations=List.of();private ProsperoLibrary.Favorite quickPlay;private ProsperoOfflineAccount offlineAccount;private boolean offlineLaunch;
 private String avatar="";private final ProsperoAccountStore accounts;
 private ProsperoAuth.Session session;private Thread worker;private long completed,total,lastProgress;private String[] cached;
 private ProsperoInstall.Receipt receipt;private java.net.URLClassLoader loader;
 ProsperoLauncher(ProsperoAuth auth)throws Exception{this(auth,Path.of(System.getProperty("ps5.launcher.root","/download0/ProsperoCraft")),null);}
 ProsperoLauncher(ProsperoAuth auth,Path root,ProsperoInstall.Source source)throws Exception{this.auth=auth;library=new ProsperoLibrary(root);accounts=new ProsperoAccountStore(root);offlineAccount=ProsperoOfflineAccount.load(root,System.currentTimeMillis());installer=source==null?new ProsperoInstall(root.resolve("cache")):new ProsperoInstall(root.resolve("cache"),source);if(library.settings().showIntro&&!Boolean.getBoolean("ps5.launcher.resume")){page=7;row=1;}if(ProsperoChannel.tempGameTest()&&accounts.exists())restoreAccount();}
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
 private void runTask(String kind,Job job){if(busy){message="A task is running. Circle cancels it.";return;}busy=true;task=kind;int attempt=++generation;worker=new Thread(()->{try{job.run(attempt);}catch(Exception failure){synchronized(this){if(generation==attempt){message=failure instanceof ProsperoAuth.Failure?failure.getMessage():friendly(failure);feedback("error");System.err.println("PS5_LAUNCHER task="+kind+" result=FAILED storageCode="+(failure instanceof java.io.IOException io?ProsperoStorage.code(io):"NONE"));}}}finally{synchronized(this){if(generation==attempt||worker==Thread.currentThread()){busy=false;task="";code="";uri="";cached=null;}}}},"ProsperoCraft "+kind);worker.setDaemon(true);worker.start();}
 interface Job{void run(int attempt)throws Exception;}
 private static String friendly(Exception error){if(error instanceof java.io.IOException io&&java.util.Set.of("ENOSPC","QUOTA").contains(ProsperoStorage.code(io)))return "App storage is full. Refresh the loader metadata and relaunch; this build requests4GiB.";if(error instanceof IllegalArgumentException)return "Use1-40 letters, numbers, spaces or ._()!+-";if(error instanceof java.io.IOException)return error.getMessage()==null?"Storage or download error. Retry when ready.":error.getMessage();return "This action could not finish. Your worlds are kept. Try again.";}
 private synchronized boolean cancelled(int attempt){return attempt!=generation;}
 private String defaultName(String version){String base="Vanilla "+version;if(base.length()>34)base=base.substring(0,34);String name=base;int n=2;var existing=library.instances().stream().map(i->i.name).toList();while(existing.contains(name))name=base+" ("+(n++)+")";return name;}
 private void catalog(){message="Getting available26.x versions";runTask("CATALOG",attempt->{var result=installer.catalog(library.settings().snapshots,()->cancelled(attempt));synchronized(this){if(!cancelled(attempt)){versions=result;versionChoice=0;if(draftName.isEmpty()&&!versions.isEmpty())draftName=defaultName(versions.get(0).id());message="Choose a version, name and icon.";cached=null;}}});}
 private ProsperoAuth.View accountView(int attempt){return new ProsperoAuth.View(){public void stage(String text){synchronized(ProsperoLauncher.this){if(!cancelled(attempt)){message=text;cached=null;}}}public void code(String value,String address){synchronized(ProsperoLauncher.this){if(!cancelled(attempt)){code=value;uri=address;cached=null;}}}};}
 private void acceptAccount(ProsperoAuth.Session result,int attempt)throws Exception {
  synchronized(this){if(cancelled(attempt))return;session=result;avatar="";message="Connected. Owned Minecraft Java is ready to play.";feedback("success");cached=null;try{accounts.save(auth.refreshCredential(result));}catch(Exception storage){message="Connected. Account could not be saved on this console.";}}
  String face="";try{face=ProsperoAvatar.fetch(auth.skin(result));if(face.isEmpty()&&auth.skin(result).isEmpty())face=ProsperoAvatar.defaultFace(library.root,result.id);}catch(Exception unavailable){}
  synchronized(this){if(!cancelled(attempt)&&session==result){avatar=face;cached=null;}}
 }
 private void restoreAccount(){runTask("ACCOUNT",attempt->{String refresh=accounts.load();if(refresh.isEmpty())return;try{acceptAccount(auth.resume(refresh,accountView(attempt),()->cancelled(attempt)),attempt);}catch(ProsperoAuth.Failure failure){if(failure.code.equals("DECLINED")||failure.code.equals("REGISTRATION"))accounts.clear();throw failure;}});}
 private void signIn(){if(busy)return;message="Connecting to Microsoft";runTask("AUTH",attempt->acceptAccount(auth.signIn(accountView(attempt),()->cancelled(attempt)),attempt));}

 private void install(boolean play){if(detail==null||busy)return;var instance=detail;message="Preparing "+instance.version;completed=0;total=1;runTask("DOWNLOAD",attempt->{
  ProsperoInstall.Version version=versions.stream().filter(v->v.id().equals(instance.version)).findFirst().orElse(null);
  if(version==null)version=installer.catalog(true,()->cancelled(attempt)).stream().filter(v->v.id().equals(instance.version)).findFirst().orElseThrow(()->new java.io.IOException("This version is not in the publisher catalog"));
  var installed=installer.install(version,library.settings().workers,(text,done,size)->{synchronized(this){if(!cancelled(attempt)){completed=done;total=size;long now=System.currentTimeMillis();if(now-lastProgress>100||done==size){message=text;lastProgress=now;cached=null;}}}},()->cancelled(attempt));
  synchronized(this){if(!cancelled(attempt)){library.ready(instance,true);if(session!=null&&avatar.isEmpty()&&auth.skin(session).isEmpty())try{avatar=ProsperoAvatar.defaultFace(library.root,session.id);}catch(Exception ignored){}message="Download complete. Ready for your next world.";feedback("success");if(play)prepareLaunch(instance,installed);cached=null;}}
 });}
 private void prepareLaunch(ProsperoLibrary.Instance instance,ProsperoInstall.Receipt installed)throws Exception {prepareLaunch(instance,installed,false);}
 private void prepareLaunch(ProsperoLibrary.Instance instance,ProsperoInstall.Receipt installed,boolean offline)throws Exception {
  if(offline&&(!ProsperoChannel.offline()||offlineAccount==null||!offlineAccount.valid(System.currentTimeMillis())))throw new java.io.IOException("Offline profile expired. Verify your account again on your computer.");
  if(ProsperoChannel.tempGameTest()&&!offline&&(session==null||!session.valid(System.currentTimeMillis())))throw new java.io.IOException("Sign in with an owning Microsoft account before playing the full game.");
  if(!supported(instance.version)||!"SDL".equals(installed.window)){message="Coming soon for this version. Downloads are kept.";return;}
  installer.verify(installed);receipt=installed;loader=installer.loader(installed);detail=instance;offlineLaunch=offline;launchPrepared=true;launch=!awaitingTutorial;message="Starting "+instance.name;
 }
 static boolean supported(String version){return version.equals("26.3");}
 private void play(){if(detail==null||busy)return;if(!supported(detail.version)){message="Coming soon. Only26.3 can launch on this build.";feedback("error");return;}if(ProsperoChannel.tempGameTest()&&(session==null||!session.valid(System.currentTimeMillis()))){page=3;tab=3;top=false;row=0;signIn();return;}awaitingTutorial=ProsperoChannel.tempGameTest()&&library.settings().showControls;if(awaitingTutorial){page=11;row=1;top=false;launchPrepared=false;}if(!detail.ready){install(true);return;}var instance=detail;runTask("VERIFY",attempt->{var installed=installer.receipt(instance.version);installer.verify(installed);synchronized(this){if(!cancelled(attempt))prepareLaunch(instance,installed);}});}
 private void playOffline(){
  if(detail==null||busy)return;
  if(!ProsperoChannel.offline()){message="This is the Demo branch.";return;}
  offlineAccount=ProsperoOfflineAccount.load(library.root,System.currentTimeMillis());
  if(offlineAccount==null){message="A verified offline profile is required. Export it from your computer.";return;}
  if(!supported(detail.version)||!detail.ready){message="Download the supported26.3 instance before playing offline.";return;}
  var instance=detail;runTask("VERIFY",attempt->{var installed=installer.receipt(instance.version);synchronized(this){if(!cancelled(attempt))prepareLaunch(instance,installed,true);}});
 }
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
  String[] before=state();int serial=feedbackSerial;String[] after=tickModel(buttons);
  if(buttons!=0&&serial==feedbackSerial){
   boolean changed=false;for(int at:new int[]{2,8,9,10,11,12,13,15,19,22,24,26,27,28,29,30,31,64,68,75,79})changed|=!before[at].equals(after[at]);
   if(changed)feedback((buttons&0x2000)!=0?"back":(buttons&0xf008)!=0?"confirm":"move");
  }
  return state();
 }
 private int tabPage(){return switch(tab){case 0->12;case 1->0;case 2->2;default->3;};}
 private void selectTab(int next){tab=Math.floorMod(next,4);page=tabPage();top=false;selected=0;row=0;cached=null;}
 private void createInstance(){quickPlay=null;page=1;tab=1;top=false;row=0;if(versions.isEmpty()&&!busy)catalog();}
 private void browse(ProsperoLibrary.Instance instance){if(busy){message="Wait for the current task, then open worlds and servers.";return;}detail=instance;page=14;selected=0;top=false;row=0;destinations=List.of();message="Reading worlds and saved servers";runTask("LIBRARY",attempt->{var entries=ProsperoDestinations.read(library.game(instance));synchronized(this){if(!cancelled(attempt)){destinations=entries;message=entries.isEmpty()?"No saved worlds or servers yet. Add them in Minecraft.":"Choose a world or server to pin on Home.";cached=null;}}});}
 private int cardCount(){return page==12?library.favorites().size()+1:library.instances().size()+1;}
 private void navigateCards(int buttons){int count=cardCount();if((buttons&0x80)!=0)selected=Math.max(0,selected-1);if((buttons&0x20)!=0)selected=Math.min(count-1,selected+1);if((buttons&0x10)!=0){if(selected<4)top=true;else selected-=4;}if((buttons&0x40)!=0)selected=Math.min(count-1,selected+4);}
 private List<String> choices(){return switch(dropdownKind){case 0->versions.stream().map(v->v.id()+(v.type().equals("snapshot")?"  [snapshot]":"")+(supported(v.id())?"":"  [Coming soon]")).toList();case 1,2->List.of(ProsperoLibrary.ICONS);case 3->java.util.stream.IntStream.range(0,ProsperoLibrary.RESOLUTIONS.length).mapToObj(ProsperoLibrary::resolutionLabel).toList();case 4->List.of("1","2","3","4","5","6");default->List.of(BACKGROUNDS);};}
 private void dropdown(int kind,int choice){dropdownKind=kind;dropdownChoice=choice;dropdownReturn=page;dropdownRow=row;page=10;row=choice;top=false;}
 private void choose()throws Exception {switch(dropdownKind){case 0->{versionChoice=row;if(!customName)draftName=defaultName(versions.get(row).id());}case 1->draftIcon=row;case 2->library.icon(detail,row);case 3->{library.settings().resolution=row;library.save();}case 4->{library.settings().workers=row+1;library.save();}case 5->{library.settings().background=row+1;library.save();}}page=dropdownReturn;row=dropdownRow;}
 private String[] tickModel(int buttons){
  try{
   if(page==10){int count=choices().size();if((buttons&0x10)!=0)row=Math.max(0,row-1);if((buttons&0x40)!=0)row=Math.min(count-1,row+1);if((buttons&0x80)!=0)row=Math.max(0,row-8);if((buttons&0x20)!=0)row=Math.min(count-1,row+8);if((buttons&0x2000)!=0){page=dropdownReturn;row=dropdownRow;}else if((buttons&0x4000)!=0&&count>0)choose();if(buttons!=0)cached=null;return state();}
   if(page==9){
    if((buttons&0x2000)!=0){page=5;row=3;}
    else if((buttons&0x4008)!=0&&busy){message="Wait for the current task before deleting an instance.";feedback("error");}
    else{if((buttons&0x90)!=0)row=0;if((buttons&0x60)!=0)row=1;
     if((buttons&0x4000)!=0){if(row==0){page=5;row=3;}else{boolean cleaned=library.delete(detail);detail=null;selected=0;page=0;tab=1;top=false;row=0;quickPlay=null;message=cleaned?"Instance and its worlds permanently deleted.":"Instance removed. Storage cleanup will finish on next launch.";}}}
    if(buttons!=0)cached=null;return state();
   }
   if(page==11){
    if((buttons&0x8)!=0){guideReturn=11;guideTab=tab;guideTop=top;guideSection=0;page=8;cached=null;return state();}
    if((buttons&0x80)!=0)row=1;if((buttons&0x20)!=0)row=0;
    if((buttons&0x2000)!=0){cancel();page=4;row=0;launchPrepared=false;awaitingTutorial=false;}
    else if((buttons&0x4000)!=0){if(row==0){library.settings().showControls=!library.settings().showControls;library.save();}else if(launchPrepared){awaitingTutorial=false;launch=true;}else message="Preparing Minecraft. Continue when loading is ready.";}
    if(buttons!=0)cached=null;return state();
   }
   if(page==7){if((buttons&0x80)!=0)row=1;if((buttons&0x20)!=0)row=0;if((buttons&0x4000)!=0){if(row==0){library.settings().showIntro=!library.settings().showIntro;library.save();}else{page=12;tab=0;row=0;}}if(buttons!=0)cached=null;return state();}
   if(page==8){if((buttons&0x2008)!=0){page=guideReturn;tab=guideTab;top=guideTop;}else if((buttons&0x20)!=0)guideSection=(guideSection+1)%5;else if((buttons&0x80)!=0)guideSection=Math.floorMod(guideSection-1,5);if(buttons!=0)cached=null;return state();}
   if(page==6){keyboard(buttons);if(buttons!=0)cached=null;return state();}
   if((buttons&0x8)!=0){guideReturn=page;guideTab=tab;guideTop=top;guideSection=0;page=8;cached=null;return state();}
   if((buttons&0xc00)!=0){selectTab(tab+((buttons&0x800)!=0?1:-1));return state();}
   if((buttons&0x2000)!=0){if(busy){cancel();message="Cancelled. Verified downloads are kept.";}if(page==14){page=13;selected=0;}else if(page==13){selectTab(0);}else{page=tabPage();top=false;row=0;selected=0;}cached=null;return state();}
   if(top){if((buttons&0xa0)!=0){selectTab(tab+((buttons&0x20)!=0?1:-1));return state();}if((buttons&0x4040)!=0){top=false;row=0;}cached=null;return state();}
   if(page==14){
    if((buttons&0x10)!=0)selected=Math.max(0,selected-1);if((buttons&0x40)!=0)selected=Math.min(Math.max(0,destinations.size()-1),selected+1);
    if((buttons&0x4000)!=0&&!busy&&!destinations.isEmpty()){library.toggleFavorite(detail,destinations.get(selected));message=library.favorite(detail,destinations.get(selected))?"Pinned on Home.":"Removed from Home.";}
    if(buttons!=0)cached=null;return state();
   }
   if(page==0||page==12||page==13){navigateCards(buttons);
    if((buttons&0x4000)!=0&&!top){
     if(page==12){var pins=library.favorites();if(selected==pins.size()){if(library.instances().isEmpty())createInstance();else{page=13;selected=0;}}else{quickPlay=pins.get(selected);detail=library.instances().stream().filter(i->i.id.equals(quickPlay.instance)).findFirst().orElseThrow();page=4;row=0;}}
     else if(selected==library.instances().size())createInstance();
     else if(page==13)browse(library.instances().get(selected));
     else{quickPlay=null;detail=library.instances().get(selected);page=4;row=0;}
    }
    if(buttons!=0)cached=null;return state();
   }
   if((buttons&0x10)!=0){if(row==0)top=true;else row--;}
   if((buttons&0x40)!=0)row=Math.min(page==1?3:page==2?4:page==3?1:page==4?5:page==5?3:2,row+1);
   if(page==4){int max=ProsperoChannel.offline()&&offlineAccount!=null?5:quickPlay!=null?4:3;row=Math.min(row,max);if(row==4&&quickPlay==null)row=(buttons&0x10)!=0?3:5;}
   int direction=(buttons&0x80)!=0?-1:(buttons&0x20)!=0?1:0;
   if(!top&&page==1&&direction!=0&&!busy){if(row==0&&!versions.isEmpty()){versionChoice=Math.floorMod(versionChoice+direction,versions.size());if(!customName)draftName=defaultName(versions.get(versionChoice).id());}if(row==2)draftIcon=Math.floorMod(draftIcon+direction,ProsperoLibrary.ICONS.length);}
   if(!top&&page==5&&row==1&&direction!=0)library.icon(detail,Math.floorMod(detail.icon+direction,ProsperoLibrary.ICONS.length));
   if(!top&&page==2&&direction!=0){var settings=library.settings();if(row==0){settings.resolution=Math.floorMod(settings.resolution+direction,ProsperoLibrary.RESOLUTIONS.length);};if(row==1)settings.workers=Math.max(1,Math.min(6,settings.workers+direction));if(row==2)settings.reducedMotion=!settings.reducedMotion;if(row==3){settings.snapshots=!settings.snapshots;versions=List.of();}if(row==4)settings.showIntro=!settings.showIntro;library.save();}
   if(!top&&page==2&&(buttons&0x1000)!=0){library.settings().vibration=!library.settings().vibration;library.save();}
   if(!top&&page==2&&(buttons&0x8000)!=0){dropdown(5,library.settings().background-1);cached=null;return state();}
   if((buttons&0x4000)!=0){
    if(!top&&page==1&&!busy){if(row==0){if(versions.isEmpty())catalog();else{dropdown(0,versionChoice);cached=null;return state();}}if(row==1)beginName(1);if(row==2){dropdown(1,draftIcon);cached=null;return state();}if(row==3){if(versions.isEmpty())throw new java.io.IOException("Choose a version first");detail=library.add(draftName,versions.get(versionChoice).id(),draftIcon);selected=library.instances().size()-1;page=4;row=0;install(false);customName=false;draftName=defaultName(versions.get(versionChoice).id());}}
    else if(page==2){var settings=library.settings();if(row==0){dropdown(3,settings.resolution);cached=null;return state();}if(row==1){dropdown(4,settings.workers-1);cached=null;return state();}if(row==2)settings.reducedMotion=!settings.reducedMotion;if(row==3){settings.snapshots=!settings.snapshots;versions=List.of();}if(row==4)settings.showIntro=!settings.showIntro;library.save();}
    else if(page==3){if(row==0)signIn();else{cancel();session=null;avatar="";accounts.clear();message="Signed out. Saved account removed from this console.";}}
    else if(!top&&page==4){if(row==0){play();cached=null;return state();}else if(row==1){page=5;row=0;}else if(row==2)install(false);else if(row==3){browse(detail);cached=null;return state();}else if(row==4&&quickPlay!=null){library.toggleFavorite(detail,new ProsperoDestinations.Entry(quickPlay.kind,quickPlay.target,quickPlay.name));quickPlay=null;message="Removed from Home.";}else if(row==5)playOffline();}
    else if(page==5){if(row==0)beginName(5);if(row==1){dropdown(2,detail.icon);cached=null;return state();}if(row==2){page=4;row=0;}if(row==3){if(busy){message="Wait for the current task before deleting an instance.";feedback("error");}else{page=9;row=0;}}}
   }
   if(buttons!=0)cached=null;
  }catch(Exception error){message=friendly(error);feedback("error");}
  return state();
 }
 private String[] state(){
  if(cached!=null)return cached;String[] f=new String[FIELD_COUNT];Arrays.fill(f,"");
  f[0]=page==12?"Home":"Instances";f[1]="";f[2]=message;f[3]=code;f[4]=uri;f[5]=session==null?"Not signed in":session.name;f[6]=detail!=null&&!supported(detail.version)?"COMING SOON":ProsperoChannel.tempGameTest()&&(session==null||!session.valid(System.currentTimeMillis()))?"PLAY - Sign in":detail!=null&&detail.ready?(ProsperoChannel.tempGameTest()?"PLAY":"PLAY DEMO"):"DOWNLOAD & PLAY";f[7]=page==14?"X Pin / unpin     CIRCLE Back":page==8?"LEFT / RIGHT Pages     CIRCLE Back":page==11||page==7?"LEFT / RIGHT Choose     X Confirm":page==9?"X Confirm     CIRCLE No":busy?"CIRCLE Cancel":"L1 / R1 Pages     X Select     CIRCLE Back     OPTIONS Controls";f[8]=busy?task:session==null?"MICROSOFT ACCOUNT":"CONNECTED";f[9]=""+selected;f[10]=launch?"LAUNCH":"WAIT";f[11]=""+page;f[12]=""+tab;f[13]=""+library.instances().size();f[14]=""+(selected/8*8);f[15]=""+(top?-1:row);f[16]=detail==null?"":detail.name;f[17]=detail==null?"":detail.version;f[18]=""+(detail==null?1:detail.icon);f[19]=detail==null?"":detail.ready?"READY":"NOT DOWNLOADED";f[20]=""+(total==0?0:Math.min(1000,completed*1000/total));f[21]=total>1?String.format(java.util.Locale.ROOT,"%.0f / %.0f MB",completed/1048576.0,total/1048576.0):"";f[22]=draftName;f[23]=versions.isEmpty()?"Select to refresh versions":versions.get(versionChoice).id();f[24]=""+draftIcon;f[25]=ProsperoLibrary.resolutionLabel(library.settings().resolution);f[26]=""+library.settings().workers;f[27]=library.settings().snapshots?"ON":"OFF";f[28]=top?"TOP":"CONTENT";f[29]=keyboard;f[30]=library.settings().reducedMotion?"ON":"OFF";f[31]=""+key;
  var all=library.instances();int start=selected/8*8;
  if(page==12){var pins=library.favorites();f[13]=""+(pins.size()+1);for(int i=0;i<8&&start+i<=pins.size();i++){int at=32+i*4;if(start+i==pins.size()){f[at]="";f[at+2]="-1";f[at+3]="ADD";}else{var pin=pins.get(start+i);var instance=all.stream().filter(n->n.id.equals(pin.instance)).findFirst().orElseThrow();f[at]=pin.name;f[at+1]=instance.name;f[at+2]=""+instance.icon;f[at+3]=pin.kind;}}}
  else {f[13]=""+(all.size()+1);for(int i=0;i<8&&start+i<=all.size();i++){int at=32+i*4;if(start+i==all.size()){f[at]="";f[at+2]="-1";f[at+3]="ADD";}else{var instance=all.get(start+i);f[at]=instance.name;f[at+1]=instance.version;f[at+2]=""+instance.icon;f[at+3]=!supported(instance.version)?"COMING SOON":instance.ready?"READY":"DOWNLOAD";}}}
  if(page==14){f[13]=""+destinations.size();f[14]=""+(selected/6*6);for(int i=0;i<8;i++)for(int j=0;j<4;j++)f[32+i*4+j]="";for(int i=0;i<6&&selected/6*6+i<destinations.size();i++){var e=destinations.get(selected/6*6+i);int at=32+i*4;f[at]=e.name();f[at+1]=e.kind();f[at+2]=e.target();f[at+3]=library.favorite(detail,e)?"PINNED":"";}}
  if(page==10){List<String> options=choices();int first=row/8*8;f[82]=switch(dropdownKind){case 0->"Choose version";case 1,2->"Choose instance icon";case 3->"Game resolution";case 4->"Parallel downloads";default->"Animated background";};f[83]=""+options.size();f[84]=""+first;for(int i=0;i<8&&first+i<options.size();i++)f[85+i]=options.get(first+i);f[93]=""+dropdownKind;}
  f[80]=avatar;f[81]=session==null?"Sign in":session.name;f[94]=library.settings().showControls?"ON":"OFF";f[95]=launchPrepared?"READY":"WAIT";
  f[77]=""+feedbackSerial;f[78]=feedbackCue;f[79]=library.settings().vibration?"ON":"OFF";
  f[75]=""+library.settings().background;f[76]=BACKGROUNDS[library.settings().background-1];
  f[73]=ProsperoChannel.label();f[74]=page==8?""+guideSection:quickPlay!=null?"FAVORITE":"";
  if(quickPlay!=null&&page==4)f[16]=quickPlay.name;
  f[71]=ProsperoChannel.offline()&&offlineAccount!=null&&offlineAccount.valid(System.currentTimeMillis())?"OFFLINE":"";f[72]=offlineAccount==null?"":offlineAccount.name;
  f[69]=detail!=null&&supported(detail.version)?"SUPPORTED":"PENDING";f[70]=versions.isEmpty()?"":supported(versions.get(versionChoice).id())?(ProsperoChannel.tempGameTest()?"26.3 full game requires Microsoft sign-in.":"26.3 demo can launch on this build."):"Download available. Play support coming soon.";f[68]=library.settings().showIntro?"ON":"OFF";f[67]="Data and downloads: "+library.root;f[66]=lowercase?"LOWER":"UPPER";f[64]=busy?"BUSY":"IDLE";f[65]=detail!=null&&!supported(detail.version)?"Download available. Play support coming soon.":(ProsperoChannel.tempGameTest()?"26.3 full game / native SDL gameplay":"26.3 demo / native SDL gameplay");if(quickPlay!=null&&page==4)f[65]=quickPlay.kind+" / "+detail.name;return cached=f;
 }
 synchronized String[] arguments(Path ignoredWork,Path ignoredAssets)throws Exception {
  if(!launch||detail==null||receipt==null)throw new IllegalStateException("No installed instance selected");
  if(offlineLaunch){if(!ProsperoChannel.offline())throw new java.io.IOException("Offline launch is unavailable in the Demo branch");offlineAccount=ProsperoOfflineAccount.load(library.root,System.currentTimeMillis());if(offlineAccount==null)throw new java.io.IOException("Offline profile needs verification");}
  boolean full=ProsperoChannel.tempGameTest()&&!offlineLaunch;
  if(full&&(session==null||!session.valid(System.currentTimeMillis())))throw new java.io.IOException("Your session expired. Sign in again before launching.");
  String player=full?session.name:offlineLaunch?offlineAccount.name:"PS5Demo",id=full?session.id:offlineLaunch?offlineAccount.id:UUID.nameUUIDFromBytes("OfflinePlayer:PS5Demo".getBytes(java.nio.charset.StandardCharsets.UTF_8)).toString();
  java.util.List<String> args=new java.util.ArrayList<>(java.util.List.of("--username",player,"--uuid",id,"--accessToken",full?session.accessToken():"0","--version",detail.version,"--versionType","release","--gameDir",library.game(detail).toString(),"--assetsDir",library.root.resolve("cache/assets").toString(),"--assetIndex",receipt.assetIndex,"--width",""+ProsperoLibrary.RESOLUTIONS[library.settings().resolution][0],"--height",""+ProsperoLibrary.RESOLUTIONS[library.settings().resolution][1]));if(!full){args.add(0,"--disableChat");args.add(0,"--disableMultiplayer");if(!offlineLaunch)args.add(0,"--demo");}if(full&&quickPlay!=null){if(!ProsperoDestinations.valid(quickPlay.kind,quickPlay.target))throw new java.io.IOException("Invalid Home favorite");java.util.Collections.addAll(args,quickPlay.kind.equals("WORLD")?"--quickPlaySingleplayer":"--quickPlayMultiplayer",quickPlay.target);}
  if("SDL".equals(receipt.window))java.util.Collections.addAll(args,"--graphicsBackend","vulkan");return args.toArray(String[]::new);
 }
 @Override public String toString(){return "ProsperoCraft launcher [credentials redacted]";}
}
