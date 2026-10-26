/* Host-only enum-dispatch control;never packaged. Not a PS5 hardware test. */
import org.lwjgl.system.*;
import java.lang.reflect.*;
import sun.misc.Unsafe;
public class PS5OpenGLDispatchHost25 {
 public static void main(String[]args)throws Exception{
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.LIBRARY_NAME.set(System.getProperty("ps5.test.ffiCore"));Library.initialize();MemoryUtil.memBackend();
  Field uf=Unsafe.class.getDeclaredField("theUnsafe");uf.setAccessible(true);Unsafe u=(Unsafe)uf.get(null);
  Field field=Platform.class.getDeclaredField("current");Object base=u.staticFieldBase(field);long offset=u.staticFieldOffset(field);Platform previous=Platform.get();
  u.putObjectVolatile(base,offset,Platform.PS5);
  try{ClientOpenGL25.main(args);}finally{u.putObjectVolatile(base,offset,previous);}
 }
}
