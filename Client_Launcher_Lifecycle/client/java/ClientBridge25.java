import java.nio.ByteBuffer;

/** Actual synchronous JNI buffer handoff, before any graphics-library binding. */
public final class ClientBridge25 {
    public static native void checkpoint(String text);
    private static native long pageSize();
    private static native long fill(ByteBuffer buffer, long seed);
    static long write(ByteBuffer buffer, long seed) {
        if (buffer != null && buffer.isReadOnly()) throw new IllegalArgumentException("writable direct ByteBuffer required");
        return fill(buffer, seed);
    }
    public static void main(String[] args) {
        if (pageSize() <= 0) throw new AssertionError("OS page size unavailable");
        for (int size : new int[] {0, 1, 255, 16384, 65537}) {
            ByteBuffer owner = ByteBuffer.allocateDirect(size + 32);
            for (int i=0;i<owner.capacity();i++) owner.put(i,(byte)0x5a);
            owner.position(16);owner.limit(16+size);ByteBuffer slice=owner.slice();
            long expected=0;for(int i=0;i<size;i++)expected+=(123L+i*17)&255;
            long actual=write(slice,123);
            if(actual!=expected)throw new AssertionError("native checksum");
            for(int i=0;i<size;i++)if((slice.get(i)&255)!=((123+i*17)&255))throw new AssertionError("native bytes");
            owner.clear();
            for(int i=0;i<16;i++)if(owner.get(i)!=(byte)0x5a||owner.get(size+16+i)!=(byte)0x5a)throw new AssertionError("native bounds");
        }
        try{write(ByteBuffer.allocate(4),0);throw new AssertionError("heap accepted");}catch(IllegalArgumentException expected){}
        try{write(null,0);throw new AssertionError("null accepted");}catch(NullPointerException expected){}
        try{write(ByteBuffer.allocateDirect(4).asReadOnlyBuffer(),0);throw new AssertionError("readonly accepted");}catch(IllegalArgumentException expected){}
        checkpoint("MC_CLIENT_JNI_BUFFER_OK real native direct-buffer writes, slices/bounds/errors; pageSize="+pageSize()+"; graphics not initialized");
    }
}
