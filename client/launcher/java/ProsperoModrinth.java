import com.google.gson.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.function.BooleanSupplier;

/** Instance-scoped Modrinth browser and checksum-verified download queue. */
final class ProsperoModrinth {
 static final String API="https://api.modrinth.com/v2/";
 enum Kind {MOD("mod","mods","Mods"),SHADER("shader","shaderpacks","Shaders"),RESOURCE("resourcepack","resourcepacks","Resource packs");final String type,folder,title;Kind(String t,String f,String n){type=t;folder=f;title=n;}}
 record Hit(String id,String title,String description,long downloads,String icon){Hit(String id,String t,String d,long n){this(id,t,d,n,"");}}
 record Results(List<Hit> hits,int total){}
 record Selection(String project,String title,Kind kind){}
 record File(String project,String version,Kind kind,String filename,ProsperoDownloads.Pin pin){}
 static final class Installed {ArrayList<File> files=new ArrayList<>();}
 final ProsperoDownloads download;
 ProsperoModrinth(){this(new ProsperoDownloads());}
 ProsperoModrinth(ProsperoDownloads download){this.download=download;}
 static void id(String id)throws IOException {if(id==null||!id.matches("[A-Za-z0-9_-]{1,80}"))throw new IOException("Invalid Modrinth identifier");}
 static String array(String s){return new Gson().toJson(List.of(s));}
 Results search(Kind kind,String game,String loader,String query,int offset,BooleanSupplier cancel)throws Exception {
  ProsperoFabric.game(game);if(query.length()>80||offset<0||offset>100000)throw new IOException("Invalid content search");
  if(kind==Kind.MOD&&!loader.equals("fabric"))return new Results(List.of(),0);
  var facets=new ArrayList<List<String>>();facets.add(List.of("project_type:"+kind.type));facets.add(List.of("versions:"+game));
  if(kind==Kind.MOD){facets.add(List.of("categories:fabric"));facets.add(List.of("client_side:required","client_side:optional"));}
  String url=API+"search?index=downloads&limit=6&offset="+offset+"&query="+ProsperoDownloads.encode(query)+"&facets="+ProsperoDownloads.encode(new Gson().toJson(facets));
  var data=download.json(url,cancel).getAsJsonObject();ArrayList<Hit> hits=new ArrayList<>();
  for(var item:data.getAsJsonArray("hits")){var row=item.getAsJsonObject();String project=row.get("project_id").getAsString();id(project);hits.add(new Hit(project,row.get("title").getAsString(),ProsperoDownloads.text(row,"description"),row.get("downloads").getAsLong(),ProsperoDownloads.text(row,"icon_url")));if(hits.size()==6)break;}
  return new Results(List.copyOf(hits),data.get("total_hits").getAsInt());
 }
 // Installed lists use the actual instance folders, including manually added files.
 record Local(String title,String filename,String project,Kind kind){}
 List<Local> local(Path game,Kind kind)throws Exception {
  var receipt=installed(game);Path folder=game.resolve(kind.folder);ProsperoDownloads.noLinks(folder);
  if(!Files.isDirectory(folder))return List.of();var found=new ArrayList<Local>();
  try(var files=Files.list(folder)){for(Path p:files.limit(1025).toList()){
   if(found.size()>=1024)throw new IOException("Too many installed files");String name=p.getFileName().toString();
   if(!Files.isRegularFile(p,LinkOption.NOFOLLOW_LINKS)||!name.endsWith(kind==Kind.MOD?".jar":".zip"))continue;
   var known=receipt.files.stream().filter(f->f.kind==kind&&f.filename.equals(name)).findFirst();
   found.add(new Local(name,name,known.isPresent()?known.get().project:"",kind));
  }}found.sort(Comparator.comparing(Local::title,String.CASE_INSENSITIVE_ORDER));return List.copyOf(found);
 }
 String icon(Path game,String project,String url,BooleanSupplier cancel){
  if(project.isEmpty())return "";
  try{id(project);Path path=state(game,"content-icons").resolve(project+".txt");ProsperoDownloads.noLinks(path);
   if(Files.isRegularFile(path)&&Files.size(path)==1536){String saved=Files.readString(path);if(saved.matches("[a-f0-9]{1536}"))return saved;}
   if(url.isEmpty())url=ProsperoDownloads.text(download.json(API+"project/"+project,cancel).getAsJsonObject(),"icon_url");
   if(url.isEmpty())return "";ProsperoDownloads.safe(url);if(!java.net.URI.create(url).getHost().equals("cdn.modrinth.com"))return "";
   String pixels=ProsperoAvatar.icon(download.bytes(url,1024*1024,cancel));ProsperoInstall.save(path,pixels);return pixels;
  }catch(Exception unavailable){return "";}
 }
 static Path state(Path game,String file)throws IOException {Path p=game.getParent().resolve(file);ProsperoDownloads.noLinks(p);return p;}
 List<Selection> queue(Path game)throws Exception {
  Path path=state(game,"content-queue.json");if(!Files.exists(path))return List.of();if(Files.size(path)>256*1024)throw new IOException("Content queue is too large");
  var result=new ArrayList<Selection>();for(var item:JsonParser.parseString(Files.readString(path)).getAsJsonArray()){
   Selection s=new Gson().fromJson(item,Selection.class);if(s==null||s.kind==null||s.title==null)throw new IOException("Invalid content queue");id(s.project);result.add(s);if(result.size()>128)throw new IOException("Content queue is full");
  }return List.copyOf(result);
 }
 synchronized void toggle(Path game,Selection selection)throws Exception {
  id(selection.project);var list=new ArrayList<>(queue(game));boolean removed=list.removeIf(s->s.project.equals(selection.project)&&s.kind==selection.kind);
  if(!removed){if(list.size()>=128)throw new IOException("Download queue is full");list.add(selection);}ProsperoInstall.save(state(game,"content-queue.json"),new Gson().toJson(list));
 }
 JsonObject version(String project,String pinned,Kind kind,String game,BooleanSupplier cancel)throws Exception {
  id(project);JsonObject version;
  if(!pinned.isEmpty()){id(pinned);version=download.json(API+"version/"+pinned,cancel).getAsJsonObject();}
  else{
   String filter=kind==Kind.MOD?"&loaders="+ProsperoDownloads.encode(array("fabric")):"";
   var versions=download.json(API+"project/"+project+"/version?game_versions="+ProsperoDownloads.encode(array(game))+filter+"&include_changelog=false",cancel).getAsJsonArray();
   if(versions.isEmpty())throw new IOException("No compatible download for "+project+" on "+game);
   version=versions.get(0).getAsJsonObject();
  }
  if(!project.equals(ProsperoDownloads.text(version,"project_id"))||!ProsperoDownloads.contains(version,"game_versions",game)||(kind==Kind.MOD&&!ProsperoDownloads.contains(version,"loaders","fabric")))throw new IOException("Content version is incompatible with this instance");
  if("unsupported".equals(ProsperoDownloads.text(version,"client_side"))||ProsperoDownloads.text(version,"environment").matches("server_only|dedicated_server_only|server_only_client_optional"))throw new IOException("This download is server-only");
  return version;
 }
 File file(JsonObject version,Kind kind)throws Exception {
  JsonObject selected=null;for(var item:version.getAsJsonArray("files")){var f=item.getAsJsonObject();if(selected==null)selected=f;if(f.has("primary")&&f.get("primary").getAsBoolean()){selected=f;break;}}
  if(selected==null)throw new IOException("Content has no downloadable file");String name=selected.get("filename").getAsString();
  if(!name.matches("[A-Za-z0-9_.+() -]{1,180}")||name.startsWith(".")||!name.endsWith(kind==Kind.MOD?".jar":".zip"))throw new IOException("Unsupported content filename");
  String project=version.get("project_id").getAsString(),id=version.get("id").getAsString();id(project);id(id);
  JsonObject hashes=selected.getAsJsonObject("hashes");String algorithm=hashes.has("sha512")?"SHA-512":"SHA-1",hash=hashes.get(algorithm.equals("SHA-512")?"sha512":"sha1").getAsString();
  return new File(project,id,kind,name,new ProsperoDownloads.Pin(selected.get("url").getAsString(),algorithm,hash,selected.get("size").getAsLong()));
 }
 private void resolve(Selection s,String pinned,String game,LinkedHashMap<String,File> plan,Set<String> active,List<JsonObject> versions,BooleanSupplier cancel)throws Exception {
  String key=s.kind+":"+s.project;File prior=plan.get(key);if(prior!=null){if(!pinned.isEmpty()&&!pinned.equals(prior.version))throw new IOException("Required mod versions conflict");return;}
  if(plan.size()+active.size()>=128)throw new IOException("Too many required dependencies");if(!active.add(key))throw new IOException("Dependency cycle in Modrinth metadata");
  var v=version(s.project,pinned,s.kind,game,cancel);File f=file(v,s.kind);versions.add(v);
  if(v.has("dependencies"))for(var element:v.getAsJsonArray("dependencies")){
   var dep=element.getAsJsonObject();if(!"required".equals(ProsperoDownloads.text(dep,"dependency_type")))continue;
   String project=ProsperoDownloads.text(dep,"project_id"),id=ProsperoDownloads.text(dep,"version_id");
   if(project.isEmpty()&&!id.isEmpty()){ProsperoModrinth.id(id);project=download.json(API+"version/"+id,cancel).getAsJsonObject().get("project_id").getAsString();}
   if(project.isEmpty())throw new IOException("A required dependency needs manual installation");
   // Modrinth libraries required by Fabric mods are mods, never desktop natives.
   if(s.kind!=Kind.MOD)throw new IOException("This pack has required dependencies; install them separately first");
   resolve(new Selection(project,project,Kind.MOD),id,game,plan,active,versions,cancel);
  }
  active.remove(key);plan.put(key,f);
 }
 Installed installed(Path game)throws Exception {
  Path path=state(game,"content-installed.json");if(!Files.exists(path))return new Installed();if(Files.size(path)>1024*1024)throw new IOException("Content receipt too large");
  Installed r=new Gson().fromJson(Files.readString(path),Installed.class);if(r==null||r.files==null||r.files.size()>1024)throw new IOException("Invalid content receipt");return r;
 }
 void downloadAll(Path game,String gameVersion,String loader,ProsperoInstall.Progress progress,BooleanSupplier cancel)throws Exception {downloadAll(game,gameVersion,loader,progress,cancel,f->{});}
 void downloadAll(Path game,String gameVersion,String loader,ProsperoInstall.Progress progress,BooleanSupplier cancel,java.util.function.Consumer<File> current)throws Exception {
  var selected=queue(game);if(selected.isEmpty())throw new IOException("Select something for the queue first");
  if(!loader.equals("fabric")&&selected.stream().anyMatch(s->s.kind==Kind.MOD))throw new IOException("Mods require a Fabric instance");
  LinkedHashMap<String,File> plan=new LinkedHashMap<>();ArrayList<JsonObject> versions=new ArrayList<>();
  for(var s:selected){progress.update("Resolving "+s.title,0,1);resolve(s,"",gameVersion,plan,new HashSet<>(),versions,cancel);}
  Installed receipt=installed(game);
  for(var v:versions)if(v.has("dependencies"))for(var item:v.getAsJsonArray("dependencies")){
   var d=item.getAsJsonObject();if(!"incompatible".equals(ProsperoDownloads.text(d,"dependency_type")))continue;
   String project=ProsperoDownloads.text(d,"project_id"),id=ProsperoDownloads.text(d,"version_id");
   if(plan.values().stream().anyMatch(f->f.project.equals(project)||( !id.isEmpty()&&f.version.equals(id)))||receipt.files.stream().anyMatch(f->f.project.equals(project)||(!id.isEmpty()&&f.version.equals(id))))throw new IOException("Selected content conflicts with another installed or queued mod");
  }
  Set<Path> targets=new HashSet<>();for(File f:plan.values()){
   Path target=game.resolve(f.kind.folder).resolve(f.filename);ProsperoDownloads.noLinks(target);if(!targets.add(target))throw new IOException("Two downloads use the same filename");
   if(Files.exists(target)&&!ProsperoDownloads.hash(target,f.pin.algorithm()).equals(f.pin.hash()))throw new IOException("Existing content uses "+f.filename+". Keep or remove it before downloading.");
   for(File old:receipt.files)if(old.project.equals(f.project)&&old.kind==f.kind&&!old.version.equals(f.version))throw new IOException("Another version is already installed. Keep it or remove it before adding a new version.");
  }
  // Resolve and verify every body before publishing any newly downloaded file.
  Path stage=game.getParent().resolve("content-downloads");long total=plan.values().stream().mapToLong(f->f.pin.size()).sum(),done=0;
  for(File f:plan.values()){ProsperoInstall.active(cancel);current.accept(f);progress.update("Downloading "+f.filename,done,total);download.obtain(f.pin,stage.resolve(f.pin.hash()+".bin"),cancel);done+=f.pin.size();progress.update("Downloading "+f.filename,done,total);}
  for(File f:plan.values()){
   ProsperoInstall.active(cancel);Path target=game.resolve(f.kind.folder).resolve(f.filename);ProsperoDownloads.noLinks(target);Files.createDirectories(target.getParent());
   if(!Files.exists(target)){Path part=target.resolveSibling(f.filename+".part");ProsperoDownloads.noLinks(part);try{Files.copy(stage.resolve(f.pin.hash()+".bin"),part,StandardCopyOption.REPLACE_EXISTING);ProsperoInstall.active(cancel);Files.move(part,target);}finally{Files.deleteIfExists(part);}}
   receipt.files.removeIf(old->old.project.equals(f.project)&&old.kind==f.kind);receipt.files.add(f);
   ProsperoInstall.save(state(game,"content-installed.json"),new Gson().toJson(receipt));
  }
  ProsperoInstall.active(cancel);ProsperoInstall.save(state(game,"content-queue.json"),"[]");
  for(File f:plan.values())Files.deleteIfExists(stage.resolve(f.pin.hash()+".bin"));progress.update("Downloads complete",total,total);
 }
}
