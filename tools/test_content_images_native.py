#!/usr/bin/env python3
"""Actual JNI PNG/JPEG/WebP icon decoder against reference pixels and live project icons."""
from pathlib import Path
import json,subprocess,urllib.request,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];w=ROOT/'build/content107-icons';w.mkdir(exist_ok=True)
urls={
 'fabric':'https://cdn.modrinth.com/data/P7dR8mSH/icon.png',
 'sodium':'https://cdn.modrinth.com/data/AANobbMI/295862f4724dc3f78df3447ad6072b2dcd3ef0c9_96.webp',
 'vitrail':'https://cdn.modrinth.com/data/oSIKhgz3/cc5f6d81f2d9363074834e7e7207b08ceb046fb2_96.webp',
 'modmenu':'https://cdn.modrinth.com/data/mOgUt4GM/5a20ed1450a0e1e79a1fe04e61bb4e5878bf1d20.png'}
for name,url in urls.items():
 p=w/(name+'.image')
 if not p.exists():p.write_bytes(urllib.request.urlopen(url,timeout=30).read())
Image.new('RGB',(1025,1),(1,2,3)).save(w/'too-wide.reject',format='PNG')
Image.new('RGBA',(40,24),(240,64,32,128)).save(w/'alpha.image',format='PNG')
Image.new('RGB',(32,48),(210,50,70)).save(w/'jpeg.image',format='JPEG')
fixtures={}
for p in sorted(w.glob('*.image')):
 im=Image.open(p).convert('RGBA');out=''
 for y in range(32):
  for x in range(32):
   color=im.getpixel((x*im.width//32,y*im.height//32));out+=''.join(f'{(c*color[3]+24*(255-color[3])+127)//255:02x}'for c in color[:3])
 (w/(p.stem+'.expected')).write_text(out);fixtures[p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'format':Image.open(p).format,'size':im.size}
(w/'fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n')
source=r'''import java.nio.file.*;import java.io.*;import java.util.*;
public class NativeIconCheck{public static void main(String[]args)throws Exception{
 Path root=Path.of(args[0]);for(Path p:Files.list(root).filter(f->f.toString().endsWith(".image")).toList()){
  byte[] data=Files.readAllBytes(p);String icon=ProsperoContentImages.decode(data),name=p.getFileName().toString().replace(".image","");
  if(!icon.equals(Files.readString(root.resolve(name+".expected"))))throw new AssertionError("reference pixels: "+name);Files.writeString(root.resolve(name+".hex"),icon);
  try{ProsperoContentImages.decode(Arrays.copyOf(data,Math.min(20,data.length)));throw new AssertionError("truncated image accepted");}catch(IOException expected){}
 }
 for(Path bad:Files.list(root).filter(f->f.toString().endsWith(".reject")).toList())try{ProsperoContentImages.decode(Files.readAllBytes(bad));throw new AssertionError("dimension limit accepted");}catch(IOException expected){}
 try{ProsperoContentImages.decode(new byte[1048577]);throw new AssertionError("oversize accepted");}catch(IOException expected){}
 var api=new ProsperoModrinth(new ProsperoDownloads(u->new ByteArrayInputStream(Files.readAllBytes(root.resolve("sodium.image")))));Path game=root.resolve("instance/game");Files.createDirectories(game);
 String icon=api.icon(game,"sodium","https://cdn.modrinth.com/data/fixture/icon.webp",()->false);if(!icon.equals(Files.readString(root.resolve("sodium.expected"))))throw new AssertionError("Modrinth native image pipeline");
 System.out.println("PASS actual JNI pinned scalar libwebp/STB: real Fabric4bitPNG,Sodium/VitrailWebP,RGBPNG,alphaPNG,JPEG exact reference pixels;truncation/oversize refusal and content pipeline");}}
'''
(w/'NativeIconCheck.java').write_text(source)
jdk=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home');cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in json.loads((ROOT/'client/26.3.lock.json').read_text())['artifacts'])
subprocess.run([str(jdk/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),*[str(p)for p in (ROOT/'client/launcher/java').glob('*.java')],str(w/'NativeIconCheck.java')],check=True)
subprocess.run([str(jdk/'bin/java'),'--enable-native-access=ALL-UNNAMED','-Xcheck:jni','-Xverify:all','-Djava.library.path='+str(ROOT/'build/content-images-host'),'-cp',str(w)+':'+cp,'NativeIconCheck',str(w)],check=True)
