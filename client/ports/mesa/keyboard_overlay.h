/* SPDX-License-Identifier: MIT
 * CPU keyboard composition after the presentation fence, before the owned flip.
 * Tile addressing matches the existing PS5 VideoOut framebuffer layout.
 * Font rows are the original cursor font from0006; no game assets are copied. */
#ifndef PROSPERO_KEYBOARD_OVERLAY_H
#define PROSPERO_KEYBOARD_OVERLAY_H
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "keyboard_layout.h"
struct prospero_keyboard {bool visible;int selected,lower,symbols;char preview[129];};
static struct prospero_keyboard prospero_keyboard_state;
static size_t prospero_keyboard_offset(unsigned width,unsigned x,unsigned y)
{
 uint32_t offset=((y<<4)&0x70u)^((y<<5)&0xf00u)^((y<<9)&0x1000u)^((y<<8)&0x4000u)^((x<<2)&0xcu)^((x<<5)&0x380u)^((x<<4)&0x400u)^((x<<6)&0x800u)^((x<<9)&0xa000u);
 return ((size_t)((y>>7)*((width+127u)>>7)+(x>>7))<<16)+offset;
}
struct prospero_keyboard_canvas {uint8_t*data;unsigned width,height;};
static void prospero_keyboard_rect(struct prospero_keyboard_canvas*c,int x,int y,int w,int h,uint32_t color)
{
 int x0=x*(int)c->width/1920,y0=y*(int)c->height/1080,x1=(x+w)*(int)c->width/1920,y1=(y+h)*(int)c->height/1080;
 if(x0<0)x0=0;if(y0<0)y0=0;if(x1>(int)c->width)x1=(int)c->width;if(y1>(int)c->height)y1=(int)c->height;
 for(int py=y0;py<y1;py++)for(int px=x0;px<x1;px++)*(uint32_t*)(c->data+prospero_keyboard_offset(c->width,(unsigned)px,(unsigned)py))=color;
}
static void prospero_keyboard_text(struct prospero_keyboard_canvas*c,int x,int y,const char*text,int scale,uint32_t color,int limit)
{
 static const uint8_t glyphs[][7] = {
          {14,17,17,31,17,17,17},{30,17,17,30,17,17,30},{14,17,16,16,16,17,14},
          {30,17,17,17,17,17,30},{31,16,16,30,16,16,31},{31,16,16,30,16,16,16},
          {14,17,16,23,17,17,14},{17,17,17,31,17,17,17},{14,4,4,4,4,4,14},
          {7,2,2,2,18,18,12},{17,18,20,24,20,18,17},{16,16,16,16,16,16,31},
          {17,27,21,21,17,17,17},{17,25,21,19,17,17,17},{14,17,17,17,17,17,14},
          {30,17,17,30,16,16,16},{14,17,17,17,21,18,13},{30,17,17,30,20,18,17},
          {15,16,16,14,1,1,30},{31,4,4,4,4,4,4},{17,17,17,17,17,17,14},
          {17,17,17,17,17,10,4},{17,17,17,21,21,21,10},{17,17,10,4,10,17,17},
          {17,17,10,4,4,4,4},{31,1,2,4,8,16,31},
          {14,17,19,21,25,17,14},{4,12,4,4,4,4,14},{14,17,1,2,4,8,31},
          {30,1,1,14,1,1,30},{2,6,10,18,31,2,2},{31,16,16,30,1,1,30},
          {14,16,16,30,17,17,14},{31,1,2,4,8,8,8},{14,17,17,14,17,17,14},
          {14,17,17,15,1,1,14},{0,0,0,0,0,0,0},{0,0,0,0,0,12,12},
          {0,0,0,0,0,0,31},{0,0,0,31,0,0,0},{1,2,2,4,8,8,16},
          {0,12,12,0,12,12,0},{4,4,4,4,4,0,4},{14,17,1,2,4,0,4},
          {14,17,23,21,23,16,14},{2,4,8,8,8,4,2},{8,4,2,2,2,4,8},
          {0,4,4,31,4,4,0},{0,31,0,31,0,0,0}};
 const char*alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ._-/:!?@()+=";
 static const char extra_chars[]=";#${}[]<>\\|~`%^&*\"',";
 static const uint8_t extra[][7]={
 {0,4,4,0,4,4,8},{10,31,10,10,31,10,0},{4,15,20,14,5,30,4},{2,4,4,8,4,4,2},{8,4,4,2,4,4,8},
 {14,8,8,8,8,8,14},{14,2,2,2,2,2,14},{2,4,8,16,8,4,2},{8,4,2,1,2,4,8},{16,8,8,4,2,2,1},
 {4,4,4,4,4,4,4},{0,0,9,22,0,0,0},{8,4,2,0,0,0,0},{17,2,4,8,17,0,0},{4,10,17,0,0,0,0},
 {12,18,20,8,21,18,13},{0,21,14,31,14,21,0},{10,10,0,0,0,0,0},{4,4,0,0,0,0,0},{0,0,0,0,4,4,8}};
 static const uint8_t small[][7]={
 {0,0,14,1,15,17,15},{16,16,30,17,17,17,30},{0,0,14,16,16,17,14},{1,1,15,17,17,17,15},
 {0,0,14,17,31,16,14},{6,9,8,28,8,8,8},{0,15,17,17,15,1,14},{16,16,30,17,17,17,17},
 {4,0,12,4,4,4,14},{2,0,6,2,2,18,12},{16,16,18,20,24,20,18},{12,4,4,4,4,4,14},
 {0,0,26,21,21,21,21},{0,0,30,17,17,17,17},{0,0,14,17,17,17,14},{0,0,30,17,30,16,16},
 {0,0,15,17,15,1,1},{0,0,22,25,16,16,16},{0,0,15,16,14,1,30},{8,8,28,8,8,9,6},
 {0,0,17,17,17,19,13},{0,0,17,17,17,10,4},{0,0,17,17,21,21,10},{0,0,17,10,4,10,17},
 {0,0,17,17,15,1,14},{0,0,31,2,4,8,31}};
 for(int n=0;text[n]&&n<limit;n++){
  int ch=(unsigned char)text[n];const char*found=strchr(alphabet,ch);int index=found?(int)(found-alphabet):42;const char*other=strchr(extra_chars,ch);const uint8_t*rows=ch>='a'&&ch<='z'?small[ch-'a']:other?extra[(int)(other-extra_chars)]:glyphs[index];
  for(int row=0;row<7;row++)for(int col=0;col<5;col++)if(rows[row]&(16>>col))prospero_keyboard_rect(c,x+n*6*scale+col*scale,y+row*scale,scale,scale,color);
 }
}
static void prospero_keyboard_draw(uint8_t*data,unsigned width,unsigned height)
{
 const struct prospero_keyboard*k=&prospero_keyboard_state;
 if(!k->visible||!data||width<320||height<240||width>7680||height>4320)return;
 struct prospero_keyboard_canvas canvas={data,width,height},*c=&canvas;
 prospero_keyboard_rect(c,280,450,1360,590,0xff13271f);
 prospero_keyboard_rect(c,300,468,1320,3,0xffa9eab6);
 prospero_keyboard_text(c,320,488,"TEXT INPUT",4,0xffeaf0e8,40);
 prospero_keyboard_text(c,800,493,k->symbols?"SYMBOLS":k->lower?"LOWERCASE":"UPPERCASE",3,0xffa9eab6,30);
 prospero_keyboard_rect(c,320,533,1280,45,0xff081a13);
 size_t len=strlen(k->preview);const char*preview=k->preview+(len>96?len-96:0);
 prospero_keyboard_text(c,334,546,*preview?preview:"TYPE INTO THE SELECTED GAME FIELD",2,0xffd6e6d9,100);
 for(int i=0;i<50;i++){
  int x=320+(i%10)*128,y=592+(i/10)*66;bool active=k->selected==i;
  prospero_keyboard_rect(c,x,y,116,56,active?0xffb6f2be:0xff244438);
  char label[2]={prospero_keyboard_character(i,k->lower,k->symbols),0};if(label[0]==' ')label[0]='_';
  prospero_keyboard_text(c,x+44,y+13,label,4,active?0xff102c1b:0xffeaf0e8,1);
 }
 const char*actions[]={"DELETE","SPACE","CASE","SYMBOLS","ENTER","CLOSE"};
 for(int i=0;i<6;i++){int x=320+i*214;bool active=k->selected==50+i;prospero_keyboard_rect(c,x,930,202,48,active?0xffb6f2be:0xff244438);prospero_keyboard_text(c,x+18,944,actions[i],3,active?0xff102c1b:0xffeaf0e8,9);}
 prospero_keyboard_text(c,320,998,"X TYPE / L1 DELETE / R1 SPACE / R2 CASE / L2 SYMBOLS / OPTIONS ENTER / CIRCLE CLOSE",2,0xffa9c6b2,106);
 /* Flush only touched128x128tiles; no new output, buffer or GPU resource. */
#ifdef __PROSPERO__
 unsigned x0=280*width/1920/128,x1=((1640*width/1920)+127)/128,y0=450*height/1080/128,y1=((1040*height/1080)+127)/128;
 unsigned stride=(width+127)/128;for(unsigned ty=y0;ty<y1;ty++)for(unsigned tx=x0;tx<x1;tx++){uint8_t*tile=data+((size_t)ty*stride+tx)*65536;for(unsigned at=0;at<65536;at+=64)_mm_clflush(tile+at);}_mm_mfence();
#endif
}
#endif
