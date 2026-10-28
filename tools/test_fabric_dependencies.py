#!/usr/bin/env python3
"""Actual upstream predicates plus manifest/nested-module dependency auto downloads."""
from pathlib import Path
import subprocess,json,shutil
ROOT=Path(__file__).resolve().parents[1];JDK=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home');w=ROOT/'build/dependencies108-test';w.mkdir(exist_ok=True)
loader=ROOT/'build/content103-live/cache/fabric/libraries/net/fabricmc/fabric-loader/0.20.1/fabric-loader-0.20.1.jar'
source=r'''
import com.google.gson.*;import java.nio.file.*;import java.io.*;import java.util.*;import java.util.zip.*;import java.security.*;
public class DependencyCheck {
 static Map<String,byte[]> network=new HashMap<>();static int reads;
 static byte[] bytes(String s){return s.getBytes(java.nio.charset.StandardCharsets.UTF_8);}
 static byte[] jar(String id,String version,String depends,byte[] nested)throws Exception {var out=new ByteArrayOutputStream();try(var z=new ZipOutputStream(out)){z.putNextEntry(new ZipEntry("fabric.mod.json"));z.write(bytes("{\"id\":\""+id+"\",\"version\":\""+version+"\",\"depends\":"+depends+(nested==null?"":",\"jars\":[{\"file\":\"META-INF/jars/keys.jar\"}]")+"}"));z.closeEntry();if(nested!=null){z.putNextEntry(new ZipEntry("META-INF/jars/keys.jar"));z.write(nested);z.closeEntry();}}return out.toByteArray();}
 static void version(String project,String version,String filename,byte[] jar,String deps)throws Exception {String url="https://cdn.modrinth.com/data/"+project+"/"+filename;network.put(url,jar);String hash=HexFormat.of().formatHex(MessageDigest.getInstance("SHA-512").digest(jar));String metadata="{\"id\":\""+version+"\",\"project_id\":\""+project+"\",\"game_versions\":[\"26.3\"],\"loaders\":[\"fabric\"],\"dependencies\":"+deps+",\"files\":[{\"filename\":\""+filename+"\",\"url\":\""+url+"\",\"primary\":true,\"size\":"+jar.length+",\"hashes\":{\"sha512\":\""+hash+"\"}}]}";network.put("meta:"+project,bytes("["+metadata+"]"));network.put(ProsperoModrinth.API+"version/"+version,bytes(metadata));}
 static InputStream open(String url)throws Exception{reads++;byte[] b=network.get(url);if(b==null&&url.contains("/project/"))b=network.get("meta:"+url.split("/project/")[1].split("/")[0]);if(b==null)throw new IOException("Unexpected request "+url);return new ByteArrayInputStream(b);}
 static void check(boolean yes,String why){if(!yes)throw new AssertionError(why);}
 public static void main(String[]args)throws Exception {Path root=Path.of(args[0]),game=root.resolve("game");Files.createDirectories(game);Files.writeString(game.resolve("world-marker"),"KEEP");
  try(var versions=new ProsperoDependencies.Versions(Path.of(args[1]),"0.20.1")){
   check(versions.accepts("0.20.1",List.of(">=0.18.4"))&&versions.accepts("26.3",List.of("~26.3"))&&!versions.accepts("1.0.0",List.of(">=2")),"official version predicates");
   byte[] mod=jar("vitrail","0.13.0-beta","{\"fabric-key-mapping-api-v1\":\"*\",\"minecraft\":\"~26.3\",\"java\":\">=25\"}",null);
   byte[] api=jar("fabric-api","0.165.0+26.3","{\"fabricloader\":\">=0.18\"}",jar("fabric-key-mapping-api-v1","3.0.0","{}",null));
   version("vitrail","vRoot","vitrail.jar",mod,"[]");version("P7dR8mSH","vAPI","fabric-api.jar",api,"[]");
   var client=new ProsperoModrinth(new ProsperoDownloads(DependencyCheck::open));client.toggle(game,new ProsperoModrinth.Selection("vitrail","Vitrail",ProsperoModrinth.Kind.MOD));
   client.downloadAll(game,"26.3","fabric",(m,d,t)->{},()->false,f->{},versions);
   check(Files.exists(game.resolve("mods/fabric-api.jar"))&&client.installed(game).files.size()==2&&client.queue(game).isEmpty(),"JAR-only required Fabric API not installed");
   check(ProsperoDependencies.missing(List.of(game.resolve("mods/vitrail.jar"),game.resolve("mods/fabric-api.jar")),"26.3",versions).isEmpty(),"nested API module not recognized");
   Path bundled=game.resolve("mods/bundled.jar");Files.write(bundled,jar("bundled","1.0.0","{}",jar("fabric-key-mapping-api-v1","2.0.0","{}",null)));
   var variants=new ArrayList<Path>(List.of(game.resolve("mods/vitrail.jar"),game.resolve("mods/fabric-api.jar"),bundled));check(ProsperoDependencies.missing(variants,"26.3",versions).isEmpty(),"compatible nested provider versions rejected");Files.delete(bundled);
   int before=reads;client.repair(game,"26.3","fabric",versions,(m,d,t)->{},()->false,false);check(reads==before,"healthy launch used network");
   var entry=client.local(game,ProsperoModrinth.Kind.MOD).stream().filter(i->i.project().equals("P7dR8mSH")).findFirst().orElseThrow();client.uninstall(game,entry);
   try{client.repair(game,"26.3","fabric",versions,(m,d,t)->{},()->false,true);throw new AssertionError("offline missing dependency allowed");}catch(IOException expected){}
   client.repair(game,"26.3","fabric",versions,(m,d,t)->{},()->false,false);check(Files.exists(game.resolve("mods/fabric-api.jar")),"old instance repair failed");
   Files.delete(game.resolve("mods/fabric-api.jar"));client.repair(game,"26.3","fabric",versions,(m,d,t)->{},()->false,false);check(Files.exists(game.resolve("mods/fabric-api.jar")),"missing dependency with retained receipt not restored");
   check(Files.readString(game.resolve("world-marker")).equals("KEEP"),"world changed");
   byte[] conflict=jar("other","1.0.0","{\"fabric-key-mapping-api-v1\":\">=99\"}",null);Files.write(game.resolve("mods/conflict.jar"),conflict);
   try{client.repair(game,"26.3","fabric",versions,(m,d,t)->{},()->false,false);throw new AssertionError("wrong dependency version accepted");}catch(IOException expected){check(expected.getMessage().contains("installed 3.0.0"),"conflict not explained");}
   check(Arrays.equals(conflict,Files.readAllBytes(game.resolve("mods/conflict.jar"))),"conflict overwritten");Files.delete(game.resolve("mods/conflict.jar"));
   byte[] unknown=jar("unknown","1.0","{\"unmapped-library\":\"*\"}",null);version("unknown","vUnknown","unknown.jar",unknown,"[]");client.toggle(game,new ProsperoModrinth.Selection("unknown","Unknown",ProsperoModrinth.Kind.MOD));
   try{client.downloadAll(game,"26.3","fabric",(m,d,t)->{},()->false,f->{},versions);throw new AssertionError("missing unknown dependency allowed");}catch(IOException expected){check(expected.getMessage().contains("unmapped-library"),"missing dependency not named");}
   check(!Files.exists(game.resolve("mods/unknown.jar"))&&client.queue(game).size()==1,"unresolved dependency published or queue lost");

   version("sodium","oldSodium","sodium-old.jar",jar("sodium","0.9.2","{}",null),"[]");
   version("unused","unusedVersion","unused.jar",jar("unused","1.0","{}",null),"[]");
   version("sodium","newSodium","sodium-new.jar",jar("sodium","0.9.3-beta.1","{}",null),"[{\"project_id\":\"unused\",\"version_id\":\"unusedVersion\",\"dependency_type\":\"required\"}]");
   version("iris","irisVersion","iris.jar",jar("iris","1.11.7","{\"sodium\":\"0.9.x\"}",null),"[{\"project_id\":\"sodium\",\"version_id\":\"oldSodium\",\"dependency_type\":\"required\"}]");
   for(boolean reverse:List.of(false,true)){
    Path fresh=root.resolve("queue-"+reverse+"/game");Files.createDirectories(fresh);
    for(String project:reverse?List.of("sodium","iris"):List.of("iris","sodium"))client.toggle(fresh,new ProsperoModrinth.Selection(project,project,ProsperoModrinth.Kind.MOD));
    client.downloadAll(fresh,"26.3","fabric",(m,d,t)->{},()->false,f->{},versions);
    check(Files.exists(fresh.resolve("mods/iris.jar"))&&Files.exists(fresh.resolve("mods/sodium-old.jar"))&&!Files.exists(fresh.resolve("mods/sodium-new.jar"))&&!Files.exists(fresh.resolve("mods/unused.jar")),"queue order selected wrong version or retained obsolete dependency");
    check(client.installed(fresh).files.size()==2&&client.queue(fresh).isEmpty(),"wrong dependency receipt or queue");
   }

   Path existing=root.resolve("already-installed/game");Files.createDirectories(existing.resolve("mods"));
   byte[] installedNew=jar("sodium","0.9.3-beta.1","{}",null);Files.write(existing.resolve("mods/sodium-new.jar"),installedNew);
   client.toggle(existing,new ProsperoModrinth.Selection("iris","Iris",ProsperoModrinth.Kind.MOD));
   try{client.downloadAll(existing,"26.3","fabric",(m,d,t)->{},()->false,f->{},versions);throw new AssertionError("existing Sodium silently replaced");}catch(IOException expected){check(expected.getMessage().contains("Multiple top-level versions"),"installed conflict not explained");}
   check(Arrays.equals(installedNew,Files.readAllBytes(existing.resolve("mods/sodium-new.jar")))&&!Files.exists(existing.resolve("mods/iris.jar"))&&client.queue(existing).size()==1,"existing conflicting files changed or queue lost");
   version("otherroot","otherVersion","otherroot.jar",jar("otherroot","1.0","{}",null),"[{\"project_id\":\"sodium\",\"version_id\":\"newSodium\",\"dependency_type\":\"required\"}]");
   Path incompatible=root.resolve("incompatible/game");Files.createDirectories(incompatible);
   for(String project:List.of("iris","otherroot"))client.toggle(incompatible,new ProsperoModrinth.Selection(project,project,ProsperoModrinth.Kind.MOD));
   try{client.downloadAll(incompatible,"26.3","fabric",(m,d,t)->{},()->false,f->{},versions);throw new AssertionError("incompatible exact dependency pins accepted");}catch(IOException expected){check(expected.getMessage().contains("sodium")&&expected.getMessage().contains("oldSodium")&&expected.getMessage().contains("newSodium"),"conflicting dependency not identified");}
   check(client.local(incompatible,ProsperoModrinth.Kind.MOD).isEmpty()&&client.queue(incompatible).size()==2,"conflict published files or lost queue");
  }
  System.out.println("PASS actual upstream Fabric predicates,manifest-only missing API,nested module providers,hash-pinned auto-install,old-instance repair,healthy offline/no-network launch,offline failure,conflicts/unmapped requirements before publication and world/file preservation");
 }
}
'''
(w/'DependencyCheck.java').write_text(source);cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in json.loads((ROOT/'client/26.3.lock.json').read_text())['artifacts'])
subprocess.run([str(JDK/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p)for p in (ROOT/'client/launcher/java').glob('*.java')],str(w/'DependencyCheck.java')],check=True)
shutil.rmtree(w/'data',ignore_errors=True)
subprocess.run([str(JDK/'bin/java'),'-Xverify:all','-cp',str(w)+':'+cp,'DependencyCheck',str(w/'data'),str(loader)],check=True)
