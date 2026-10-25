import java.nio.*;
import java.nio.file.*;
import java.util.Arrays;
import org.lwjgl.*;
import org.lwjgl.system.*;
import org.lwjgl.util.freetype.*;
import static org.lwjgl.system.MemoryUtil.*;
import static org.lwjgl.util.freetype.FreeType.*;
/** Genuine FreeType downcalls/font rasterization;no game startup or replacement classes. */
public final class ClientFreeType25 {
 public static native void checkpoint(String text);
 static void stage(String text){if(System.getProperty("ps5.test.ffiCore")!=null)System.out.println(text);else checkpoint("FONT033: "+text);}
 static void check(boolean ok,String text){if(!ok)throw new AssertionError(text);}
 public static void main(String[]args)throws Exception{
  boolean host=System.getProperty("ps5.test.ffiCore")!=null;
  Configuration.MEMORY_ALLOCATOR.set("system");
  if(host){Configuration.LIBRARY_NAME.set(System.getProperty("ps5.test.ffiCore"));Configuration.FREETYPE_LIBRARY_NAME.set(System.getProperty("ps5.test.freetype"));System.load(System.getProperty("ps5.test.hostLoader"));}
  else System.loadLibrary("ps5clientgpu");
  Library.initialize();
  byte[]file=Files.readAllBytes(Path.of(host?System.getProperty("ps5.test.font"):"/app0/assets/java25/font-probe/Abel-Regular.ttf"));
  ByteBuffer font=memAlloc(file.length+128);font.put(0,file);for(int i=file.length;i<font.capacity();i++)font.put(i,(byte)0x5a);font.limit(file.length);
  long digest=0xcbf29ce484222325L;
  try{
   for(int cycle=0;cycle<3;cycle++){
    try(MemoryStack stack=MemoryStack.stackPush()){
     PointerBuffer output=stack.callocPointer(1);check(FT_Init_FreeType(output)==0&&output.get(0)!=0,"real FT_Init_FreeType");long library=output.get(0);
     try{
      IntBuffer major=stack.mallocInt(1),minor=stack.mallocInt(1),patch=stack.mallocInt(1);FT_Library_Version(library,major,minor,patch);check(major.get(0)==2&&minor.get(0)==14&&patch.get(0)==1,"pinned FreeType2.14.1");
      ByteBuffer invalid=stack.bytes((byte)'N',(byte)'O',(byte)'P',(byte)'E');output.put(0,0);int bad=FT_New_Memory_Face(library,invalid,0,output);if(bad==0){if(output.get(0)!=0)FT_Done_Face(FT_Face.create(output.get(0)));throw new AssertionError("invalid font accepted");}check(output.get(0)==0,"failed font output");
      check(FT_New_Memory_Face(library,font,0,output)==0&&output.get(0)!=0,"real font face");FT_Face face=FT_Face.create(output.get(0));
      try{
       check("Abel".equals(face.family_nameString())&&face.num_glyphs()>100,"native font metadata/struct ABI");int size=16+cycle*8;check(FT_Set_Pixel_Sizes(face,0,size)==0,"pixel size");
       for(int character:new int[]{'A','g','@'}){
        check(FT_Get_Char_Index(face,character)>0,"glyph index");check(FT_Load_Char(face,character,FT_LOAD_RENDER|FT_LOAD_NO_HINTING)==0,"real glyph render");FT_GlyphSlot glyph=face.glyph();FT_Bitmap bitmap=glyph.bitmap();int width=bitmap.width(),rows=bitmap.rows(),pitch=bitmap.pitch();
        check(width>0&&width<=size*2&&rows>0&&rows<=size*2&&pitch>=width&&pitch<=size*4&&bitmap.pixel_mode()==FT_PIXEL_MODE_GRAY,"native bitmap shape/mode");check(glyph.advance().x()>0&&glyph.advance().x()<size*128,"glyph advance");
        byte[]pixels=new byte[pitch*rows];bitmap.buffer(pixels.length).get(pixels);long sum=0;for(byte value:pixels){int v=Byte.toUnsignedInt(value);sum+=v;digest=(digest^v)*0x100000001b3L;}check(sum>0&&sum<(long)width*rows*255,"real antialiased glyph pixels");
        check(FT_Load_Char(face,character,FT_LOAD_RENDER|FT_LOAD_NO_HINTING)==0,"repeat render");byte[]repeat=new byte[pixels.length];face.glyph().bitmap().buffer(repeat.length).get(repeat);check(Arrays.equals(pixels,repeat),"repeat exact glyph bitmap");
        stage("glyph cycle"+cycle+" char"+character+" "+width+"x"+rows+" pitch"+pitch+" sum"+sum);
       }
       check(FT_Load_Char(face,' ',FT_LOAD_RENDER|FT_LOAD_NO_HINTING)==0&&face.glyph().bitmap().rows()==0&&face.glyph().advance().x()>0,"space control");
      }finally{check(FT_Done_Face(face)==0,"FT_Done_Face");}
     }finally{check(FT_Done_FreeType(library)==0,"FT_Done_FreeType");}
     font.limit(font.capacity());for(int i=0;i<file.length;i++)check(font.get(i)==file[i],"font input unchanged");for(int i=file.length;i<font.capacity();i++)check(font.get(i)==(byte)0x5a,"font input guard");font.limit(file.length);
     stage("PASS actual FreeType cycle"+cycle+":version2.14.1,3glyphs+repeat,space/invalid font controls,128guards,face/library cleanup");
    }
   }
   stage("FreeType nine glyph FNV64="+Long.toUnsignedString(digest,16));check(digest==0xfc260d7c9d8a2036L,"exact nine glyph rasterization fingerprint");
  }finally{memFree(font);}
 }
}
