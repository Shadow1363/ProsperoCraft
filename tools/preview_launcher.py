#!/usr/bin/env python3
"""Render actual native launcher draw code; exercise return/ownership on host fixtures."""
from pathlib import Path
import argparse,subprocess
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args();runtime=a.runtime_workspace.resolve()
w=ROOT/'build/launcher-preview';w.mkdir(parents=True,exist_ok=True)
source='''#include <cstdlib>\n#include <cassert>\n#include <vector>\n#include <string>\n#include <fstream>\n#include <thread>\n#include <chrono>\n#include "jni.h"\n#include "pad.h"\n#include "'''+str(runtime/'native/renderer/demo_renderer.cpp')+'''"\n#include "'''+str(ROOT/'client/launcher/native_menu.hpp')+'''"\n'''
source+=r'''
static std::atomic<unsigned> fake_buttons{0},pad_reads{0},flips{0};
static void* storage=nullptr;static std::vector<std::string> operations;static int failure=0;static std::string output;
extern "C" {
bool ps5ObserveOwnedAllocation(const void* p) noexcept{return p!=nullptr;}
size_t sceKernelGetDirectMemorySize(){return 256*1024*1024;}
int sceKernelAllocateDirectMemory(int64_t,int64_t,size_t n,size_t alignment,int,int64_t*physical){assert(!storage);assert(!posix_memalign(&storage,alignment,n));*physical=0;return 0;}
int sceKernelMapDirectMemory(void**p,size_t,int,int,int64_t,size_t){*p=storage;return 0;}
int sceKernelMunmap(void*,size_t){operations.push_back("unmap");return failure==2?-1:0;}
int sceKernelReleaseDirectMemory(int64_t,size_t){operations.push_back("release");if(failure==3)return -1;free(storage);storage=nullptr;return 0;}
int sceKernelSendNotificationRequest(uint32_t,void*,size_t,int){return 0;}
int sceKernelUsleep(uint32_t us){std::this_thread::sleep_for(std::chrono::microseconds(us));return 0;}
int sceUserServiceGetInitialUser(int32_t* user){*user=1;return 0;}
int scePadOpen(int32_t,int,int,const void*){return 42;}
int scePadClose(int){return 0;}
int scePadRead(int,PadSample* samples,int){samples[0]={};samples[0].connected=1;samples[0].buttons=fake_buttons.load();pad_reads.fetch_add(1);return 1;}
int sceSystemServiceHideSplashScreen(){return 0;}
int sceVideoOutOpen(int32_t,int32_t,int32_t,const void*){return 17;}
int sceVideoOutClose(int32_t){operations.push_back("close");return failure==1?-1:0;}
int sceVideoOutSetFlipRate(int32_t,int32_t){return 0;}
int sceVideoOutWaitVblank(int32_t){return 0;}
int sceVideoOutSubmitFlip(int32_t,int32_t,uint32_t,int64_t){
 flips.fetch_add(1);
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
static pthread_t jni_owner{};static std::string ui_strings[12];static unsigned java_calls=0;
static void check_jni(){assert(pthread_equal(jni_owner,pthread_self()));}
static jmethodID method_id(JNIEnv*,jclass,const char*,const char*){check_jni();return reinterpret_cast<jmethodID>(1);}
static jobject java_tick(JNIEnv*,jclass,jmethodID,va_list args){check_jni();++java_calls;unsigned buttons=va_arg(args,jint);if(buttons&0x4000)ui_strings[10]="LAUNCH";return reinterpret_cast<jobject>(1);}
static jsize array_length(JNIEnv*,jarray){check_jni();return 12;}
static jobject array_element(JNIEnv*,jobjectArray,jsize index){check_jni();return reinterpret_cast<jobject>(uintptr_t(index+10));}
static const char* utf_chars(JNIEnv*,jstring value,jboolean*){check_jni();return ui_strings[reinterpret_cast<uintptr_t>(value)-10].c_str();}
static void release_chars(JNIEnv*,jstring,const char*){check_jni();}
static void delete_ref(JNIEnv*,jobject){check_jni();}
static jboolean exception_check(JNIEnv*){check_jni();return JNI_FALSE;}
static bool update() noexcept{return false;}static bool stop() noexcept{return true;}
int main(int argc,char**argv){assert(argc==2);
 const char* values[]={"Your next world.","Starts right here.","Pick your instance. Make it your world.","","","Not signed in","SIGN IN & PLAY","SQUARE  Play demo     TRIANGLE  Sign out","MICROSOFT ACCOUNT","0","WAIT","0"};
 for(int i=0;i<12;i++)snprintf(prospero_menu::fields[i].data(),512,"%s",values[i]);
 output=std::string(argv[1])+"/home.ppm";
 assert(ps5::demo::run_ui_until(prospero_menu::draw,update,stop,"preview"));assert((operations==std::vector<std::string>{"close","unmap","release"})&&!storage);
 snprintf(prospero_menu::fields[3].data(),512,"ABCD-EFGH");snprintf(prospero_menu::fields[4].data(),512,"https://www.microsoft.com/link");snprintf(prospero_menu::fields[2].data(),512,"Approve sign-in on your phone or computer");
 output=std::string(argv[1])+"/signin.ppm";operations.clear();assert(ps5::demo::run_ui_until(prospero_menu::draw,update,stop,"preview"));
 for(failure=1;failure<=3;failure++){operations.clear();assert(!ps5::demo::run_ui_until(prospero_menu::draw,update,stop,"fixture"));assert(storage);assert(operations.size()==unsigned(failure));free(storage);storage=nullptr;}
 failure=0;operations.clear();unsigned before=flips.load();
 assert(prospero_menu::start_frontend());assert(flips.load()>before); // no JVM exists in this process
 auto await=[&](auto predicate){auto until=std::chrono::steady_clock::now()+std::chrono::seconds(3);while(!predicate()&&std::chrono::steady_clock::now()<until)std::this_thread::sleep_for(std::chrono::milliseconds(1));assert(predicate());};
 // Simulate blocked/unavailable Java initialization. Native drawing/controller
 // polling must remain responsive and preserve ordered button edges.
 unsigned reads=pad_reads.load();fake_buttons=0x40;await([&]{return pad_reads.load()>reads+1;});fake_buttons=0;reads=pad_reads.load();await([&]{return pad_reads.load()>reads+1;});
 fake_buttons=0x4000;reads=pad_reads.load();await([&]{return pad_reads.load()>reads+1;});fake_buttons=0;
 assert(!prospero_menu::online.load());assert(prospero_menu::take_input()==0x40);assert(prospero_menu::take_input()==0x4000);assert(prospero_menu::take_input()==0);
 // A failed Java boot leaves a real, responsive native failure screen.
 prospero_menu::show_failure();reads=pad_reads.load();await([&]{return pad_reads.load()>reads+1;});assert(!prospero_menu::display_done.load());
 prospero_menu::exit_requested=true;pthread_join(prospero_menu::ui_thread,nullptr);
 assert(prospero_menu::display_done.load()&&prospero_menu::display_ok.load());assert(!storage);assert((operations==std::vector<std::string>{"close","unmap","release"}));
 operations.clear();assert(prospero_menu::start_frontend());jni_owner=pthread_self();
 for(int i=0;i<12;++i)ui_strings[i]=values[i];
 JNINativeInterface_ functions{};functions.GetStaticMethodID=method_id;functions.CallStaticObjectMethodV=java_tick;
 functions.GetArrayLength=array_length;functions.GetObjectArrayElement=array_element;functions.GetStringUTFChars=utf_chars;functions.ReleaseStringUTFChars=release_chars;functions.DeleteLocalRef=delete_ref;functions.ExceptionCheck=exception_check;
 JNIEnv environment{&functions};prospero_menu::push_input(0x4000);
 assert(prospero_menu::menu(&environment,reinterpret_cast<jclass>(1))==JNI_TRUE);assert(java_calls>0);
 assert(!storage&&prospero_menu::display_done.load()&&prospero_menu::display_ok.load());
 assert((operations==std::vector<std::string>{"close","unmap","release"}));
 puts("PASS actual JNI bridge via fixture table: callbacks remain on JVM caller thread, input delivered, launch waits for UI close/unmap/release/join");
 puts("PASS native frontend presents before any JVM; remains responsive with blocked account boot, ordered input mailbox, boot failure screen and joined cleanup");
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
