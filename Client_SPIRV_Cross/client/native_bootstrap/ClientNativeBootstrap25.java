import java.nio.*;
import java.util.concurrent.atomic.AtomicInteger;
import org.lwjgl.system.*;
import org.lwjgl.vulkan.*;
import org.lwjgl.openal.*;
import static org.lwjgl.system.MemoryUtil.*;
import static org.lwjgl.openal.AL10.*;
import static org.lwjgl.openal.ALC10.*;
import static org.lwjgl.openal.SOFTLoopback.*;
/** Actual original LWJGL callback/Vulkan-loader/OpenAL mixer acceptance;not Minecraft startup. */
public final class ClientNativeBootstrap25 {
 public static native void checkpoint(String text);
 public static native int invokeCallback(long address,boolean threaded);
 private static void stage(String s){checkpoint("Native026: "+s);}
 private static void check(boolean value,String what){if(!value)throw new AssertionError(what);}
 public static void callbacks(){
  for(int cycle=0;cycle<3;++cycle){
   AtomicInteger calls=new AtomicInteger();
   try(VkDebugUtilsMessengerCallbackEXT cb=VkDebugUtilsMessengerCallbackEXT.create((severity,type,data,user)->{calls.incrementAndGet();return severity==7&&type==11&&data==0x35&&user==0x1234?0x6a55:0;})){
    check(invokeCallback(cb.address(),false)==32*0x6a55,"synchronous native->Java callback values");
    check(invokeCallback(cb.address(),true)==32*0x6a55,"native pthread->Java callback values/attach");
    check(calls.get()==64,"callback invocation count");
   }
   stage("PASS genuine libffi/LWJGL callback cycle"+cycle+":32 current-thread+32 native-pthread calls;closure freed after join");
  }
 }
 public static void mixer(){
  for(int cycle=0;cycle<3;++cycle){
   long device=alcLoopbackOpenDeviceSOFT((ByteBuffer)null);check(device!=0,"actual loopback device");long context=0;int buffer=0,source=0;
   try{
    ALCCapabilities caps=ALC.createCapabilities(device);check(caps.ALC_SOFT_loopback,"loopback extension");check(alcIsRenderFormatSupportedSOFT(device,48000,ALC_STEREO_SOFT,ALC_SHORT_SOFT),"real stereo16 mixer support");
    try(MemoryStack stack=MemoryStack.stackPush()){
     context=alcCreateContext(device,stack.ints(ALC_FREQUENCY,48000,ALC_FORMAT_CHANNELS_SOFT,ALC_STEREO_SOFT,ALC_FORMAT_TYPE_SOFT,ALC_SHORT_SOFT,0));
    }
    check(context!=0&&alcMakeContextCurrent(context),"real OpenAL context");AL.createCapabilities(caps);
    ShortBuffer pcm=memAllocShort(4800),mixed=memAllocShort(4800*2+128);
    try{
     for(int i=0;i<4800;++i)pcm.put(i,(short)Math.round(10000*Math.sin(2*Math.PI*440*i/48000.0)));
     for(int i=0;i<mixed.capacity();++i)mixed.put(i,(short)0x5a35);
     buffer=alGenBuffers();source=alGenSources();alBufferData(buffer,AL_FORMAT_MONO16,pcm,48000);alSourcei(source,AL_BUFFER,buffer);alSourcei(source,AL_SOURCE_RELATIVE,AL_TRUE);alSourcef(source,AL_ROLLOFF_FACTOR,0);alSourcePlay(source);check(alGetError()==AL_NO_ERROR,"source PCM upload/start");
     mixed.limit(4800*2);alcRenderSamplesSOFT(device,mixed,4800);check(alcGetError(device)==ALC_NO_ERROR&&alGetError()==AL_NO_ERROR,"actual render");
     long energy=0;int peak=0,nonzero=0,crossings=0;short previous=0;for(int frame=0;frame<4800;++frame){short sample=mixed.get(frame*2);energy+=(long)sample*sample;peak=Math.max(peak,Math.abs((int)sample));if(sample!=0)nonzero++;if(frame>128&&previous<=0&&sample>0)crossings++;previous=sample;}
     check(peak>1000&&peak<20000&&nonzero>4000&&energy>1000000000L,"actual non-silent/unclipped tone samples");check(crossings>=39&&crossings<=46,"440Hz waveform frequency control");
     mixed.limit(mixed.capacity());for(int i=4800*2;i<mixed.capacity();++i)check(mixed.get(i)==(short)0x5a35,"mixer output guard");
     alSourceStop(source);alDeleteSources(source);source=0;alDeleteBuffers(buffer);buffer=0;
     // Drain one mixer block for the upstream source-stop fade/filter tail.
     mixed.limit(2048);alcRenderSamplesSOFT(device,mixed,1024);alcRenderSamplesSOFT(device,mixed,1024);int silentPeak=0;for(int i=0;i<2048;++i)silentPeak=Math.max(silentPeak,Math.abs((int)mixed.get(i)));check(silentPeak<=2,"stopped source produces silence after draining one block;peak="+silentPeak);
     stage("PASS real OpenAL Soft loopback cycle"+cycle+":4800 stereo frames/440Hz PCM peak"+peak+" crossings"+crossings+" guards+stopped-source silence");
    }finally{memFree(pcm);memFree(mixed);}
   }finally{
    if(source!=0)alDeleteSources(source);if(buffer!=0)alDeleteBuffers(buffer);if(context!=0){alcMakeContextCurrent(0);alcDestroyContext(context);}check(alcCloseDevice(device),"close loopback device");
   }
  }
 }
 public static void main(String[]args){
  boolean host=System.getProperty("ps5.test.ffiCore")!=null;
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.VULKAN_EXPLICIT_INIT.set(true);Configuration.OPENAL_EXPLICIT_INIT.set(true);
  if(host){Configuration.LIBRARY_NAME.set(System.getProperty("ps5.test.ffiCore"));System.load(System.getProperty("ps5.test.callbackHelper"));System.load(System.getProperty("ps5.test.hostLoader"));Configuration.VULKAN_LIBRARY_NAME.set("/opt/homebrew/lib/libMoltenVK.dylib");Configuration.OPENAL_LIBRARY_NAME.set(System.getProperty("ps5.test.openal"));}
  else{Configuration.VULKAN_LIBRARY_NAME.set(System.mapLibraryName("ps5clientgpu"));Configuration.OPENAL_LIBRARY_NAME.set(System.mapLibraryName("ps5openal"));System.loadLibrary("ps5clientgpu");System.loadLibrary("ps5shaderc");System.loadLibrary("ps5openal");System.loadLibrary("ps5nativeprobe");}
  Library.initialize();stage("real core loaded;prepare no-argument Vulkan module bootstrap");
  VK.create();check(VK.getInstanceVersionSupported()!=0,"real Vulkan global function table");stage("PASS no-argument VK.create including genuine allocation-callback/libffi class initialization");VK.destroy();
  callbacks();ALC.create();try{check(ALC.getFunctionProvider()!=null,"real OpenAL provider");mixer();}finally{ALC.destroy();}
  stage("PASS native bootstrap:192 Java callbacks,3 OpenAL mixer/context lifecycles,and genuine Vulkan loader;no speaker output or Minecraft menu claim");
 }
}
