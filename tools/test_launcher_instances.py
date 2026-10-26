#!/usr/bin/env python3
"""Actual instance persistence, publisher install/cache validation and controller model."""
from pathlib import Path
import tempfile,json,subprocess
ROOT=Path(__file__).resolve().parents[1];jdk=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in json.loads((ROOT/'client/26.3.lock.json').read_text())['artifacts'])
source=r'''
import java.nio.file.*;import java.util.*;import java.io.*;import java.security.*;import com.google.gson.*;
public class InstanceCheck {
 static Map<String,byte[]> files=new HashMap<>();static int reads=0;static final String META="https://piston-meta.mojang.com/version/26.2.json",JAR="https://piston-data.mojang.com/objects/client.jar",LIB="https://libraries.minecraft.net/example/test.jar",INDEX="https://piston-meta.mojang.com/index.json";
 static byte[] bytes(String s){return s.getBytes(java.nio.charset.StandardCharsets.UTF_8);}static String hash(byte[] b)throws Exception{return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-1").digest(b));}
 static String pin(String url,byte[] b)throws Exception{return "{\"url\":\""+url+"\",\"sha1\":\""+hash(b)+"\",\"size\":"+b.length+"}";}
 static void fixture()throws Exception{
  byte[] client=bytes("original client bytes"),library=bytes("original library bytes"),asset=bytes("asset bytes");String sha=hash(asset);files.put(JAR,client);files.put(LIB,library);files.put("https://resources.download.minecraft.net/"+sha.substring(0,2)+"/"+sha,asset);
  byte[] index=bytes("{\"objects\":{\"a\":{\"hash\":\""+sha+"\",\"size\":"+asset.length+"},\"same hash\":{\"hash\":\""+sha+"\",\"size\":"+asset.length+"}}}");files.put(INDEX,index);
  String libraryPin=pin(LIB,library).replace("{","{\"path\":\"example/test.jar\",");
  String meta="{\"id\":\"26.2\",\"type\":\"release\",\"mainClass\":\"net.minecraft.client.main.Main\",\"javaVersion\":{\"majorVersion\":25},\"downloads\":{\"client\":"+pin(JAR,client)+"},\"assetIndex\":"+pin(INDEX,index).replace("{","{\"id\":\"32\",")+",\"libraries\":[{\"name\":\"example:test:1\",\"downloads\":{\"artifact\":"+libraryPin+"}},{\"name\":\"example:test:1:natives-windows\",\"downloads\":{\"artifact\":"+libraryPin+"}}]}";
  files.put(META,bytes(meta));String entry="{\"id\":\"26.2\",\"type\":\"release\",\"url\":\""+META+"\",\"sha1\":\""+hash(files.get(META))+"\"}";files.put(ProsperoInstall.MANIFEST,bytes("{\"versions\":["+entry+"]}"));
 }
 static synchronized InputStream open(String url)throws Exception{reads++;byte[] b=files.get(url);if(b==null)throw new IOException("Unexpected fixture request");return new ByteArrayInputStream(b);}
 interface Action{void run()throws Exception;}static void denied(Action action)throws Exception{try{action.run();throw new AssertionError("accepted invalid input");}catch(IOException|IllegalArgumentException expected){}}
 static void waitFor(ProsperoLauncher model)throws Exception{long end=System.nanoTime()+5_000_000_000L;while(model.tick(0)[64].equals("BUSY")&&System.nanoTime()<end)Thread.sleep(5);if(model.tick(0)[64].equals("BUSY"))throw new AssertionError("worker stuck");}
 public static void main(String[]args)throws Exception{
  Path root=Path.of(args[0]);fixture();var store=new ProsperoLibrary(root.resolve("store"));if(!store.instances().isEmpty())throw new AssertionError("preset instance");
  var first=store.add("Vanilla26.2","26.2",1);var second=store.add("Other world","26.2",2);if(store.game(first).equals(store.game(second)))throw new AssertionError("shared saves");Files.writeString(store.game(first).resolve("keep-world.txt"),"world");store.rename(first,"My world");store.icon(first,5);
  var reopened=new ProsperoLibrary(root.resolve("store"));if(!reopened.instances().get(0).name.equals("My world")||reopened.instances().get(0).icon!=5||!Files.readString(store.game(first).resolve("keep-world.txt")).equals("world"))throw new AssertionError("persistence/world");
  denied(()->store.add("../bad","26.2",1));denied(()->store.add("bad","../../escape",1));denied(()->ProsperoInstall.relative(root,"../escape"));denied(()->ProsperoInstall.safeUrl("https://evil.example/file"));denied(()->ProsperoInstall.safeUrl("http://piston-meta.mojang.com/file"));
  Path oldLibrary=root.resolve("store/library.json");var oldJson=JsonParser.parseString(Files.readString(oldLibrary)).getAsJsonObject();oldJson.getAsJsonObject("settings").remove("showIntro");Files.writeString(oldLibrary,oldJson.toString());if(!new ProsperoLibrary(root.resolve("store")).settings().showIntro)throw new AssertionError("old library notice default");
  var install=new ProsperoInstall(root.resolve("cache"),InstanceCheck::open);var versions=install.catalog(false,()->false);if(versions.size()!=1)throw new AssertionError();var receipt=install.install(versions.get(0),3,(s,d,t)->{},()->false);install.verify(receipt);
  if(!receipt.version.equals("26.2")||!receipt.assetIndex.equals("32")||receipt.classpath.size()!=2||receipt.files.size()!=4||!Files.readString(root.resolve("cache/versions/26.2/client.jar")).equals("original client bytes"))throw new AssertionError("wrong version/classifier/asset dedup");
  int before=reads;install.install(versions.get(0),3,(s,d,t)->{},()->false);if(reads!=before+1)throw new AssertionError("verified cache downloaded again");
  Files.writeString(root.resolve("cache/versions/26.2/client.jar"),"tamper");denied(()->install.verify(receipt));install.install(versions.get(0),2,(s,d,t)->{},()->false);install.verify(install.receipt("26.2"));
  denied(()->install.install(versions.get(0),2,(s,d,t)->{},()->true));
  var corrupt=new ProsperoInstall(root.resolve("corrupt"),url->url.equals(JAR)?new ByteArrayInputStream(bytes("WRONG bytes")):open(url));denied(()->corrupt.install(versions.get(0),1,(s,d,t)->{},()->false));if(Files.exists(root.resolve("corrupt/versions/26.2/receipt.json")))throw new AssertionError("failed install marked ready");
  var interrupted=new java.util.concurrent.atomic.AtomicBoolean();var mid=new ProsperoInstall(root.resolve("mid-cancel"),url->{InputStream original=open(url);return new FilterInputStream(original){public int read(byte[] b,int off,int len)throws IOException{int n=super.read(b,off,len);if(url.equals(JAR))interrupted.set(true);return n;}};});
  denied(()->mid.install(versions.get(0),1,(s,d,t)->{},interrupted::get));try(var paths=Files.walk(root.resolve("mid-cancel"))){if(paths.anyMatch(p->p.toString().endsWith(".part")||p.toString().endsWith("receipt.json")))throw new AssertionError("cancel left unverified file/receipt");}
  var model=new ProsperoLauncher(new ProsperoAuth(),root.resolve("model"),InstanceCheck::open);if(!model.tick(0)[13].equals("0"))throw new AssertionError("not empty");
  if(!model.tick(0)[11].equals("7")||!model.tick(0)[68].equals("ON"))throw new AssertionError("intro default");model.tick(0x10);model.tick(0x4000);model.tick(0x40);model.tick(0x4000);if(!new ProsperoLauncher(new ProsperoAuth(),root.resolve("model"),InstanceCheck::open).tick(0)[11].equals("0"))throw new AssertionError("intro preference");
  model.tick(0x800);if(!model.tick(0)[12].equals("1")||!model.tick(0)[28].equals("TOP"))throw new AssertionError("R1 topbar");model.tick(0x4000);model.tick(0x20);if(!model.tick(0)[25].equals("1600 x 900"))throw new AssertionError("resolution");model.tick(0x2000);
  model.tick(0x400);model.tick(0x4000);waitFor(model);if(!model.tick(0)[23].equals("26.2"))throw new AssertionError("catalog");model.tick(0x40);model.tick(0x4000);if(!model.tick(0)[11].equals("6"))throw new AssertionError("name keyboard");model.tick(0x4000);model.tick(0x8000);
  model.tick(0x40);model.tick(0x20);model.tick(0x40);model.tick(0x4000);waitFor(model);if(!model.tick(0)[13].equals("1")||!model.tick(0)[19].equals("READY"))throw new AssertionError("instance install "+model.tick(0)[2]);
  model.tick(0x4000);waitFor(model);if(!model.tick(0)[10].equals("WAIT")||!model.tick(0)[6].contains("NOT AVAILABLE YET"))throw new AssertionError("unsupported version launched");
  if(!ProsperoLauncher.supported("26.3")||ProsperoLauncher.supported("26.3-snapshot-1")||ProsperoLauncher.supported("26.2"))throw new AssertionError("compatibility allowlist");
  for(var entry:files.entrySet())if(entry.getKey().equals(META)||entry.getKey().equals(ProsperoInstall.MANIFEST))entry.setValue(bytes(new String(entry.getValue(),java.nio.charset.StandardCharsets.UTF_8).replace("26.2","26.3").replace("example:test:1","org.lwjgl:lwjgl-sdl:3.4.3")));
  // The metadata URL in the manifest also changes; provide the matching fixture.
  files.put(META.replace("26.2","26.3"),files.get(META));
  byte[] metadata=files.get(META);String catalog="{\"versions\":[{\"id\":\"26.3\",\"type\":\"release\",\"url\":\""+META+"\",\"sha1\":\""+hash(metadata)+"\"}]}";files.put(ProsperoInstall.MANIFEST,bytes(catalog));
  Path supportedRoot=root.resolve("supported");var supportedLibrary=new ProsperoLibrary(supportedRoot);var supportedInstance=supportedLibrary.add("Playable","26.3",1);supportedLibrary.settings().showIntro=false;supportedLibrary.save();var supportedInstaller=new ProsperoInstall(supportedRoot.resolve("cache"),InstanceCheck::open);var supportedReceipt=supportedInstaller.install(supportedInstaller.catalog(false,()->false).get(0),1,(t,d,n)->{},()->false);supportedLibrary.ready(supportedInstance,true);
  var supportedModel=new ProsperoLauncher(new ProsperoAuth(),supportedRoot,InstanceCheck::open);supportedModel.tick(0x4000);supportedModel.tick(0x4000);waitFor(supportedModel);if(!supportedModel.tick(0)[10].equals("LAUNCH"))throw new AssertionError("supported launch "+supportedModel.tick(0)[2]);List<String> launch=List.of(supportedModel.arguments(null,null));if(!launch.contains("--demo")||!launch.contains("26.3")||!launch.contains("--graphicsBackend"))throw new AssertionError("supported original demo arguments");
  var persisted=new ProsperoLibrary(root.resolve("model"));if(persisted.instances().size()!=1||persisted.instances().get(0).icon!=2||!persisted.instances().get(0).name.endsWith("A"))throw new AssertionError("controller persistence");
  System.out.println("PASS empty/persistent instances, isolated worlds, rename/icons/settings, L1/R1/keyboard/install/play controller flow, unsupported26.2 launch guard and startup-notice persistence, original bytes, pin verification/cache/repair/cancel/failure/traversal/HTTPS/native-classifier rejection");
 }
}
'''
with tempfile.TemporaryDirectory(prefix='prospero-instances-')as folder:
 w=Path(folder);(w/'InstanceCheck.java').write_text(source)
 subprocess.run([str(jdk/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p)for p in (ROOT/'client/launcher/java').glob('*.java')],str(w/'InstanceCheck.java')],check=True)
 subprocess.run([str(jdk/'bin/java'),'-cp',str(w)+':'+cp,'InstanceCheck',str(w/'data')],check=True,timeout=40)
