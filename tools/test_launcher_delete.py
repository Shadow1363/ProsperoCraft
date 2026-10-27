#!/usr/bin/env python3
"""Exercise actual delete/undo/confirmation logic, failure rollback and move recovery."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
JDK=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
source=r'''
import java.nio.file.*;import java.util.*;import java.io.*;import com.google.gson.*;
public class DeleteCheck {
 static void check(boolean ok,String why){if(!ok)throw new AssertionError(why);}
 static void set(Object obj,String name,Object value)throws Exception{var f=obj.getClass().getDeclaredField(name);f.setAccessible(true);f.set(obj,value);}
 static void reject(Job job)throws Exception{try{job.run();throw new AssertionError("expected rejection");}catch(IOException expected){}}
 interface Job{void run()throws Exception;}
 public static void main(String[] args)throws Exception{
  Path base=Path.of(args[0]);var lib=new ProsperoLibrary(base.resolve("library"));lib.settings().showIntro=false;var first=lib.add("First","26.3",1);var second=lib.add("Second","26.3",2);lib.ready(first,true);Path world=lib.game(first).resolve("saves/My World/level.dat");Files.createDirectories(world.getParent());Files.writeString(world,"world bytes");Files.writeString(lib.game(first).resolve("options.txt"),"my options");Files.createDirectories(lib.root.resolve("cache"));Files.writeString(lib.root.resolve("cache/keep.jar"),"cache");Files.writeString(lib.root.resolve("offline-account.json"),"private fixture");
  Files.createDirectory(lib.root.resolve("library.json.tmp"));reject(()->lib.delete(first));Files.delete(lib.root.resolve("library.json.tmp"));check(lib.instances().size()==2&&Files.readString(world).equals("world bytes"),"failed delete did not roll back");
  Path trash=lib.delete(first);check(lib.instances().size()==1&&!Files.exists(world)&&Files.readString(trash.resolve("files/game/saves/My World/level.dat")).equals("world bytes"),"delete archive");
  check(Files.readString(lib.root.resolve("cache/keep.jar")).equals("cache")&&Files.readString(lib.root.resolve("offline-account.json")).equals("private fixture")&&Files.isDirectory(lib.game(second)),"unrelated files touched");
  var reopened=new ProsperoLibrary(lib.root);check(reopened.instances().size()==1&&reopened.latestDeleted()!=null,"persistent deletion/undo");var restored=reopened.restore(trash);check(restored.id.equals(first.id)&&restored.ready&&restored.name.equals("First")&&restored.icon==1&&Files.readString(world).equals("world bytes")&&Files.readString(reopened.game(restored).resolve("options.txt")).equals("my options"),"restore bytes and metadata");
  reject(()->reopened.restore(trash));reject(()->reopened.restore(base));
  // Failed restore leaves the archive intact and no live entry.
  var failing=new ProsperoLibrary(lib.root);var target=failing.instances().stream().filter(i->i.id.equals(first.id)).findFirst().orElseThrow();Path again=failing.delete(target);Files.createDirectory(failing.root.resolve("library.json.tmp"));reject(()->failing.restore(again));Files.delete(failing.root.resolve("library.json.tmp"));check(!Files.exists(world)&&Files.isRegularFile(again.resolve("files/game/saves/My World/level.dat")),"restore failure lost archive");failing.restore(again);
  // Simulate interruption after folder move but before library replacement.
  Path journal=failing.root.resolve("trash/instances/interrupted-delete");Files.createDirectories(journal);Files.writeString(journal.resolve("instance.json"),new Gson().toJson(first));Files.writeString(journal.resolve("deleted"),"1");Files.move(world.getParent().getParent().getParent().getParent(),journal.resolve("files"));
  new ProsperoLibrary(failing.root);check(Files.readString(world).equals("world bytes")&&!Files.exists(journal.resolve("files")),"crashed delete not recovered");
  // Simulate interruption during restore, before saving the new live entry.
  var fresh=new ProsperoLibrary(failing.root);var found=fresh.instances().stream().filter(i->i.id.equals(first.id)).findFirst().orElseThrow();Path interrupted=fresh.delete(found);Files.move(interrupted.resolve("files"),world.getParent().getParent().getParent().getParent());var recovered=new ProsperoLibrary(failing.root);check(!Files.exists(world)&&Files.isRegularFile(interrupted.resolve("files/game/saves/My World/level.dat")),"crashed restore not recovered");recovered.restore(interrupted);
  // A symlinked instance must never relocate unrelated data.
  var safe=new ProsperoLibrary(base.resolve("symlink"));var link=safe.add("Link","26.3",1);Path folder=safe.game(link).getParent();Files.delete(safe.game(link));Files.delete(folder);Path outside=base.resolve("outside");Files.createDirectories(outside);Files.writeString(outside.resolve("keep"),"keep");Files.createSymbolicLink(folder,outside);reject(()->safe.delete(link));check(Files.readString(outside.resolve("keep")).equals("keep"),"followed symlink");
  // Actual controller flow in each build flavor: cancel default, confirm delete, undo.
  for(String channel:List.of("demo","offline")){
   Files.writeString(Path.of(args[1]).resolve("prosperocraft-channel.txt"),channel);Path root=base.resolve(channel);var store=new ProsperoLibrary(root);store.settings().showIntro=false;var entry=store.add("Delete me","26.3",1);Files.writeString(store.game(entry).resolve("keep-world"),"keep");
   var model=new ProsperoLauncher(new ProsperoAuth(),root,url->{throw new AssertionError("unexpected network");});model.tick(0x4000);model.tick(0x40);model.tick(0x4000);for(int n=0;n<3;n++)model.tick(0x40);
   set(model,"busy",true);model.tick(0x4000);check(model.tick(0)[11].equals("5"),"busy delete allowed");set(model,"busy",false);
   model.tick(0x4000);check(model.tick(0)[11].equals("9")&&model.tick(0)[15].equals("0"),"confirmation did not default cancel");model.tick(0x4000);check(model.tick(0)[11].equals("5")&&new ProsperoLibrary(root).instances().size()==1,"default X deleted instance");
   model.tick(0x4000);model.tick(0x2000);check(model.tick(0)[11].equals("5"),"Circle did not cancel");model.tick(0x4000);model.tick(0x20);model.tick(0x4000);check(model.tick(0)[11].equals("0")&&model.tick(0)[13].equals("0")&&model.tick(0)[74].equals("UNDO"),"last instance delete failed");
   var restart=new ProsperoLauncher(new ProsperoAuth(),root,url->{throw new AssertionError("network");});check(restart.tick(0)[74].equals("UNDO"),"restart lost undo");restart.tick(0x1000);check(restart.tick(0)[13].equals("1")&&Files.readString(store.game(entry).resolve("keep-world")).equals("keep"),"controller undo lost world");
   check(restart.tick(0)[73].equals(channel.equals("demo")?"DEMO BRANCH":"OFFLINE BRANCH"),"wrong channel label");
  }
  System.out.println("PASS delete/undo/metadata/world/options/cache/account preservation; save failure rollback; interrupted delete/restore recovery; symlink rejection; Demo+Offline controller confirmation/cancel/busy/last instance/restart undo");
 }
}'''
with tempfile.TemporaryDirectory(prefix='prospero-delete-') as folder:
 w=Path(folder);(w/'DeleteCheck.java').write_text(source);cp=str(ROOT/'.tools/client/gson-2.14.0.jar')
 subprocess.run([str(JDK/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p) for p in (ROOT/'client/launcher/java').glob('*.java')],str(w/'DeleteCheck.java')],check=True)
 subprocess.run([str(JDK/'bin/java'),'-cp',str(w)+':'+cp,'DeleteCheck',str(w/'data'),str(w)],check=True,timeout=40)
