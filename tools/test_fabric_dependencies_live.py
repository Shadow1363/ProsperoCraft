#!/usr/bin/env python3
"""Real pinned Vitrail/Sodium/Fabric API bytes; no game invocation or class rewriting."""
from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parents[1];JDK=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home');w=ROOT/'build/dependencies108-live';w.mkdir(exist_ok=True)
source=r'''
import java.nio.file.*;import java.io.*;import java.util.*;
public class LiveDependencies {
 public static void main(String[]args)throws Exception{Path root=Path.of(args[0]),game=root.resolve("instance/game");Files.createDirectories(game);var fabric=new ProsperoFabric(root.resolve("cache"));var f=fabric.install("26.3",(m,d,t)->{},()->false);
  try(var versions=fabric.dependencies("26.3")){
   byte[] pinned=new ProsperoDownloads().bytes(ProsperoModrinth.API+"version/Q3nKuPKJ",1024*1024,()->false);
   var api=new ProsperoModrinth(new ProsperoDownloads(url->{if(url.startsWith(ProsperoModrinth.API+"project/oSIKhgz3/version?"))return new ByteArrayInputStream(("["+new String(pinned,java.nio.charset.StandardCharsets.UTF_8)+"]").getBytes(java.nio.charset.StandardCharsets.UTF_8));return ProsperoDownloads.network(url);}));
   if(api.local(game,ProsperoModrinth.Kind.MOD).isEmpty()){if(api.queue(game).stream().noneMatch(q->q.project().equals("oSIKhgz3")))api.toggle(game,new ProsperoModrinth.Selection("oSIKhgz3","Vitrail0.13.0",ProsperoModrinth.Kind.MOD));api.downloadAll(game,"26.3","fabric",(m,d,t)->System.out.println(m),()->false,x->{},versions);}
   if(api.installed(game).files.stream().noneMatch(x->x.project().equals("P7dR8mSH")))throw new AssertionError("real Fabric API was not auto-installed");
   var jars=api.local(game,ProsperoModrinth.Kind.MOD).stream().map(x->game.resolve("mods").resolve(x.filename())).toList();if(!ProsperoDependencies.missing(jars,"26.3",versions).isEmpty())throw new AssertionError("real JAR dependencies unresolved");
   var item=api.local(game,ProsperoModrinth.Kind.MOD).stream().filter(x->x.project().equals("P7dR8mSH")).findFirst().orElseThrow();api.uninstall(game,item);api.repair(game,"26.3","fabric",versions,(m,d,t)->{},()->false,false);
   if(api.local(game,ProsperoModrinth.Kind.MOD).stream().noneMatch(x->x.project().equals("P7dR8mSH")))throw new AssertionError("real existing-instance repair failed");
   api.repair(game,"26.3","fabric",versions,(m,d,t)->{},()->false,true);
   System.out.println("PASS real pinned Vitrail0.13.0/Sodium/Fabric API verified downloads,upstream0.20.1predicates,nested required module discovery,API auto-install and existing-instance repair;official JARs untouched,no game execution");
  }
 }
}
'''
(w/'LiveDependencies.java').write_text(source);cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in json.loads((ROOT/'client/26.3.lock.json').read_text())['artifacts'])
subprocess.run([str(JDK/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p)for p in (ROOT/'client/launcher/java').glob('*.java')],str(w/'LiveDependencies.java')],check=True)
subprocess.run([str(JDK/'bin/java'),'-Xverify:all','-cp',str(w)+':'+cp,'LiveDependencies',str(w/'data')],check=True,timeout=180)
