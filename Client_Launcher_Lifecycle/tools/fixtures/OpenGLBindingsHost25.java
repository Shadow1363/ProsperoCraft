/* Host-only real CGL/OpenGL GPU check;not a PS5 driver or console pass. */
import java.nio.*;
import org.lwjgl.system.*;
import org.lwjgl.opengl.*;
import static org.lwjgl.opengl.CGL.*;
import static org.lwjgl.opengl.GL11C.*;
import static org.lwjgl.opengl.GL30C.*;
public class OpenGLBindingsHost25 {
 static void check(boolean ok,String what){if(!ok)throw new AssertionError(what);}
 public static void main(String[]args){
  Configuration.MEMORY_ALLOCATOR.set("system");Configuration.LIBRARY_NAME.set(args[0]);System.load(args[1]);Library.initialize();
  for(int cycle=0;cycle<3;++cycle){
   long pixel=0,context=0;
   try(MemoryStack stack=MemoryStack.stackPush()){
    var result=stack.mallocPointer(1);IntBuffer count=stack.mallocInt(1);
    check(CGLChoosePixelFormat(stack.ints(kCGLPFAOpenGLProfile,kCGLOGLPVersion_3_2_Core,kCGLPFAColorSize,24,kCGLPFAAllowOfflineRenderers,0),result,count)==0&&count.get(0)>0,"real CGL pixel format");pixel=result.get(0);
    check(CGLCreateContext(pixel,0,result)==0,"real CGL context");context=result.get(0);check(CGLSetCurrentContext(context)==0,"make current");GL.createCapabilities();
    int texture=glGenTextures(),fbo=glGenFramebuffers();ByteBuffer pixels=MemoryUtil.memAlloc(8*8*4+128);
    try{
     glBindTexture(GL_TEXTURE_2D,texture);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA8,8,8,0,GL_RGBA,GL_UNSIGNED_BYTE,(ByteBuffer)null);glBindFramebuffer(GL_FRAMEBUFFER,fbo);glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,texture,0);check(glCheckFramebufferStatus(GL_FRAMEBUFFER)==GL_FRAMEBUFFER_COMPLETE,"framebuffer");
     for(int i=0;i<pixels.capacity();++i)pixels.put(i,(byte)0x5a);
     glViewport(0,0,8,8);glClearColor(0.25f,0.5f,0.75f,1);glClear(GL_COLOR_BUFFER_BIT);glReadPixels(0,0,8,8,GL_RGBA,GL_UNSIGNED_BYTE,pixels);glFinish();check(glGetError()==GL_NO_ERROR,"real GL calls");
     int[]want={64,128,191,255};for(int i=0;i<256;++i)check(Math.abs((pixels.get(i)&255)-want[i%4])<=1,"GPU clear/readback pixel");for(int i=256;i<pixels.capacity();++i)check(pixels.get(i)==(byte)0x5a,"readback guard");
     System.out.println("PASS actual original OpenGL JNI/host GPU cycle"+cycle+":64RGBA pixels+128guards,renderer="+glGetString(GL_RENDERER));
    }finally{MemoryUtil.memFree(pixels);glDeleteFramebuffers(fbo);glDeleteTextures(texture);GL.setCapabilities(null);}
   }finally{CGLSetCurrentContext(0);if(context!=0)check(CGLDestroyContext(context)==0,"destroy context");if(pixel!=0)check(CGLDestroyPixelFormat(pixel)==0,"destroy pixel format");}
  }
  GL.destroy();
 }
}
