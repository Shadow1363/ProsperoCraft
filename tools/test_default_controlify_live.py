#!/usr/bin/env python3
"""Install original pinned Controlify and the actual Unicode C418 pack through real APIs."""
from pathlib import Path
import subprocess,json,shutil
r=Path(__file__).resolve().parents[1];w=r/'build/defaults115-live';w.mkdir(exist_ok=True);jdk=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
s=r'''
import java.nio.file.*;import java.util.*;import java.io.*;
public class DefaultContentLive{
 public static void main(String[]a)throws Exception{
  Path root=Path.of(a[0]);var library=new ProsperoLibrary(root);var instance=library.add("Fabric defaults","26.3",16,"fabric");Path game=library.game(instance);Files.writeString(game.resolve("world-marker"),"KEEP");
  var fabric=new ProsperoFabric(root.resolve("cache"));fabric.install("26.3",(m,d,t)->{},()->false);
  byte[] controlify=new ProsperoDownloads().bytes(ProsperoModrinth.API+"version/fo76vL20",1024*1024,()->false);
  byte[] resource=new ProsperoDownloads().bytes(ProsperoModrinth.API+"version/xkCRrVC3",1024*1024,()->false);
  var client=new ProsperoModrinth(new ProsperoDownloads(url->{
   if(url.startsWith(ProsperoModrinth.API+"project/DOUdJVEm/version?"))return new ByteArrayInputStream(("["+new String(controlify,java.nio.charset.StandardCharsets.UTF_8)+"]").getBytes(java.nio.charset.StandardCharsets.UTF_8));
   if(url.startsWith(ProsperoModrinth.API+"project/jJAtxomy/version?"))return new ByteArrayInputStream(("["+new String(resource,java.nio.charset.StandardCharsets.UTF_8)+"]").getBytes(java.nio.charset.StandardCharsets.UTF_8));
   return ProsperoDownloads.network(url);
  }));
  client.toggle(game,new ProsperoModrinth.Selection("jJAtxomy","C418 Songs Only",ProsperoModrinth.Kind.RESOURCE));
  try(var versions=fabric.dependencies("26.3")){
   client.installDefaults(game,"26.3","fabric",versions,(m,d,t)->{},()->false);
   var installed=client.installed(game);for(String id:List.of("DOUdJVEm","P7dR8mSH","1eAoo2KR"))if(installed.files.stream().noneMatch(f->f.project().equals(id)))throw new AssertionError("Missing default/dependency "+id);
   var jars=client.local(game,ProsperoModrinth.Kind.MOD).stream().map(f->game.resolve("mods").resolve(f.filename())).toList();if(!ProsperoDependencies.missing(jars,"26.3",versions).isEmpty())throw new AssertionError("Default graph incomplete");
   if(client.queue(game).size()!=1)throw new AssertionError("Defaults consumed user queue");library.defaultContentInstalled(instance);
   client.downloadAll(game,"26.3","fabric",(m,d,t)->{},()->false,f->{},versions);
   var pack=client.local(game,ProsperoModrinth.Kind.RESOURCE).getFirst();if(!pack.filename().equals("§lC418 §rSongs Only.zip"))throw new AssertionError("Filename changed");
   var receipt=client.installed(game);for(var file:receipt.files){Path path=game.resolve(file.kind().folder).resolve(file.filename());if(!ProsperoDownloads.hash(path,file.pin().algorithm()).equals(file.pin().hash()))throw new AssertionError("Publisher bytes changed");}
   try(var zip=new java.util.zip.ZipFile(game.resolve("resourcepacks").resolve(pack.filename()).toFile())){if(zip.getEntry("pack.mcmeta")==null)throw new AssertionError("Invalid actual pack");}
   var current=client.local(game,ProsperoModrinth.Kind.MOD).stream().filter(f->f.project().equals("DOUdJVEm")).findFirst().orElseThrow();client.uninstall(game,current);client.uninstall(game,pack);
   if(new ProsperoLibrary(root).instances().getFirst().defaultContentPending)throw new AssertionError("Uninstall will force defaults back");
   if(Files.exists(game.resolve("resourcepacks").resolve(pack.filename()))||!Files.readString(game.resolve("world-marker")).equals("KEEP"))throw new AssertionError("Uninstall/world");
  }
  System.out.println("PASS original Controlify3.5.3 + required Fabric API/YACL,upstream Fabric predicates,user queue preserved,one-time metadata completion;actual C418 § filename download/receipt/pack.mcmeta/publisher hashes/uninstall;world marker unchanged. PS5 new-instance validation pending.");
 }
}
'''
(w/'DefaultContentLive.java').write_text(s);cp=':'.join(str(r/'.tools/client'/row['file'])for row in json.loads((r/'client/26.3.lock.json').read_text())['artifacts'])
subprocess.run([str(jdk/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p)for p in (r/'client/launcher/java').glob('*.java')],str(w/'DefaultContentLive.java')],check=True)
shutil.rmtree(w/'data',ignore_errors=True)
subprocess.run([str(jdk/'bin/java'),'-Xverify:all','-cp',str(w)+':'+cp,'DefaultContentLive',str(w/'data')],check=True,timeout=180)
