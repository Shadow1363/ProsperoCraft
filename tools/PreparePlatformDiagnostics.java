import java.lang.classfile.*;
import java.lang.constant.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.*;

/** Local build transform: optional OSHI telemetry and a server tick hook for diagnostics and authorized operator policy. */
public class PreparePlatformDiagnostics {
 public static void main(String[] args)throws Exception {
  String entry="net/minecraft/SystemReport.class",tickEntry="net/minecraft/server/MinecraftServer.class";byte[] original,tickOriginal;
  try(ZipFile jar=new ZipFile(args[0])){original=jar.getInputStream(jar.getEntry(entry)).readAllBytes();tickOriginal=jar.getInputStream(jar.getEntry(tickEntry)).readAllBytes();}
  ClassFile cf=ClassFile.of();ClassModel model=cf.parse(original);Set<String> found=new HashSet<>();
  ClassDesc owner=ClassDesc.of("net.minecraft.SystemReport");
  MethodTypeDesc detail=MethodTypeDesc.ofDescriptor("(Ljava/lang/String;Ljava/lang/String;)V");
  byte[] adapted=cf.transformClass(model,(builder,element)->{
   if(element instanceof MethodModel method && Set.of("putHardware","putSoftware").contains(method.methodName().stringValue())) {
    String name=method.methodName().stringValue();
    if(!method.methodType().stringValue().equals("(Loshi/SystemInfo;)V")||!found.add(name))throw new IllegalStateException("Unexpected telemetry method: "+name);
    int flags=method.flags().flagsMask();MethodTypeDesc type=method.methodTypeSymbol();
    builder.withMethod("ps5$"+name,type,flags,mb->method.forEach(mb::with));
    builder.withMethodBody(name,type,flags,code->code
     .ldc("PS5").ldc("os.name").invokestatic(ClassDesc.of("java.lang.System"),"getProperty",MethodTypeDesc.ofDescriptor("(Ljava/lang/String;)Ljava/lang/String;"))
     .invokevirtual(ClassDesc.of("java.lang.String"),"equals",MethodTypeDesc.ofDescriptor("(Ljava/lang/Object;)Z"))
     .ifThenElse(ps5->ps5.aload(0).ldc(name.equals("putHardware")?"Hardware telemetry":"Operating system telemetry")
       .ldc("Unavailable on PS5: no supported OSHI backend; JVM memory and flags are reported separately")
       .invokevirtual(owner,"setDetail",detail).return_(),
       desktop->desktop.aload(0).aload(1).invokespecial(owner,"ps5$"+name,type).return_()));
   }else builder.with(element);
  });
  if(found.size()!=2)throw new IllegalStateException("Expected exactly two telemetry methods");
  if(!cf.verify(adapted).isEmpty())throw new IllegalStateException("Transformed class failed verification");
  int[] hooks={0};
  byte[] tickAdapted=cf.transformClass(cf.parse(tickOriginal),ClassTransform.transformingMethodBodies(
   method->method.methodName().equalsString("tickServer")&&method.methodType().equalsString("(Ljava/util/function/BooleanSupplier;)V"),
   (code,element)->{
    if(element instanceof java.lang.classfile.instruction.ReturnInstruction&&++hooks[0]==2){code.aload(0).invokestatic(ClassDesc.of("ServerGameplay25"),"tick",MethodTypeDesc.ofDescriptor("(Ljava/lang/Object;)V"));}
    code.with(element);
   }));
  if(hooks[0]!=2||!cf.verify(tickAdapted).isEmpty())throw new IllegalStateException("Expected two original returns with one final tick observer: "+hooks[0]+" errors="+cf.verify(tickAdapted));
  // Minecraft packages are signed: never mix an unsigned replacement class
  // into a signed package. Produce an explicitly unsigned local derivative,
  // keeping the verified original JAR untouched. No signature checks are disabled.
  try(ZipFile source=new ZipFile(args[0]);ZipOutputStream zip=new ZipOutputStream(Files.newOutputStream(Path.of(args[1])))){
   for(String name:Collections.list(source.entries()).stream().map(ZipEntry::getName).sorted().toList()){
    String upper=name.toUpperCase(Locale.ROOT);
    if(upper.startsWith("META-INF/")&&(upper.endsWith(".SF")||upper.endsWith(".RSA")||upper.endsWith(".DSA")||upper.endsWith(".EC")||upper.startsWith("META-INF/SIG-")))continue;
    byte[] bytes=source.getInputStream(source.getEntry(name)).readAllBytes();
    if(name.equals(entry))bytes=adapted;
    if(name.equals(tickEntry))bytes=tickAdapted;
    if(upper.equals("META-INF/MANIFEST.MF")){
     var manifest=new java.util.jar.Manifest(new java.io.ByteArrayInputStream(bytes));
     manifest.getEntries().clear();manifest.getMainAttributes().keySet().removeIf(key->key.toString().toUpperCase(Locale.ROOT).contains("DIGEST")||key.toString().equalsIgnoreCase("Signature-Version"));
     var output=new java.io.ByteArrayOutputStream();manifest.write(output);bytes=output.toByteArray();
    }
    ZipEntry output=new ZipEntry(name);output.setTimeLocal(java.time.LocalDateTime.of(1980,1,1,0,0));zip.putNextEntry(output);zip.write(bytes);zip.closeEntry();
   }
  }
  String before=HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(original));
  String after=HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(adapted));
  String tickBefore=HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(tickOriginal));
  String tickAfter=HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(tickAdapted));
  Files.writeString(Path.of(args[2]),"{\"scope\":\"Local unsigned derivative of hash-verified server JAR; SystemReport optional PS5 OSHI telemetry and one MinecraftServer tick hook for diagnostics and authorized operator policy; desktop telemetry methods preserved; do not redistribute as official\",\"original_class_sha256\":\""+before+"\",\"adapted_class_sha256\":\""+after+"\",\"original_tick_class_sha256\":\""+tickBefore+"\",\"adapted_tick_class_sha256\":\""+tickAfter+"\"}\n");
 }
}
