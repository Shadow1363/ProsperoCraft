import java.nio.*;
import org.lwjgl.vulkan.*;
import org.lwjgl.system.*;
import static org.lwjgl.system.MemoryUtil.*;
import static org.lwjgl.vulkan.VK10.*;
/** Borrowed-device direct BGRA scene renderer shared by console and host checks. */
public final class ClientDirectScene25 {
 private final VkDevice device;private final int width,height;
 private long texture,textureMemory,textureView,depth,depthMemory,depthView,sampler,setLayout,descriptorPool,descriptorSet,vertexBuffer,vertexMemory,renderPass,vertex,fragment,pipelineLayout,pipeline,noDepthPipeline,blendPipeline;
 private long[] framebuffers,views;
 private static void check(int rc,String text){if(rc!=VK_SUCCESS)throw new IllegalStateException(text+" VkResult="+rc);}
 public ClientDirectScene25(VkDevice device,VkPhysicalDevice physical,int width,int height,long[] images,VkCommandBuffer cmd,VkQueue queue,long fence,long buffer,long memory,ByteBuffer pixels){
  this.device=device;this.width=width;this.height=height;
  try(MemoryStack stack=MemoryStack.stackPush()){
   org.lwjgl.PointerBuffer ptr=stack.mallocPointer(1);LongBuffer handle=stack.mallocLong(1);VkMemoryRequirements req=VkMemoryRequirements.malloc(stack);
   VkPhysicalDeviceMemoryProperties mp=VkPhysicalDeviceMemoryProperties.malloc(stack);vkGetPhysicalDeviceMemoryProperties(physical,mp);
   texture=ClientScene25.createImage(device,mp,stack,2,2,VK_FORMAT_R8G8B8A8_UNORM,VK_IMAGE_USAGE_TRANSFER_DST_BIT|VK_IMAGE_USAGE_SAMPLED_BIT,handle,0);textureMemory=handle.get(0);
   textureView=ClientDirectScene25.createView(device,stack,texture,VK_FORMAT_R8G8B8A8_UNORM,VK_IMAGE_ASPECT_COLOR_BIT);
   VkFormatProperties depthProperties=VkFormatProperties.malloc(stack);vkGetPhysicalDeviceFormatProperties(physical,VK_FORMAT_D32_SFLOAT,depthProperties);
   if((depthProperties.optimalTilingFeatures()&VK_FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT)==0)throw new AssertionError("D32 depth attachment unsupported");
   depth=ClientScene25.createImage(device,mp,stack,width,height,VK_FORMAT_D32_SFLOAT,VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT,handle,0);depthMemory=handle.get(0);
   depthView=ClientDirectScene25.createView(device,stack,depth,VK_FORMAT_D32_SFLOAT,VK_IMAGE_ASPECT_DEPTH_BIT);
   VkSamplerCreateInfo si=VkSamplerCreateInfo.calloc(stack).sType$Default().magFilter(VK_FILTER_NEAREST).minFilter(VK_FILTER_NEAREST).mipmapMode(VK_SAMPLER_MIPMAP_MODE_NEAREST).addressModeU(VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE).addressModeV(VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE).addressModeW(VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE).maxLod(0);
   check(vkCreateSampler(device,si,null,handle),"vkCreateSampler");sampler=handle.get(0);
   VkDescriptorSetLayoutBinding.Buffer binding=VkDescriptorSetLayoutBinding.calloc(1,stack);binding.get(0).binding(0).descriptorType(VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER).descriptorCount(1).stageFlags(VK_SHADER_STAGE_FRAGMENT_BIT);
   check(vkCreateDescriptorSetLayout(device,VkDescriptorSetLayoutCreateInfo.calloc(stack).sType$Default().pBindings(binding),null,handle),"sampled texture descriptor layout");setLayout=handle.get(0);
   VkDescriptorPoolSize.Buffer poolSize=VkDescriptorPoolSize.calloc(1,stack);poolSize.get(0).type(VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER).descriptorCount(1);
   check(vkCreateDescriptorPool(device,VkDescriptorPoolCreateInfo.calloc(stack).sType$Default().maxSets(1).pPoolSizes(poolSize),null,handle),"texture descriptor pool");descriptorPool=handle.get(0);
   check(vkAllocateDescriptorSets(device,VkDescriptorSetAllocateInfo.calloc(stack).sType$Default().descriptorPool(descriptorPool).pSetLayouts(stack.longs(setLayout)),handle),"texture descriptor set");descriptorSet=handle.get(0);
   VkDescriptorImageInfo.Buffer texInfo=VkDescriptorImageInfo.calloc(1,stack);texInfo.get(0).sampler(sampler).imageView(textureView).imageLayout(VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL);
   VkWriteDescriptorSet.Buffer write=VkWriteDescriptorSet.calloc(1,stack);write.get(0).sType$Default().dstSet(descriptorSet).dstBinding(0).descriptorType(VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER).descriptorCount(1).pImageInfo(texInfo);vkUpdateDescriptorSets(device,write,null);
   VkAttachmentDescription.Buffer attachment=VkAttachmentDescription.calloc(2,stack);
   attachment.get(0).format(VK_FORMAT_B8G8R8A8_UNORM).samples(VK_SAMPLE_COUNT_1_BIT).loadOp(VK_ATTACHMENT_LOAD_OP_CLEAR).storeOp(VK_ATTACHMENT_STORE_OP_STORE).stencilLoadOp(VK_ATTACHMENT_LOAD_OP_DONT_CARE).stencilStoreOp(VK_ATTACHMENT_STORE_OP_DONT_CARE).initialLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL).finalLayout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL);
   attachment.get(1).format(VK_FORMAT_D32_SFLOAT).samples(VK_SAMPLE_COUNT_1_BIT).loadOp(VK_ATTACHMENT_LOAD_OP_CLEAR).storeOp(VK_ATTACHMENT_STORE_OP_DONT_CARE).stencilLoadOp(VK_ATTACHMENT_LOAD_OP_DONT_CARE).stencilStoreOp(VK_ATTACHMENT_STORE_OP_DONT_CARE).initialLayout(VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL).finalLayout(VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL);
   VkAttachmentReference.Buffer reference=VkAttachmentReference.calloc(1,stack);reference.get(0).attachment(0).layout(VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL);
   VkAttachmentReference depthReference=VkAttachmentReference.calloc(stack).attachment(1).layout(VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL);
   VkSubpassDescription.Buffer subpass=VkSubpassDescription.calloc(1,stack);subpass.get(0).pipelineBindPoint(VK_PIPELINE_BIND_POINT_GRAPHICS).colorAttachmentCount(1).pColorAttachments(reference).pDepthStencilAttachment(depthReference);
   check(vkCreateRenderPass(device,VkRenderPassCreateInfo.calloc(stack).sType$Default().pAttachments(attachment).pSubpasses(subpass),null,handle),"vkCreateRenderPass");renderPass=handle.get(0);
   framebuffers=new long[images.length];views=new long[images.length];
   for(int i=0;i<images.length;i++){
    views[i]=createView(device,stack,images[i],VK_FORMAT_B8G8R8A8_UNORM,VK_IMAGE_ASPECT_COLOR_BIT);
    check(vkCreateFramebuffer(device,VkFramebufferCreateInfo.calloc(stack).sType$Default().renderPass(renderPass).pAttachments(stack.longs(views[i],depthView)).width(width).height(height).layers(1),null,handle),"direct scene framebuffer");framebuffers[i]=handle.get(0);
   }
   VkShaderModuleCreateInfo sm=VkShaderModuleCreateInfo.calloc(stack).sType$Default();sm.pCode(ClientSceneCode25.vertex(stack));check(vkCreateShaderModule(device,sm,null,handle),"vertex module");vertex=handle.get(0);sm.pCode(ClientSceneCode25.fragment(stack));check(vkCreateShaderModule(device,sm,null,handle),"fragment module");fragment=handle.get(0);
   VkPushConstantRange.Buffer push=VkPushConstantRange.calloc(1,stack);push.get(0).stageFlags(VK_SHADER_STAGE_VERTEX_BIT|VK_SHADER_STAGE_FRAGMENT_BIT).offset(0).size(24);VkPipelineLayoutCreateInfo pl=VkPipelineLayoutCreateInfo.calloc(stack).sType$Default().pPushConstantRanges(push).pSetLayouts(stack.longs(setLayout));check(vkCreatePipelineLayout(device,pl,null,handle),"vkCreatePipelineLayout");pipelineLayout=handle.get(0);
   VkPipelineShaderStageCreateInfo.Buffer stages=VkPipelineShaderStageCreateInfo.calloc(2,stack);stages.get(0).sType$Default().stage(VK_SHADER_STAGE_VERTEX_BIT).module(vertex).pName(stack.UTF8("main"));stages.get(1).sType$Default().stage(VK_SHADER_STAGE_FRAGMENT_BIT).module(fragment).pName(stack.UTF8("main"));
   float[] vertices={-1.2f,-1.2f,2,0,0, 2.4f,-2.4f,4,1,0, 2.4f,2.4f,4,1,1, -1.2f,-1.2f,2,0,0, 2.4f,2.4f,4,1,1, -1.2f,1.2f,2,0,1};
   VkBufferCreateInfo vbi=VkBufferCreateInfo.calloc(stack).sType$Default().size(vertices.length*4).usage(VK_BUFFER_USAGE_VERTEX_BUFFER_BIT).sharingMode(VK_SHARING_MODE_EXCLUSIVE);
   check(vkCreateBuffer(device,vbi,null,handle),"create actual vertex buffer");vertexBuffer=handle.get(0);vkGetBufferMemoryRequirements(device,vertexBuffer,req);
   int vertexType=-1;for(int i=0;i<mp.memoryTypeCount();i++)if((req.memoryTypeBits()&(1<<i))!=0&&(mp.memoryTypes(i).propertyFlags()&VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)!=0){vertexType=i;break;}if(vertexType<0)throw new AssertionError("No vertex memory");
   check(vkAllocateMemory(device,VkMemoryAllocateInfo.calloc(stack).sType$Default().allocationSize(req.size()).memoryTypeIndex(vertexType),null,handle),"vertex memory");vertexMemory=handle.get(0);check(vkBindBufferMemory(device,vertexBuffer,vertexMemory,0),"bind vertex buffer");check(vkMapMemory(device,vertexMemory,0,VK_WHOLE_SIZE,0,ptr),"map vertices");
   ByteBuffer vb=memByteBuffer(ptr.get(0),vertices.length*4).order(ByteOrder.nativeOrder());for(float f:vertices)vb.putFloat(f);
   VkMappedMemoryRange.Buffer vertexRange=VkMappedMemoryRange.calloc(1,stack);vertexRange.get(0).sType$Default().memory(vertexMemory).size(VK_WHOLE_SIZE);check(vkFlushMappedMemoryRanges(device,vertexRange),"flush vertices");vkUnmapMemory(device,vertexMemory);
   VkVertexInputBindingDescription.Buffer vertexBinding=VkVertexInputBindingDescription.calloc(1,stack);vertexBinding.get(0).binding(0).stride(20).inputRate(VK_VERTEX_INPUT_RATE_VERTEX);
   VkVertexInputAttributeDescription.Buffer attributes=VkVertexInputAttributeDescription.calloc(2,stack);attributes.get(0).location(0).binding(0).format(VK_FORMAT_R32G32B32_SFLOAT).offset(0);attributes.get(1).location(1).binding(0).format(VK_FORMAT_R32G32_SFLOAT).offset(12);
   VkPipelineVertexInputStateCreateInfo input=VkPipelineVertexInputStateCreateInfo.calloc(stack).sType$Default().pVertexBindingDescriptions(vertexBinding).pVertexAttributeDescriptions(attributes);VkPipelineInputAssemblyStateCreateInfo assembly=VkPipelineInputAssemblyStateCreateInfo.calloc(stack).sType$Default().topology(VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST);
   VkViewport.Buffer viewport=VkViewport.calloc(1,stack);viewport.get(0).x(0).y(0).width(width).height(height).minDepth(0).maxDepth(1);VkRect2D.Buffer scissors=VkRect2D.calloc(1,stack);scissors.get(0).extent().set(width,height);
   VkPipelineViewportStateCreateInfo vp=VkPipelineViewportStateCreateInfo.calloc(stack).sType$Default().pViewports(viewport).pScissors(scissors);
   VkPipelineRasterizationStateCreateInfo raster=VkPipelineRasterizationStateCreateInfo.calloc(stack).sType$Default().polygonMode(VK_POLYGON_MODE_FILL).cullMode(VK_CULL_MODE_NONE).frontFace(VK_FRONT_FACE_COUNTER_CLOCKWISE).lineWidth(1);
   VkPipelineMultisampleStateCreateInfo ms=VkPipelineMultisampleStateCreateInfo.calloc(stack).sType$Default().rasterizationSamples(VK_SAMPLE_COUNT_1_BIT);
   VkPipelineColorBlendAttachmentState.Buffer colors=VkPipelineColorBlendAttachmentState.calloc(1,stack);colors.get(0).colorWriteMask(VK_COLOR_COMPONENT_R_BIT|VK_COLOR_COMPONENT_G_BIT|VK_COLOR_COMPONENT_B_BIT|VK_COLOR_COMPONENT_A_BIT);
   VkPipelineColorBlendStateCreateInfo blend=VkPipelineColorBlendStateCreateInfo.calloc(stack).sType$Default().pAttachments(colors);
   VkPipelineDepthStencilStateCreateInfo ds=VkPipelineDepthStencilStateCreateInfo.calloc(stack).sType$Default().depthTestEnable(true).depthWriteEnable(true).depthCompareOp(VK_COMPARE_OP_LESS);
   VkGraphicsPipelineCreateInfo.Buffer gp=VkGraphicsPipelineCreateInfo.calloc(1,stack);gp.get(0).sType$Default().pStages(stages).pVertexInputState(input).pInputAssemblyState(assembly).pViewportState(vp).pRasterizationState(raster).pMultisampleState(ms).pColorBlendState(blend).pDepthStencilState(ds).layout(pipelineLayout).renderPass(renderPass).subpass(0);
check(vkCreateGraphicsPipelines(device,VK_NULL_HANDLE,gp,null,handle),"vkCreateGraphicsPipelines");pipeline=handle.get(0);
   ds.depthTestEnable(false).depthWriteEnable(false);check(vkCreateGraphicsPipelines(device,VK_NULL_HANDLE,gp,null,handle),"depth-disabled control pipeline");noDepthPipeline=handle.get(0);
   colors.get(0).blendEnable(true).srcColorBlendFactor(VK_BLEND_FACTOR_SRC_ALPHA).dstColorBlendFactor(VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA).colorBlendOp(VK_BLEND_OP_ADD).srcAlphaBlendFactor(VK_BLEND_FACTOR_ONE).dstAlphaBlendFactor(VK_BLEND_FACTOR_ZERO).alphaBlendOp(VK_BLEND_OP_ADD);
   check(vkCreateGraphicsPipelines(device,VK_NULL_HANDLE,gp,null,handle),"alpha blend pipeline");blendPipeline=handle.get(0);

