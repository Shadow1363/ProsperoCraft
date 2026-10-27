import java.io.IOException;
/** Scoped native thumbnail codecs. Does not initialize SDL, LWJGL or Minecraft. */
final class ProsperoContentImages {
 private static boolean attempted,available;
 private static synchronized boolean available(){if(!attempted){attempted=true;try{System.loadLibrary("ps5contentimages");available=true;}catch(UnsatisfiedLinkError absent){available=false;}}return available;}
 private static native String nativeDecode(byte[] image);
 static String decode(byte[] image)throws Exception {
  if(image.length>1024*1024)throw new IOException("Project icon too large");
  if(available()){String decoded=nativeDecode(image);if(decoded!=null)return decoded;throw new IOException("Unsupported or damaged project icon");}
  return ProsperoAvatar.icon(image);
 }
}
