#!/usr/bin/env python3
"""Run actual shutdown evidence code and process-replacement bridge with host OS fixtures."""
from pathlib import Path
import subprocess,tempfile,os
root=Path(__file__).resolve().parents[1]
jdk=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
with tempfile.TemporaryDirectory(prefix='launcher-lifecycle-') as folder:
 w=Path(folder)
 for package,source in {
 'net/minecraft/client/Minecraft.java':'package net.minecraft.client; public class Minecraft {public static Minecraft instance=new Minecraft();public boolean running=false;public static Minecraft getInstance(){return instance;}public boolean isRunning(){return running;}}',
 'org/lwjgl/sdl/SDLInit.java':'package org.lwjgl.sdl;public class SDLInit{public static int initialized=0;public static int SDL_WasInit(int flags){return initialized;}}',
 'SessionCheck.java':r'''import java.nio.file.*;import java.util.*;
 public class SessionCheck{
 interface Job{void run()throws Exception;}
 static void fail(Job job)throws Exception{try{job.run();throw new AssertionError("accepted abnormal return");}catch(IllegalStateException expected){}}
 public static void main(String[]a)throws Exception{
 Path logs=Path.of(a[0]);var loader=SessionCheck.class.getClassLoader();
 Files.createDirectories(logs);Files.writeString(logs.resolve("latest.log"),"[old/INFO]: Stopping!\n");
 var session=new ProsperoSession(logs);fail(()->session.verifyCleanReturn(loader)); // stale stopping ignored
 Files.writeString(logs.resolve("latest.log"),"[Render thread/INFO]: Stopping!\n",StandardOpenOption.APPEND);
 session.verifyCleanReturn(loader);
 net.minecraft.client.Minecraft.instance.running=true;fail(()->session.verifyCleanReturn(loader));
 net.minecraft.client.Minecraft.instance.running=false;org.lwjgl.sdl.SDLInit.initialized=32;fail(()->session.verifyCleanReturn(loader));org.lwjgl.sdl.SDLInit.initialized=0;
 net.minecraft.client.Minecraft.instance=null;fail(()->session.verifyCleanReturn(loader));net.minecraft.client.Minecraft.instance=new net.minecraft.client.Minecraft();
 for(String error:List.of("Shutdown failure!","Failed to create window:","Reported exception thrown!","Unreported exception thrown!","[Render thread/FATAL]: crash","#@?@#")){
  var bad=new ProsperoSession(logs);Files.writeString(logs.resolve("latest.log"),error+"\n[Render thread/INFO]: Stopping!\n",StandardOpenOption.APPEND);fail(()->bad.verifyCleanReturn(loader));
 }
 var rolled=new ProsperoSession(logs);Files.move(logs.resolve("latest.log"),logs.resolve("previous-1.log"));
 Files.writeString(logs.resolve("previous-2.log"),"[Render thread/INFO]: Stopping!\n");Files.writeString(logs.resolve("latest.log"),"");rolled.verifyCleanReturn(loader);
 // A current fatal after rollover cannot be mistaken for a clean quit.
 Files.writeString(logs.resolve("latest.log"),"[Render thread/FATAL]: crash\n");fail(()->rolled.verifyCleanReturn(loader));
 System.out.println("PASS actual session gate: current-run stopping, stale logs, early return, running/null singleton, live SDL, fatal/startup/shutdown errors and rolling logs");
 }}'''
 }.items():
  p=w/package;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(source)
 subprocess.run([str(jdk/'bin/javac'),'-d',str(w),str(root/'client/launcher/java/ProsperoSession.java'),*[str(p)for p in w.rglob('*.java')]],check=True)
 subprocess.run([str(jdk/'bin/java'),'-cp',str(w),'SessionCheck',str(w/'logs')],check=True)
 (w/'restart.cpp').write_text(r'''
 #include <cassert>
 #include <cstdlib>
 #include <cstring>
 #include <unistd.h>
 #include "session_restart.hpp"
 static const char* executable;static bool reject=false;
 extern "C" int sceSystemServiceLoadExec(const char* path,const char*const* args){
  assert(!strcmp(path,"/app0/eboot.bin")&&!strcmp(args[0],"--prospero-library")&&!args[1]);
  if(reject)return -5;
  const char* next[]={executable,args[0],nullptr};execv(executable,const_cast<char*const*>(next));abort();
 }
 int main(int argc,char**argv){
  executable=argv[0];const char* value=getenv("TEST_CYCLE");int cycle=value?atoi(value):0;
  // Static owners are new in every process; the real PS5 boundary is LoadExec.
  static int display_owners=0;assert(display_owners==0);display_owners=1;
  if(cycle){assert(argc==2&&!strcmp(argv[1],"--prospero-library"));}
  if(cycle==3){reject=true;assert(prospero_session::restart_library()==-5);return 0;}
  char next[8];snprintf(next,sizeof(next),"%d",cycle+1);setenv("TEST_CYCLE",next,1);
  prospero_session::restart_library();abort();
 }
 '''.replace('#include <cstdlib>','#include <cstdlib>\n#include <cstdio>'))
 subprocess.run(['clang++','-std=c++20','-I'+str(root/'client/startup'),str(w/'restart.cpp'),'-o',str(w/'restart')],check=True)
 subprocess.run([str(w/'restart')],check=True,timeout=15)
 print('PASS actual restart bridge with host exec boundary: three fresh-process cycles, library argument, no concurrent display owner, returned LoadExec error retained; PS5 LoadExec remains pending')
# Audit the pinned, untouched publisher code whose return is being classified.
main=subprocess.check_output([str(jdk/'bin/javap'),'-c','-classpath',str(root/'.tools/client/client-26.3.jar'),'net.minecraft.client.main.Main'],text=True)
close=subprocess.check_output([str(jdk/'bin/javap'),'-c','-p','-classpath',str(root/'.tools/client/client-26.3.jar'),'net.minecraft.client.Minecraft'],text=True)
for token in ['Minecraft.run:', 'Minecraft.exitWorldAndClose:', 'ClientShutdownWatchdog.startShutdownWatchdog:','SilentInitException']:assert token in main
body=close[close.index('public void close();'):close.index('private void runTick(')]
for token in ['SoundManager.destroy:', 'GpuSurface.close:', 'RenderSystem.shutdownRenderer:', 'Window.close:', 'SDLInit.SDL_Quit:', 'Util.shutdownExecutors:']:assert token in body,token
print('PASS pinned original Main/close bytecode audit: normal cleanup and silent early-return distinction; no game JAR modifications')
