import java.io.*;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.UUID;
import org.lwjgl.system.Configuration;
import org.lwjgl.system.MemoryUtil;

/** Invokes the original client entry point; no game class replacement/hooks. */
public final class ClientStartup25 {
 public static native void checkpoint(String text);
 private static void stage(String text){checkpoint("MC Startup043: "+text);}
 public static String[] launchArguments(Path work,Path assets){
  String name="PS5Probe",uuid=UUID.nameUUIDFromBytes(("OfflinePlayer:"+name).getBytes(StandardCharsets.UTF_8)).toString();
  return new String[]{"--demo","--disableMultiplayer","--disableChat","--username",name,"--uuid",uuid,"--accessToken","0","--version","26.3","--versionType","release","--gameDir",work.toString(),"--assetsDir",assets.toString(),"--assetIndex","34","--graphicsBackend","vulkan","--width","1280","--height","720"};
 }
 public static void prepareWork(Path work)throws IOException{
  Files.createDirectories(work);Files.createDirectories(work.resolve("native-cache"));Files.createDirectories(work.resolve("resourcepacks"));
  Path options=work.resolve("options.txt");if(!Files.exists(options))Files.writeString(options,"soundCategory_master:0.0\nsoundCategory_music:0.0\n",StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW);
 }
 /** Real LWJGL system allocator,including paired grow/free and alignment. */
 public static String verifyNativeAllocation(){
  var allocator=MemoryUtil.getAllocator();long[] pointers=new long[3];long aligned=0,zeroed=0;int bytes=4*1024*1024;
  try{
   for(int i=0;i<pointers.length;i++){
    pointers[i]=allocator.malloc(bytes);if(pointers[i]==0)throw new OutOfMemoryError("LWJGL native preflight4MiB allocation"+i);
    MemoryUtil.memSet(pointers[i],0x35+i,bytes);
   }
   long grown=allocator.realloc(pointers[0],bytes*2L);if(grown==0)throw new OutOfMemoryError("LWJGL native preflight grow8MiB");pointers[0]=grown;
   for(int i=0;i<pointers.length;i++)for(int offset=0;offset<bytes;offset+=4096)if(MemoryUtil.memGetByte(pointers[i]+offset)!=(byte)(0x35+i))throw new AssertionError("Native allocation/grow contents");
   if(MemoryUtil.memGetByte(grown+bytes-1)!=0x35)throw new AssertionError("Native grow tail");MemoryUtil.memSet(grown+bytes,0x6a,bytes);if(MemoryUtil.memGetByte(grown+bytes*2L-1)!=0x6a)throw new AssertionError("Native grown extent");
   zeroed=allocator.calloc(1,65536);if(zeroed==0)throw new OutOfMemoryError("Native calloc");for(int i=0;i<65536;i++)if(MemoryUtil.memGetByte(zeroed+i)!=0)throw new AssertionError("Native calloc zeroing");
   aligned=allocator.aligned_alloc(4096,bytes);if(aligned==0||(aligned&4095)!=0)throw new AssertionError("Native4096 alignment");MemoryUtil.memSet(aligned,0x5c,bytes);if(MemoryUtil.memGetByte(aligned+bytes-1)!=0x5c)throw new AssertionError("Native aligned extent");
  }finally{if(aligned!=0)allocator.aligned_free(aligned);if(zeroed!=0)allocator.free(zeroed);for(long pointer:pointers)if(pointer!=0)allocator.free(pointer);}
  return "PASS real LWJGL system allocator:3x4MiB,grow8MiB/preserved pages,new extent,calloc64KiB zeroes,4096-aligned4MiB and paired cleanup";
 }
 public static void main(String[] args)throws Throwable{
  Path work=Path.of("/download0/mc-client"),assets=Path.of("/app0/assets/java25/game-assets");prepareWork(work);
  if(!Files.isRegularFile(assets.resolve("indexes/34.json")))throw new IOException("Packaged original asset index missing");
  PrintStream previousOut=System.out,previousErr=System.err;
  PrintStream console=new PrintStream(new FileOutputStream(Path.of("/download0/java25-exceptions.log").toFile(),false),true,StandardCharsets.UTF_8);
  System.setOut(console);System.setErr(console);
  try{
   System.setProperty("user.dir",work.toString());System.setProperty("user.home",work.toString());System.setProperty("java.io.tmpdir",work.resolve("native-cache").toString());
   for(String key:new String[]{"jna.tmpdir","io.netty.native.workdir"})System.setProperty(key,work.resolve("native-cache").toString());
   System.setProperty("jna.nosys","true");
   Configuration.OPENGL_CONTEXT_API.set("OSMesa");Configuration.OPENGL_OSMESA_LIBRARY_NAME.set(System.mapLibraryName("ps5clientgl"));
   Configuration.SPVC_LIBRARY_NAME.set(System.mapLibraryName("ps5spvc"));
   Configuration.MEMORY_ALLOCATOR.set("system");Configuration.OPENAL_LIBRARY_NAME.set(System.mapLibraryName("ps5openal"));Configuration.SDL_LIBRARY_NAME.set(System.mapLibraryName("ps5sdl"));Configuration.VULKAN_LIBRARY_NAME.set(System.mapLibraryName("ps5clientgpu"));Configuration.SHADERC_LIBRARY_NAME.set(System.mapLibraryName("ps5shaderc"));Configuration.SHARED_LIBRARY_EXTRACT_PATH.set(work.resolve("native-cache").toString());
   stage("configure validated036 SPIRV-Cross,035 VMA,033 FreeType,031 STB and029 real OSMesa/OpenGL plus026 libffi/OpenAL and resident SDL/Vulkan/shaderc;other native bindings remain incomplete");
   System.loadLibrary("ps5clientgpu");System.loadLibrary("ps5clientgl");System.loadLibrary("ps5shaderc");System.loadLibrary("ps5sdl");System.loadLibrary("ps5openal");
   stage(verifyNativeAllocation());
   Runtime heap=Runtime.getRuntime();stage("heap maxMiB="+(heap.maxMemory()/1048576)+" committedMiB="+(heap.totalMemory()/1048576)+" usedMiB="+((heap.totalMemory()-heap.freeMemory())/1048576));
   stage("original Main class lookup;offline demo arguments,no credentials or multiplayer");
   Class<?> main=Class.forName("net.minecraft.client.main.Main",false,ClassLoader.getSystemClassLoader());Method method=main.getMethod("main",String[].class);
   stage("ENTER original net.minecraft.client.main.Main.main;menu/world not yet validated");
   console.println("Original Minecraft26.3 Main entry;offline demo test. Native dependency coverage remains incomplete.");
   try{method.invoke(null,(Object)launchArguments(work,assets));}
   catch(InvocationTargetException failure){throw failure.getCause();}
   stage("Original Main returned;this alone does not establish menu or gameplay success");
   throw new IllegalStateException("Original game main returned;inspect exceptions.log/latest.log and actual visible state;no automatic menu PASS");
  }catch(Throwable failure){failure.printStackTrace(console);stage("Original startup stopped: "+failure);throw failure;}
  finally{console.flush();System.setOut(previousOut);System.setErr(previousErr);console.close();}
 }
}
