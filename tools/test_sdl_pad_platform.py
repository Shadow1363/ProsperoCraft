#!/usr/bin/env python3
"""Exercise the SDL port's real input adapter with deterministic host OS-call fixtures."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
source=r'''
#include "platform.h"
#include <assert.h>
#include <string.h>
#include <stdio.h>
int prospero_pad_set_vibration_mode(int,int);
static int motion_calls,motion_fail,rumble_fail,rumble_calls;static unsigned char last_motors[2];
int scePadSetVibrationMode(int32_t h,int32_t mode){assert(h==7&&(mode==1||mode==2));return rumble_fail?-1:0;}
int scePadSetVibration(int32_t h,const void*p){assert(h==7);memcpy(last_motors,p,2);rumble_calls++;return rumble_fail?-1:0;}
int scePadSetMotionSensorState(int32_t h,bool on){assert(h==7);motion_calls++;return motion_fail?-1:0;}
static int init_calls,opens,reads;static int buttons=PAD_CROSS;static int connected=1;
int sceUserServiceGetInitialUser(int32_t*u){*u=42;return 0;}
int sceUserServiceInitialize(const void*p){(void)p;return 0;}
int sceUserServiceGetLoginUserIdList(void*p){int32_t*v=p;v[0]=42;v[1]=v[2]=v[3]=-1;return 0;}
int scePadInit(void){init_calls++;return -1;} /* already initialized by bootstrap */
int scePadOpen(int32_t u,int32_t type,int32_t index,const void*p){(void)type;(void)index;(void)p;assert(u==42);opens++;return 7;}
int scePadGetHandle(int32_t u,int32_t type,int32_t index){(void)u;(void)type;(void)index;return 7;}
int scePadClose(int32_t h){assert(h==7);return 0;}
int sceKernelUsleep(uint32_t t){(void)t;return 0;}
int scePadRead(int32_t h,void*data,int32_t capacity){assert(h==7&&capacity==64);unsigned char*p=data;memset(p,0,120);memcpy(p,&buttons,4);p[4]=255;p[5]=p[6]=p[7]=128;float gyro[3]={0.25f,-0.5f,1.0f};memcpy(p+0x28,gyro,sizeof(gyro));uint64_t timestamp=12345;memcpy(p+0x50,&timestamp,8);memcpy(p+0x4c,&connected,4);reads++;return 1;}
void client_sdl_diagnostic(const char*t){assert(t&&*t);}
int main(int argc,char**argv){(void)argv;rumble_fail=argc>1;assert(pad_open());if(rumble_fail){assert(!pad_player_has_rumble(0)&&!pad_player_rumble(0,65535,65535));puts("PASS rumble capability absent after native zero-output probe failure");return 0;}assert(pad_open());assert(opens==1&&init_calls==0);assert(pad_player_has_rumble(0)&&!pad_player_has_rumble(9));assert(prospero_pad_set_vibration_mode(7,1)==0);assert(pad_player_rumble(0,65535,32768)&&last_motors[0]==255&&last_motors[1]==128);assert(pad_player_rumble(0,0,0)&&last_motors[0]==0&&last_motors[1]==0);rumble_fail=1;assert(!pad_player_rumble(0,1234,5678));rumble_fail=0;assert(pad_player_has_gyro(0)&&!pad_player_has_gyro(9)&&motion_calls==1);assert(pad_player_set_motion(0,true)&&pad_player_motion_enabled(0));struct pad p={0};pad_poll(&p);const struct pad_reading *samples;assert(pad_readings(&samples)==1&&samples[0].angular_velocity[0]==0.25f&&samples[0].angular_velocity[1]==-0.5f&&samples[0].angular_velocity[2]==1.0f&&samples[0].timestamp_us==12345);motion_fail=1;assert(!pad_player_set_motion(0,false)&&pad_player_motion_enabled(0));motion_fail=0;assert(pad_player_set_motion(0,false)&&!pad_player_motion_enabled(0));assert(reads==1&&pad_players()==1);assert(p.held==PAD_CROSS&&p.left_x>0.9f);buttons=0;pad_poll(&p);assert(p.held==0);connected=0;pad_poll(&p);assert(pad_players()==0);puts("PASS real SDL input adapter: bootstrap-owned init reused, real open/read path, button/axis/release/disconnect state,native gyro ABI/sample values,enable/disable/failure; host OS fixtures, not PS5 hardware");}
'''
with tempfile.TemporaryDirectory(prefix='sdl-pad-test-')as folder:
 p=Path(folder);(p/'test.c').write_text(source)
 subprocess.run(['clang','-std=c11','-fsanitize=address,undefined','-I'+str(ROOT/'client/ports/sdl'),str(ROOT/'client/ports/sdl/platform-input.c'),str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True);subprocess.run([str(p/'test'),'probe-failure'],check=True)
