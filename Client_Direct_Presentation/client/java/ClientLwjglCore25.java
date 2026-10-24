import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.IntBuffer;
import org.lwjgl.system.Configuration;
import org.lwjgl.system.Library;
import org.lwjgl.system.JNI;
import org.lwjgl.system.APIUtil;
import org.lwjgl.system.Platform;
import org.lwjgl.system.SharedLibrary;
import org.lwjgl.system.ps5.PS5Library;
import org.lwjgl.system.MemoryStack;
import org.lwjgl.system.MemoryUtil;
import org.lwjgl.system.Pointer;

/** Actual upstream LWJGL memory/core JNI; no graphics driver or callbacks. */
public final class ClientLwjglCore25 {
 public static native void checkpoint(String text);
 public static void main(String[] args) {
  Configuration.MEMORY_ALLOCATOR.set("system");
  Library.initialize();
  if(Pointer.POINTER_SIZE!=8||MemoryUtil.PAGE_SIZE<=0||MemoryUtil.CACHE_LINE_SIZE<=0)throw new AssertionError("native sizes");
  String backend=MemoryUtil.memBackend().getClass().getSimpleName();
  if(!backend.equals("MemoryBackendUnsafe"))throw new AssertionError("Expected Java25 Unsafe backend, got "+backend);
  for(int repeat=0;repeat<16;repeat++) {
   ByteBuffer bytes=MemoryUtil.memAlloc(1024).order(ByteOrder.nativeOrder());
   try {
    long address=MemoryUtil.memAddress(bytes);MemoryUtil.memSet(address,0,1024);
    IntBuffer ints=bytes.asIntBuffer();
    for(int i=0;i<ints.capacity();i++)ints.put(i,i*19+7);
    for(int i=0;i<ints.capacity();i++)if(MemoryUtil.memGetInt(address+i*4L)!=i*19+7)throw new AssertionError("native memory view");
    MemoryUtil.memCopy(address,address+512,512);
    for(int i=0;i<128;i++)if(ints.get(i+128)!=ints.get(i))throw new AssertionError("native memcpy");
    bytes=MemoryUtil.memRealloc(bytes,2048);
    for(int i=0;i<128;i++)if(bytes.getInt(i*4)!=i*19+7)throw new AssertionError("native realloc prefix");
   } finally {MemoryUtil.memFree(bytes);}
   ByteBuffer zero=MemoryUtil.memCalloc(257);try{for(int i=0;i<zero.capacity();i++)if(zero.get(i)!=0)throw new AssertionError("native calloc");}finally{MemoryUtil.memFree(zero);}
   ByteBuffer aligned=MemoryUtil.memAlignedAlloc(64,512);try{if((MemoryUtil.memAddress(aligned)&63)!=0)throw new AssertionError("native alignment");}finally{MemoryUtil.memAlignedFree(aligned);}
  }
  long raw=JNI.invokePP(128L,MemoryUtil.getAllocator().getMalloc());
  if(raw==0)throw new OutOfMemoryError("native function-pointer malloc");
  try{MemoryUtil.memSet(raw,0x35,128);for(int i=0;i<128;i++)if(MemoryUtil.memGetByte(raw+i)!=0x35)throw new AssertionError("JNI function-pointer memory");}
  finally{JNI.invokePV(raw,MemoryUtil.getAllocator().getFree());}
  String text="PS5 — λ / 😀";ByteBuffer utf=MemoryUtil.memUTF8(text,false);try{if(!MemoryUtil.memUTF8(utf).equals(text))throw new AssertionError("native UTF8");}finally{MemoryUtil.memFree(utf);}
  try(MemoryStack stack=MemoryStack.stackPush()) {
   var ints=stack.callocInt(32);for(int i=0;i<32;i++)if(ints.get(i)!=0)throw new AssertionError("stack calloc");
   var encoded=stack.UTF8(text,false);if(!MemoryUtil.memUTF8(encoded).equals(text))throw new AssertionError("stack UTF8");
  }
  String library=System.getProperty("ps5.test.coreLibrary","liblwjgl.so");
  SharedLibrary resident=Platform.get()==Platform.PS5?APIUtil.apiCreateLibrary(library):new PS5Library(library);
  try {
   long function=resident.getFunctionAddress("ps5_lwjgl_pointer_size");
   if(function==0||JNI.invokeI(function)!=Pointer.POINTER_SIZE)throw new AssertionError("real resident provider invocation");
   if(resident.getFunctionAddress("ps5_lwjgl_missing_function")!=0)throw new AssertionError("missing function not zero");
   try{resident.getFunctionAddress(ByteBuffer.allocate(4));throw new AssertionError("heap function name accepted");}catch(IllegalArgumentException expected){}
   try{resident.getFunctionAddress(ByteBuffer.allocateDirect(1).put(0,(byte)1));throw new AssertionError("unterminated function name accepted");}catch(IllegalArgumentException expected){}
   try{resident.getFunctionAddress((CharSequence)null);throw new AssertionError("null function name accepted");}catch(NullPointerException expected){}

   try(MemoryStack stack=MemoryStack.stackPush()) {
    if(resident.getFunctionAddress(stack.ASCII("ps5_lwjgl_pointer_size"))!=function)throw new AssertionError("buffer function lookup");
   }
  } finally{resident.free();resident.free();}
  try{resident.getFunctionAddress("ps5_lwjgl_pointer_size");throw new AssertionError("closed provider accepted");}catch(IllegalStateException expected){}
  try{new PS5Library("ps5_lwjgl_missing_library");throw new AssertionError("missing resident library accepted");}catch(UnsatisfiedLinkError expected){}
  checkpoint("MC_CLIENT_LWJGL_CORE_OK actual upstream memory/core JNI; backend="+backend+" pageSize="+MemoryUtil.PAGE_SIZE+" cacheLine="+MemoryUtil.CACHE_LINE_SIZE+"; no graphics/callbacks");
 }
}
