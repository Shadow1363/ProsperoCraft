import java.io.*;
import java.net.*;
import java.nio.*;
import java.util.*;
import java.util.zip.*;
import javax.net.ssl.HttpsURLConnection;

/** Bounded pure-Java Minecraft PNG face decoder; no AWT/native image dependency. */
final class ProsperoAvatar {
 static String fetch(String address)throws Exception {
  URI uri=URI.create(address);if("http".equals(uri.getScheme())&&"textures.minecraft.net".equals(uri.getHost())&&uri.getPort()==-1&&uri.getUserInfo()==null)uri=URI.create("https://textures.minecraft.net"+uri.getRawPath());if(!"https".equals(uri.getScheme())||!"textures.minecraft.net".equals(uri.getHost())||uri.getPort()!=-1||uri.getUserInfo()!=null||!uri.getPath().matches("/texture/[a-fA-F0-9]{32,128}"))return "";
  HttpsURLConnection c=(HttpsURLConnection)uri.toURL().openConnection();c.setInstanceFollowRedirects(false);c.setConnectTimeout(8000);c.setReadTimeout(8000);
  try{if(c.getResponseCode()!=200)return "";try(var in=c.getInputStream()){return decode(in.readNBytes(1024*1024+1));}}finally{c.disconnect();}
 }
 static String defaultFace(java.nio.file.Path library,String id)throws Exception {
  if(!id.matches("[a-fA-F0-9]{32}"))return "";String uuid=id.substring(0,8)+"-"+id.substring(8,12)+"-"+id.substring(12,16)+"-"+id.substring(16,20)+"-"+id.substring(20);int index=Math.floorMod(java.util.UUID.fromString(uuid).hashCode(),18);String[] names={"alex","ari","efe","kai","makena","noor","steve","sunny","zuri"};java.nio.file.Path jar=library.resolve("cache/versions/26.3/client.jar");if(!java.nio.file.Files.isRegularFile(jar))return "";
  try(var z=new java.util.zip.ZipFile(jar.toFile())){var entry=z.getEntry("assets/minecraft/textures/entity/player/"+(index<9?"slim/":"wide/")+names[index%9]+".png");if(entry==null)return "";try(var in=z.getInputStream(entry)){return decode(in.readNBytes(1024*1024+1));}}
 }
 static String decode(byte[] png)throws Exception {return decode(png,false);}
 static String icon(byte[] png)throws Exception{return decode(png,true);}
 private static String decode(byte[] png,boolean icon)throws Exception {
  if(png.length>1024*1024||png.length<33||ByteBuffer.wrap(png).getLong()!=0x89504e470d0a1a0aL)throw new IOException("Invalid skin");
  ByteBuffer in=ByteBuffer.wrap(png);in.position(8);int w=0,h=0,type=-1;byte[] palette=null,alpha=null;ByteArrayOutputStream packed=new ByteArrayOutputStream();
  while(in.remaining()>=12){int len=in.getInt(),tag=in.getInt();if(len<0||len>in.remaining()-4)throw new IOException("Invalid skin");byte[] data=new byte[len];in.get(data);long expected=Integer.toUnsignedLong(in.getInt());CRC32 crc=new CRC32();crc.update(ByteBuffer.allocate(4).putInt(tag).array());crc.update(data);if(crc.getValue()!=expected)throw new IOException("Invalid skin checksum");
   if(tag==0x49484452){if(len!=13)throw new IOException("Invalid skin header");ByteBuffer head=ByteBuffer.wrap(data);w=head.getInt();h=head.getInt();if((icon?(w<1||h<1||w>512||h>512):((w!=64&&w!=128)||(h!=w&&h!=w/2)))||head.get()!=8)throw new IOException("Unsupported skin");type=head.get();if(head.get()!=0||head.get()!=0||head.get()!=0)throw new IOException("Unsupported skin encoding");}
   else if(tag==0x49444154)packed.write(data);else if(tag==0x504c5445)palette=data;else if(tag==0x74524e53)alpha=data;else if(tag==0x49454e44)break;
  }
  int bpp=type==6?4:type==2?3:type==3?1:0;if(bpp==0||w==0)throw new IOException("Unsupported skin pixels");int stride=w*bpp;byte[] raw;try(var z=new InflaterInputStream(new ByteArrayInputStream(packed.toByteArray()))){raw=z.readNBytes((stride+1)*h+1);}if(raw.length!=(stride+1)*h)throw new IOException("Invalid skin size");
  byte[] pixels=new byte[stride*h];int at=0;for(int y=0;y<h;y++){int filter=raw[at++]&255;for(int x=0;x<stride;x++){int a=x>=bpp?pixels[y*stride+x-bpp]&255:0,b=y>0?pixels[(y-1)*stride+x]&255:0,c=y>0&&x>=bpp?pixels[(y-1)*stride+x-bpp]&255:0;int prediction=switch(filter){case 0->0;case 1->a;case 2->b;case 3->(a+b)/2;case 4->{int p=a+b-c,pa=Math.abs(p-a),pb=Math.abs(p-b),pc=Math.abs(p-c);yield pa<=pb&&pa<=pc?a:pb<=pc?b:c;}default->throw new IOException("Invalid skin filter");};pixels[y*stride+x]=(byte)((raw[at++]&255)+prediction);}}
  if(icon){StringBuilder out=new StringBuilder(1536);char[] hex="0123456789abcdef".toCharArray();for(int y=0;y<16;y++)for(int x=0;x<16;x++){int[] col=color(pixels,palette,alpha,type,bpp,stride,x*w/16,y*h/16);for(int n=0;n<3;n++){int v=(col[n]*col[3]+24*(255-col[3])+127)/255;out.append(hex[v>>4]).append(hex[v&15]);}}return out.toString();}
  StringBuilder face=new StringBuilder(384);int scale=w/64;for(int y=0;y<8;y++)for(int x=0;x<8;x++){int[] base=color(pixels,palette,alpha,type,bpp,stride,(8+x)*scale,(8+y)*scale),hat=color(pixels,palette,alpha,type,bpp,stride,(40+x)*scale,(8+y)*scale);int a=hat[3];for(int i=0;i<3;i++)face.append(String.format(Locale.ROOT,"%02x",(hat[i]*a+base[i]*(255-a)+127)/255));}return face.toString();
 }
 static int[] color(byte[] p,byte[] palette,byte[] alpha,int type,int bpp,int stride,int x,int y)throws IOException{int at=y*stride+x*bpp;if(type==3){int index=p[at]&255;if(palette==null||index*3+2>=palette.length)throw new IOException("Invalid skin palette");return new int[]{palette[index*3]&255,palette[index*3+1]&255,palette[index*3+2]&255,alpha!=null&&index<alpha.length?alpha[index]&255:255};}return new int[]{p[at]&255,p[at+1]&255,p[at+2]&255,type==6?p[at+3]&255:255};}
}
