#!/usr/bin/env python3
"""Real Vulkan resource cycles, readback, partial init and timeout retention."""
from pathlib import Path
import subprocess
from build_launcher_toolkit import ROOT,KIT,LLVM,build
work=ROOT/'build/toolkit-surface-test';objects=build(work)
source=r'''
#include <cassert>
#include <cstdio>
#include "toolkit_surface.hpp"
static VKAPI_ATTR VkResult VKAPI_CALL timeout(VkDevice,std::uint32_t,const VkFence*,VkBool32,std::uint64_t){return VK_TIMEOUT;}
int main(int argc,char** argv){
 assert(argc==2);
 for(int cycle=0;cycle<3;cycle++){
  prospero_ui::Surface s;assert(s.init(argv[1]));
  for(unsigned frame=0;frame<12;frame++){
   s.list.clear();s.list.rounded_rect({0,0,1920,1080},0,hui::gfx::Color::rgb(frame%2?0x123456:0xabcdef));
   assert(s.render());auto* pixels=static_cast<const unsigned char*>(s.pixels);
   for(unsigned offset:{0u,4u*(1919u),4u*(1920u*1079u),4u*(1920u*1080u-1u)}){
    assert(pixels[offset]==(frame%2?0x12:0xab));assert(pixels[offset+1]==(frame%2?0x34:0xcd));assert(pixels[offset+2]==(frame%2?0x56:0xef));
   }
  }
  auto wait=prospero_ui_dispatch::fn_WaitForFences;prospero_ui_dispatch::fn_WaitForFences=timeout;
  assert(!s.render()&&s.poisoned&&s.error==VK_TIMEOUT);auto device=s.device;auto memory=s.read_memory;
  assert(!s.close()&&s.device==device&&s.read_memory==memory&&s.pixels);
  prospero_ui_dispatch::fn_WaitForFences=wait;
  // Test-only recovery: this injected timeout submitted no new work. Confirm
  // idle with the real driver before allowing fixture cleanup.
  assert(vkDeviceWaitIdle(s.device)==VK_SUCCESS);s.poisoned=false;assert(s.close());assert(!s.device&&!s.instance&&!s.pixels);
 }
 {prospero_ui::Surface s;assert(!s.init("/this-font-path-does-not-exist"));assert(s.device&&!s.ready);assert(s.close());}
 puts("PASS real Vulkan:3device/resource cycles,36one-slot submissions/readbacks with all four image corners,missing-font partial-init cleanup,timeout blocks reuse and retains GPU ownership");
}
'''
(work/'test.cpp').write_text(source)
subprocess.run([str(LLVM/'clang++'),'-std=c++20','-O1','-Wall','-Wextra','-Werror','-I'+str(KIT/'src'),'-I'+str(ROOT/'client/launcher'),'-I'+str(work),'-I'+str(ROOT/'.tools/PS5_Mesa/include'),str(work/'test.cpp'),*map(str,objects),'/opt/homebrew/lib/libvulkan_lvp.dylib','-o',str(work/'test')],check=True)
subprocess.run([str(work/'test'),str(KIT/'assets/fonts')],check=True,timeout=90)
