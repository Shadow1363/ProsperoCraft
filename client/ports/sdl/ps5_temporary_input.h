/* Temporary vanilla controls through normal SDL keyboard/mouse events and state.
 * SPDX-License-Identifier: MIT
 * Included after SDL keyboard/mouse internals. No game hooks or replacements. */
#include "platform.h"
static struct {
    SDL_KeyboardID keyboard;
    SDL_MouseID mouse;
    Uint32 keys, blocked;
    Uint8 buttons;
    Uint64 repeat_at[14], last_pump;
    bool primed, devices;
} ps5_temp;
static const SDL_Scancode ps5_temp_keys[] = {
    SDL_SCANCODE_UP, SDL_SCANCODE_DOWN, SDL_SCANCODE_LEFT, SDL_SCANCODE_RIGHT,
    SDL_SCANCODE_RETURN, SDL_SCANCODE_ESCAPE, SDL_SCANCODE_TAB, SDL_SCANCODE_BACKSPACE,
    SDL_SCANCODE_W, SDL_SCANCODE_S, SDL_SCANCODE_A, SDL_SCANCODE_D,
    SDL_SCANCODE_SPACE, SDL_SCANCODE_E
};
static void PS5_TempKeys(Uint64 now, Uint32 keys, Uint8 buttons, SDL_Window *window)
{
    for(int i=0;i<14;++i) {
        Uint32 bit=1u<<i;
        if((keys ^ ps5_temp.keys)&bit) {
            SDL_SendKeyboardKey(now,ps5_temp.keyboard,0,ps5_temp_keys[i],(keys&bit)!=0);
            ps5_temp.repeat_at[i]=now+350000000ull;
        }
    }
    for(int i=0;i<2;++i)if((buttons ^ ps5_temp.buttons)&(1u<<i))
        SDL_SendMouseButton(now,window,ps5_temp.mouse,(Uint8)(i?SDL_BUTTON_RIGHT:SDL_BUTTON_LEFT),(buttons&(1u<<i))!=0);
    ps5_temp.keys=keys;ps5_temp.buttons=buttons;
}
static void PS5_TempRelease(SDL_Window *window, Uint64 now)
{
    PS5_TempKeys(now,0,0,window);
    ps5_temp.primed=false;ps5_temp.last_pump=0;
}
static void PS5_PumpTemporaryInput(SDL_Window *window)
{
    Uint64 now=SDL_GetTicksNS();
    /* Explicit opt-in, with automatic handoff when a mod initializes gamepads.
     * Future Controlify integration must also turn this hint off explicitly. */
    if(!window || SDL_GetKeyboardFocus()!=window ||
       !SDL_GetHintBoolean("PS5_TEMPORARY_CONTROLS",false) || SDL_WasInit(SDL_INIT_GAMEPAD)) {
        PS5_TempRelease(window,now);return;
    }
    if(!ps5_temp.devices) {
        ps5_temp.keyboard=SDL_GetNextObjectID();ps5_temp.mouse=SDL_GetNextObjectID();
        SDL_AddKeyboard(ps5_temp.keyboard,"PS5 temporary controller keys");
        SDL_AddMouse(ps5_temp.mouse,"PS5 temporary controller mouse");
        ps5_temp.devices=true;(void)pad_open();
    }
    struct pad state;pad_poll(&state);
    const struct pad_reading *readings=NULL,*last=NULL;
    int count=pad_readings(&readings);
    bool captured=SDL_GetWindowRelativeMouseMode(window);
    /* Buffered edges retain taps shorter than one rendered frame. */
    for(int n=0;n<count;++n) {
        const struct pad_reading *p=&readings[n];
        if(!p->connected || (p->buttons&PAD_INTERCEPTED)) {
            PS5_TempRelease(window,now);last=NULL;continue;
        }
        Uint32 held=p->buttons;
        if(p->l2>127)held|=0x10000000u;
        if(p->r2>127)held|=0x20000000u;
        if(!ps5_temp.primed) {ps5_temp.blocked=held;ps5_temp.primed=true;}
        /* Release launch-held buttons/triggers before they can activate items. */
        ps5_temp.blocked&=held;held&=~ps5_temp.blocked;
        Uint32 keys=0;
        if(held&PAD_UP)keys|=1u<<0;
        if(held&PAD_DOWN)keys|=1u<<1;
        if(held&PAD_LEFT)keys|=1u<<2;
        if(held&PAD_RIGHT)keys|=1u<<3;
        if(held&PAD_CROSS)keys|=1u<<(captured?12:4);
        if(held&PAD_CIRCLE)keys|=1u<<5;
        if(held&PAD_TRIANGLE)keys|=1u<<(captured?13:6);
        if(held&PAD_SQUARE)keys|=1u<<7;
        if(p->left_y<80)keys|=1u<<(captured?8:0);
        if(p->left_y>176)keys|=1u<<(captured?9:1);
        if(p->left_x<80)keys|=1u<<(captured?10:2);
        if(p->left_x>176)keys|=1u<<(captured?11:3);
        Uint8 buttons=((held&0x20000000u)?1:0)|((held&0x10000000u)?2:0);
        PS5_TempKeys(now,keys,buttons,window);last=p;
    }
    if(!(pad_players()&1u)) {PS5_TempRelease(window,now);return;}
    /* Repeats for navigation/editing; never repeated activation or idle input. */
    for(int i=0;i<8;++i)if(i!=4 && i!=5 && (ps5_temp.keys&(1u<<i)) && now>=ps5_temp.repeat_at[i]) {
        SDL_SendKeyboardKey(now,ps5_temp.keyboard,0,ps5_temp_keys[i],true);
        ps5_temp.repeat_at[i]=now+100000000ull;
    }
    if(captured && last && ps5_temp.last_pump) {
        float dt=(float)(now-ps5_temp.last_pump)/1e9f;if(dt>0.05f)dt=0.05f;
        float x=((float)last->right_x-128.0f)/127.0f,y=((float)last->right_y-128.0f)/127.0f;
        if(x>-0.16f && x<0.16f)x=0;
        if(y>-0.16f && y<0.16f)y=0;
        if(x || y)SDL_SendMouseMotion(now,window,ps5_temp.mouse,true,x*650.0f*dt,y*650.0f*dt);
    }
    ps5_temp.last_pump=now;
}
