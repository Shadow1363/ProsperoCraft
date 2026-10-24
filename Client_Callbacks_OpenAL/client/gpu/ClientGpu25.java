import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import org.lwjgl.system.Configuration;
import org.lwjgl.system.Library;
import org.lwjgl.system.MemoryUtil;

/** Consumer-owned real JNI/Vulkan transfer acceptance; does not replace game classes. */
public final class ClientGpu25 {
 public static native void checkpoint(String text);
 private static native long open();
 private static native void transfer(long handle, ByteBuffer in, ByteBuffer out, int bytes, int pattern);
 private static native void close(long handle);
 private static void rejects(Class<? extends Throwable> kind,Runnable call) {
  try {call.run();} catch(Throwable e) {if(kind.isInstance(e))return;throw new AssertionError("Unexpected error",e);}
  throw new AssertionError("Expected "+kind.getSimpleName());
 }
 public static void main(String[] args) {
  Configuration.MEMORY_ALLOCATOR.set("system");Library.initialize();
  if(!MemoryUtil.memBackend().getClass().getSimpleName().equals("MemoryBackendUnsafe"))throw new AssertionError("Java25 Unsafe backend");
  System.loadLibrary("ps5clientgpu");
  checkpoint("Java GPU native library loaded; real LWJGL memory active");
  for(int cycle=0;cycle<3;cycle++) {
   long session=open();if(session==0)throw new AssertionError("No GPU session");
   ByteBuffer in=MemoryUtil.memAlloc(65536+32).order(ByteOrder.nativeOrder());
   ByteBuffer out=MemoryUtil.memAlloc(65536+32).order(ByteOrder.nativeOrder());
   try {
    rejects(IllegalStateException.class,()->open());
    rejects(IllegalArgumentException.class,()->transfer(session,null,out,16,0));
    rejects(IllegalArgumentException.class,()->transfer(session,in,null,16,0));
    rejects(IllegalArgumentException.class,()->transfer(session,ByteBuffer.allocateDirect(8),out,16,0));
    rejects(IllegalArgumentException.class,()->transfer(session,ByteBuffer.allocate(64),out,16,0));
    rejects(IllegalArgumentException.class,()->transfer(session,in,in,16,0));
    rejects(IllegalArgumentException.class,()->transfer(session,in,out,7,0));
    rejects(IllegalArgumentException.class,()->transfer(session,in,out,65544,0));
    rejects(IllegalStateException.class,()->transfer(0,in,out,16,0));
    Throwable[] crossThread=new Throwable[1];
    Thread t=new Thread(()->{try{transfer(session,in,out,16,0);}catch(Throwable error){crossThread[0]=error;}},"GPU-owner-control");
    t.start();try{t.join();}catch(InterruptedException e){Thread.currentThread().interrupt();throw new AssertionError(e);}
    if(!(crossThread[0] instanceof IllegalStateException))throw new AssertionError("GPU session thread ownership");
    for(int size:new int[]{8,256,4096,65536}) {
     int pattern=0xa5f00d00^size^cycle;
     MemoryUtil.memSet(MemoryUtil.memAddress(out),0x6d,out.capacity());
     for(int i=0;i<size/4;i++)in.putInt(i*4,(i*0x9e3779b9)^pattern);
     transfer(session,in,out,size,pattern);
     for(int i=0;i<size/4;i++) {
      int expected=i<size/8?in.getInt(i*4):pattern;
      if(out.getInt(i*4)!=expected)throw new AssertionError("GPU readback mismatch at"+i+" size"+size);
     }
     for(int i=size;i<out.capacity();i++)if(out.get(i)!=(byte)0x6d)throw new AssertionError("GPU destination guard overwritten");
    }
    checkpoint("GPU cycle "+cycle+": copy/fill/readback8..65536 bytes, Java byte checks and native error controls PASS");
   } finally {MemoryUtil.memFree(out);MemoryUtil.memFree(in);close(session);}
   close(session);
   rejects(IllegalStateException.class,()->transfer(session,ByteBuffer.allocateDirect(16),ByteBuffer.allocateDirect(16),16,0));
  }
  checkpoint("PASS Java25 + actual LWJGL + Vulkan GPU submission/readback; three create/destroy cycles");
 }
}
