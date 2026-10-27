#!/usr/bin/env python3
from pathlib import Path
import subprocess,struct,zlib
ROOT=Path(__file__).resolve().parents[1];w=ROOT/'build/content106-icons';w.mkdir(exist_ok=True)
def chunk(tag,data):return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data))
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',32,32,8,2,0,0,0))+chunk(b'IDAT',zlib.compress((b'\0'+b'\xf0\x40\x20'*32)*32))+chunk(b'IEND',b'')
(w/'icon.png').write_bytes(png)
source=r'''import java.nio.file.*;import java.io.*;public class IconCheck{public static void main(String[]a)throws Exception{
 byte[] png=Files.readAllBytes(Path.of(a[0]));String icon=ProsperoAvatar.icon(png);if(!icon.equals("f04020".repeat(1024)))throw new AssertionError("pixels");
 var api=new ProsperoModrinth(new ProsperoDownloads(u->new ByteArrayInputStream(png)));Path game=Path.of(a[1]).resolve("game");Files.createDirectories(game);
 String cached=api.icon(game,"fixture","https://cdn.modrinth.com/data/fixture/icon.png",()->false);if(!cached.equals(icon))throw new AssertionError("download icon");
 var offline=new ProsperoModrinth(new ProsperoDownloads(u->{throw new IOException("offline");}));if(!offline.icon(game,"fixture","",()->false).equals(icon))throw new AssertionError("offline icon cache");
 if(!api.icon(game,"bad","https://evil.invalid/icon.png",()->false).isEmpty())throw new AssertionError("host guard");
 png[30]^=1;try{ProsperoAvatar.icon(png);throw new AssertionError("bad PNG accepted");}catch(IOException expected){}
 System.out.println("PASS actual pure Java bounded PNG thumbnail decode/exact pixels/CRC,restricted CDN transport,persistent offline icon cache and rejected hosts;no game/native image initialization");}}
'''
(w/'IconCheck.java').write_text(source)
import json
jdk=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home');cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in json.loads((ROOT/'client/26.3.lock.json').read_text())['artifacts'])
subprocess.run([str(jdk/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p)for p in (ROOT/'client/launcher/java').glob('*.java')],str(w/'IconCheck.java')],check=True)
subprocess.run([str(jdk/'bin/java'),'--enable-native-access=ALL-UNNAMED','-Xverify:all','-cp',str(w)+':'+cp,'IconCheck',str(w/'icon.png'),str(w/'data')],check=True)
