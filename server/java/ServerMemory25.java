import java.lang.reflect.*;
import java.util.Arrays;

/** Verify the configured allocator without changing any packet bytes/codecs. */
public final class ServerMemory25 {
 public static void check()throws Exception {
  if(!"unpooled".equals(System.getProperty("io.netty.allocator.type")))throw new IllegalStateException("PS5 network memory settings missing");
  Class<?> allocType=Class.forName("io.netty.buffer.ByteBufAllocator"),bufType=Class.forName("io.netty.buffer.ByteBuf");
  Object allocator=allocType.getField("DEFAULT").get(null);
  if(!allocator.getClass().getSimpleName().equals("UnpooledByteBufAllocator"))throw new IllegalStateException("Unexpected network allocator: "+allocator.getClass());
  Object buffer=allocType.getMethod("ioBuffer",int.class,int.class).invoke(allocator,256,1048576);
  try {
   boolean direct=(boolean)bufType.getMethod("isDirect").invoke(buffer);
   byte[] expected=new byte[65536],observed=new byte[expected.length];for(int i=0;i<expected.length;i++)expected[i]=(byte)(i*31);
   bufType.getMethod("writeBytes",byte[].class).invoke(buffer,(Object)expected);
   bufType.getMethod("readBytes",byte[].class).invoke(buffer,(Object)observed);
   if(!Arrays.equals(expected,observed))throw new IllegalStateException("Network buffer growth changed bytes");
   System.out.println("MC_NETWORK_MEMORY_OK allocator=unpooled ioBufferDirect="+direct+" growthBytes=65536 heapMax="+Runtime.getRuntime().maxMemory());
  }finally{bufType.getMethod("release").invoke(buffer);}
 }
}
