#!/usr/bin/env python3
"""Exercise actual temporary input adapter with deterministic SDL/OS boundaries."""
from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
source=r'''
#include <SDL3/SDL.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "platform.h"
static SDL_Window *window=(SDL_Window*)(uintptr_t)1,*focus;
static bool enabled,captured,mod;
static Uint64 tick=1;
static int opens,events,downs,ups,motions;
static bool keys[SDL_SCANCODE_COUNT],mouse[4];
static float motion_x;
static struct pad_reading samples[64];static int count=1;static uint32_t players=1;
Uint64 SDL_GetTicksNS(void){return tick;}
SDL_Window *SDL_GetKeyboardFocus(void){return focus;}
bool SDL_GetHintBoolean(const char *name,bool fallback){assert(!strcmp(name,"PS5_TEMPORARY_CONTROLS")&&!fallback);return enabled;}
SDL_InitFlags SDL_WasInit(SDL_InitFlags flags){assert(flags==SDL_INIT_GAMEPAD);return mod?SDL_INIT_GAMEPAD:0;}
bool SDL_GetWindowRelativeMouseMode(SDL_Window*w){assert(w==window);return captured;}
Uint32 SDL_GetNextObjectID(void){static Uint32 id;return ++id;}
void SDL_AddKeyboard(SDL_KeyboardID id,const char*name){assert(id&&name);}
void SDL_AddMouse(SDL_MouseID id,const char*name){assert(id&&name);}
bool SDL_SendKeyboardKey(Uint64 time,SDL_KeyboardID id,int raw,SDL_Scancode key,bool down){assert(time==tick&&id&&raw==0);keys[key]=down;events++;if(down)downs++;else ups++;return true;}
void SDL_SendMouseButton(Uint64 time,SDL_Window*w,SDL_MouseID id,Uint8 b,bool down){assert(time==tick&&id);mouse[b]=down;events++;}
void SDL_SendMouseMotion(Uint64 time,SDL_Window*w,SDL_MouseID id,bool relative,float x,float y){assert(time==tick&&id&&relative&&isfinite(x)&&isfinite(y));motion_x=x;motions++;}
bool pad_open(void){opens++;return true;}
void pad_poll(struct pad*p){memset(p,0,sizeof(*p));}
uint32_t pad_players(void){return players;}
int pad_readings(const struct pad_reading**p){*p=samples;return count;}
#include "ps5_temporary_input.h"
static void sample(uint32_t buttons){samples[0]=(struct pad_reading){.buttons=buttons,.left_x=128,.left_y=128,.right_x=128,.right_y=128,.connected=true};count=1;}
static void pump(void){tick+=16000000;PS5_PumpTemporaryInput(window);}
int main(void){
 focus=window;sample(0);pump();assert(!opens&&!events);
 enabled=true;sample(PAD_CROSS);pump();assert(opens==1&&!events); /* no launch-held activation */
 sample(0);pump();sample(PAD_CROSS);pump();assert(keys[SDL_SCANCODE_RETURN]);int prior=events;
 tick+=500000000;pump();assert(events==prior); /* no repeated confirmation */
 sample(0);pump();assert(!keys[SDL_SCANCODE_RETURN]);
 sample(PAD_CROSS);samples[1]=samples[0];samples[1].buttons=0;count=2;prior=events;pump();assert(events==prior+2&&!keys[SDL_SCANCODE_RETURN]);
 sample(PAD_DOWN);pump();assert(keys[SDL_SCANCODE_DOWN]);prior=downs;tick+=400000000;pump();assert(downs==prior+1);sample(0);pump();assert(!keys[SDL_SCANCODE_DOWN]);
 sample(0);samples[0].left_x=255;pump();assert(keys[SDL_SCANCODE_RIGHT]);
 captured=true;sample(PAD_CROSS|PAD_TRIANGLE);samples[0].left_x=255;samples[0].right_x=255;samples[0].r2=255;pump();
 assert(!keys[SDL_SCANCODE_RIGHT]&&keys[SDL_SCANCODE_D]&&keys[SDL_SCANCODE_SPACE]&&keys[SDL_SCANCODE_E]&&mouse[SDL_BUTTON_LEFT]);
 tick+=2000000000;pump();assert(motions&&motion_x<=32.51f); /* bounded after stall */
 sample(PAD_INTERCEPTED);pump();assert(!keys[SDL_SCANCODE_D]&&!keys[SDL_SCANCODE_SPACE]&&!mouse[SDL_BUTTON_LEFT]);
 sample(PAD_CROSS);pump();assert(!keys[SDL_SCANCODE_SPACE]);sample(0);pump();sample(PAD_CROSS);pump();assert(keys[SDL_SCANCODE_SPACE]);
 players=0;count=0;pump();assert(!keys[SDL_SCANCODE_SPACE]);players=1;
 sample(0);captured=false;pump();sample(PAD_CIRCLE);pump();assert(keys[SDL_SCANCODE_ESCAPE]);
 mod=true;pump();assert(!keys[SDL_SCANCODE_ESCAPE]);prior=events;pump();assert(events==prior);mod=false;
 sample(0);pump();sample(PAD_UP);pump();assert(keys[SDL_SCANCODE_UP]);focus=NULL;pump();assert(!keys[SDL_SCANCODE_UP]);focus=window;
 enabled=false;prior=events;pump();assert(events==prior);
 puts("PASS actual PS5 temporary SDL adapter under ASan/UBSan:opt-in,launch-held suppression,buffered tap,menu navigation/repeat,mode mapping,trigger releases,capped look,interception/disconnect/focus release,gamepad-mod handoff,no idle keepalive;SDL/OS boundaries are host fixtures,console pending");
}
'''
with tempfile.TemporaryDirectory(prefix='ps5-temporary-input-')as folder:
    p=Path(folder);(p/'test.c').write_text(source)
    subprocess.run(['clang','-std=c11','-fsanitize=address,undefined','-I/opt/homebrew/include','-I'+str(ROOT/'client/ports/sdl'),str(p/'test.c'),'-o',str(p/'test')],check=True)
    subprocess.run([str(p/'test')],check=True)
