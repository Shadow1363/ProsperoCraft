#!/usr/bin/env python3
"""Exercise actual Vulkan draw + native mailbox/VideoOut fixtures on lavapipe.

Run preview_launcher.py first to generate the shared controller/JNI fixture.
The VideoOut functions are host doubles; the kit, driver, shaders, queue,
render pass, uploads, synchronization and readback are real Vulkan.
"""
import argparse, os, subprocess
from pathlib import Path
from build_launcher_toolkit import ROOT, KIT, LLVM, build

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--runtime-workspace',required=True,type=Path)
a=p.parse_args()
work=ROOT/'build/launcher-toolkit-preview';work.mkdir(parents=True,exist_ok=True)
objects=build(work)
runtime=a.runtime_workspace.resolve()
# The host is ARM64. Only the VideoOut fixture's x86 streaming copy is
# replaced with memcpy; the target continues to compile the original SSE path.
cpu=(runtime/'native/renderer/demo_renderer.cpp').read_text().replace('#include <emmintrin.h>','')
start=cpu.index('    auto *out = static_cast<__m128i *>')
end=cpu.index('    _mm_sfence();',start)+len('    _mm_sfence();')
cpu=cpu[:start]+'    std::memcpy(destination,source,frame_bytes);'+cpu[end:]
(work/'videoout_host.cpp').write_text(cpu)
source=(ROOT/'build/launcher-preview/preview.cpp').read_text()
source=source.replace(str(runtime/'native/renderer/demo_renderer.cpp'),str(work/'videoout_host.cpp'))
source=source.replace('#include "'+str(ROOT/'client/launcher/native_menu.hpp')+'"', '#define PROSPERO_TOOLKIT 1\n#define PROSPERO_TOOLKIT_FONT_DIR "'+str(KIT/'assets/fonts')+'"\n#include "'+str(ROOT/'client/launcher/native_menu.hpp')+'"\nnamespace prospero_menu {void initialize_toolkit_graphics(){}}')
source=source.replace('output=std::string(argv[1])+"/"+scene+".ppm";prospero_menu::focus={};', 'output=std::string(argv[1])+"/"+scene+".ppm";prospero_menu::focus={};for(int settle=0;settle<60;settle++){prospero_ui::surface->list.clear();prospero_ui::Canvas canvas;prospero_menu::compose(canvas);}')
source=source.replace('snprintf(prospero_menu::fields[13].data(),512,"6");', 'snprintf(prospero_menu::fields[13].data(),512,"6");snprintf(prospero_menu::fields[30].data(),512,"OFF");snprintf(prospero_menu::fields[73].data(),512,"DEMO BRANCH");')
source=source.replace('int main(int argc,char**argv){assert(argc==2);','int main(int argc,char**argv){assert(argc==2);assert(prospero_ui::open(PROSPERO_TOOLKIT_FONT_DIR));')
source=source.replace('static void animation_check(ps5::demo::Canvas& c) noexcept {','static void animation_check(ps5::demo::Canvas&) noexcept {prospero_ui::Canvas c;')
# The legacy discrete interpolation assertion has its own fixture. Here dt
# and the toolkit spring are exercised by the rendered controller transitions.
source=source.replace(' assert(ps5::demo::run_ui_until(animation_check,update,stop,""));','')
(work/'preview.cpp').write_text(source)
jdk=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
runtime=a.runtime_workspace.resolve()
subprocess.run([str(LLVM/'clang++'),'-std=c++20','-O1','-Wno-unused-function','-I'+str(KIT/'src'),'-I'+str(work),'-I'+str(ROOT/'.tools/PS5_Mesa/include'),'-I'+str(runtime/'native/renderer'),'-I'+str(runtime/'build/native'),'-I'+str(runtime/'src'),'-I'+str(jdk/'include'),'-I'+str(jdk/'include/darwin'),str(work/'preview.cpp'),*map(str,objects),'/opt/homebrew/lib/libvulkan_lvp.dylib','-o',str(work/'preview')],check=True)
subprocess.run([str(work/'preview'),str(work)],check=True,timeout=180)
from PIL import Image
for path in work.glob('*.ppm'):
    with Image.open(path) as picture: picture.save(path.with_suffix('.png'))
print(work/'home.png')
