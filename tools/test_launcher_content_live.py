#!/usr/bin/env python3
"""Opt-in live upstream Fabric install and Modrinth/Vitrail resolution, host only."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1];JDK=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
w=ROOT/'build/content103-live';w.mkdir(exist_ok=True)
gson=next(ROOT.glob('.tools/client/gson-*.jar'))
source=r'''
import java.nio.file.*;import java.util.*;import com.google.gson.*;
public class ContentLive {
 public static void main(String[]args)throws Exception {
  Path root=Path.of(args[0]);var fabric=new ProsperoFabric(root.resolve("cache"));var receipt=fabric.install("26.3",(s,d,t)->System.out.println(s),()->false);fabric.verify(fabric.read("26.3"));
  var modrinth=new ProsperoModrinth();var result=modrinth.search(ProsperoModrinth.Kind.MOD,"26.3","fabric","Vitrail",0,()->false);
  if(result.hits().stream().noneMatch(h->h.id().equals("oSIKhgz3")))throw new AssertionError("Vitrail not found");
  Path game=root.resolve("instance/game");Files.createDirectories(game);
  if(modrinth.queue(game).isEmpty())modrinth.toggle(game,new ProsperoModrinth.Selection("oSIKhgz3","Vitrail Shaders",ProsperoModrinth.Kind.MOD));
  modrinth.downloadAll(game,"26.3","fabric",(s,d,t)->System.out.println(s),()->false);
  var installed=modrinth.installed(game);if(installed.files.stream().noneMatch(f->f.project().equals("oSIKhgz3"))||installed.files.stream().noneMatch(f->f.project().equals("AANobbMI")))throw new AssertionError("Missing Vitrail or required Sodium");
  for(var f:installed.files)if(!ProsperoDownloads.hash(game.resolve(f.kind().folder).resolve(f.filename()),f.pin().algorithm()).equals(f.pin().hash()))throw new AssertionError("download hash");
  var report=new JsonObject();report.addProperty("fabric_loader",receipt.loader);report.addProperty("fabric_libraries",receipt.files.size());report.add("mods",new Gson().toJsonTree(installed.files));
  for(var kind:List.of(ProsperoModrinth.Kind.SHADER,ProsperoModrinth.Kind.RESOURCE))report.addProperty(kind.title,modrinth.search(kind,"26.3","fabric","",0,()->false).total());
  Files.writeString(root.resolve("upstream-receipt.json"),new GsonBuilder().setPrettyPrinting().create().toJson(report));
  System.out.println("PASS live Fabric profile/libraries and exact hashes; Modrinth Vitrail26.3Fabric + required Sodium downloaded/verified, shader/resource searches. No PS5 mod or shader-rendering pass.");
 }
}
'''
(w/'ContentLive.java').write_text(source)
subprocess.run([str(JDK/'bin/javac'),'--release','25','-cp',str(gson),'-d',str(w),*[str(p)for p in (ROOT/'client/launcher/java').glob('*.java')],str(w/'ContentLive.java')],check=True)
subprocess.run([str(JDK/'bin/java'),'-Xverify:all','-cp',str(w)+':'+str(gson),'ContentLive',str(w)],check=True,timeout=180)
