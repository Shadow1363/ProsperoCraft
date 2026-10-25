import java.nio.*;
import java.nio.file.*;
import org.lwjgl.system.*;
import org.lwjgl.stb.*;
import static org.lwjgl.system.MemoryUtil.*;
import static org.lwjgl.stb.STBImage.*;
import static org.lwjgl.stb.STBImageWrite.*;
/** Real STB JNI/codecs acceptance;not Minecraft startup or full codec coverage. */
public final class ClientSTB25 {
 public static native void checkpoint(String text);
 static void stage(String text){if(System.getProperty("ps5.test.ffiCore")!=null)System.out.println(text);else checkpoint("STB031: "+text);}
 static void check(boolean ok,String what){if(!ok)throw new AssertionError(what);}
 public static void main(String[]args)throws Exception{
  boolean host=System.getProperty("ps5.test.ffiCore")!=null;
  Configuration.MEMORY_ALLOCATOR.set("system");
  if(host)Configuration.LIBRARY_NAME.set(System.getProperty("ps5.test.ffiCore"));else System.loadLibrary("ps5clientgpu");
  Library.initialize();Path directory=host?Files.createTempDirectory("real-stb-"):Path.of("/download0/stb-probe");Files.createDirectories(directory);
  try{
   for(int cycle=0;cycle<3;cycle++){
    ByteBuffer original=memAlloc(256),encoded=null;Path png=directory.resolve("cycle"+cycle+".png");
    try(MemoryStack stack=MemoryStack.stackPush()){
     for(int i=0;i<256;i++)original.put(i,(byte)((i*37+cycle*53)&255));
     check(stbi_write_png(png.toString(),8,8,4,original,32),"real PNG encode/file write");byte[]file=Files.readAllBytes(png);check(file.length>8&&file[0]==(byte)137&&file[1]=='P',"real encoded PNG");
     encoded=memAlloc(file.length+128);for(int i=0;i<encoded.capacity();i++)encoded.put(i,(byte)0x5a);encoded.put(0,file);encoded.limit(file.length);
     IntBuffer width=stack.mallocInt(1),height=stack.mallocInt(1),channels=stack.mallocInt(1);
     check(stbi_info_from_memory(encoded,width,height,channels)&&width.get(0)==8&&height.get(0)==8&&channels.get(0)==4,"native PNG dimensions/channels");
     ByteBuffer decoded=stbi_load_from_memory(encoded,width,height,channels,4);check(decoded!=null,"real PNG decode: "+stbi_failure_reason());
     try{check(decoded.remaining()==256,"decoded size");for(int i=0;i<256;i++)check(decoded.get(i)==original.get(i),"RGBA roundtrip byte"+i);}finally{stbi_image_free(decoded);}
     encoded.limit(8);ByteBuffer bad=stbi_load_from_memory(encoded,width,height,channels,4);if(bad!=null){stbi_image_free(bad);throw new AssertionError("truncated PNG accepted");}check(stbi_failure_reason()!=null,"native failure reason");
     encoded.limit(encoded.capacity());for(int i=file.length;i<encoded.capacity();i++)check(encoded.get(i)==(byte)0x5a,"encoded input guard");
     ByteBuffer invalid=stack.bytes((byte)'N',(byte)'O',(byte)'P',(byte)'E');IntBuffer error=stack.ints(0);long vorbis=STBVorbis.stb_vorbis_open_memory(invalid,error,null);if(vorbis!=0){STBVorbis.stb_vorbis_close(vorbis);throw new AssertionError("invalid Vorbis accepted");}check(error.get(0)!=0,"real Vorbis error control");
     float noise=STBPerlin.stb_perlin_noise3(0.125f+cycle,0.25f,0.75f,0,0,0);check(Float.isFinite(noise)&&Math.abs(noise)<2,"actual Perlin result");check(STBTTFontinfo.SIZEOF>0&&STBVorbisInfo.SIZEOF>0,"native struct ABI sizes");
     stage("PASS actual STB cycle"+cycle+":PNG8x8/256exact RGBA bytes,128guards,truncated PNG+invalid Vorbis controls,Perlin/native structs");
    }finally{memFree(original);if(encoded!=null)memFree(encoded);Files.deleteIfExists(png);}
   }
  }finally{if(host)Files.deleteIfExists(directory);}
 }
}
