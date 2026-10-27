#!/usr/bin/env python3
"""Actual spatial menu navigation, QWERTY typing and scoped JAR stream handles."""
from pathlib import Path
import json,subprocess,shutil
ROOT=Path(__file__).resolve().parents[1];JDK=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home');w=ROOT/'build/client104-controls';w.mkdir(exist_ok=True)
cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in json.loads((ROOT/'client/26.3.lock.json').read_text())['artifacts'])
source=r'''
import java.nio.file.*;import java.net.*;import java.util.*;import java.io.*;import java.util.jar.*;
public class Controls104 {
 static void check(boolean b,String s){if(!b)throw new AssertionError(s);}
 static void set(ProsperoLauncher m,String f,Object v)throws Exception {var field=ProsperoLauncher.class.getDeclaredField(f);field.setAccessible(true);field.set(m,v);var c=ProsperoLauncher.class.getDeclaredField("cached");c.setAccessible(true);c.set(m,null);}
 static void focus(ProsperoLauncher m,int page,int row)throws Exception{set(m,"page",page);set(m,"row",row);set(m,"top",false);}
 static int row(ProsperoLauncher m,int button){return Integer.parseInt(m.tick(button)[15]);}
 public static void main(String[]a)throws Exception {
  Path root=Path.of(a[0]);var lib=new ProsperoLibrary(root);var entry=lib.add("Navigation fixture","26.3",1);lib.settings().showIntro=false;lib.save();var model=new ProsperoLauncher(new ProsperoAuth(),root,u->{throw new IOException();});set(model,"detail",entry);
  focus(model,5,2);check(row(model,0x20)==3&&row(model,0x80)==2,"Mods/Shaders horizontal");check(row(model,0x40)==4&&row(model,0x40)==5&&row(model,0x20)==6,"resource/done/delete navigation");check(row(model,0x10)==4&&row(model,0x10)==2&&row(model,0x10)==1&&row(model,0x10)==0&&row(model,0x10)==-1,"settings vertical geometry/top");
  focus(model,12,0);check(row(model,0x20)==1&&row(model,0x40)==3&&row(model,0x80)==2&&row(model,0x10)==0,"search/download/paging geometry");
  focus(model,6,0);set(model,"keyboard","");set(model,"key",10);set(model,"keyboardReturn",1);model.tick(0x4000);check(model.tick(0)[29].equals("Q"),"QWERTY first letter row");model.tick(0x100);model.tick(0x4000);check(model.tick(0)[29].equals("Qq"),"lowercase QWERTY");model.tick(0x1000);check(model.tick(0)[29].equals("Q"),"backspace");set(model,"key",0);model.tick(0x4000);check(model.tick(0)[29].equals("Q1"),"number row");
  // Real JAR URLs show why useCaches matters: the default retains a second FD
  // even after InputStream.close. Configure uses the standard scoped-stream API.
  var bean=(com.sun.management.UnixOperatingSystemMXBean)java.lang.management.ManagementFactory.getOperatingSystemMXBean();
  Path jars=root.resolve("jars");Files.createDirectories(jars);for(int n=0;n<80;n++)try(var out=new JarOutputStream(Files.newOutputStream(jars.resolve(n+".jar")))){out.putNextEntry(new JarEntry("payload"));out.write(n);out.closeEntry();}
  URLConnection.setDefaultUseCaches("jar",true);long before=bean.getOpenFileDescriptorCount();for(int n=0;n<40;n++)try(var in=URI.create("jar:"+jars.resolve(n+".jar").toUri()+"!/payload").toURL().openStream()){check(in.read()==n,"resource bytes");}long retained=bean.getOpenFileDescriptorCount()-before;check(retained>=35,"control did not retain JAR descriptors");
  URLConnection.setDefaultUseCaches("jar",false); // Historical104 mechanism test only;105 restores cached Fabric reads.
  before=bean.getOpenFileDescriptorCount();for(int n=40;n<80;n++)try(var in=URI.create("jar:"+jars.resolve(n+".jar").toUri()+"!/payload").toURL().openStream()){check(in.read()==n,"scoped resource bytes");}long delta=bean.getOpenFileDescriptorCount()-before;check(delta<=2,"scoped JAR handles retained: "+delta);
  System.out.println("PASS real model spatial settings/browser navigation and QWERTY case/numbers/backspace;40 real JAR streams retained "+retained+" extra descriptors with cache vs "+delta+" scoped;PS5 pressure repair still pending");
 }
}'''
(w/'Controls104.java').write_text(source)
subprocess.run([str(JDK/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p)for p in (ROOT/'client/launcher/java').glob('*.java')],str(w/'Controls104.java')],check=True)
data=w/'data';shutil.rmtree(data,ignore_errors=True);data.mkdir()
subprocess.run([str(JDK/'bin/java'),'-Xverify:all','-cp',str(w)+':'+cp,'Controls104',str(data)],check=True,timeout=30)
layout='1234567890QWERTYUIOPASDFGHJKL_ZXCVBNM .-'
assert len(layout)==40 and set(layout)==set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ._-')
assert layout in (ROOT/'client/launcher/native_menu.hpp').read_text()
for title,row in [('MODS',2),('SHADERS',3),('RESOURCE PACKS',4)]:assert f'"{title}",row=={row},true' not in (ROOT/'client/launcher/native_menu.hpp').read_text()
print('PASS native/model QWERTY layouts agree; content buttons use standard secondary style')
