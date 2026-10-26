/* SPDX-License-Identifier: GPL-3.0-or-later */
#pragma once
#include "demo_renderer.hpp"
#include "branding_logo.hpp"
#include <array>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <atomic>
#include <pthread.h>
extern "C" int sceKernelUsleep(std::uint32_t);
extern "C" std::uint64_t sceKernelGetProcessTime();
namespace prospero_menu {
using ps5::demo::Canvas;
constexpr std::uint32_t ink(std::uint32_t rgb){return 0xff000000u|((rgb&255)<<16)|(rgb&0xff00)|((rgb>>16)&255);}
using Fields=std::array<std::array<char,512>,80>;
// Only the native UI thread draws/reads the controller. JNI stays on the JVM
// startup thread. A bounded mailbox exchanges public UI text and button edges.
inline Fields fields{},published{};
inline pthread_mutex_t mailbox=PTHREAD_MUTEX_INITIALIZER;
inline pthread_t ui_thread{};
inline unsigned events[64]{},event_read=0,event_write=0;
inline std::atomic<bool> visible{false},online{false},exit_requested{false},display_done{false},display_ok{false};
inline bool armed=false;
inline std::uint32_t previous=0;
inline int controller=-1;
inline unsigned updates=0;
inline unsigned held_direction=0;inline std::uint64_t repeat_at=0;
inline void publish(const Fields& values) noexcept {
 pthread_mutex_lock(&mailbox);published=values;pthread_mutex_unlock(&mailbox);
}
inline unsigned take_input() noexcept {
 pthread_mutex_lock(&mailbox);unsigned value=0;if(event_read!=event_write){value=events[event_read%64];++event_read;}pthread_mutex_unlock(&mailbox);return value;
}
inline void push_input(unsigned value) noexcept {
 if(!value)return;pthread_mutex_lock(&mailbox);
 if(event_write-event_read<64)events[event_write++%64]=value;
 pthread_mutex_unlock(&mailbox);
}
inline void label(Canvas& c,int x,int y,const char* text,unsigned size=24,std::uint32_t rgb=0xeaf0e8){c.label(x,y,text,size,ink(rgb));}
inline void wrap(Canvas& c,int x,int y,std::string_view text,unsigned width,int lines=3){
 while(!text.empty()&&lines-->0){std::size_t n=text.size();while(n>0&&Canvas::text_width(text.substr(0,n),24)>width)--n;if(!n)break;
  if(n<text.size()){auto space=text.substr(0,n).find_last_of(' ');if(space!=std::string_view::npos&&space>0)n=space;}
  c.label(x,y,text.substr(0,n),24,ink(0xaac0b6));text.remove_prefix(n);while(!text.empty()&&text.front()==' ')text.remove_prefix(1);y+=34;
 }
}
inline void card(Canvas& c,int x,int y,unsigned w,unsigned h,bool focus=false){c.rounded(x,y,w,h,24,ink(focus?0xa9eab6:0x294138));c.rounded(x+2,y+2,w-4,h-4,22,ink(0x13271f));}
inline void title(Canvas& c,int x,int y,const char* text,unsigned size=30,unsigned width=1000,std::uint32_t color=0xeaf0e8){
 std::string_view value(text);if(Canvas::text_width(value,size)>width){while(!value.empty()&&Canvas::text_width(value,size)+Canvas::text_width("...",size)>width)value.remove_suffix(1);c.label(x,y,value,size,ink(color));c.label(x+Canvas::text_width(value,size),y,"...",size,ink(color));}else label(c,x,y,text,size,color);
}
inline int number(int index){return std::atoi(fields[index].data());}
inline void block(Canvas& c,int x,int y,int size,int kind){
 if(kind==0){for(int yy=0;yy<72;++yy)for(int xx=0;xx<72;++xx){auto color=logo_pixels[yy*72+xx];if(color)c.rectangle(x+xx*size/72,y+yy*size/72,(size+71)/72,(size+71)/72,static_cast<ps5::demo::Color>(color));}return;}
 const std::uint32_t top[]={0,0x91b979,0xb7a0e4,0x79c5d8,0xe58b81,0x6ea78b,0xead27c,0xc8dfe2};
 const std::uint32_t body[]={0,0x87785a,0x6b5c91,0x355f7f,0x8a4b4f,0x3f6952,0x9f824e,0x839fa7};
 kind=kind<1||kind>7?1:kind;c.rounded(x,y,size,size,static_cast<unsigned>(size/5),ink(body[kind]));c.rounded(x,y,size,static_cast<unsigned>(size*0.43f),static_cast<unsigned>(size/5),ink(top[kind]));
 for(int row=0;row<4;row++)for(int col=0;col<4;col++){unsigned tile=static_cast<unsigned>(size/7);auto color=(row+col)%3==0?top[kind]:body[kind];c.rectangle(x+size/10+col*size/5,y+size/3+row*size/7,tile,tile,static_cast<ps5::demo::Color>(ink(color)));}
}
struct Focus {float x=0,y=0,w=0,h=0;bool initialized=false;};
inline Focus focus{};inline std::uint64_t transition_start=0,last_draw_time=0;inline bool animating=false;
inline std::uint64_t now_ms(){return sceKernelGetProcessTime()/1000;}
inline void selection(Canvas& c,int x,int y,int w,int h){
 const bool reduced=std::strcmp(fields[30].data(),"ON")==0;
 if(!focus.initialized||reduced){focus={float(x),float(y),float(w),float(h),true};}
 const float rate=reduced?1.0f:0.34f;focus.x+=(x-focus.x)*rate;focus.y+=(y-focus.y)*rate;focus.w+=(w-focus.w)*rate;focus.h+=(h-focus.h)*rate;
 auto distance=[](float a,float b){return a>b?a-b:b-a;};if(distance(focus.x,float(x))+distance(focus.y,float(y))+distance(focus.w,float(w))+distance(focus.h,float(h))>1.0f)animating=true;
 c.rounded(x-3,y-3,unsigned(w)+6,unsigned(h)+6,22,ink(animating?0x81bd90:0xa9eab6));
}
inline void action(Canvas& c,int x,int y,int w,const char* text,bool active,bool primary=false){
 if(active)selection(c,x,y,w,76);c.rounded(x,y,w,76,18,ink(primary?0xb6f2be:0x244438));label(c,x+28,y+22,text,30,primary?0x102c1b:0xeaf0e8);
}
inline void row_control(Canvas& c,int y,const char* name,const char* value,bool active){
 if(active)selection(c,760,y,1080,96);c.rounded(760,y,1080,96,20,ink(active?0x1e3c30:0x142b24));label(c,792,y+16,name,24,0x8fae9d);title(c,792,y+47,value,30,960);label(c,1779,y+43,">",30,0xa9eab6);
}
inline void draw(Canvas& c) noexcept {
 animating=false;last_draw_time=now_ms();
 c.gradient(ink(0x0b1815),ink(0x08120f));c.disc(1760,850,380,ink(0x0c211a));
 const int page=number(11),row=number(15),selected=number(9),tab=number(12);const bool top=std::strcmp(fields[28].data(),"TOP")==0;
 float elapsed=float(now_ms()-transition_start)/180.0f;if(elapsed<0)elapsed=0;if(elapsed>1)elapsed=1;
 const int slide=std::strcmp(fields[30].data(),"ON")==0?0:int(16*(1-elapsed)*(1-elapsed));if(slide>0)animating=true;
 c.rounded(40,32,1840,108,24,ink(0x10221c));block(c,66,53,64,0);label(c,149,66,"ProsperoCraft",30);label(c,405,72,"NATIVE JAVA 25",24,0x718d7b);
 const char* tabs[]={"+  Add instance","Settings","Account"};const int tx[]={865,1245,1555},tw[]={350,280,280};
 for(int i=0;i<3;i++){bool current=(top&&tab==i)||(page>0&&page<=3&&page==i+1);if(current&&top)selection(c,tx[i],52,tw[i],68);c.rounded(tx[i],52,tw[i],68,18,ink(current?0x284f3c:0x172e24));label(c,tx[i]+24,72,tabs[i],30,current?0xc7f4cf:0xb0c4b5);}
 if(page==0){
  label(c,70,192+slide,"Your worlds, together.",64);label(c,74,276+slide,"A little space for your next big idea.",24,0x90ad9c);
  const int count=number(13),start=number(14);
  if(count==0){
   c.rounded(70,337+slide,1770,528,30,ink(0x10251d));block(c,325,470+slide,170,1);block(c,210,590+slide,86,2);block(c,510,405+slide,100,3);
   label(c,775,437+slide,"Make room for adventure.",42);wrap(c,779,510+slide,"Start with a fresh instance. Choose a26.x version and download it straight from the publisher.",880,3);
   action(c,780,673+slide,690,"+  ADD YOUR FIRST INSTANCE",!top,true);
  }else{
   for(int i=0;i<8&&start+i<count;i++){int x=70+(i%4)*450,y=342+(i/4)*272+slide,at=32+i*4;bool active=!top&&selected==start+i;if(active)selection(c,x,y,420,242);c.rounded(x,y,420,242,22,ink(active?0x1f3a2b:0x13291f));block(c,x+27,y+26,88,number(at+2));title(c,x+26,y+137,fields[at].data(),30,365);label(c,x+27,y+187,fields[at+1].data(),24,0x92b6a0);label(c,x+235,y+187,fields[at+3].data(),24,0xa7d4ae);}
   char pages[80];std::snprintf(pages,sizeof(pages),"%d instances    /    Page %d of %d",count,start/8+1,(count+7)/8);label(c,78,918,pages,24,0x6d927b);
  }
 }else if(page==1||page==5){
  label(c,70,185+slide,page==1?"A world of your own.":"Make it yours.",64);label(c,75,269+slide,page==1?"One instance. Its own settings, worlds and memories.":"Your worlds stay right where they are.",24,0x91ad9b);
  c.rounded(70,338+slide,620,548,28,ink(0x10221c));block(c,275,402+slide,204,page==1?number(24):number(18));title(c,105,690+slide,page==1?fields[22].data():fields[16].data(),42,540);label(c,108,761+slide,"JAVA EDITION / DEMO",24,0x8db69a);
  if(page==1){row_control(c,340+slide,"VERSION",fields[23].data(),row==0);row_control(c,458+slide,"NAME",fields[22].data(),row==1);const char* icons[]={"Crafting table","Grass","Amethyst","Ocean","Redstone","Forest","Gold","Snow"};int icon=number(24);row_control(c,576+slide,"ICON",icons[icon>=0&&icon<8?icon:0],row==2);action(c,760,738+slide,1080,"CREATE & DOWNLOAD",row==3,true);}
  else{row_control(c,340+slide,"INSTANCE NAME",fields[16].data(),row==0);const char* icons[]={"Crafting table","Grass","Amethyst","Ocean","Redstone","Forest","Gold","Snow"};int icon=number(18);row_control(c,458+slide,"INSTANCE ICON",icons[icon>=0&&icon<8?icon:0],row==1);action(c,760,640+slide,1080,"DONE",row==2,true);wrap(c,791,759+slide,"Version files are shared. Your worlds and options belong only to this instance.",1000,3);}
 }else if(page==2){
  label(c,70,185+slide,"Settle in.",64);label(c,75,270+slide,"A few thoughtful defaults. You're in control.",24,0x91ad9b);
  c.rounded(70,340+slide,620,548,28,ink(0x10221c));label(c,112,391+slide,"YOUR SETUP",24,0x8fbb9b);label(c,112,459+slide,"Native Java 25",42);wrap(c,114,545+slide,"Resolution applies to the game window on the next launch. Your in-game video and audio options stay with each instance.",520,5);label(c,114,773+slide,"L1 / R1  Switch top-bar focus",24,0x7fa78b);
  row_control(c,340+slide,"GAME RESOLUTION",fields[25].data(),row==0);row_control(c,465+slide,"PARALLEL DOWNLOADS",fields[26].data(),row==1);row_control(c,590+slide,"REDUCED MOTION",fields[30].data(),row==2);row_control(c,715+slide,"SHOW SNAPSHOTS",fields[27].data(),row==3);
 }else if(page==3){
  label(c,70,185+slide,"Your account. Your adventure.",64);label(c,75,270+slide,"Sign in on your phone. Your password stays with Microsoft.",24,0x91ad9b);
  c.rounded(70,340+slide,1000,548,28,ink(0x10221c));label(c,116,391+slide,"MICROSOFT ACCOUNT",24,0x8fbb9b);title(c,116,447+slide,fields[5].data(),42,900);
  if(fields[3][0]){label(c,116,539+slide,"ENTER THIS CODE",24,0x8eaf9a);label(c,115,584+slide,fields[3].data(),64,0xc9f5cd);wrap(c,117,699+slide,fields[4].data(),880,2);}
  else wrap(c,117,547+slide,"Demo instances work while application review is pending. Full account access completes only when all sign-in and ownership checks succeed.",850,5);
  action(c,1140,366+slide,700,"SIGN IN WITH MICROSOFT",row==0,true);action(c,1140,481+slide,700,"SIGN OUT",row==1);wrap(c,1167,634+slide,fields[2].data(),620,6);
 }else if(page==4){
  label(c,70,185+slide,"Ready when you are.",64);c.rounded(70,330+slide,620,560,28,ink(0x10221c));block(c,245,385+slide,270,number(18));title(c,109,721+slide,fields[16].data(),42,540);label(c,112,794+slide,fields[17].data(),24,0x97bea3);
  title(c,762,352+slide,fields[16].data(),64,1060);label(c,768,441+slide,"JAVA EDITION    /    DEMO INSTANCE",24,0x94b69f);
  action(c,760,505+slide,1080,fields[6].data(),row==0,true);action(c,760,621+slide,1080,"INSTANCE SETTINGS",row==1);action(c,760,737+slide,1080,"REPAIR DOWNLOAD",row==2);wrap(c,790,857+slide,fields[65].data(),1000,1);
 }else if(page==6){
  label(c,70,185,"Give it a name.",64);c.rounded(70,300,1770,116,22,ink(0x183c2a));title(c,103,330,fields[29].data(),42,1650);
  const char* chars=std::strcmp(fields[66].data(),"LOWER")==0?"abcdefghijklmnopqrstuvwxyz0123456789 ._-":"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ._-";int chosen=number(31);
  for(int i=0;i<40;i++){int x=80+(i%10)*176,y=465+(i/10)*91;if(i==chosen)selection(c,x,y,152,73);c.rounded(x,y,152,73,16,ink(i==chosen?0x356647:0x172e24));char letter[2]={chars[i],0};label(c,x+61,y+21,letter,30);}
  label(c,100,873,"X  Add     TRIANGLE  Backspace     L2  Case     R2  Space     OPTIONS  Clear     SQUARE  Done",24,0x8daf99);
 }
 if(std::strcmp(fields[64].data(),"BUSY")==0){
  if(page!=3)title(c,78,942,fields[2].data(),24,1300,0xaac8b2);label(c,1450,942,fields[21].data(),24,0xaac8b2);c.rounded(72,982,1770,5,2,ink(0x233c2c));if(number(20)>0)c.rounded(72,982,unsigned(1770*number(20)/1000),5,2,ink(0xa9eab6));
 }else if(page!=3)title(c,78,949,fields[2].data(),24,1760,0x83a58d);
 label(c,76,1020,fields[7].data(),24,0x7d9f89);label(c,1740,1020,"079",24,0x4e715b);
}
inline bool update() noexcept {
 // The second update follows the initial submit/WaitVblank in run_ui_until.
 if(++updates>=2)visible.store(true,std::memory_order_release);
 std::uint32_t pressed=0;PadSample batch[64]{};const int count=scePadRead(controller,batch,64);
 if(count>=0&&count<=64)for(int i=0;i<count;++i){auto buttons=batch[i].connected&&!(batch[i].buttons&0x80000000u)?batch[i].buttons:0u;if(!(buttons&0x4000))armed=true;if(armed)pressed|=buttons&~previous;previous=buttons;}
 unsigned direction=previous&0xf0u;auto current_time=now_ms();
 if(direction!=held_direction){held_direction=direction;repeat_at=current_time+400;}
 else if(direction&&current_time>=repeat_at){pressed|=direction;repeat_at=current_time+100;}
 push_input(pressed);
 bool changed=false;
 if(!online.load(std::memory_order_acquire)){
  if(pressed&0x400){std::snprintf(fields[12].data(),512,"%d",(number(12)+2)%3);std::snprintf(fields[28].data(),512,"TOP");changed=true;}
  if(pressed&0x800){std::snprintf(fields[12].data(),512,"%d",(number(12)+1)%3);std::snprintf(fields[28].data(),512,"TOP");changed=true;}
 }else{
  pthread_mutex_lock(&mailbox);changed=fields!=published;
  if(changed){if(std::strcmp(fields[11].data(),published[11].data())!=0){transition_start=now_ms();focus.initialized=false;}fields=published;}
  pthread_mutex_unlock(&mailbox);
 }
 if(changed)return true;
 return animating&&now_ms()-last_draw_time>=16;

}
inline bool stop() noexcept{return exit_requested.load(std::memory_order_acquire);}
inline void* ui_main(void*) noexcept {
 const bool closed=ps5::demo::run_ui_until(draw,update,stop,"ProsperoCraft native launcher visible before Java and Minecraft graphics");
 scePadClose(controller);controller=-1;
 display_ok.store(closed,std::memory_order_release);display_done.store(true,std::memory_order_release);return nullptr;
}
inline bool start_frontend() noexcept {
 visible=false;online=false;exit_requested=false;display_done=false;display_ok=false;
 updates=0;previous=0;held_direction=0;repeat_at=0;armed=false;focus={};transition_start=now_ms();animating=false;event_read=event_write=0;fields={};published={};
 const char* boot[]={"Your worlds, together.","A little space for your next big idea.","Opening your library...","","","Not signed in","PLAY DEMO","L1 / R1  Top bar     X  Select","PREPARING","0","WAIT","0"};
 for(int i=0;i<12;++i)std::snprintf(fields[i].data(),512,"%s",boot[i]);
 std::int32_t user=-1;if(sceUserServiceGetInitialUser(&user)<0)return false;controller=scePadOpen(user,0,0,nullptr);if(controller<0)return false;
 if(pthread_create(&ui_thread,nullptr,ui_main,nullptr)!=0){scePadClose(controller);controller=-1;return false;}
 while(!visible.load(std::memory_order_acquire)&&!display_done.load(std::memory_order_acquire))(void)sceKernelUsleep(1000);
 return visible.load(std::memory_order_acquire)&&!display_done.load(std::memory_order_acquire);
}
inline void show_failure() noexcept {
 Fields text{};
 // Do not touch UI-owned fields: supply a complete independent failure state.
 const char* boot[]={"Your next world.","Starts right here.","Account services could not start. Keep app open for startup logs.","","","Not signed in","STARTUP FAILED","Close and reopen after collecting the startup report","STARTUP FAILED","0","WAIT","0"};
 for(int i=0;i<12;++i)std::snprintf(text[i].data(),512,"%s",boot[i]);publish(text);online.store(true,std::memory_order_release);
}
inline jboolean menu(JNIEnv* env,jclass owner){
 const jmethodID tick=env->GetStaticMethodID(owner,"launcherTick","(I)[Ljava/lang/String;");if(!tick)return false;
 bool launch=false,failed=false;
 while(!launch&&!failed&&!display_done.load(std::memory_order_acquire)){
  auto array=static_cast<jobjectArray>(env->CallStaticObjectMethod(owner,tick,static_cast<jint>(take_input())));
  if(env->ExceptionCheck()||!array){failed=true;break;}
  Fields next{};
  if(env->GetArrayLength(array)!=80){env->DeleteLocalRef(array);failed=true;break;}
  for(int i=0;i<80;++i){auto value=static_cast<jstring>(env->GetObjectArrayElement(array,i));if(!value){failed=true;break;}const char* bytes=env->GetStringUTFChars(value,nullptr);if(!bytes){env->DeleteLocalRef(value);failed=true;break;}std::snprintf(next[i].data(),512,"%s",bytes);env->ReleaseStringUTFChars(value,bytes);env->DeleteLocalRef(value);}
  env->DeleteLocalRef(array);if(failed)break;
  publish(next);online.store(true,std::memory_order_release);
  launch=std::strcmp(next[10].data(),"LAUNCH")==0;
  if(!launch)(void)sceKernelUsleep(16000);
 }
 exit_requested.store(true,std::memory_order_release);
 while(!display_done.load(std::memory_order_acquire))(void)sceKernelUsleep(1000);
 pthread_join(ui_thread,nullptr);
 return display_ok.load(std::memory_order_acquire)&&launch&&!failed&&!env->ExceptionCheck();
}
}
