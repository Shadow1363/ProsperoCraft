/* SPDX-License-Identifier: GPL-3.0-or-later */
#pragma once
#include <cstdint>
namespace prospero_menu {
// Pure input policy shared by the actual frontend and deterministic host tests.
struct Navigation {
 bool actions_armed=false,nav_armed=false;
 unsigned previous=0,stick=0,held=0;std::uint64_t repeat_at=0,last_sample=0;
 void clear(){*this={};}
 static unsigned axis(int x,int y,int threshold){
  int ax=x<0?-x:x,ay=y<0?-y:y;
  if(ax<threshold&&ay<threshold)return 0;
  return ax>=ay?(x<0?0x80:0x20):(y<0?0x10:0x40);
 }
 unsigned sample(unsigned buttons,int lx,int ly,bool connected,std::uint64_t now){
  if(!connected||(buttons&0x80000000u)){clear();return 0;}
  last_sample=now;int x=lx-128,y=ly-128;
  if(!actions_armed&&!(buttons&0xff0fu))actions_armed=true;
  if(!nav_armed&&!(buttons&0xf0u)&&!axis(x,y,29))nav_armed=true;
  // Schmitt trigger: engage at56, release at28. Diagonal noise cannot change
  // the held axis until that axis releases. Reversal rearms through neutral.
  bool retained=(stick==0x80&&x<-28)||(stick==0x20&&x>28)||(stick==0x10&&y<-28)||(stick==0x40&&y>28);
  if(!retained)stick=axis(x,y,56);
  unsigned dpad=buttons&0xf0u;
  if((dpad&0xa0)==0xa0)dpad&=~0xa0u;if((dpad&0x50)==0x50)dpad&=~0x50u;
  if(dpad&0xa0)dpad&=0xa0u; // one direction per sample; D-pad takes precedence
  unsigned direction=nav_armed?(dpad?dpad:stick):0;
  unsigned edges=actions_armed?buttons&~previous&~0xf0u:0;previous=buttons;
  if(direction!=held){held=direction;repeat_at=now+400;edges|=direction;}
  return edges;
 }
 unsigned repeat(std::uint64_t now){
  if(now-last_sample>250){clear();return 0;} // no stale held input after read loss
  if(held&&now>=repeat_at){repeat_at=now+100;return held;}return 0;
 }
};
}
