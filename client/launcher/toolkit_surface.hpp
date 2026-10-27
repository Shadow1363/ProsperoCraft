/* SPDX-License-Identifier: GPL-3.0-or-later
 * ProsperoCraft's private offscreen UI device. No SDL, WSI, audio or JNI.
 */
#pragma once
#include "toolkit_dispatch.hpp"
#include "gfx/vk/vk_renderer.hpp"
#include "ui/components/button.hpp"
#include <cstdio>
#include <string>
#include <vector>

namespace prospero_ui {
class Surface {
public:
 VkInstance instance{};VkPhysicalDevice physical{};VkDevice device{};VkQueue queue{};
 VkCommandPool pool{};VkCommandBuffer cmd{};VkFence fence{};
 VkImage image{};VkDeviceMemory image_memory{},read_memory{};VkImageView view{};
 VkRenderPass pass{};VkFramebuffer framebuffer{};VkBuffer read_buffer{};void* pixels{};
 hui::gfx::VkRenderer renderer;hui::gfx::Font regular,semibold;hui::ui::Fonts fonts{};
 hui::gfx::DrawList list;std::uint32_t logo=0;bool poisoned=false,ready=false;
 VkPhysicalDeviceMemoryProperties memory{};
 const char* stage="not initialized";
 VkResult error=VK_SUCCESS;
 bool ok(VkResult value){if(value==VK_SUCCESS)return true;error=value;return false;}
 std::uint32_t type(std::uint32_t bits,VkMemoryPropertyFlags flags){for(unsigned i=0;i<memory.memoryTypeCount;i++)if((bits&(1u<<i))&&(memory.memoryTypes[i].propertyFlags&flags)==flags)return i;return UINT32_MAX;}
 bool allocate(VkMemoryRequirements req,VkMemoryPropertyFlags flags,VkDeviceMemory& out){auto t=type(req.memoryTypeBits,flags);if(t==UINT32_MAX)return false;VkMemoryAllocateInfo a{};a.sType=VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;a.allocationSize=req.size;a.memoryTypeIndex=t;return ok(vkAllocateMemory(device,&a,nullptr,&out));}
 bool font(const char* base,const char* name,hui::gfx::Font& face,hui::ui::FontRef& ref){
  std::string path=std::string(base)+"/"+name;FILE* file=std::fopen(path.c_str(),"rb");if(!file)return false;
  std::fseek(file,0,SEEK_END);long n=std::ftell(file);std::rewind(file);if(n<=0||n>16*1024*1024){std::fclose(file);return false;}
  std::string data(static_cast<std::size_t>(n),'\0');bool read=std::fread(data.data(),1,data.size(),file)==data.size();std::fclose(file);
  if(!read||!face.load(data))return false;ref={&face,renderer.create_font_texture(face)};return ref.texture!=0;
 }
 bool init(const char* font_dir){
  stage="Vulkan dispatch";if(!toolkit_load_global())return false;
  VkApplicationInfo a{};a.sType=VK_STRUCTURE_TYPE_APPLICATION_INFO;a.pApplicationName="ProsperoCraft launcher";a.apiVersion=VK_API_VERSION_1_0;
  VkInstanceCreateInfo i{};i.sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;i.pApplicationInfo=&a;
  if(!ok(vkCreateInstance(&i,nullptr,&instance))||!toolkit_load_instance(instance))return false;
  std::uint32_t count=0;if(!ok(vkEnumeratePhysicalDevices(instance,&count,nullptr))||!count||count>16)return false;
  std::vector<VkPhysicalDevice> devices(count);if(!ok(vkEnumeratePhysicalDevices(instance,&count,devices.data())))return false;physical=devices[0];
  vkGetPhysicalDeviceMemoryProperties(physical,&memory);count=0;vkGetPhysicalDeviceQueueFamilyProperties(physical,&count,nullptr);
  std::vector<VkQueueFamilyProperties> families(count);vkGetPhysicalDeviceQueueFamilyProperties(physical,&count,families.data());
  std::uint32_t family=UINT32_MAX;for(unsigned f=0;f<count;f++)if(families[f].queueCount&&(families[f].queueFlags&VK_QUEUE_GRAPHICS_BIT)){family=f;break;}if(family==UINT32_MAX)return false;
  float priority=1;VkDeviceQueueCreateInfo qi{};qi.sType=VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;qi.queueFamilyIndex=family;qi.queueCount=1;qi.pQueuePriorities=&priority;
  VkDeviceCreateInfo di{};di.sType=VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;di.queueCreateInfoCount=1;di.pQueueCreateInfos=&qi;
  if(!ok(vkCreateDevice(physical,&di,nullptr,&device))||!toolkit_load_device(device))return false;vkGetDeviceQueue(device,family,0,&queue);
  stage="offscreen resources";VkCommandPoolCreateInfo pi{};pi.sType=VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;pi.queueFamilyIndex=family;pi.flags=VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
  if(!ok(vkCreateCommandPool(device,&pi,nullptr,&pool)))return false;
  VkCommandBufferAllocateInfo ca{};ca.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;ca.commandPool=pool;ca.level=VK_COMMAND_BUFFER_LEVEL_PRIMARY;ca.commandBufferCount=1;
  if(!ok(vkAllocateCommandBuffers(device,&ca,&cmd)))return false;
  VkFenceCreateInfo fi{};fi.sType=VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;fi.flags=VK_FENCE_CREATE_SIGNALED_BIT;if(!ok(vkCreateFence(device,&fi,nullptr,&fence)))return false;
  VkImageCreateInfo im{};im.sType=VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO;im.imageType=VK_IMAGE_TYPE_2D;im.format=VK_FORMAT_R8G8B8A8_UNORM;im.extent={1920,1080,1};im.mipLevels=im.arrayLayers=1;im.samples=VK_SAMPLE_COUNT_1_BIT;im.tiling=VK_IMAGE_TILING_OPTIMAL;im.usage=VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT|VK_IMAGE_USAGE_TRANSFER_SRC_BIT;
  if(!ok(vkCreateImage(device,&im,nullptr,&image)))return false;VkMemoryRequirements req{};vkGetImageMemoryRequirements(device,image,&req);
  if(!allocate(req,VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,image_memory)||!ok(vkBindImageMemory(device,image,image_memory,0)))return false;
  VkImageViewCreateInfo vi{};vi.sType=VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;vi.image=image;vi.viewType=VK_IMAGE_VIEW_TYPE_2D;vi.format=im.format;vi.subresourceRange={VK_IMAGE_ASPECT_COLOR_BIT,0,1,0,1};if(!ok(vkCreateImageView(device,&vi,nullptr,&view)))return false;
  VkAttachmentDescription at{};at.format=im.format;at.samples=VK_SAMPLE_COUNT_1_BIT;at.loadOp=VK_ATTACHMENT_LOAD_OP_CLEAR;at.storeOp=VK_ATTACHMENT_STORE_OP_STORE;at.initialLayout=VK_IMAGE_LAYOUT_UNDEFINED;at.finalLayout=VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL;
  VkAttachmentReference ar{0,VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL};VkSubpassDescription sub{};sub.pipelineBindPoint=VK_PIPELINE_BIND_POINT_GRAPHICS;sub.colorAttachmentCount=1;sub.pColorAttachments=&ar;
  VkSubpassDependency dep[2]{};dep[0].srcSubpass=VK_SUBPASS_EXTERNAL;dep[0].dstSubpass=0;dep[0].srcStageMask=VK_PIPELINE_STAGE_TRANSFER_BIT;dep[0].dstStageMask=VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;dep[0].srcAccessMask=VK_ACCESS_TRANSFER_READ_BIT;dep[0].dstAccessMask=VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
  dep[1].srcSubpass=0;dep[1].dstSubpass=VK_SUBPASS_EXTERNAL;dep[1].srcStageMask=VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;dep[1].dstStageMask=VK_PIPELINE_STAGE_TRANSFER_BIT;dep[1].srcAccessMask=VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;dep[1].dstAccessMask=VK_ACCESS_TRANSFER_READ_BIT;
  VkRenderPassCreateInfo rp{};rp.sType=VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;rp.attachmentCount=1;rp.pAttachments=&at;rp.subpassCount=1;rp.pSubpasses=&sub;rp.dependencyCount=2;rp.pDependencies=dep;if(!ok(vkCreateRenderPass(device,&rp,nullptr,&pass)))return false;
  VkFramebufferCreateInfo fb{};fb.sType=VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;fb.renderPass=pass;fb.attachmentCount=1;fb.pAttachments=&view;fb.width=1920;fb.height=1080;fb.layers=1;if(!ok(vkCreateFramebuffer(device,&fb,nullptr,&framebuffer)))return false;
  VkBufferCreateInfo bi{};bi.sType=VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;bi.size=1920*1080*4;bi.usage=VK_BUFFER_USAGE_TRANSFER_DST_BIT;if(!ok(vkCreateBuffer(device,&bi,nullptr,&read_buffer)))return false;
  vkGetBufferMemoryRequirements(device,read_buffer,&req);if(!allocate(req,VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT|VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,read_memory)||!ok(vkBindBufferMemory(device,read_buffer,read_memory,0))||!ok(vkMapMemory(device,read_memory,0,VK_WHOLE_SIZE,0,&pixels)))return false;
  hui::gfx::VkRendererConfig config;config.physical_device=physical;config.device=device;config.queue=queue;config.queue_family=family;config.frames_in_flight=1;config.render_pass=pass;
  stage="toolkit pipelines and font uploads";if(!renderer.init(config)||!font(font_dir,"inter-regular.huifont",regular,fonts.regular)||!font(font_dir,"inter-semibold.huifont",semibold,fonts.semibold))return false;
  fonts.display=fonts.mono=fonts.pixel=fonts.hand=fonts.semibold;stage="ready";ready=true;return true;
 }
 bool render(){
  // A single slot: completion precedes every prepare and every CPU read.
  if(!ready||poisoned)return false;
  if(!ok(vkWaitForFences(device,1,&fence,VK_TRUE,5000000000ULL))){poisoned=true;return false;}
  if(!ok(vkResetCommandBuffer(cmd,0)))return false;
  VkCommandBufferBeginInfo begin{};begin.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;if(!ok(vkBeginCommandBuffer(cmd,&begin)))return false;
  renderer.begin();renderer.draw(list);renderer.prepare(cmd,0);
  if(renderer.last_error()!=VK_SUCCESS){error=renderer.last_error();return false;}
  VkClearValue clear{};VkRenderPassBeginInfo rp{};rp.sType=VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;rp.renderPass=pass;rp.framebuffer=framebuffer;rp.renderArea.extent={1920,1080};rp.clearValueCount=1;rp.pClearValues=&clear;
  vkCmdBeginRenderPass(cmd,&rp,VK_SUBPASS_CONTENTS_INLINE);renderer.draw(cmd,1920,1080);vkCmdEndRenderPass(cmd);
  VkBufferImageCopy copy{};copy.imageSubresource={VK_IMAGE_ASPECT_COLOR_BIT,0,0,1};copy.imageExtent={1920,1080,1};vkCmdCopyImageToBuffer(cmd,image,VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,read_buffer,1,&copy);
  VkBufferMemoryBarrier barrier{};barrier.sType=VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER;barrier.srcAccessMask=VK_ACCESS_TRANSFER_WRITE_BIT;barrier.dstAccessMask=VK_ACCESS_HOST_READ_BIT;barrier.srcQueueFamilyIndex=barrier.dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED;barrier.buffer=read_buffer;barrier.size=VK_WHOLE_SIZE;
  vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_TRANSFER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,0,nullptr,1,&barrier,0,nullptr);
  if(!ok(vkEndCommandBuffer(cmd))||!ok(vkResetFences(device,1,&fence)))return false;
  VkSubmitInfo submit{};submit.sType=VK_STRUCTURE_TYPE_SUBMIT_INFO;submit.commandBufferCount=1;submit.pCommandBuffers=&cmd;
  if(!ok(vkQueueSubmit(queue,1,&submit,fence))||!ok(vkWaitForFences(device,1,&fence,VK_TRUE,5000000000ULL))){poisoned=true;return false;}
  return true;
 }
 bool close(){
  // Timeout/failed submit retains uncertain GPU ownership until process exit.
  if(poisoned)return false;
  if(device&&!ok(vkDeviceWaitIdle(device))){poisoned=true;return false;}
  renderer.release();ready=false;
  if(device){if(pixels)vkUnmapMemory(device,read_memory);if(read_buffer)vkDestroyBuffer(device,read_buffer,nullptr);if(read_memory)vkFreeMemory(device,read_memory,nullptr);if(framebuffer)vkDestroyFramebuffer(device,framebuffer,nullptr);if(pass)vkDestroyRenderPass(device,pass,nullptr);if(view)vkDestroyImageView(device,view,nullptr);if(image)vkDestroyImage(device,image,nullptr);if(image_memory)vkFreeMemory(device,image_memory,nullptr);if(fence)vkDestroyFence(device,fence,nullptr);if(pool)vkDestroyCommandPool(device,pool,nullptr);vkDestroyDevice(device,nullptr);}
  if(instance)vkDestroyInstance(instance,nullptr);instance={};device={};pixels=nullptr;return true;
 }
};
}
