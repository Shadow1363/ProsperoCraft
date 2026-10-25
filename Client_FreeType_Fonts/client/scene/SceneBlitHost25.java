import java.nio.*;
import org.lwjgl.vulkan.*;
import org.lwjgl.system.*;
import static org.lwjgl.vulkan.VK10.*;
/** Host-only real GPU scaling/BGRA conversion companion; no SDL/WSI claims. */
public final class SceneBlitHost25 {
 private static void check(int n,String stage){if(n!=VK_SUCCESS)throw new AssertionError(stage+" "+n);}
 public static void verify(VkDevice device,VkPhysicalDeviceMemoryProperties mp,VkCommandBuffer cmd,VkQueue queue,long fence,long source,long buffer,long memory,ByteBuffer pixels){
  long image=0,allocation=0;boolean pending=false;
  try(MemoryStack s=MemoryStack.stackPush()){
   LongBuffer out=s.mallocLong(1);image=ClientScene25.createImage(device,mp,s,128,96,VK_FORMAT_B8G8R8A8_UNORM,VK_IMAGE_USAGE_TRANSFER_DST_BIT|VK_IMAGE_USAGE_TRANSFER_SRC_BIT,out,0);allocation=out.get(0);
   check(vkResetCommandBuffer(cmd,0),"reset blit");check(vkResetFences(device,fence),"reset blit fence");check(vkBeginCommandBuffer(cmd,VkCommandBufferBeginInfo.calloc(s).sType$Default().flags(VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)),"begin blit");
   ClientScene25.imageBarrier(cmd,s,image,VK_IMAGE_ASPECT_COLOR_BIT,VK_IMAGE_LAYOUT_UNDEFINED,VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,0,VK_ACCESS_TRANSFER_WRITE_BIT,VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT);
   VkImageBlit.Buffer blit=VkImageBlit.calloc(1,s);blit.get(0).srcSubresource().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).layerCount(1);blit.get(0).srcOffsets(1).set(256,256,1);blit.get(0).dstSubresource().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).layerCount(1);blit.get(0).dstOffsets(1).set(128,96,1);vkCmdBlitImage(cmd,source,VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,image,VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,blit,VK_FILTER_NEAREST);
   ClientScene25.imageBarrier(cmd,s,image,VK_IMAGE_ASPECT_COLOR_BIT,VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,VK_ACCESS_TRANSFER_WRITE_BIT,VK_ACCESS_TRANSFER_READ_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT);
   VkBufferMemoryBarrier.Buffer barrier=VkBufferMemoryBarrier.calloc(1,s);barrier.get(0).sType$Default().srcAccessMask(VK_ACCESS_HOST_READ_BIT).dstAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).buffer(buffer).size(VK_WHOLE_SIZE);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_HOST_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,null,barrier,null);
   VkBufferImageCopy.Buffer copy=VkBufferImageCopy.calloc(1,s);copy.get(0).imageSubresource().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).layerCount(1);copy.get(0).imageExtent().set(128,96,1);vkCmdCopyImageToBuffer(cmd,image,VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,buffer,copy);
   barrier.get(0).srcAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT).dstAccessMask(VK_ACCESS_HOST_READ_BIT);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,null,barrier,null);check(vkEndCommandBuffer(cmd),"end blit");VkSubmitInfo.Buffer submit=VkSubmitInfo.calloc(1,s);submit.get(0).sType$Default().pCommandBuffers(s.pointers(cmd.address()));pending=true;check(vkQueueSubmit(queue,submit,fence),"submit blit");check(vkWaitForFences(device,fence,true,5_000_000_000L),"wait blit");pending=false;
   VkMappedMemoryRange.Buffer range=VkMappedMemoryRange.calloc(1,s);range.get(0).sType$Default().memory(memory).size(VK_WHOLE_SIZE);check(vkInvalidateMappedMemoryRanges(device,range),"invalidate blit");
   for(int y=0;y<96;y++)for(int x=0;x<128;x++){
    int sx=(int)((x+.5)*256/128),sy=(int)((y+.5)*256/96),i=(sy*256+sx)*4,o=(y*128+x)*4;byte[] original=ClientScene25.latestPixels;
    int expected=(Byte.toUnsignedInt(original[i+3])<<24)|(Byte.toUnsignedInt(original[i])<<16)|(Byte.toUnsignedInt(original[i+1])<<8)|Byte.toUnsignedInt(original[i+2]);
    if(pixels.getInt(o)!=expected)throw new AssertionError("Host real BGRA blit mismatch "+x+","+y);
   }
   System.out.println("PASS real scene RGBA->BGRA nearest scaling blit:128x96 full pixels match actual rendered source. No SDL/WSI exercised.");
  }finally{if(!pending){if(image!=0)vkDestroyImage(device,image,null);if(allocation!=0)vkFreeMemory(device,allocation,null);}}
 }
}
