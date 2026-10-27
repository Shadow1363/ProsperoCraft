#!/usr/bin/env python3
"""Actual vanilla NBT discovery, persistent Home pins, terminal add cards and focus."""
from pathlib import Path
import subprocess,tempfile
R=Path(__file__).resolve().parents[1];J=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home/bin')
source=r'''
import java.io.*;import java.nio.file.*;import java.util.*;import java.util.zip.*;
public class HomeCheck {
 static void check(boolean b,String m){if(!b)throw new AssertionError(m);}
 static void set(Object o,String n,Object v)throws Exception{var f=o.getClass().getDeclaredField(n);f.setAccessible(true);f.set(o,v);}
 static void string(DataOutputStream d,String name,String value)throws Exception{d.writeByte(8);d.writeUTF(name);d.writeUTF(value);}
 static byte[] world()throws Exception{var b=new ByteArrayOutputStream();try(var d=new DataOutputStream(new GZIPOutputStream(b))){d.writeByte(10);d.writeUTF("");d.writeByte(10);d.writeUTF("Data");string(d,"LevelName","A quiet morning");d.writeByte(0);d.writeByte(0);}return b.toByteArray();}
 static byte[] servers()throws Exception{var b=new ByteArrayOutputStream();try(var d=new DataOutputStream(b)){d.writeByte(10);d.writeUTF("");d.writeByte(9);d.writeUTF("servers");d.writeByte(10);d.writeInt(3);for(String ip:List.of("mc.example.test:25565","mc.example.test:25565","bad address")){string(d,"name","Friends");string(d,"ip",ip);d.writeByte(0);}d.writeByte(0);}return b.toByteArray();}
 static void idle(ProsperoLauncher m)throws Exception{long end=System.nanoTime()+5_000_000_000L;while(m.tick(0)[64].equals("BUSY")&&System.nanoTime()<end)Thread.sleep(5);check(!m.tick(0)[64].equals("BUSY"),"worker stuck");}
 public static void main(String[]args)throws Exception{
  Path root=Path.of(args[0]);var lib=new ProsperoLibrary(root);lib.settings().showIntro=false;lib.save();var empty=new ProsperoLauncher(new ProsperoAuth(),root,url->{throw new AssertionError("network");});check(empty.tick(0)[11].equals("12")&&empty.tick(0)[13].equals("1")&&empty.tick(0)[35].equals("ADD"),"empty Home plus");
  var i=lib.add("Vanilla","26.3",1);Path level=lib.game(i).resolve("saves/World Folder/level.dat");Files.createDirectories(level.getParent());Files.write(level,world());Path servers=lib.game(i).resolve("servers.dat");Files.write(servers,servers());byte[] original=Files.readAllBytes(servers);
  var entries=ProsperoDestinations.read(lib.game(i));check(entries.size()==2&&entries.get(0).name().equals("A quiet morning")&&entries.get(0).target().equals("World Folder")&&entries.get(1).target().equals("mc.example.test:25565"),"vanilla discovery/dedup/invalid address");
  var m=new ProsperoLauncher(new ProsperoAuth(),root,url->{throw new AssertionError("network");});m.tick(0x4000);check(m.tick(0)[11].equals("13"),"Home choose instance");m.tick(0x4000);idle(m);check(m.tick(0)[11].equals("14")&&m.tick(0)[13].equals("2"),"browse destinations");m.tick(0x4000);check(m.tick(0)[35].equals("PINNED"),"pin world");m.tick(0x40);m.tick(0x4000);check(new ProsperoLibrary(root).favorites().size()==2,"pins persisted");
  var reopened=new ProsperoLauncher(new ProsperoAuth(),root,url->{throw new AssertionError("network");});check(reopened.tick(0)[13].equals("3")&&reopened.tick(0)[32].equals("A quiet morning")&&reopened.tick(0)[39].equals("SERVER")&&reopened.tick(0)[43].equals("ADD"),"Home pins then final add");reopened.tick(0x4000);check(reopened.tick(0)[11].equals("4")&&reopened.tick(0)[74].equals("FAVORITE"),"favorite detail");
  reopened.tick(0x800);check(reopened.tick(0)[11].equals("0")&&reopened.tick(0)[12].equals("1")&&reopened.tick(0)[28].equals("CONTENT"),"Instances automatic selection");reopened.tick(0x800);check(reopened.tick(0)[11].equals("2")&&reopened.tick(0)[15].equals("0")&&reopened.tick(0)[28].equals("CONTENT"),"settings single content focus");reopened.tick(0x10);check(reopened.tick(0)[28].equals("TOP")&&reopened.tick(0)[15].equals("-1"),"header suppresses content focus");reopened.tick(0x800);check(reopened.tick(0)[11].equals("3")&&reopened.tick(0)[81].equals("Sign in"),"account autoselect");
  reopened.tick(0x8);for(int n=1;n<=5;n++){reopened.tick(0x20);check(reopened.tick(0)[74].equals(""+(n%5)),"guide sections");}reopened.tick(0x2000);check(reopened.tick(0)[11].equals("3"),"guide return");
  for(int n=1;n<9;n++)lib.add("Instance "+n,"26.3",n);var many=new ProsperoLauncher(new ProsperoAuth(),root,url->{throw new AssertionError("network");});many.tick(0x800);for(int n=0;n<9;n++)many.tick(0x20);check(many.tick(0)[9].equals("9")&&many.tick(0)[14].equals("8")&&many.tick(0)[39].equals("ADD"),"last add card across page boundary");
  check(Arrays.equals(original,Files.readAllBytes(servers))&&Arrays.equals(world(),Files.readAllBytes(level)),"read modified game files");
  // Malformed saved servers report a bounded error; symlink discovery is refused.
  Files.write(servers,new byte[]{10,0,0,9,0,7,'s','e','r','v','e','r','s',10,127,-1,-1,-1});try{ProsperoDestinations.read(lib.game(i));throw new AssertionError("bad length accepted");}catch(IOException expected){}
  Path outside=root.resolve("outside");Files.createDirectories(outside);Files.delete(servers);Files.createSymbolicLink(servers,outside);check(ProsperoDestinations.read(lib.game(i)).size()==1,"followed server symlink");
  System.out.println("PASS real gzip/plain NBT discovery, read-only world/server inventory, invalid/dedup bounds, persisted per-instance Home favorites, empty/final plus cards across pages, automatic tabs/single focus, guide pages/return");
 }
}
'''
with tempfile.TemporaryDirectory(prefix='prospero-home-')as folder:
 w=Path(folder);(w/'HomeCheck.java').write_text(source);cp=str(R/'.tools/client/gson-2.14.0.jar')
 subprocess.run([str(J/'javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p)for p in(R/'client/launcher/java').glob('*.java')],str(w/'HomeCheck.java')],check=True)
 subprocess.run([str(J/'java'),'-cp',str(w)+':'+cp,'HomeCheck',str(w/'data')],check=True,timeout=30)
