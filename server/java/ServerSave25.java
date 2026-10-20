import java.io.*;
import java.nio.file.*;
import java.lang.reflect.*;
import java.util.Comparator;

/** Probe-owned files only; exercise the vanilla compressed NBT save path. */
public final class ServerSave25 {
 static Object call(Method method,Object target,Object...args)throws Exception {
  try{return method.invoke(target,args);}catch(InvocationTargetException e){if(e.getCause() instanceof Exception x)throw x;throw e;}
 }
 public static void check(Path world)throws Exception {check(world,ClassLoader.getSystemClassLoader());}
 public static void check(Path world,ClassLoader loader)throws Exception {
  String stage="directory";Path directory=null;
  try {
   directory=Files.createTempDirectory(world,".ps5-save-check-");
   Class<?> tag=Class.forName("net.minecraft.nbt.CompoundTag",true,loader),io=Class.forName("net.minecraft.nbt.NbtIo",true,loader),util=Class.forName("net.minecraft.util.Util",true,loader),account=Class.forName("net.minecraft.nbt.NbtAccounter",true,loader);
   Method write=io.getMethod("writeCompressed",tag,Path.class),replace=util.getMethod("safeReplaceFile",Path.class,Path.class,Path.class);
   Path current=directory.resolve("probe.dat"),backup=directory.resolve("probe.dat_old");
   for(int revision=1;revision<=2;revision++) {
    stage="createTempFile";System.out.println("MC_SAVE_CHECK phase="+stage+" revision="+revision);
    Path temp=Files.createTempFile(directory,"probe-",".dat");
    Object data=tag.getConstructor().newInstance();call(tag.getMethod("putInt",String.class,int.class),data,"Revision",revision);
    stage="writeCompressed_SYNC";System.out.println("MC_SAVE_CHECK phase="+stage+" revision="+revision);call(write,null,data,temp);
    stage="safeReplaceFile";System.out.println("MC_SAVE_CHECK phase="+stage+" revision="+revision);call(replace,null,current,temp,backup);
    stage="readCompressed";Object limiter=call(account.getMethod("unlimitedHeap"),null);
    Object read=call(io.getMethod("readCompressed",Path.class,account),null,current,limiter);
    if((int)call(tag.getMethod("getIntOr",String.class,int.class),read,"Revision",-1)!=revision)throw new IOException("NBT revision mismatch");
   }
   if(!Files.isRegularFile(backup)||Files.size(backup)==0)throw new IOException("Save backup missing");
   System.out.println("MC_SAVE_CHECK_OK vanilla NBT SYNC write/read, replacement and backup; probe-owned files only");
  }catch(Exception e){System.out.println("MC_SAVE_CHECK_FAILED phase="+stage);e.printStackTrace(System.out);throw e;}
  finally{if(directory!=null)try(var paths=Files.walk(directory)){for(Path path:paths.sorted(Comparator.reverseOrder()).toList())Files.delete(path);}}
 }
 public static void main(String[] args)throws Exception {check(Path.of(args[0]));}
}
