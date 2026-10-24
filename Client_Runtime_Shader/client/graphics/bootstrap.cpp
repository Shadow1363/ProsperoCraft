/* SPDX-License-Identifier: GPL-3.0-or-later */
#include "log_share.hpp"
#include "pad.h"
#include <cstdio>
#include <cstdint>
#include <ctime>
extern "C" int graphics_run();
extern "C" int sceKernelUsleep(std::uint32_t);
extern "C" int sceSystemServiceHideSplashScreen();
extern "C" int sceKernelSendNotificationRequest(std::uint32_t,void*,std::size_t,int);
namespace {
FILE *report_file;
struct Notification {std::uint8_t reserved[45];char message[3075];};
void notify(const char *text) {
 Notification n{};std::snprintf(n.message,sizeof(n.message),"%s",text);
 (void)sceKernelSendNotificationRequest(0,&n,sizeof(n),0);
}
}
extern "C" void graphics_report(const char *stage,int result) {
 const char *label=result==INT32_MIN?"RUN":result==0?"PASS":"FAIL";
 if(report_file) {std::fprintf(report_file,"%s result=%d: %s\n",label,result,stage);std::fflush(report_file);}
 char note[768];std::snprintf(note,sizeof(note),"Client Native Graphics 01.000.003 / PPSA99874\n%s result=%d: %s\nNative-only RADV; Java/game not launched.\n",result==INT32_MIN?"RUNNING":result==0?"PROGRESS":"FAILED",result,stage);
 ps5::log_share::write_note("/download0/probe-session.txt",note);
}
int main() {
 // Opening the app shares existing reports; only an explicit X press starts a new run.
 ps5::log_share::write_note("/download0/probe-build.txt","Client Native Graphics 01.000.003 / PPSA99874\n");
 ps5::log_share::start();
 notify("Client003 ready: press X for native GPU test. Initial screen may be blank; logs available on port8765.");
 sceUserServiceInitialize(nullptr);std::int32_t user=-1;int pad=-1;
 if(sceUserServiceGetInitialUser(&user)>=0&&scePadInit()>=0)pad=scePadOpen(user,0,0,nullptr);
 if(pad<0) {
  notify("Client003 controller initialization failed. Existing logs remain available.");
  for(;;)(void)sceKernelUsleep(1000000);
 }
 bool start=false,armed=false;std::uint32_t previous=0;
 while(!start) {
  PadSample batch[64]{};int count=scePadRead(pad,batch,64);
  if(count>=0&&count<=64)for(int i=0;i<count;i++) {
   auto buttons=batch[i].connected&&!(batch[i].buttons&0x80000000u)?batch[i].buttons:0u;
   if(batch[i].connected&&!(batch[i].buttons&0x80000000u)&&!(buttons&0x4000))armed=true;
   if(armed&&((buttons&~previous)&0x4000))start=true;
   previous=buttons;
  }
  (void)sceKernelUsleep(16000);
 }
 scePadClose(pad);
 ps5::log_share::archive_report("/download0/java25-vm-trace.log","/download0/previous-client-graphics-driver.log");
 ps5::log_share::begin_session("01.000.003","native-graphics");
 report_file=std::fopen("/download0/java25-startup.log","a");
 if(report_file) {std::fprintf(report_file,"\n=== Client Native Graphics003 RUN %lld ===\n",static_cast<long long>(std::time(nullptr)));std::fflush(report_file);}
 (void)std::freopen("/download0/java25-vm-trace.log","w",stderr);
 std::setvbuf(stderr,nullptr,_IONBF,0);
 notify("Client003 native GPU test starting. Logs: http://<PS5-IP>:8765/");
 (void)sceSystemServiceHideSplashScreen();
 graphics_report("Starting pinned RADV instance/device/display test",0);
 int result=graphics_run();
 if(result==0) {
  ps5::log_share::write_note("/download0/probe-session.txt","Client Native Graphics 01.000.003 / PPSA99874\nAUTOMATED CHECKS PASS:91 frames, GPU readback and presentation.\nHuman confirmation of RGB sequence and legible final card pending.\nFinal swapchain retained; lifecycle teardown not tested.\n");
  notify("Client003 GPU checks PASS. Confirm the RGB sequence and final graphics test card. Keep open for logs.");
 } else notify("Client003 GPU test FAILED. Keep the app open for logs at port8765.");
 // Do not exit this homebrew launch context; keep presentation and logs alive.
 for(;;)(void)sceKernelUsleep(1000000);
}
