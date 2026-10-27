#!/usr/bin/env python3
"""Exercise real CPUID decoding and original Minecraft debug entry through the OSHI port."""
from pathlib import Path
import subprocess,tempfile,json,hashlib,zipfile
from build_oshi_platform import build
ROOT=Path(__file__).resolve().parents[1];JDK=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
port=build(JDK,True)
cpp=r'''
#include <cassert>
#include <cstring>
#include "native_cpu.hpp"
static bool bad_brand=false,missing_brand=false,missing_cpu=false;
static bool query(unsigned leaf,unsigned sub,unsigned& a,unsigned& b,unsigned& c,unsigned& d){
 a=b=c=d=0;
 if(leaf==0){a=0x0b;memcpy(&b,"Auth",4);memcpy(&d,"enti",4);memcpy(&c,"cAMD",4);return true;}
 if(leaf==1){if(missing_cpu)return false;a=0x00870f10;b=16<<16;return true;}
 if(leaf==0x0b&&sub==1){b=16;return true;}
 if(leaf>=0x80000002&&leaf<=0x80000004){if(missing_brand)return false;char text[48]={};memcpy(text,"  AMD Fixture CPU  ",19);if(bad_brand)text[5]=1;unsigned n=(leaf-0x80000002)*16;memcpy(&a,text+n,4);memcpy(&b,text+n+4,4);memcpy(&c,text+n+8,4);memcpy(&d,text+n+12,4);return true;}return false;
}
int main(){
 auto p=prospero_cpu::read(query,8);assert(p.valid&&p.logical==8&&p.kernel_count);assert(!strcmp(p.brand,"AMD Fixture CPU")&&!strcmp(p.vendor,"AuthenticAMD"));assert(p.family==23&&p.model==113&&p.stepping==0&&!strcmp(p.signature,"00870F10"));
 p=prospero_cpu::read(query,0);assert(p.valid&&p.logical==16&&!p.kernel_count);p=prospero_cpu::read(query,5000);assert(p.logical==16&&!p.kernel_count);
 bad_brand=true;p=prospero_cpu::read(query,8);assert(!strcmp(p.brand,"AuthenticAMD Family 23 Model 113"));bad_brand=false;missing_brand=true;p=prospero_cpu::read(query,8);assert(!strcmp(p.brand,"AuthenticAMD Family 23 Model 113"));missing_cpu=true;assert(!prospero_cpu::read(query,8).valid);
 puts("PASS actual CPU query decoding: real fields, kernel count preference, topology fallback, malformed/missing brand and missing CPU; no model/frequency fabrication");
}'''
java=r'''
import oshi.SystemInfo;
public class CpuDebugCheck {
 public static void main(String[] args)throws Exception{
  if(args[0].equals("desktop")){System.clearProperty("oshi.ps5");if(new SystemInfo().getCurrentPlatform()!=oshi.PlatformEnum.MACOS)throw new AssertionError("desktop platform changed");System.out.println("PASS original desktop platform path retained");return;}
  System.setProperty("oshi.ps5","true");
  if(args[0].equals("valid")){
   System.setProperty("ps5.cpu.brand","AMD Fixture CPU");System.setProperty("ps5.cpu.vendor","AuthenticAMD");System.setProperty("ps5.cpu.signature","00870F10");System.setProperty("ps5.cpu.family","23");System.setProperty("ps5.cpu.model","113");System.setProperty("ps5.cpu.stepping","0");System.setProperty("ps5.cpu.logical","8");
   var hardware=new SystemInfo().getHardware();var cpu=hardware.getProcessor();if(cpu.getLogicalProcessorCount()!=8||!cpu.getProcessorIdentifier().getName().equals("AMD Fixture CPU"))throw new AssertionError();
   try{cpu.getSystemCpuLoadTicks();throw new AssertionError("invented CPU load");}catch(UnsupportedOperationException expected){}
   try{hardware.getMemory();throw new AssertionError("invented memory");}catch(UnsupportedOperationException expected){}
   try{new SystemInfo().getOperatingSystem();throw new AssertionError("unsupported desktop syscall path");}catch(UnsupportedOperationException expected){}
  }
  Class<?> entry=Class.forName("net.minecraft.client.gui.components.debug.DebugEntrySystemSpecs");
  String text=(String)entry.getMethod("getCpuInfo").invoke(null);String expected=args[0].equals("valid")?"8x AMD Fixture CPU":"<unknown>";
  if(!text.equals(expected))throw new AssertionError("Original debug CPU text: "+text);
  if(!entry.getProtectionDomain().getCodeSource().getLocation().toString().endsWith("client-26.3.jar"))throw new AssertionError("game class replaced");
  System.out.println("PASS original Minecraft debug entry: "+text+"; game class loaded from intact official JAR");
 }
}'''
with tempfile.TemporaryDirectory(prefix='prospero-cpu-') as folder:
 w=Path(folder);(w/'cpu.cpp').write_text(cpp)
 subprocess.run(['clang++','-arch','x86_64','-std=c++20','-fsanitize=address,undefined','-I'+str(ROOT/'client/ports/oshi'),str(w/'cpu.cpp'),'-o',str(w/'cpu')],check=True)
 subprocess.run([str(w/'cpu')],check=True)
 (w/'CpuDebugCheck.java').write_text(java);lock=json.loads((ROOT/'client/26.3.lock.json').read_text());cp=':'.join([str(port),*[str(ROOT/'.tools/client'/a['file']) for a in lock['artifacts']]])
 game=ROOT/'.tools/client/client-26.3.jar';before=hashlib.sha256(game.read_bytes()).hexdigest()
 subprocess.run([str(JDK/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(w/'CpuDebugCheck.java')],check=True)
 for mode in ('valid','missing','desktop'):
  log=w/(mode+'-classes.log');subprocess.run([str(JDK/'bin/java'),'-Xlog:class+init=info:file='+str(log),'-cp',str(w)+':'+cp,'CpuDebugCheck',mode],check=True,timeout=25)
  if mode=='valid':assert "Initializing 'com/sun/jna/Native'" not in log.read_text(), 'CPU path initialized desktop JNA dispatch'
 assert hashlib.sha256(game.read_bytes()).hexdigest()==before
 with zipfile.ZipFile(port) as z:assert all(not n.startswith('net/minecraft/') and not n.startswith('com/mojang/') for n in z.namelist())
print('PASS original game JAR unchanged; overlay contains dependency classes only')
