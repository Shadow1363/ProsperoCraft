#!/usr/bin/env python3
"""Actual SDL relative-mode transitions with PS5 software callback and host fixtures."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
mouse=(ROOT/'build/sdl-src/src/events/SDL_mouse.c').read_text()
video=(ROOT/'build/sdl-src/src/video/SDL_video.c').read_text()
def function(text,start):
 a=text.index(start);b=text.index('\n}',a)+2;return text[a:b]
setmode=function(mouse,'bool SDL_SetRelativeMouseMode(bool enabled)')
update=function(mouse,'bool SDL_UpdateRelativeMouseMode(void)')
windowmode=function(video,'bool SDL_SetWindowRelativeMouseMode(SDL_Window *window, bool enabled)')
code=r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
typedef struct SDL_Window {unsigned flags;} SDL_Window;
typedef struct SDL_Mouse {bool relative_mode,warp_emulation_active;float x,y;bool(*SetRelativeMouseMode)(bool);} SDL_Mouse;
static SDL_Mouse mouse;
static SDL_Window main_window,*focus;
static int redraws,warps,flushes;
#define SDL_WINDOW_MOUSE_RELATIVE_MODE 1u
#define SDL_EVENT_MOUSE_MOTION 0x400
#define CHECK_WINDOW_MAGIC(w,v) do{if(!(w))return (v);}while(0)
static SDL_Mouse *SDL_GetMouse(void){return &mouse;}
static SDL_Window *SDL_GetKeyboardFocus(void){return focus;}
static bool SDL_Unsupported(void){return false;}
static void SDL_RedrawCursor(void){++redraws;}
static void SDL_SetMouseFocus(SDL_Window*w){assert(w==&main_window);}
static void SDL_UpdateWindowGrab(SDL_Window*w){assert(w==&main_window);}
static bool SDL_UpdateMouseCapture(bool b){return true;}
static void SDL_PerformWarpMouseInWindow(SDL_Window*w,float x,float y,bool b){++warps;}
static void SDL_FlushEvent(int e){assert(e==SDL_EVENT_MOUSE_MOTION);++flushes;}
static void SDL_DisableMouseWarpEmulation(void){}
static bool SDL_GetWindowRelativeMouseMode(SDL_Window*w){return (w->flags&SDL_WINDOW_MOUSE_RELATIVE_MODE)!=0;}
static void SDL_Log(const char*f,const char*s){assert(f&&s);}
#include "ps5_relative_mouse.h"
'''
tail=r'''
int main(void){
 focus=&main_window;
 // Reproduce065: callback absent -> actual SDL rolls the window flag back.
 assert(!SDL_SetWindowRelativeMouseMode(focus,true));assert(!mouse.relative_mode&&!SDL_GetWindowRelativeMouseMode(focus));
 mouse.SetRelativeMouseMode=PS5_SetRelativeMouseMode;
 assert(SDL_SetWindowRelativeMouseMode(focus,true));assert(mouse.relative_mode&&SDL_GetWindowRelativeMouseMode(focus));
 int before=flushes;assert(SDL_SetWindowRelativeMouseMode(focus,true)&&flushes==before);
 focus=NULL;assert(SDL_UpdateRelativeMouseMode()&&!mouse.relative_mode);
 focus=&main_window;assert(SDL_UpdateRelativeMouseMode()&&mouse.relative_mode);
 assert(SDL_SetWindowRelativeMouseMode(focus,false));assert(!mouse.relative_mode&&!SDL_GetWindowRelativeMouseMode(focus));
 assert(redraws&&warps&&flushes);
 puts("PASS actual SDL window/global relative-mode path:065missing-callback failure reproduced,PS5callback enables retained capture,focus loss/reacquire,menu release/idempotence;ASan/UBSan fixtures,PS5movement pending");
}
'''
with tempfile.TemporaryDirectory(prefix='ps5-relative-mouse-')as folder:
 p=Path(folder);(p/'test.c').write_text(code+setmode+'\n'+update+'\n'+windowmode+'\n'+tail)
 subprocess.run(['clang','-std=c11','-fsanitize=address,undefined','-I'+str(ROOT/'client/ports/sdl'),str(p/'test.c'),'-o',str(p/'check')],check=True)
 subprocess.run([str(p/'check')],check=True)
