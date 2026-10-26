#!/usr/bin/env python3
"""Run actual installer on real pinned26.3publisher data supplied from verified local cache."""
from pathlib import Path
import json,tempfile,subprocess
ROOT=Path(__file__).resolve().parents[1];jdk=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home');lock=json.loads((ROOT/'client/26.3.lock.json').read_text());w=ROOT/'build/launcher-publisher';w.mkdir(exist_ok=True)
source=r'''
import java.nio.file.*;import java.io.*;import java.util.*;import com.google.gson.*;
public class PublisherCheck {
 public static void main(String[]args)throws Exception{
  Path project=Path.of(args[0]),root=Path.of(args[1]);JsonObject lock=JsonParser.parseString(Files.readString(project.resolve("client/26.3.lock.json"))).getAsJsonObject();Map<String,Path> paths=new HashMap<>();
  for(var item:lock.getAsJsonArray("artifacts")){var row=item.getAsJsonObject();paths.put(row.get("url").getAsString(),project.resolve(".tools/client/"+row.get("file").getAsString()));}
  var metadata=lock.getAsJsonObject("metadata");paths.put(metadata.get("url").getAsString(),project.resolve(".tools/client/26.3.metadata.json"));var index=lock.getAsJsonObject("asset_index");paths.put(index.get("url").getAsString(),project.resolve(".tools/client/"+index.get("file").getAsString()));
  var installer=new ProsperoInstall(root,url->{Path path=paths.get(url);if(path==null&&url.startsWith("https://resources.download.minecraft.net/"))path=project.resolve(".tools/client-assets/objects/"+url.substring("https://resources.download.minecraft.net/".length()));if(path==null)throw new IOException("Publisher file missing from fixture cache");return Files.newInputStream(path);});
  var version=new ProsperoInstall.Version("26.3","release",metadata.get("url").getAsString(),metadata.get("sha1").getAsString());var receipt=installer.install(version,4,(s,d,t)->{},()->false);installer.verify(receipt);
  if(!receipt.window.equals("SDL")||!receipt.assetIndex.equals("34")||receipt.classpath.size()!=54||receipt.files.size()!=5202)throw new AssertionError("publisher inventory "+receipt.classpath.size()+"/"+receipt.files.size());
  var loader=installer.loader(receipt);var main=Class.forName("net.minecraft.client.main.Main",false,loader);
  if(main.getClassLoader()!=loader||!main.getProtectionDomain().getCodeSource().getLocation().toString().endsWith("versions/26.3/client.jar"))throw new AssertionError("not downloaded game loader");
  if(Class.forName("org.lwjgl.system.Configuration",false,loader).getClassLoader()!=ProsperoInstall.class.getClassLoader())throw new AssertionError("native binding loader split");
  Files.writeString(project.resolve("build/launcher-publisher/classpath.txt"),String.join(java.io.File.pathSeparator,receipt.classpath.stream().map(p->root.resolve(p).toString()).toList()));
  if(args.length>2){
   Thread.currentThread().setContextClassLoader(loader);Path game=project.resolve("build/launcher-publisher/world");Files.createDirectories(game);
   String[] demo={"--demo","--disableMultiplayer","--disableChat","--username","PS5Demo","--uuid","00000000-0000-3000-8000-000000000000","--accessToken","0","--version","26.3","--versionType","release","--gameDir",game.toString(),"--assetsDir",root.resolve("assets").toString(),"--assetIndex","34","--graphicsBackend","vulkan","--width","1280","--height","720"};
   main.getMethod("main",String[].class).invoke(null,(Object)demo);throw new AssertionError("Unexpected host game return");
  }
  System.out.println("PASS actual installer/receipt/isolated game loader on real publisher26.3:54originalJARs,5147unique assets,index34,SDL,game from downloaded cache and native bindings from parent; no PS5 acceptance");
 }
}
'''
(w/'PublisherCheck.java').write_text(source)
keep=[row for row in lock['artifacts']if row['id'].startswith(('org.lwjgl:','com.google.code.gson:'))and not row['id'].startswith('org.lwjgl:lwjgl:')]
parent=[w,ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar',ROOT/'build/client-ports/lwjgl-modules/lwjgl-3.4.3-ps5-modules.jar',*[ROOT/'.tools/client'/r['file']for r in keep]]
cp=':'.join(map(str,parent))
subprocess.run([str(jdk/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p)for p in (ROOT/'client/launcher/java').glob('*.java')],str(w/'PublisherCheck.java')],check=True)
subprocess.run([str(jdk/'bin/java'),'-cp',cp,'PublisherCheck',str(ROOT),str(w/'cache')],check=True,timeout=120)

result=subprocess.run([str(jdk/'bin/java'),'-Xmx512m','--enable-native-access=ALL-UNNAMED','-cp',cp,'PublisherCheck',str(ROOT),str(w/'cache'),'run'],text=True,capture_output=True,timeout=90)
text=result.stdout+result.stderr;(w/'original-main.log').write_text(text)
assert result.returncode!=0 and ('NativeLibrariesBootstrap' in text or 'UnsatisfiedLinkError' in text),text[-5000:]
assert 'ClassNotFoundException' not in text and 'Missing required option' not in text,text[-5000:]
print('PASS original downloaded Main invoked through isolated loader with bundled-binding parent and downloaded dependencies; expected unavailable host native failure; not PS5 gameplay proof')
