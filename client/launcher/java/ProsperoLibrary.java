import com.google.gson.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;

/** Persistent instance metadata; display names are never used as directory names. */
public final class ProsperoLibrary {
 static final String[] ICONS={"Crafting table","Grass","Amethyst","Ocean","Redstone","Forest","Gold","Snow"};
 static final int GAME_WIDTH=1920,GAME_HEIGHT=1080,LOCKED_RESOLUTION=2;
 static final class Instance {String id=UUID.randomUUID().toString(),name,version;int icon;boolean ready;Instance(String n,String v,int i){name=clean(n);version=v;icon=i;}}
 static final class Settings {int resolution=LOCKED_RESOLUTION,workers=4;boolean reducedMotion=false,snapshots=false,showIntro=true;}
 static final class State {int schema=1;ArrayList<Instance> instances=new ArrayList<>();Settings settings=new Settings();}
 final Path root;private State state;
 ProsperoLibrary(Path root)throws Exception {
  this.root=root;Files.createDirectories(root);Path file=root.resolve("library.json");
  if(Files.isRegularFile(file)){
   try{if(Files.size(file)>1024*1024)throw new IOException();state=new Gson().fromJson(Files.readString(file),State.class);validate();}
   catch(Exception bad){throw new IOException("Library data could not be read. Your instance folders are preserved.");}
  }else state=new State();
  recoverInterruptedMoves();
  // Preserve the legacy0/1/2field, but migrate every valid older library to1080p.
  if(state.settings.resolution!=LOCKED_RESOLUTION)save();
 }
 static String clean(String name){String value=name==null?"":name.strip();if(value.isEmpty()||value.length()>40||!value.matches("[A-Za-z0-9 ._()!+-]+"))throw new IllegalArgumentException("Use1-40 letters, numbers, spaces or ._()!+-");return value;}
 private void validate()throws Exception {
  if(state==null||state.schema!=1||state.instances==null||state.settings==null||state.instances.size()>256)throw new IOException();Set<String> ids=new HashSet<>();
  for(var i:state.instances){if(i==null||!i.id.matches("[a-f0-9-]{36}")||!ids.add(i.id)||!i.version.matches("26\\.[0-9][A-Za-z0-9._-]{0,70}")||i.icon<0||i.icon>=ICONS.length)throw new IOException();clean(i.name);}
  if(state.settings.resolution<0||state.settings.resolution>LOCKED_RESOLUTION||state.settings.workers<1||state.settings.workers>6)throw new IOException();
 }
 synchronized List<Instance> instances(){return List.copyOf(state.instances);}
 synchronized Settings settings(){return state.settings;}
 synchronized Instance add(String name,String version,int icon)throws Exception {
  if(state.instances.size()>=256)throw new IOException("This library is full");if(!version.matches("26\\.[0-9][A-Za-z0-9._-]{0,70}")||icon<0||icon>=ICONS.length)throw new IOException("Invalid instance choice");
  Instance instance=new Instance(name,version,icon);Files.createDirectories(game(instance));state.instances.add(instance);try{save();}catch(Exception error){state.instances.remove(instance);throw error;}return instance;
 }
 Path game(Instance i){return root.resolve("instances").resolve(i.id).resolve("game");}
 // Each deletion archives the complete UUID folder, with its original metadata.
 // No shared cache or account files are moved; failures restore the live entry.
 private Path trash(){return root.resolve("trash/instances");}
 private static void noLink(Path path)throws IOException{if(Files.isSymbolicLink(path))throw new IOException("Instance storage contains an unexpected link");}
 synchronized Path delete(Instance instance)throws Exception {
  int at=state.instances.indexOf(instance);if(at<0)throw new IOException("Instance is no longer in this library");
  noLink(root.resolve("instances"));noLink(trash().getParent());noLink(trash());
  Path source=game(instance).getParent();noLink(source);
  Path archive=trash().resolve(System.currentTimeMillis()+"-"+instance.id+"-"+UUID.randomUUID());Files.createDirectories(archive);
  ProsperoInstall.save(archive.resolve("instance.json"),new Gson().toJson(instance));
  Files.writeString(archive.resolve("deleted"),"1");
  boolean moved=Files.exists(source,LinkOption.NOFOLLOW_LINKS);
  if(moved)Files.move(source,archive.resolve("files"));else Files.createDirectory(archive.resolve("files"));
  state.instances.remove(at);
  try{save();}catch(Exception failure){state.instances.add(at,instance);if(moved)try{Files.move(archive.resolve("files"),source);}catch(Exception rollback){failure.addSuppressed(rollback);}try{if(!moved||!Files.exists(archive.resolve("files"),LinkOption.NOFOLLOW_LINKS))Files.deleteIfExists(archive.resolve("deleted"));}catch(Exception cleanup){failure.addSuppressed(cleanup);}throw failure;}
  return archive;
 }
 // Complete neither half of a crashed move: roll it back to the persisted library.
 private void recoverInterruptedMoves()throws Exception {
  noLink(root.resolve("instances"));noLink(trash().getParent());noLink(trash());if(!Files.isDirectory(trash()))return;
  try(var entries=Files.list(trash())){for(Path folder:entries.toList()){
   if(Files.isSymbolicLink(folder)||!Files.isRegularFile(folder.resolve("deleted")))continue;
   noLink(folder.resolve("instance.json"));if(Files.size(folder.resolve("instance.json"))>8192)throw new IOException("Invalid deleted instance metadata");
   Instance instance=new Gson().fromJson(Files.readString(folder.resolve("instance.json")),Instance.class);
   if(instance==null||instance.id==null||!instance.id.matches("[a-f0-9-]{36}"))throw new IOException("Invalid deleted instance metadata");
   Path files=folder.resolve("files"),live=game(instance).getParent();noLink(files);noLink(live);
   boolean listed=state.instances.stream().anyMatch(i->i.id.equals(instance.id));
   if(listed&&Files.isDirectory(files)){
    if(Files.exists(live,LinkOption.NOFOLLOW_LINKS))throw new IOException("Interrupted deletion has conflicting folders. Both copies are kept.");
    Files.createDirectories(live.getParent());Files.move(files,live);Files.delete(folder.resolve("deleted"));
   }else if(listed&&!Files.exists(files,LinkOption.NOFOLLOW_LINKS))Files.delete(folder.resolve("deleted"));
   else if(!listed&&!Files.exists(files,LinkOption.NOFOLLOW_LINKS)&&Files.isDirectory(live))Files.move(live,files);
  }}
 }
 synchronized Path latestDeleted(){
  try{noLink(trash().getParent());noLink(trash());if(!Files.isDirectory(trash()))return null;
   try(var entries=Files.list(trash())){return entries.filter(p->!Files.isSymbolicLink(p)&&Files.isRegularFile(p.resolve("deleted"))&&Files.isDirectory(p.resolve("files"))).max(Comparator.comparing(p->p.getFileName().toString())).orElse(null);}
  }catch(Exception unavailable){return null;}
 }
 synchronized Instance restore(Path archive)throws Exception {
  Path base=trash().toAbsolutePath().normalize(),folder=archive.toAbsolutePath().normalize();
  if(!base.equals(folder.getParent())||state.instances.size()>=256)throw new IOException("Cannot restore this instance");
  noLink(trash().getParent());noLink(trash());noLink(folder);noLink(folder.resolve("files"));noLink(root.resolve("instances"));noLink(folder.resolve("instance.json"));
  if(!Files.isRegularFile(folder.resolve("deleted"))||Files.size(folder.resolve("instance.json"))>8192)throw new IOException("Invalid deleted instance");
  Instance instance=new Gson().fromJson(Files.readString(folder.resolve("instance.json")),Instance.class);
  if(instance==null||instance.id==null||!instance.id.matches("[a-f0-9-]{36}")||instance.version==null||!instance.version.matches("26\\.[0-9][A-Za-z0-9._-]{0,70}")||instance.icon<0||instance.icon>=ICONS.length)throw new IOException("Invalid deleted instance");clean(instance.name);
  if(state.instances.stream().anyMatch(i->i.id.equals(instance.id)))throw new IOException("This instance is already present");
  Path destination=game(instance).getParent();if(Files.exists(destination,LinkOption.NOFOLLOW_LINKS))throw new IOException("Instance folder already exists. It was kept.");
  Files.createDirectories(destination.getParent());Files.move(folder.resolve("files"),destination);state.instances.add(instance);
  try{save();}catch(Exception failure){state.instances.remove(instance);try{Files.move(destination,folder.resolve("files"));}catch(Exception rollback){failure.addSuppressed(rollback);}throw failure;}
  Files.delete(folder.resolve("deleted"));return instance;
 }
 synchronized void rename(Instance i,String name)throws Exception{String before=i.name;i.name=clean(name);try{save();}catch(Exception error){i.name=before;throw error;}}
 synchronized void icon(Instance i,int icon)throws Exception{if(icon<0||icon>=ICONS.length)throw new IOException("Invalid icon");int before=i.icon;i.icon=icon;try{save();}catch(Exception error){i.icon=before;throw error;}}
 synchronized void ready(Instance i,boolean value)throws Exception{i.ready=value;save();}
 synchronized void save()throws Exception {
  validate();state.settings.resolution=LOCKED_RESOLUTION;Path file=root.resolve("library.json");if(Files.isRegularFile(file))Files.copy(file,root.resolve("library.json.backup"),StandardCopyOption.REPLACE_EXISTING);ProsperoInstall.save(file,new GsonBuilder().setPrettyPrinting().create().toJson(state));
 }
}
