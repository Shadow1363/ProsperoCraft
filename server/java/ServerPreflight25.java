import java.io.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.jar.JarFile;

public class ServerPreflight25 {
 private static native void checkpoint(String stage);
 private static void trace(String stage){if(Boolean.getBoolean("ps5.probe.dependencyTrace"))checkpoint("MC preflight: "+stage);}
 private static final class NullProbe {int value;}
 private static int readNullProbe(NullProbe probe){return probe.value;}
 public static void main(String[] args) throws Exception {
  String stage="read official artifact inventory";
  try {
   trace(stage);if(Runtime.version().feature()!=25)throw new AssertionError("Java 25 required");
   stage="exercise Java null exception and signal continuation";trace(stage);
   try{readNullProbe(null);throw new AssertionError("Missing null exception");}catch(NullPointerException expected){}
   System.out.println("MC_NULL_EXCEPTION_OK normal Java null exception caught");
   stage="exercise native ZIP compression allocations";trace(stage);
   byte[] zipInput=new byte[65536],zipEncoded=new byte[66000],zipOutput=new byte[65536];new Random(38).nextBytes(zipInput);int zipSize;
   try(var deflater=new java.util.zip.Deflater()){deflater.setInput(zipInput);deflater.finish();zipSize=deflater.deflate(zipEncoded);if(!deflater.finished())throw new IOException("ZIP preflight compression incomplete");}
   try(var inflater=new java.util.zip.Inflater()){inflater.setInput(zipEncoded,0,zipSize);if(inflater.inflate(zipOutput)!=zipInput.length||!inflater.finished()||!Arrays.equals(zipInput,zipOutput))throw new IOException("ZIP preflight decompression mismatch");}
   System.out.println("MC_ZIP_STREAM_OK native deflate/inflate allocations and content verified");
   Path root=Path.of(System.getProperty("ps5.mc.assets","/app0/assets/java25"));
   Properties inventory=new Properties();try(var input=Files.newInputStream(root.resolve("server-inventory.properties"))){inventory.load(input);}
   if(inventory.size()!=40)throw new AssertionError("Expected 40 pinned JARs");
   for(String file:new TreeSet<>(inventory.stringPropertyNames())) {
    if(file.contains("/")||file.contains("\\")||!file.endsWith(".jar"))throw new AssertionError("Invalid inventory path");
    stage="verify JAR SHA-256 "+file;trace(stage);
    MessageDigest digest=MessageDigest.getInstance("SHA-256");
    try(var input=Files.newInputStream(root.resolve("jars").resolve(file))){byte[] block=new byte[65536];int count;while((count=input.read(block))!=-1)digest.update(block,0,count);}
    if(!HexFormat.of().formatHex(digest.digest()).equals(inventory.getProperty(file)))throw new AssertionError("JAR checksum "+file);
   }
   stage="check server Java 25 bytecode";trace(stage);
   try(JarFile jar=new JarFile(root.resolve("jars/server-26.3.jar").toFile())) {
    var entry=jar.getJarEntry("net/minecraft/server/Main.class");if(entry==null)throw new AssertionError("Missing server main");
    try(var input=new DataInputStream(jar.getInputStream(entry))) {
     if(input.readInt()!=0xCAFEBABE)throw new AssertionError("Class magic");input.readUnsignedShort();if(input.readUnsignedShort()!=69)throw new AssertionError("Server class version");
    }
   }
   stage="canonicalize and mount vanilla assets through ZipFS";trace(stage);
   Path assetsJar=root.resolve("jars/ps5-platform-diagnostics.jar").toRealPath();
   stage="check readable vanilla asset JAR";trace(stage);
   assetsJar.getFileSystem().provider().checkAccess(assetsJar,AccessMode.READ);
   stage="enumerate packaged asset directory";trace(stage);
   try(var entries=Files.newDirectoryStream(assetsJar.getParent())){boolean found=false;for(Path entry:entries)if(entry.getFileName().equals(assetsJar.getFileName()))found=true;if(!found)throw new IOException("Asset JAR missing from real directory enumeration");}
   stage="mount canonical vanilla asset JAR";trace(stage);
   try(FileSystem assetsFs=FileSystems.newFileSystem(assetsJar,Map.of());InputStream version=Files.newInputStream(assetsFs.getPath("/version.json"))) {
    stage="read vanilla version.json from mounted JAR";trace(stage);
    if(version.read()<0)throw new IOException("Empty vanilla version.json");
   }
   stage="closed vanilla asset ZipFS";trace(stage);
   System.out.println("MC_ASSET_ZIPFS_OK canonical asset path, mount and real version.json read");
   stage="resolve platform modules and server dependency classes";trace(stage);
   ClassLoader loader=ClassLoader.getSystemClassLoader();
   for(String name:new String[]{"org.xml.sax.SAXException","java.util.logging.Logger","java.lang.management.ManagementFactory","sun.misc.Unsafe","org.slf4j.Logger","org.apache.logging.log4j.core.LoggerContext","joptsimple.OptionParser","io.netty.channel.nio.NioEventLoopGroup","com.google.gson.Gson","net.minecraft.server.Main"}) {
    stage="resolve "+name;trace(stage);Class.forName(name,false,loader);
   }
   stage="initialize real memory MXBean and management native library";trace(stage);
   var memory=java.lang.management.ManagementFactory.getMemoryMXBean();
   stage="query real heap memory usage";trace(stage);
   if(memory.getHeapMemoryUsage().getMax()!=Runtime.getRuntime().maxMemory())throw new AssertionError("JVM heap management mismatch");
   stage="query real non-heap memory usage";trace(stage);
   if(memory.getNonHeapMemoryUsage().getUsed()<0)throw new AssertionError("Non-heap management unavailable");
   stage="query actual runtime VM flags";trace(stage);
   var flags=java.lang.management.ManagementFactory.getRuntimeMXBean().getInputArguments();
   if(Boolean.getBoolean("ps5.probe.requireC1")){stage="verify actual C1 compiled results";trace(stage);ps5probe.JitWarmup25.check();}
   else if(!flags.contains("-Xint"))throw new AssertionError("Missing actual interpreter control flag");
   System.out.println("MC_MANAGEMENT_OK actual heap, non-heap and VM flags");
   System.out.println("MC_PREFLIGHT_OK 26.3 / Java25 / 40 verified JARs");
  }catch(Throwable error){
   StringBuilder causes=new StringBuilder();Throwable cause=error;
   for(int depth=0;cause!=null&&depth<8;depth++,cause=cause.getCause()) {
    if(depth>0)causes.append(" | caused by: ");causes.append(cause);
   }
   throw new Exception("MC preflight stage "+stage+": "+causes,error);
  }
 }
}
