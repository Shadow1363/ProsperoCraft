#!/usr/bin/env python3
"""Decode packets serialized by the unchanged Controlify JAR, with native ABI/sanitizer checks."""
from pathlib import Path
import subprocess,json,urllib.request,hashlib,shutil
r=Path(__file__).resolve().parents[1];w=r/'build/triggers116-test';w.mkdir(exist_ok=True);jdk=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
metadata=json.load(urllib.request.urlopen('https://api.modrinth.com/v2/version/fo76vL20'));pin=next(f for f in metadata['files']if f['primary']);jar=w/'controlify.jar'
if not jar.exists():
 cached=next((r/'build/defaults115-live/data/instances').glob('*/content-downloads/'+pin['hashes']['sha512']+'.bin'),None)
 if cached:shutil.copy2(cached,jar)
 else:jar.write_bytes(urllib.request.urlopen(pin['url']).read())
assert hashlib.sha512(jar.read_bytes()).hexdigest()==pin['hashes']['sha512']
(w/'Packets.java').write_text(r'''
import dev.isxander.controlify.driver.dualsense.*;import java.lang.foreign.*;import java.io.*;import java.nio.file.*;
public class Packets{
 static void packet(OutputStream out,int mask,DualsenseTriggerEffect left,DualsenseTriggerEffect right)throws Exception{var state=new DualsenseEffectsState();state.ucEnableBits1=(byte)mask;state.ucEnableBits2=1;state.rgucLeftTriggerEffect=left.createState();state.rgucRightTriggerEffect=right.createState();byte[] bytes=new byte[47];state.writeTo(MemorySegment.ofArray(bytes));out.write(bytes);}
 public static void main(String[]a)throws Exception{var off=DualsenseTriggerEffect.Off.INSTANCE;byte[] zones={0,1,0,3,4,5,6,7,8,0};try(var out=Files.newOutputStream(Path.of(a[0]))){
  packet(out,12,off,off);
  packet(out,8,new DualsenseTriggerEffect.Feedback((byte)2,(byte)6),off);
  packet(out,4,off,new DualsenseTriggerEffect.Weapon((byte)3,(byte)7,(byte)5));
  packet(out,8,new DualsenseTriggerEffect.Vibration((byte)1,(byte)7,(byte)80),off);
  packet(out,8,new DualsenseTriggerEffect.FeedbackMultiplePosition(zones),off);
  packet(out,4,off,new DualsenseTriggerEffect.VibrationMultiplePosition((byte)127,zones));
  packet(out,8,new DualsenseTriggerEffect.FeedbackSlope((byte)1,(byte)8,(byte)1,(byte)8),off);
  packet(out,12,new DualsenseTriggerEffect.Feedback((byte)2,(byte)6),new DualsenseTriggerEffect.Weapon((byte)3,(byte)7,(byte)5));
 }}
}
''')
cp=':'.join([str(jar),*[str(r/'.tools/client'/row['file'])for row in json.loads((r/'client/26.3.lock.json').read_text())['artifacts']]])
subprocess.run([str(jdk/'bin/javac'),'-cp',cp,'-d',str(w),str(w/'Packets.java')],check=True);subprocess.run([str(jdk/'bin/java'),'-Xverify:all','-cp',str(w)+':'+cp,'Packets',str(w/'packets.bin')],check=True)
(w/'check.c').write_text(r'''
#include "ps5_trigger_effect.h"
#include <assert.h>
#include <stdio.h>
int main(int argc,char**argv){assert(argc==2);FILE*f=fopen(argv[1],"rb");assert(f);uint8_t p[47];ProsperoTriggerEffect out;
 for(int i=0;i<8;i++){assert(fread(p,1,47,f)==47);assert(prospero_trigger_packet(p,47,&out));
  if(i==0)assert(out.mask==3&&out.left.mode==0&&out.right.mode==0);
  if(i==1||i==7)assert((out.mask&1)&&out.left.mode==1&&out.left.data[0]==2&&out.left.data[1]==6);
  if(i==2||i==7)assert((out.mask&2)&&out.right.mode==2&&out.right.data[0]==3&&out.right.data[1]==7&&out.right.data[2]==5);
  if(i==3)assert(out.mask==1&&out.left.mode==3&&out.left.data[0]==1&&out.left.data[1]==7&&out.left.data[2]==80);
  if(i==4){uint8_t zones[10]={0,1,0,3,4,5,6,7,8,0};assert(out.left.mode==4&&!memcmp(zones,out.left.data,10));}
  if(i==5){uint8_t zones[10]={0,1,0,3,4,5,6,7,8,0};assert(out.right.mode==6&&out.right.data[0]==127&&!memcmp(zones,out.right.data+1,10));}
  if(i==6){uint8_t zones[10]={0,1,2,3,4,5,6,7,8,8};assert(out.left.mode==4&&!memcmp(zones,out.left.data,10));}
 }
 assert(fclose(f)==0);memset(p,0,47);assert(prospero_trigger_packet(p,47,&out)&&out.mask==0);assert(!prospero_trigger_packet(p,46,&out)&&!prospero_trigger_packet(p,48,&out)&&!prospero_trigger_packet(NULL,47,&out));
 p[0]=8;p[21]=0xfc;assert(!prospero_trigger_packet(p,47,&out));p[21]=0x25;p[22]=3;assert(!prospero_trigger_packet(p,47,&out));p[21]=0x21;p[23]=0x80;assert(!prospero_trigger_packet(p,47,&out));
 puts("PASS original Controlify3.5.3 FFM47-byte serialization -> native120-byte ABI:OFF,uniform resistance,weapon,vibration,per-zone feedback/vibration,slope,both/partial masks;unknown/calibration/truncated/malformed packets rejected under ASan/UBSan. Physical PS5 effects pending.");
}
''')
subprocess.run(['clang','-std=c11','-O1','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I'+str(r/'client/ports/sdl'),str(w/'check.c'),'-o',str(w/'check')],check=True);subprocess.run([str(w/'check'),str(w/'packets.bin')],check=True)
