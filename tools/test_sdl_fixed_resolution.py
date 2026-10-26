#!/usr/bin/env python3
"""Exercise actual PS5 SDL window callbacks: logical/input and surface are1080p."""
from pathlib import Path
import subprocess,tempfile
r=Path(__file__).resolve().parents[1];s=(r/'client/ports/sdl/SDL_ps5video.c').read_text()
create=s[s.index('static bool PS5_CreateWindow('):s.index('static bool PS5_SetWindowPosition(')]
resize=s[s.index('static void PS5_SetWindowSize('):s.index('static SDL_FullscreenResult PS5_SetWindowFullscreen(')]
preamble=r'''
#include <stdbool.h>
#include <assert.h>
typedef void SDL_VideoDevice;typedef unsigned SDL_PropertiesID;
typedef struct {int w,h,min_w,min_h,max_w,max_h;}SDL_Window;
#define SDL_EVENT_WINDOW_RESIZED 1
static SDL_Window* focused;static unsigned resizes;
static void SDL_SetKeyboardFocus(SDL_Window*w){focused=w;}
static void SDL_SendWindowEvent(SDL_Window*w,int event,int x,int y){assert(event==SDL_EVENT_WINDOW_RESIZED);w->w=x;w->h=y;resizes++;}
'''
main=r'''
int main(){
 for(int old=0;old<3;old++){
  SDL_Window w={.w=old==0?1280:old==1?1600:1920,.h=old==0?720:old==1?900:1080};
  assert(PS5_CreateWindow(0,&w,0)&&focused==&w);
  assert(w.w==1920&&w.h==1080&&w.min_w==1920&&w.max_w==1920&&w.min_h==1080&&w.max_h==1080);
  w.w=640;w.h=480;PS5_SetWindowSize(0,&w);assert(w.w==1920&&w.h==1080);
 }
 assert(resizes==6);
}
'''
with tempfile.TemporaryDirectory(prefix='sdl1080-')as d:
 w=Path(d);(w/'test.c').write_text(preamble+create+resize+main)
 subprocess.run(['clang','-std=c11','-Wno-unused-parameter','-fsanitize=address,undefined',str(w/'test.c'),'-o',str(w/'test')],check=True)
 subprocess.run([str(w/'test')],check=True)
print('PASS actual SDL create/resize callbacks force1920x1080logical/input coordinates and matching min/max bounds from720p/900p/1080p requests')
