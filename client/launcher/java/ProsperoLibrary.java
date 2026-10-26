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
 synchronized void rename(Instance i,String name)throws Exception{String before=i.name;i.name=clean(name);try{save();}catch(Exception error){i.name=before;throw error;}}
 synchronized void icon(Instance i,int icon)throws Exception{if(icon<0||icon>=ICONS.length)throw new IOException("Invalid icon");int before=i.icon;i.icon=icon;try{save();}catch(Exception error){i.icon=before;throw error;}}
 synchronized void ready(Instance i,boolean value)throws Exception{i.ready=value;save();}
 synchronized void save()throws Exception {
  validate();state.settings.resolution=LOCKED_RESOLUTION;Path file=root.resolve("library.json");if(Files.isRegularFile(file))Files.copy(file,root.resolve("library.json.backup"),StandardCopyOption.REPLACE_EXISTING);ProsperoInstall.save(file,new GsonBuilder().setPrettyPrinting().create().toJson(state));
 }
}
