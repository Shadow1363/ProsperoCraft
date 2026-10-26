#!/usr/bin/env python3
"""Render actual native launcher draw code; exercise return/ownership on host fixtures."""
from pathlib import Path
import argparse,subprocess
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args();runtime=a.runtime_workspace.resolve()
w=ROOT/'build/launcher-preview';w.mkdir(parents=True,exist_ok=True)
source='''#include <cstdlib>\n#include <cassert>\n#include <vector>\n#include <string>\n#include <fstream>\n#include "jni.h"\n#include "pad.h"\n#include "'''+str(runtime/'native/renderer/demo_renderer.cpp')+'''"\n#include "'''+str(ROOT/'client/launcher/native_menu.hpp')+'''"\n'''
source+=r'''
static void* storage=nullptr;static std::vector<std::string> operations;static int failure=0;static std::string output;
extern "C" {
bool ps5ObserveOwnedAllocation(const void* p) noexcept{return p!=nullptr;}
size_t sceKernelGetDirectMemorySize(){return 256*1024*1024;}
int sceKernelAllocateDirectMemory(int64_t,int64_t,size_t n,size_t alignment,int,int64_t*physical){assert(!storage);assert(!posix_memalign(&storage,alignment,n));*physical=0;return 0;}
int sceKernelMapDirectMemory(void**p,size_t,int,int,int64_t,size_t){*p=storage;return 0;}
int sceKernelMunmap(void*,size_t){operations.push_back("unmap");return failure==2?-1:0;}
int sceKernelReleaseDirectMemory(int64_t,size_t){operations.push_back("release");if(failure==3)return -1;free(storage);storage=nullptr;return 0;}
int sceKernelSendNotificationRequest(uint32_t,void*,size_t,int){return 0;}
int sceKernelUsleep(uint32_t){return 0;}
int sceSystemServiceHideSplashScreen(){return 0;}
int sceVideoOutOpen(int32_t,int32_t,int32_t,const void*){return 17;}
int sceVideoOutClose(int32_t){operations.push_back("close");return failure==1?-1:0;}
int sceVideoOutSetFlipRate(int32_t,int32_t){return 0;}
int sceVideoOutWaitVblank(int32_t){return 0;}
int sceVideoOutSubmitFlip(int32_t,int32_t,uint32_t,int64_t){
 if(!output.empty()){
  std::ofstream f(output,std::ios::binary);f<<"P6\n1920 1080\n255\n";
  for(unsigned y=0;y<1080;y++)for(unsigned x=0;x<1920;x++){auto px=*reinterpret_cast<uint32_t*>(static_cast<char*>(storage)+ps5::demo::tiled_byte_offset(x,y));char rgb[]={char(px&255),char((px>>8)&255),char((px>>16)&255)};f.write(rgb,3);}
  output.clear();
 }return 0;
}
}
namespace ps5::demo {
extern "C" void sceVideoOutSetBufferAttribute2(VideoAttribute*,uint64_t,uint32_t,uint32_t,uint32_t,uint64_t,uint32_t,uint64_t){}
extern "C" int sceVideoOutRegisterBuffers2(int32_t,int32_t,int32_t,VideoBuffer*,int32_t,VideoAttribute*,int32_t,void*){return 0;}
}
static bool update() noexcept{return false;}static bool stop() noexcept{return true;}
int main(int argc,char**argv){assert(argc==2);
 const char* values[]={"Your next world.","Starts right here.","Pick your instance. Make it your world.","","","Not signed in","SIGN IN & PLAY","SQUARE  Play demo     TRIANGLE  Sign out","MICROSOFT ACCOUNT","0","WAIT","0"};
 for(int i=0;i<12;i++)snprintf(prospero_menu::fields[i].data(),512,"%s",values[i]);
 output=std::string(argv[1])+"/home.ppm";
 assert(ps5::demo::run_ui_until(prospero_menu::draw,update,stop,"preview"));assert((operations==std::vector<std::string>{"close","unmap","release"})&&!storage);
 snprintf(prospero_menu::fields[3].data(),512,"ABCD-EFGH");snprintf(prospero_menu::fields[4].data(),512,"https://www.microsoft.com/link");snprintf(prospero_menu::fields[2].data(),512,"Approve sign-in on your phone or computer");
 output=std::string(argv[1])+"/signin.ppm";operations.clear();assert(ps5::demo::run_ui_until(prospero_menu::draw,update,stop,"preview"));
 for(failure=1;failure<=3;failure++){operations.clear();assert(!ps5::demo::run_ui_until(prospero_menu::draw,update,stop,"fixture"));assert(storage);assert(operations.size()==unsigned(failure));free(storage);storage=nullptr;}
 puts("PASS actual native UI draw/returning renderer fixture; close-before-unmap-before-release, retain remaining ownership on close/unmap/release failures; not PS5 handoff proof");
}
'''
(w/'preview.cpp').write_text(source)
jdk=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
subprocess.run(['clang++','-arch','x86_64','-std=c++20','-O1','-I'+str(runtime/'native/renderer'),'-I'+str(runtime/'build/native'),'-I'+str(runtime/'src'),'-I'+str(jdk/'include'),'-I'+str(jdk/'include/darwin'),str(w/'preview.cpp'),'-o',str(w/'preview')],check=True)
subprocess.run([str(w/'preview'),str(w)],check=True,timeout=30)
from PIL import Image
for name in ['home','signin']:
 with Image.open(w/(name+'.ppm'))as picture:picture.save(w/(name+'.png'))
print(w/'home.png')
