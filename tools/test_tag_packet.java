import io.netty.buffer.*;
import it.unimi.dsi.fastutil.ints.*;
import java.util.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.protocol.common.ClientboundUpdateTagsPacket;
import net.minecraft.resources.Identifier;
import net.minecraft.tags.TagNetworkSerialization.NetworkPayload;

/** Exercise the real update_tags codec across the console's failed32KiB growth. */
public class test_tag_packet {
 public static void main(String[] args)throws Exception {
  ServerMemory25.check();
  Map<Identifier,IntList> tags=new LinkedHashMap<>();
  for(int tag=0;tag<128;tag++){IntArrayList ids=new IntArrayList();for(int id=0;id<512;id++)ids.add(id);tags.put(Identifier.fromNamespaceAndPath("fixture","tag_"+tag),ids);}
  var packet=new ClientboundUpdateTagsPacket(Map.of(Registries.BLOCK,new NetworkPayload(tags)));
  int largest=0;
  for(int pass=0;pass<20;pass++){
   ByteBuf buffer=ByteBufAllocator.DEFAULT.ioBuffer(256,1048576);
   try {
    if(!buffer.isDirect())throw new AssertionError("Expected actual network ioBuffer native path");
    ClientboundUpdateTagsPacket.STREAM_CODEC.encode(buffer,packet);
    int bytes=buffer.readableBytes();if(bytes<=32768)throw new AssertionError("Did not cross failed allocation size");largest=Math.max(largest,bytes);
    var decoded=ClientboundUpdateTagsPacket.STREAM_CODEC.decode(buffer);
    if(decoded.tags().size()!=1||buffer.isReadable())throw new AssertionError("Tag packet framing changed");
    var actual=decoded.tags().get(Registries.BLOCK);if(actual==null||actual.tags().size()!=tags.size())throw new AssertionError("Registry/tag keys changed: "+decoded.tags().keySet());
    for(var entry:tags.entrySet()){IntList ids=actual.tags().get(entry.getKey());if(ids==null||!Arrays.equals(ids.toIntArray(),entry.getValue().toIntArray()))throw new AssertionError("Tag ids changed for "+entry.getKey()+": "+ids);}

   }finally{if(!buffer.release()||buffer.refCnt()!=0)throw new AssertionError("Buffer leak");}
  }
  System.out.println("PASS:20 actual update_tags codec roundtrips,128 tags x512 ids, encodedBytes="+largest+", real direct ioBuffer growth past32KiB, exact payload equality and complete reference-count release. Host codec test, not console admission.");
 }
}