   int[] texels={0xff0000ff,0xff00ff00,0xffff0000,0xff00ffff};for(int i=0;i<4;i++)pixels.putInt(i*4,texels[i]);
   VkMappedMemoryRange.Buffer uploadRange=VkMappedMemoryRange.calloc(1,stack);uploadRange.get(0).sType$Default().memory(memory).size(VK_WHOLE_SIZE);check(vkFlushMappedMemoryRanges(device,uploadRange),"texture upload flush");
   check(vkBeginCommandBuffer(cmd,VkCommandBufferBeginInfo.calloc(stack).sType$Default().flags(VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)),"begin upload");
   VkBufferMemoryBarrier.Buffer uploadBarrier=VkBufferMemoryBarrier.calloc(1,stack);uploadBarrier.get(0).sType$Default().srcAccessMask(VK_ACCESS_HOST_WRITE_BIT).dstAccessMask(VK_ACCESS_TRANSFER_READ_BIT).srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED).buffer(buffer).size(VK_WHOLE_SIZE);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_HOST_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,0,null,uploadBarrier,null);
   ClientScene25.imageBarrier(cmd,stack,texture,VK_IMAGE_ASPECT_COLOR_BIT,VK_IMAGE_LAYOUT_UNDEFINED,VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,0,VK_ACCESS_TRANSFER_WRITE_BIT,VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT);
   VkBufferImageCopy.Buffer upload=VkBufferImageCopy.calloc(1,stack);upload.get(0).imageSubresource().aspectMask(VK_IMAGE_ASPECT_COLOR_BIT).layerCount(1);upload.get(0).imageExtent().set(2,2,1);vkCmdCopyBufferToImage(cmd,buffer,texture,VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,upload);
   ClientScene25.imageBarrier(cmd,stack,texture,VK_IMAGE_ASPECT_COLOR_BIT,VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL,VK_ACCESS_TRANSFER_WRITE_BIT,VK_ACCESS_SHADER_READ_BIT,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT);
   uploadBarrier.get(0).srcAccessMask(VK_ACCESS_TRANSFER_READ_BIT).dstAccessMask(VK_ACCESS_HOST_WRITE_BIT);vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,null,uploadBarrier,null);
   check(vkEndCommandBuffer(cmd),"end upload");VkSubmitInfo.Buffer uploadSubmit=VkSubmitInfo.calloc(1,stack);uploadSubmit.get(0).sType$Default().pCommandBuffers(stack.pointers(cmd.address()));check(vkQueueSubmit(queue,uploadSubmit,fence),"submit upload");check(vkWaitForFences(device,fence,true,5_000_000_000L),"wait upload");
  }
 }
 public void record(VkCommandBuffer cmd,int index,int phase,MemoryStack work){
  // One submitted frame at a time,completed fence before next acquisition.
  ClientScene25.imageBarrier(cmd,work,depth,VK_IMAGE_ASPECT_DEPTH_BIT,VK_IMAGE_LAYOUT_UNDEFINED,VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL,0,VK_ACCESS_DEPTH_STENCIL_ATTACHMENT_READ_BIT|VK_ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT,VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,VK_PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT|VK_PIPELINE_STAGE_LATE_FRAGMENT_TESTS_BIT);
  VkClearValue.Buffer clear=VkClearValue.calloc(2,work);clear.get(0).color().float32(0,1).float32(2,1).float32(3,1);clear.get(1).depthStencil().depth(1);
  VkRenderPassBeginInfo begin=VkRenderPassBeginInfo.calloc(work).sType$Default().renderPass(renderPass).framebuffer(framebuffers[index]).pClearValues(clear);begin.renderArea().extent().set(width,height);vkCmdBeginRenderPass(cmd,begin,VK_SUBPASS_CONTENTS_INLINE);
  vkCmdBindDescriptorSets(cmd,VK_PIPELINE_BIND_POINT_GRAPHICS,pipelineLayout,0,work.longs(descriptorSet),null);vkCmdBindVertexBuffers(cmd,0,work.longs(vertexBuffer),work.longs(0));
  draw(cmd,pipeline,work,0,.25f,1,1,1,1);draw(cmd,phase==1?noDepthPipeline:pipeline,work,1,.75f,0,0,1,1);draw(cmd,phase==2?noDepthPipeline:blendPipeline,work,1,.1f,1,1,1,.5f);vkCmdEndRenderPass(cmd);
 }
 private void draw(VkCommandBuffer cmd,long pipeline,MemoryStack work,int mode,float depth,float r,float g,float b,float a){
  ByteBuffer push=work.malloc(24).order(ByteOrder.nativeOrder());push.putFloat(r).putFloat(g).putFloat(b).putFloat(a).putFloat(depth).putInt(mode).flip();
  vkCmdBindPipeline(cmd,VK_PIPELINE_BIND_POINT_GRAPHICS,pipeline);vkCmdPushConstants(cmd,pipelineLayout,VK_SHADER_STAGE_VERTEX_BIT|VK_SHADER_STAGE_FRAGMENT_BIT,0,push);vkCmdDraw(cmd,6,1,0,0);
 }
 private static long createView(VkDevice device,MemoryStack stack,long image,int format,int aspect){
  VkImageViewCreateInfo vi=VkImageViewCreateInfo.calloc(stack).sType$Default().image(image).viewType(VK_IMAGE_VIEW_TYPE_2D).format(format);vi.subresourceRange().aspectMask(aspect).levelCount(1).layerCount(1);LongBuffer out=stack.mallocLong(1);check(vkCreateImageView(device,vi,null,out),"direct scene view");return out.get(0);
 }
 public static int expected(int x,int y,int width,int height,int phase){
  double sx=2*(x+.5)/width-1,sy=2*(y+.5)/height-1;
  if(sx<-.6||sx>.6||sy<-.6||sy>.6)return 0xffff00ff;
  double u=(sx+.6)/1.2,v=(sy+.6)/1.2,a,b,c,tu,tv,den;
  if(v<=u){a=1-u;b=u-v;c=v;den=a/2+(b+c)/4;tu=(b+c)/4/den;tv=c/4/den;}
  else{a=1-v;b=u;c=v-u;den=(a+c)/2+b/4;tu=b/4/den;tv=(b/4+c/2)/den;}
  int texel=(tu<.5?(tv<.5?0xffff0000:0xff0000ff):(tv<.5?0xff00ff00:0xffffff00)); // BGRA byte order
  int base=phase==1?0xff0000ff:texel,result=128<<24;
  for(int channel=0;channel<3;channel++)result|=(phase==2?255:(((base>>>(8*channel))&255)+256)/2)<<(8*channel);
  return result;
 }
 public static void verify(ByteBuffer pixels,int offset,int expected){
  for(int channel=0;channel<4;channel++)if(Math.abs(Byte.toUnsignedInt(pixels.get(offset+channel))-((expected>>>(8*channel))&255))>1)throw new AssertionError("Direct scene pixel mismatch at"+offset+" channel"+channel);
 }
 // Host cleanup only after completed submissions; console display stays retained.
 public void close(){
  for(long fb:framebuffers)vkDestroyFramebuffer(device,fb,null);for(long v:views)vkDestroyImageView(device,v,null);
  vkDestroyPipeline(device,blendPipeline,null);vkDestroyPipeline(device,noDepthPipeline,null);vkDestroyPipeline(device,pipeline,null);vkDestroyPipelineLayout(device,pipelineLayout,null);vkDestroyShaderModule(device,vertex,null);vkDestroyShaderModule(device,fragment,null);vkDestroyRenderPass(device,renderPass,null);
  vkDestroyDescriptorPool(device,descriptorPool,null);vkDestroyDescriptorSetLayout(device,setLayout,null);vkDestroySampler(device,sampler,null);vkDestroyImageView(device,textureView,null);vkDestroyImage(device,texture,null);vkFreeMemory(device,textureMemory,null);vkDestroyImageView(device,depthView,null);vkDestroyImage(device,depth,null);vkFreeMemory(device,depthMemory,null);vkDestroyBuffer(device,vertexBuffer,null);vkFreeMemory(device,vertexMemory,null);
 }
}
