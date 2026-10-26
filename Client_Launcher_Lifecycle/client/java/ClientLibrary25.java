import java.nio.ByteBuffer;

/** Standard JVM JNI loading plus scoped resident function lookup. No GPU API. */
public final class ClientLibrary25 {
 public static native void checkpoint(String text);
 private static native int loadCount();
 private static native long resolvedChecksum(String symbol,ByteBuffer bytes);
 public static void main(String[] args) {
  System.loadLibrary("ps5clientbridge");
  System.loadLibrary("ps5clientbridge");
  if(loadCount()!=1)throw new AssertionError("JNI_OnLoad must run exactly once");
  for(int size:new int[]{0,1,257,16385}) {
   ByteBuffer owner=ByteBuffer.allocateDirect(size+16);owner.position(8);owner.limit(8+size);ByteBuffer bytes=owner.slice();
   long expected=0;for(int i=0;i<size;i++){int value=(i*13+7)&255;bytes.put(i,(byte)value);expected+=value*(long)(i+1);}
   for(int repeat=0;repeat<8;repeat++)if(resolvedChecksum("ps5_client_checksum",bytes)!=expected)throw new AssertionError("resolved function result");
  }
  try{resolvedChecksum("ps5_client_missing_export",ByteBuffer.allocateDirect(1));throw new AssertionError("missing symbol succeeded");}catch(UnsatisfiedLinkError expected){}
  try{resolvedChecksum("JNI_OnLoad",ByteBuffer.allocateDirect(1));throw new AssertionError("wrong ABI accepted");}catch(UnsatisfiedLinkError expected){}
  try{resolvedChecksum("ps5_client_checksum",ByteBuffer.allocate(1));throw new AssertionError("heap accepted");}catch(IllegalArgumentException expected){}
  try{resolvedChecksum(null,ByteBuffer.allocateDirect(1));throw new AssertionError("null accepted");}catch(NullPointerException expected){}
  try{System.loadLibrary("ps5client_missing_library");throw new AssertionError("unknown library succeeded");}catch(UnsatisfiedLinkError expected){}
  if(loadCount()!=1)throw new AssertionError("failure changed load count");
  checkpoint("MC_CLIENT_RESIDENT_LIBRARY_OK standard System.loadLibrary/JNI_OnLoad once/native symbol lookup/real function call/missing controls; no GPU or arbitrary ELF loading");
 }
}
