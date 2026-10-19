import java.lang.classfile.*;
import java.lang.classfile.instruction.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.*;

/** Verify the local derivative only inserts aload_0/invokestatic at final return. */
public class AuditTickObserver {
 static byte[] read(String jar)throws Exception{try(var zip=new ZipFile(jar)){return zip.getInputStream(zip.getEntry("net/minecraft/server/MinecraftServer.class")).readAllBytes();}}
 static List<MethodModel> methods(byte[] bytes){return ClassFile.of().parse(bytes).methods();}
 static List<Instruction> instructions(MethodModel m){return m.code().map(c->c.elementStream().filter(e->e instanceof Instruction).map(e->(Instruction)e).toList()).orElse(List.of());}
 public static void main(String[] args)throws Exception {
  var before=methods(read(args[0]));var after=methods(read(args[1]));
  if(before.size()!=after.size())throw new AssertionError("Method inventory changed");int observed=0;
  for(int n=0;n<before.size();n++){
   MethodModel a=before.get(n),b=after.get(n);
   if(!a.methodName().stringValue().equals(b.methodName().stringValue())||!a.methodType().stringValue().equals(b.methodType().stringValue())||a.flags().flagsMask()!=b.flags().flagsMask())throw new AssertionError("Method changed");
   var original=instructions(a);var changed=new ArrayList<>(instructions(b));
   if(a.methodName().equalsString("tickServer")){
    int end=changed.size();
    if(!(changed.get(end-1) instanceof ReturnInstruction)||!(changed.get(end-2) instanceof InvokeInstruction call)||!call.owner().asInternalName().equals("ServerGameplay25")||!call.name().equalsString("tick")||!call.type().equalsString("(Ljava/lang/Object;)V")||!(changed.get(end-3) instanceof LoadInstruction load)||load.slot()!=0)throw new AssertionError("Unexpected observer position");
    changed.remove(end-2);changed.remove(end-3);observed++;
   }
   if(original.size()!=changed.size())throw new AssertionError("Instruction count changed: "+a.methodName());
   for(int i=0;i<original.size();i++){
    Instruction x=original.get(i),y=changed.get(i);
    if(x.opcode()!=y.opcode())throw new AssertionError("Opcode changed "+a.methodName());
    if(x instanceof InvokeInstruction call&&y instanceof InvokeInstruction other&&!call.method().toString().equals(other.method().toString()))throw new AssertionError("Invocation changed");
   }
  }
  if(observed!=1)throw new AssertionError("Expected one observed method");
  System.out.println("PASS: method inventory/flags and every opcode/invocation preserved; only final tick return gets diagnostic/operator policy hook");
 }
}
