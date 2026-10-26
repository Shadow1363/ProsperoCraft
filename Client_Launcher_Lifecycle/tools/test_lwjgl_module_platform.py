#!/usr/bin/env python3
"""Execute actual module platform dispatch against real host Vulkan and missing OpenAL."""
from pathlib import Path
import argparse,subprocess,json,os
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--java-home',type=Path,required=True);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args()
subprocess.run(['python3',str(ROOT/'tools/build_lwjgl_platform.py'),'--java-home',str(a.java_home),'--offline'],check=True)
subprocess.run(['python3',str(ROOT/'tools/build_lwjgl_module_platform.py'),'--java-home',str(a.java_home),'--offline'],check=True)
subprocess.run(['python3',str(ROOT/'tools/test_lwjgl_core.py'),'--java-home',str(a.java_home),'--runtime-workspace',str(a.runtime_workspace)],check=True)
w=ROOT/'build/module-platform-host-026';w.mkdir(exist_ok=True)
(w/'ModuleDispatch.java').write_text('''import java.lang.reflect.*;import org.lwjgl.system.*;import org.lwjgl.vulkan.*;import org.lwjgl.openal.*;import sun.misc.Unsafe;
public class ModuleDispatch{public static void main(String[]a)throws Exception{
 Configuration.MEMORY_ALLOCATOR.set("system");Configuration.LIBRARY_NAME.set(System.getProperty("ps5.test.coreLibrary"));Library.initialize();MemoryUtil.memBackend();
 Configuration.VULKAN_EXPLICIT_INIT.set(true);Configuration.OPENAL_EXPLICIT_INIT.set(true);
 Configuration.VULKAN_LIBRARY_NAME.set("/opt/homebrew/lib/libMoltenVK.dylib");
 Configuration.OPENAL_LIBRARY_NAME.set("/not-provided/ps5-openal-absent.so");
 // Host-only dispatch control: initialize real host core first,then select the
 // actual enum branch without pretending this host GPU is a PS5 console.
 Field uf=Unsafe.class.getDeclaredField("theUnsafe");uf.setAccessible(true);Unsafe u=(Unsafe)uf.get(null);
 Field pf=Platform.class.getDeclaredField("current");Object base=u.staticFieldBase(pf);long off=u.staticFieldOffset(pf);Platform old=Platform.get();
 u.putObjectVolatile(base,off,Platform.PS5);
 try{
  if(a[0].equals("original")){
   try{VK.create();throw new AssertionError("original unexpectedly accepted PS5");}catch(IllegalStateException expected){System.out.println("PASS original VK rejects PS5 before loader");}
   try{ALC.create();throw new AssertionError("original ALC unexpectedly accepted PS5");}catch(IllegalStateException expected){System.out.println("PASS original ALC rejects PS5 before loader");}
  }else{
   try{VK.create();throw new AssertionError("callback dependency unexpectedly available");}catch(UnsatisfiedLinkError expected){if(!expected.toString().contains("LibFFI.FFI_TYPE_DOUBLE"))throw expected;System.out.println("PASS real VK loader reached upstream allocation-callback/libffi boundary;not full bootstrap success");}
   if(VK.getFunctionProvider()==null||VK.getInstanceVersionSupported()==0)throw new AssertionError("real Vulkan loader");
   System.out.println("PASS PS5 dispatch real MoltenVK function table/version "+VK.getInstanceVersionSupported());
   try{VK.create();throw new AssertionError("duplicate accepted");}catch(IllegalStateException expected){}
   VK.destroy();
   try{ALC.create();throw new AssertionError("missing OpenAL accepted");}catch(UnsatisfiedLinkError expected){if(!expected.toString().contains("PS5 resident library unavailable"))throw expected;System.out.println("PASS PS5 ALC dispatch reaches real missing-library rejection;no fake OpenAL");}
  }
 }finally{u.putObjectVolatile(base,off,old);}
}}
''')
core=ROOT/'build/lwjgl-core-test/lwjgl-host-paired.jar';overlay=ROOT/'build/client-ports/lwjgl-modules/lwjgl-3.4.3-ps5-modules.jar';lock=json.loads((ROOT/'client/26.3.lock.json').read_text());jars=[ROOT/'.tools/client'/r['file']for r in lock['artifacts']if r['file']in('lwjgl-vulkan-3.4.3.jar','lwjgl-openal-3.4.3.jar','jspecify-1.0.0.jar')]
cp=':'.join(map(str,[core,*jars]));subprocess.run([str(a.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(w),str(w/'ModuleDispatch.java')],check=True)
for mode in ['original','ported']:
 classpath=':'.join(map(str,[w,*([overlay]if mode=='ported'else[]),core,*jars]))
 command=[str(a.java_home/'bin/java'),'-Xint','-Xcheck:jni','-Xverify:all','--enable-native-access=ALL-UNNAMED','--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED','-Dps5.test.coreLibrary='+str(ROOT/'build/client-ports/lwjgl-native/host/liblwjgl.dylib'),'-cp',classpath,'ModuleDispatch',mode]
 result=subprocess.run(command,capture_output=True,text=True,timeout=60,env=dict(os.environ,UBSAN_OPTIONS='handle_segv=0:handle_sigbus=0:handle_sigfpe=0:halt_on_error=1'));(w/(mode+'.log')).write_text(result.stdout+result.stderr);print(result.stdout,result.stderr);result.check_returncode()
 for marker in ['WARNING in native method','FATAL ERROR in native method','runtime error:']:assert marker not in result.stdout+result.stderr,marker
