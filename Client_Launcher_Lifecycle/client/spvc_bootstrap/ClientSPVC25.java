import java.nio.*;
import org.lwjgl.*;
import org.lwjgl.system.*;
import org.lwjgl.util.spvc.*;
import static org.lwjgl.system.MemoryUtil.*;
import static org.lwjgl.util.spvc.Spvc.*;
import static org.lwjgl.util.spvc.Spv.*;
/** Original SPIRV-Cross C API;real shader reflection/translation,not game startup. */
public final class ClientSPVC25 {
 public static native void checkpoint(String text);
 static void stage(String text){if(System.getProperty("ps5.test.ffiCore")!=null)System.out.println(text);else checkpoint("SPVC036: "+text);}
 static void check(boolean ok,String text){if(!ok)throw new AssertionError(text);}
 static void ok(int result,String call,long context){if(result!=SPVC_SUCCESS)throw new IllegalStateException(call+" code"+result+": "+spvc_context_get_last_error_string(context));}
 public static void main(String[]args)throws Exception{
  boolean host=System.getProperty("ps5.test.ffiCore")!=null;Configuration.MEMORY_ALLOCATOR.set("system");
  if(host){Configuration.LIBRARY_NAME.set(System.getProperty("ps5.test.ffiCore"));Configuration.SPVC_LIBRARY_NAME.set(System.getProperty("ps5.test.spvc"));System.load(System.getProperty("ps5.test.hostLoader"));}else{Configuration.SPVC_LIBRARY_NAME.set(System.mapLibraryName("ps5spvc"));System.loadLibrary("ps5clientgpu");}
  Library.initialize();
  try(MemoryStack stack=MemoryStack.stackPush()){
   IntBuffer major=stack.mallocInt(1),minor=stack.mallocInt(1),patch=stack.mallocInt(1);spvc_get_version(major,minor,patch);check(major.get(0)==0&&minor.get(0)==68&&patch.get(0)==0,"pinned C API0.68.0");
  }
  for(int cycle=0;cycle<3;cycle++){
   try(MemoryStack stack=MemoryStack.stackPush()){
    PointerBuffer output=stack.callocPointer(1);check(spvc_context_create(output)==SPVC_SUCCESS&&output.get(0)!=0,"real context create");long context=output.get(0);
    try{
     IntBuffer invalid=stack.ints(0,0,0,0,0);int bad=spvc_context_parse_spirv(context,invalid,invalid.remaining(),output);check(bad==SPVC_ERROR_INVALID_SPIRV,"malformed SPIR-V error code");check(!spvc_context_get_last_error_string(context).isEmpty(),"real error message");spvc_context_release_allocations(context);
     ByteBuffer code=ClientShaderCode25.code(stack);ByteBuffer guarded=memAlloc(code.remaining()+128).order(ByteOrder.nativeOrder());
     try{
      for(int i=0;i<guarded.capacity();i++)guarded.put(i,(byte)0x5a);guarded.put(0,code,code.position(),code.remaining());guarded.limit(code.remaining());
      ok(spvc_context_parse_spirv(context,guarded.asIntBuffer(),code.remaining()/4,output),"parse actual validated SPIR-V",context);long ir=output.get(0);check(ir!=0,"parsed IR");
      for(int backend:new int[]{SPVC_BACKEND_GLSL,SPVC_BACKEND_HLSL,SPVC_BACKEND_MSL}){
       ok(spvc_context_create_compiler(context,backend,ir,SPVC_CAPTURE_MODE_COPY,output),"real compiler create",context);long compiler=output.get(0);
       check(spvc_compiler_get_execution_model(compiler)==SpvExecutionModelGLCompute,"compute execution model");check(spvc_compiler_get_execution_mode_argument_by_index(compiler,SpvExecutionModeLocalSize,0)==64,"local size64");
       ok(spvc_compiler_create_shader_resources(compiler,output),"reflect resources",context);long resources=output.get(0);PointerBuffer list=stack.mallocPointer(1),count=stack.mallocPointer(1);
       ok(spvc_resources_get_resource_list_for_type(resources,SPVC_RESOURCE_TYPE_STORAGE_BUFFER,list,count),"storage resource list",context);check(count.get(0)==1&&list.get(0)!=0,"one SSBO");SpvcReflectedResource storage=SpvcReflectedResource.create(list.get(0));check(spvc_compiler_get_decoration(compiler,storage.id(),SpvDecorationDescriptorSet)==0&&spvc_compiler_get_decoration(compiler,storage.id(),SpvDecorationBinding)==0,"descriptor set0 binding0");
       ok(spvc_resources_get_resource_list_for_type(resources,SPVC_RESOURCE_TYPE_PUSH_CONSTANT,list,count),"push resource list",context);check(count.get(0)==1&&list.get(0)!=0,"one push constant block");SpvcReflectedResource push=SpvcReflectedResource.create(list.get(0));long type=spvc_compiler_get_type_handle(compiler,push.base_type_id());ok(spvc_compiler_get_declared_struct_size(compiler,type,count),"push block size",context);check(count.get(0)==8,"push constant8bytes");
       ok(spvc_compiler_create_compiler_options(compiler,output),"compiler options",context);long options=output.get(0);
       if(backend==SPVC_BACKEND_GLSL){ok(spvc_compiler_options_set_uint(options,SPVC_COMPILER_OPTION_GLSL_VERSION,450),"GLSL450 option",context);ok(spvc_compiler_options_set_bool(options,SPVC_COMPILER_OPTION_GLSL_VULKAN_SEMANTICS,true),"Vulkan semantics",context);}
       if(backend==SPVC_BACKEND_HLSL)ok(spvc_compiler_options_set_uint(options,SPVC_COMPILER_OPTION_HLSL_SHADER_MODEL,50),"HLSL5 option",context);
       ok(spvc_compiler_install_compiler_options(compiler,options),"install options",context);ok(spvc_compiler_compile(compiler,output),"actual shader translation",context);String source=memUTF8(output.get(0));check(source.length()>100&&source.length()<65536,"bounded real source");check(source.hashCode()==(backend==SPVC_BACKEND_GLSL?265161891:backend==SPVC_BACKEND_HLSL?657299176:956349156),"exact translated source fingerprint");check(source.contains("1664525")&&source.contains("1013904223"),"translated shader arithmetic");
       check(backend==SPVC_BACKEND_GLSL?source.contains("#version 450"):backend==SPVC_BACKEND_HLSL?source.contains("numthreads(64"):source.contains("metal_stdlib"),"actual backend syntax");if(host)java.nio.file.Files.writeString(java.nio.file.Path.of(System.getProperty("ps5.test.spvcOutput"),"cycle"+cycle+"-"+backend+(backend==SPVC_BACKEND_HLSL?".hlsl":backend==SPVC_BACKEND_MSL?".metal":".comp")),source);stage("translated cycle"+cycle+" backend"+backend+" sourceBytes"+source.length()+" hash"+source.hashCode()+" reflected SSBO0/push8/local64");
      }
      guarded.limit(guarded.capacity());for(int i=0;i<code.remaining();i++)check(guarded.get(i)==code.get(i),"SPIR-V input unchanged");for(int i=code.remaining();i<guarded.capacity();i++)check(guarded.get(i)==(byte)0x5a,"input guard");
     }finally{memFree(guarded);}
     spvc_context_release_allocations(context);stage("PASS actual SPIRV-Cross cycle"+cycle+":3GLSL/HLSL/MSL translations,reflection/malformed input controls,128guards,context allocation cleanup");
    }finally{spvc_context_destroy(context);}
   }
  }
 }
}
