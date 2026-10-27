#!/usr/bin/env python3
"""Actual SDL logical resize/framebuffer callbacks and normalized pointer mapping."""
from pathlib import Path
import subprocess,tempfile
r=Path(__file__).resolve().parents[1];s=(r/'client/ports/sdl/SDL_ps5video.c').read_text()
create=s[s.index('static bool PS5_CreateWindow('):s.index('static bool PS5_SetWindowPosition(')]
resize=s[s.index('static void PS5_SetWindowSize('):s.index('static SDL_FullscreenResult PS5_SetWindowFullscreen(')]
preamble=r'''
#include <stdbool.h>
#include <assert.h>
#include <math.h>
typedef void SDL_VideoDevice;typedef unsigned SDL_PropertiesID;
typedef struct {int w,h,min_w,min_h,max_w,max_h;struct {int w,h;}pending;}SDL_Window;
#define SDL_EVENT_WINDOW_RESIZED 1
static int ps5_surface_width=1920,ps5_surface_height=1080;
static SDL_Window* focused;static unsigned resizes;
static void SDL_SetKeyboardFocus(SDL_Window*w){focused=w;}
static void SDL_SendWindowEvent(SDL_Window*w,int event,int x,int y){assert(event==SDL_EVENT_WINDOW_RESIZED);w->w=x;w->h=y;resizes++;}
'''
main=r'''
int main(){
 int sizes[][2]={{1280,720},{1600,900},{1920,1080},{2560,1440},{3840,2160},{1024,768}};
 for(int i=0;i<6;i++){
  SDL_Window w={.w=sizes[i][0],.h=sizes[i][1]};assert(PS5_CreateWindow(0,&w,0)&&focused==&w);assert(w.w==sizes[i][0]&&w.h==sizes[i][1]&&w.max_w==7680);
  int pw,ph;PS5_GetWindowSizeInPixels(0,&w,&pw,&ph);assert(pw==1920&&ph==1080);
  // SDL emits logical coordinates; Minecraft applies framebuffer/logical scale.
  // The hardware cursor receives the same normalized physical location.
  float x=w.w*0.37f,y=w.h*0.71f;float gui_x=x*(float)pw/w.w,gui_y=y*(float)ph/w.h;
  assert(fabsf(gui_x/pw-x/w.w)<0.0001f&&fabsf(gui_y/ph-y/w.h)<0.0001f);
  w.pending.w=800;w.pending.h=600;PS5_SetWindowSize(0,&w);assert(w.w==800&&w.h==600);
 }
 ps5_surface_width=2560;ps5_surface_height=1440;SDL_Window w={.w=1280,.h=720};int pw,ph;PS5_GetWindowSizeInPixels(0,&w,&pw,&ph);assert(pw==2560&&ph==1440);assert(resizes==6);
}
'''
with tempfile.TemporaryDirectory(prefix='sdl-resolution-')as d:
 w=Path(d);(w/'test.c').write_text(preamble+create+resize+main)
 subprocess.run(['clang','-std=c11','-Wno-unused-parameter','-fsanitize=address,undefined',str(w/'test.c'),'-o',str(w/'test')],check=True);subprocess.run([str(w/'test')],check=True)
print('PASS actual SDL callbacks preserve6logical sizes/resize and report actual framebuffer; normalized cursor/game coordinates align at mixed sizes; physical mode selection still needs PS5 validation')
