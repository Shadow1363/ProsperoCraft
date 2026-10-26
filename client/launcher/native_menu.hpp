/* SPDX-License-Identifier: GPL-3.0-or-later */
#pragma once
#include "demo_renderer.hpp"
#include <array>
#include <cstdio>
#include <cstdlib>
#include <cstring>
namespace prospero_menu {
using ps5::demo::Canvas;
constexpr std::uint32_t ink(std::uint32_t rgb){return 0xff000000u|((rgb&255)<<16)|(rgb&0xff00)|((rgb>>16)&255);}
inline JNIEnv* env=nullptr;inline jclass owner=nullptr;inline jmethodID tick=nullptr;
inline int controller=-1;inline std::uint32_t previous=0;inline bool armed=false,finished=false,failed=false;
inline std::array<std::array<char,512>,12> fields{};
inline void label(Canvas& c,int x,int y,const char* text,unsigned size=24,std::uint32_t rgb=0xeaf0e8){c.label(x,y,text,size,ink(rgb));}
inline void wrap(Canvas& c,int x,int y,std::string_view text,unsigned width,int lines=3){
 while(!text.empty()&&lines-->0){std::size_t n=text.size();while(n>0&&Canvas::text_width(text.substr(0,n),24)>width)--n;if(!n)break;
  if(n<text.size()){auto space=text.substr(0,n).find_last_of(' ');if(space!=std::string_view::npos&&space>0)n=space;}
  c.label(x,y,text.substr(0,n),24,ink(0xaac0b6));text.remove_prefix(n);while(!text.empty()&&text.front()==' ')text.remove_prefix(1);y+=34;
 }
}
inline void card(Canvas& c,int x,int y,unsigned w,unsigned h,bool focus=false){c.rounded(x,y,w,h,24,ink(focus?0xa9eab6:0x294138));c.rounded(x+2,y+2,w-4,h-4,22,ink(0x13271f));}
inline void draw(Canvas& c) noexcept {
 c.gradient(ink(0x0b1b17),ink(0x07120f));
 c.disc(1570,260,230,ink(0x102b24));c.disc(1650,200,150,ink(0x16352a));
 c.rounded(40,42,344,996,32,ink(0x10221c));
 c.rounded(75,78,58,58,14,ink(0xa5dfb5));label(c,91,87,"P",42,0x153525);
 label(c,148,87,"ProsperoCraft",30);label(c,79,164,"MAKE ROOM TO EXPLORE",24,0x87a795);
 const int selected=std::atoi(fields[9].data()),page=std::atoi(fields[11].data());
 const char* nav[]={"Home","Instances","Account","Settings"};
 for(int i=0;i<4;++i){int y=265+i*88;if(selected==i)c.rounded(65,y-12,292,68,16,ink(0x244e38));c.disc(93,y+13,5,ink(selected==i?0xb5f0b8:0x5d7e6b));label(c,119,y,nav[i],30,selected==i?0xe8ffe7:0xa1b7a9);}
 label(c,79,867,"JAVA EDITION",24,0x9fbaa8);label(c,79,911,"Native on PlayStation 5",24,0xd5e5d8);label(c,79,959,"ProsperoCraft 075",24,0x6d8f7b);
 label(c,440,78,"YOUR LIBRARY",24,0x99b7a5);c.rounded(1580,65,260,53,26,ink(0x244332));label(c,1605,78,"NATIVE JAVA 25",24,0xaee9b9);
 card(c,440,160,920,690,selected==0);
 label(c,485,200,page==1?"YOUR INSTANCES":page==3?"YOUR SETUP":"A WORLD OF POSSIBILITIES",24,0x9ccd9f);
 label(c,485,255,page==1?"Vanilla. Ready to go.":page==3?"Built for your PS5.":fields[0].data(),64);
 label(c,485,339,page==3?"Your game. Your settings.":fields[1].data(),42,0xaad8b4);
 if(page==3){wrap(c,485,430,"Optimized performance profile. Your existing in-game video and audio settings stay yours.",770,3);wrap(c,485,570,"Controller navigation is ready. More launcher settings and instance options will follow.",770,3);}
 else{
  // Procedural voxel landscape: native vectors, no downloaded game artwork.
  for(int row=0;row<5;++row)for(int col=0;col<17;++col){int height=(col*7+row*3)%5;int x=486+col*47,y=552+row*34-height*9;c.rounded(x,y,45,48,3,ink(row<2?0x254d3a:0x193e30));if(row==0)c.rounded(x,y,45,10,3,ink(col%3?0x80ba80:0xa1d495));}
  c.rounded(485,424,823,89,18,ink(0x1c3a2b));c.rounded(502,440,52,52,8,ink(0x89b98b));label(c,574,437,"Vanilla 26.3",30);label(c,574,476,"Java Edition / Installed",24,0x98b49f);label(c,1145,452,"READY",24,0xa9e6b3);
 }
 c.rounded(483,745,414,70,17,ink(selected==0?0xb6f2be:0x9edca9));label(c,508,763,fields[6].data(),30,0x102c1b);
 c.rounded(922,745,388,70,17,ink(selected==4?0x507b58:0x254534));label(c,967,765,"TRY THE DEMO",30,0xd3e5d4);
 card(c,1390,160,450,690,selected==2);
 // Familiar Microsoft four-square mark, with device-code sign-in on another device.
 c.rectangle(1430,202,17,17,static_cast<ps5::demo::Color>(ink(0xf35325)));c.rectangle(1450,202,17,17,static_cast<ps5::demo::Color>(ink(0x81bc06)));c.rectangle(1430,222,17,17,static_cast<ps5::demo::Color>(ink(0x05a6f0)));c.rectangle(1450,222,17,17,static_cast<ps5::demo::Color>(ink(0xffba08)));
 label(c,1482,208,"MICROSOFT",24,0xdce8df);label(c,1430,280,"Your account",42);label(c,1430,344,fields[5].data(),30,0xb6e4bf);
 if(fields[3][0]){label(c,1430,420,"Enter this code",24,0xa9bfad);label(c,1430,469,fields[3].data(),42,0xd5ffd7);wrap(c,1430,543,fields[4].data(),370,3);}
 else wrap(c,1430,420,"Sign in securely on your phone or computer. No password to type on your controller.",365,4);
 wrap(c,1430,667,fields[2].data(),365,4);
 c.disc(1440,806,5,ink(0xa9d9ab));label(c,1460,792,fields[8].data(),24,0x91b49a);
 card(c,440,880,1400,158);label(c,480,909,"D-PAD  Navigate     X  Select     CIRCLE  Back",24,0xdae8dc);label(c,480,966,fields[7].data(),24,0x88ab95);
}
inline bool update() noexcept {
 if(failed||finished)return false;
 std::uint32_t pressed=0;PadSample batch[64]{};const int count=scePadRead(controller,batch,64);
 if(count>=0&&count<=64)for(int i=0;i<count;++i){auto buttons=batch[i].connected&&!(batch[i].buttons&0x80000000u)?batch[i].buttons:0u;if(!(buttons&0x4000))armed=true;if(armed)pressed|=buttons&~previous;previous=buttons;}
 auto array=static_cast<jobjectArray>(env->CallStaticObjectMethod(owner,tick,static_cast<jint>(pressed)));
 if(env->ExceptionCheck()||!array){failed=true;return false;}
 bool changed=false;if(env->GetArrayLength(array)!=12){env->DeleteLocalRef(array);failed=true;return false;}
 for(int i=0;i<12;++i){auto value=static_cast<jstring>(env->GetObjectArrayElement(array,i));if(!value){failed=true;break;}const char* bytes=env->GetStringUTFChars(value,nullptr);if(!bytes){env->DeleteLocalRef(value);failed=true;break;}if(std::strcmp(fields[i].data(),bytes)!=0){std::snprintf(fields[i].data(),fields[i].size(),"%s",bytes);changed=true;}env->ReleaseStringUTFChars(value,bytes);env->DeleteLocalRef(value);}
 env->DeleteLocalRef(array);if(std::strcmp(fields[10].data(),"LAUNCH")==0)finished=true;
 return changed;
}
inline bool stop() noexcept{return finished||failed;}
inline jboolean menu(JNIEnv* current,jclass klass){
 env=current;owner=klass;tick=env->GetStaticMethodID(klass,"launcherTick","(I)[Ljava/lang/String;");if(!tick)return false;
 std::int32_t user=-1;if(sceUserServiceGetInitialUser(&user)<0)return false;controller=scePadOpen(user,0,0,nullptr);if(controller<0)return false;
 previous=0;armed=false;finished=false;failed=false;fields={};
 const bool closed=ps5::demo::run_ui_until(draw,update,stop,"ProsperoCraft launcher ready");
 scePadClose(controller);controller=-1;return closed&&finished&&!failed&&!env->ExceptionCheck();
}
}
