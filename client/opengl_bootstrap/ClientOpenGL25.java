/* Real software OpenGL acceptance;no game startup or hardware GL claim. */
import java.nio.*;
import org.lwjgl.system.*;
import org.lwjgl.opengl.*;
import static org.lwjgl.opengl.GL11C.*;
import static org.lwjgl.opengl.GL30C.*;
public class ClientOpenGL25 {
 public static native void checkpoint(String text);
 static void stage(String text){checkpoint("OpenGL028: "+text);}
 static native long create(ByteBuffer pixels);
 static native void destroy(long context);
 static void check(boolean ok,String what){if(!ok)throw new AssertionError(what);}
 public static void main(String[]args){
  boolean host=System.getProperty("ps5.test.ffiCore")!=null;
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.OPENGL_CONTEXT_API.set("OSMesa");
  if(host){Configuration.LIBRARY_NAME.set(System.getProperty("ps5.test.ffiCore"));Configuration.OPENGL_OSMESA_LIBRARY_NAME.set(System.getProperty("ps5.test.osmesa"));System.load(System.getProperty("ps5.test.hostLoader"));System.load(System.getProperty("ps5.test.osmesa"));}
  else{Configuration.OPENGL_OSMESA_LIBRARY_NAME.set(System.mapLibraryName("ps5clientgl"));System.loadLibrary("ps5clientgpu");System.loadLibrary("ps5clientgl");}
  Library.initialize();
  stage("genuine Mesa resident provider initialized;prepare original OpenGL JNI");
  check(create(ByteBuffer.allocate(256))==0,"reject heap buffer");check(create(ByteBuffer.allocateDirect(255))==0,"reject undersized buffer");
  for(int cycle=0;cycle<3;++cycle){
   ByteBuffer back=MemoryUtil.memAlloc(256+128),pixels=MemoryUtil.memAlloc(256+128);long context=0;
   try{
    for(int i=0;i<back.capacity();++i){back.put(i,(byte)0x6b);pixels.put(i,(byte)0x5a);}
    context=create(back);check(context!=0,"real OSMesa 3.3 context");GL.createCapabilities();
    String renderer=glGetString(GL_RENDERER);check(renderer!=null&&renderer.contains("softpipe"),"actual softpipe provider: "+renderer);
    int texture=glGenTextures(),fbo=glGenFramebuffers();
    try{
     glBindTexture(GL_TEXTURE_2D,texture);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA8,8,8,0,GL_RGBA,GL_UNSIGNED_BYTE,(ByteBuffer)null);glBindFramebuffer(GL_FRAMEBUFFER,fbo);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,texture,0);check(glCheckFramebufferStatus(GL_FRAMEBUFFER)==GL_FRAMEBUFFER_COMPLETE,"framebuffer");
     float[]color={cycle==0?1:0,cycle==1?1:0,cycle==2?1:0,1};glViewport(0,0,8,8);glClearColor(color[0],color[1],color[2],1);glClear(GL_COLOR_BUFFER_BIT);glReadPixels(0,0,8,8,GL_RGBA,GL_UNSIGNED_BYTE,pixels);glFinish();check(glGetError()==GL_NO_ERROR,"GL error");
     for(int i=0;i<256;++i)check((pixels.get(i)&255)==(int)(255*color[i%4]),"real clear/readback pixel");
     for(int i=256;i<pixels.capacity();++i){check(pixels.get(i)==(byte)0x5a,"readback guard");check(back.get(i)==(byte)0x6b,"context guard");}
     stage("PASS actual Mesa/LWJGL cycle"+cycle+":64RGBA pixels+256guards,renderer="+renderer);
    }finally{glDeleteFramebuffers(fbo);glDeleteTextures(texture);GL.setCapabilities(null);}
   }finally{if(context!=0)destroy(context);MemoryUtil.memFree(pixels);MemoryUtil.memFree(back);}
  }
  GL.destroy();
 }
}
