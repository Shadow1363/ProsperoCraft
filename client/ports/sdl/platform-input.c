/*
 * PS5 Vulkan Template - the console: klog, the splash, the pad, sound, time, the exit.
 *
 * Copyright (C) 2026 Mihawk
 *
 * This code is licensed under the MIT license (MIT) (http://opensource.org/licenses/MIT)
 *
 * Every console call here is one PS5_vkQuake, PS5_RetroArch or PS5_Vulkan's
 * smoke test runs with; no SDK header declares them.
 */
/* Consumer adapter: input plus opt-in native motion; haptic audio is separate. */
#include "platform.h"
#include "ps5_trigger_follow.h"
#include <stddef.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdatomic.h>
extern void client_sdl_diagnostic(const char* text);
void say(const char *format, ...){char line[384];va_list args;va_start(args,format);vsnprintf(line,sizeof(line),format,args);va_end(args);client_sdl_diagnostic(line);}

double now_seconds(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return (double)t.tv_sec+(double)t.tv_nsec/1e9;}
int sceSystemServiceHideSplashScreen(void);
int sceSystemServiceLoadExec(const char *path, const char *const *argv);
int sceUserServiceInitialize(const void *params);
int sceUserServiceGetInitialUser(int32_t *user_id);
/* The signed-in users, at most four; unused entries are -1. */
struct user_list {
   int32_t user_id[4];
};
int sceUserServiceGetLoginUserIdList(struct user_list *list);
int scePadInit(void);
int scePadOpen(int32_t user_id, int32_t port_type, int32_t index, const void *params);
int scePadGetHandle(int32_t user_id, int32_t port_type, int32_t index);
int scePadRead(int32_t handle, void *samples, int32_t capacity);
int scePadClose(int32_t handle);
int scePadSetVibrationMode(int32_t handle, int32_t mode);
int scePadSetMotionSensorState(int32_t handle, bool enabled);
int scePadSetVibration(int32_t handle, const void *vibration);
int scePadSetTriggerEffect(int32_t handle,const ProsperoTriggerEffect *effect);
int scePadSetLightBar(int32_t handle, const void *color);
int sceKernelUsleep(uint32_t microseconds);
static atomic_flag vibration_lock=ATOMIC_FLAG_INIT;
static int vibration_handle=-1,vibration_mode=-1;
int prospero_pad_set_vibration_mode(int handle,int mode){
 while(atomic_flag_test_and_set_explicit(&vibration_lock,memory_order_acquire)){}
 int rc=0;
 if(vibration_handle!=handle||vibration_mode!=mode){rc=scePadSetVibrationMode(handle,mode);if(rc>=0){vibration_handle=handle;vibration_mode=mode;}}
 atomic_flag_clear_explicit(&vibration_lock,memory_order_release);return rc;
}
/* ----------------------------------------------------------------- the pad */

/* One sample as the console writes it: 120 bytes, the layout PS5_vkQuake and
 * ProsperoLight read. */
struct pad_sample {
   uint32_t buttons;
   uint8_t left_x, left_y, right_x, right_y, l2, r2;
   uint8_t motion_alignment[2];
   float orientation[4];
   float acceleration[3];
   float angular_velocity[3];
   uint8_t reserved[24];
   int32_t connected;
   uint64_t timestamp_us;
   uint8_t extension[16];
   uint8_t connected_count;
   uint8_t remaining[15];
};
_Static_assert(offsetof(struct pad_sample, angular_velocity) == 0x28, "angular velocity sits at 0x28");
_Static_assert(sizeof(struct pad_sample) == 120, "the console's pad samples are 120 bytes");
_Static_assert(offsetof(struct pad_sample, connected) == 0x4c, "connection state sits at 0x4c");
_Static_assert(offsetof(struct pad_sample, timestamp_us) == 0x50, "the timestamp sits at 0x50");

/* The two-motor rumble, as PS5_vkQuake and ProsperoLight drive it (the other
 * mode is the DualSense's haptics). */
#define PAD_VIBRATION_COMPATIBLE 2

/* A player: a signed-in user's controller, PS5_ProsperoEden's way. The console
 * pairs each controller with a user, and scePadOpen opens a user's. Player 0 is
 * the user who started the title and stays theirs; about once a second
 * pad_poll reads the signed-in users again, a new user's controller takes the
 * first free player, and a player is let go when their user signs out. */
struct pad_player_state {
   int32_t user;
   int32_t handle;
   bool connected;
   bool motion_supported, motion_enabled;
   bool rumble_supported, rumble_active;
   bool trigger_supported,intercepted,trigger_reported,trigger_suspended;
   uint8_t trigger_active,trigger_requested,trigger_follow,trigger_sent;
   unsigned trigger_rejected;
   int trigger_zone[2],trigger_error[2];
   ProsperoTriggerCommand trigger_profile[2],trigger_applied[2];
   struct pad_sample last;
   struct pad_reading taken[64];
   int taken_count;
};

static struct pad_player_state pad_states[PAD_PLAYERS];
static bool pad_service;
static double pad_next_scan;
/* A user whose controller would not open, said once rather than every scan. */
static int32_t pad_unopened = -1;
#define PAD_SCAN_SECONDS 1.0

/* A player's state while they have a controller, else NULL (and always NULL
 * before pad_open has set the players up). */
static struct pad_player_state *
pad_state(int player)
{
   if (!pad_service || player < 0 || player >= PAD_PLAYERS || pad_states[player].handle < 0)
      return NULL;
   return &pad_states[player];
}

static void
pad_rest(struct pad_player_state *state)
{
   memset(state, 0, sizeof(*state));
   state->user = state->handle = -1;
   state->last.left_x = state->last.left_y = state->last.right_x = state->last.right_y = 128;
}

static bool
pad_player_open(int player, int32_t user, int attempts)
{
   struct pad_player_state *state = &pad_states[player];
   pad_rest(state);
   /* A title can start before the pad service has published the device. */
   int32_t handle = -1;
   for (int attempt = 0; attempt < attempts && handle < 0; attempt++) {
      handle = scePadOpen(user, 0, 0, NULL);
      if (handle < 0 && attempt + 1 < attempts)
         sceKernelUsleep(100000);
   }
   /* A handle this process already holds for the user is reused. */
   if (handle < 0)
      handle = scePadGetHandle(user, 0, 0);
   if (handle < 0) {
      if (user != pad_unopened)
         say("pad: scePadOpen failed for user %d (player %d)", (int)user, player);
      pad_unopened = user;
      return false;
   }
   state->user = user;
   state->handle = handle;
   unsigned char stopped[2]={0,0};
   int rumble_mode=prospero_pad_set_vibration_mode(handle,PAD_VIBRATION_COMPATIBLE);
   int rumble=rumble_mode<0?rumble_mode:scePadSetVibration(handle,stopped);
   state->rumble_supported=rumble>=0;
   say("PS5_INPUT rumble probe player=%d result=0x%x",player,(unsigned)rumble);
   ProsperoTriggerEffect off={0};off.mask=3;int trigger=scePadSetTriggerEffect(handle,&off);state->trigger_supported=trigger>=0;
   say("PS5_INPUT trigger probe player=%d result=0x%x",player,(unsigned)trigger);
   int motion = scePadSetMotionSensorState(handle, false);
   state->motion_supported = motion >= 0;
   say("PS5_INPUT motion probe player=%d result=0x%x",player,(unsigned)motion);
   say("pad: player %d opened", player);
   return true;
}

static void
pad_player_close(int player, const char *why)
{
   struct pad_player_state *state = &pad_states[player];
   if (state->handle < 0)
      return;
   (void)pad_player_reset_triggers(player);
   say("pad: player %d let go (user %d %s), close %d", player, (int)state->user, why,
       scePadClose(state->handle));
   pad_rest(state);
}

/* The signed-in users again: player 0 stays; a player whose user signed out is
 * let go; a new user's controller takes the first free player. */
static void
pad_scan(void)
{
   struct user_list list = {{-1, -1, -1, -1}};
   if (sceUserServiceGetLoginUserIdList(&list) < 0)
      return;
   for (int player = 1; player < PAD_PLAYERS; player++) {
      if (pad_states[player].handle < 0)
         continue;
      bool signed_in = false;
      for (int i = 0; i < 4; i++)
         signed_in |= list.user_id[i] >= 0 && list.user_id[i] == pad_states[player].user;
      if (!signed_in)
         pad_player_close(player, "signed out");
   }
   for (int i = 0; i < 4; i++) {
      const int32_t user = list.user_id[i];
      bool known = user < 0;
      for (int player = 0; player < PAD_PLAYERS && !known; player++)
         known = pad_states[player].handle >= 0 && pad_states[player].user == user;
      for (int player = 0; player < PAD_PLAYERS && !known; player++) {
         if (pad_states[player].handle < 0) {
            (void)pad_player_open(player, user, 1);
            break;
         }
      }
   }
}

bool
pad_open(void)
{
   /* Video's temporary mapper and the real joystick driver share these handles. */
   if (pad_service)
      return pad_states[0].handle >= 0;
   for (int player = 0; player < PAD_PLAYERS; player++)
      pad_rest(&pad_states[player]);
   /* Altered: this title's bootstrap already initializes UserService/Pad and
    * closes its start-button handle before SDL. Reuse that service lifetime;
    * a second scePadInit result must not reject an already initialized pad. */
   int32_t user = -1;
   int user_result=sceUserServiceGetInitialUser(&user);
   say("SDL pad initial user: result=%d user=%d; bootstrap owns service init",user_result,(int)user);
   if (user_result < 0) {
      say("pad: no user or no pad service");
      return false;
   }
   pad_service = true;
   const bool opened = pad_player_open(0, user, 10);
   pad_scan();
   pad_next_scan = now_seconds() + PAD_SCAN_SECONDS;
   return opened;
}

static float
stick(uint8_t value)
{
   const float v = ((float)value - 128.0f) / 127.0f;
   const float dead = 0.12f;
   if (v > -dead && v < dead)
      return 0.0f;
   return v > 0 ? (v - dead) / (1.0f - dead) : (v + dead) / (1.0f - dead);
}

static void
pad_fill(const struct pad_player_state *state, struct pad *pad)
{
   const uint32_t before = pad->held;
   pad->held = state->handle >= 0 ? state->last.buttons : 0;
   pad->pressed = pad->held & ~before;
   pad->left_x = stick(state->last.left_x);
   pad->left_y = stick(state->last.left_y);
   pad->right_x = stick(state->last.right_x);
   pad->right_y = stick(state->last.right_y);
   pad->l2 = state->last.l2 / 255.0f;
   pad->r2 = state->last.r2 / 255.0f;
}

void
pad_poll(struct pad *pad)
{
   if (pad_service && now_seconds() >= pad_next_scan) {
      pad_scan();
      pad_next_scan = now_seconds() + PAD_SCAN_SECONDS;
   }
   static struct pad_sample samples[64];
   for (int player = 0; player < PAD_PLAYERS; player++) {
      struct pad_player_state *state = pad_state(player);
      if (state == NULL)
         continue;
      state->taken_count = 0;
      const int count = scePadRead(state->handle, samples, 64);
      if (count < 0){state->connected = false;(void)pad_player_reset_triggers(player);}
      for (int i = 0; i < count && i < 64; i++) {
         const struct pad_sample *s = &samples[i];
         state->taken[state->taken_count++] = (struct pad_reading){
            s->buttons, s->left_x, s->left_y, s->right_x, s->right_y, s->l2, s->r2,
            s->connected != 0, s->timestamp_us,
            {s->angular_velocity[0],s->angular_velocity[1],s->angular_velocity[2]}};
         state->connected = s->connected != 0;state->intercepted=(s->buttons&PAD_INTERCEPTED)!=0;
         if(!s->connected)(void)pad_player_reset_triggers(player);
         else if(s->buttons&PAD_INTERCEPTED)pad_player_suspend_triggers(player);
         if (s->connected && !(s->buttons & PAD_INTERCEPTED))
            state->last = *s;
      }
   }
   for(int player=0;player<PAD_PLAYERS;player++)pad_player_update_triggers(player);
   (void)pad_player(0, pad);
}

uint32_t
pad_players(void)
{
   uint32_t players = 0;
   for (int player = 0; player < PAD_PLAYERS; player++) {
      const struct pad_player_state *state = pad_state(player);
      if (state != NULL && state->connected)
         players |= 1u << player;
   }
   return players;
}

bool
pad_player(int player, struct pad *pad)
{
   const struct pad_player_state *state = pad_state(player);
   if (state == NULL) {
      struct pad_player_state rest;
      pad_rest(&rest);
      pad_fill(&rest, pad);
      return false;
   }
   pad_fill(state, pad);
   return true;
}

int
pad_player_readings(int player, const struct pad_reading **readings)
{
   const struct pad_player_state *state = pad_state(player);
   *readings = state != NULL ? state->taken : NULL;
   return state != NULL ? state->taken_count : 0;
}

int
pad_readings(const struct pad_reading **readings)
{
   return pad_player_readings(0, readings);
}


/* ScePad angular velocity uses radians/second in the controller's local axes. */
bool pad_player_has_gyro(int player){const struct pad_player_state *s=pad_state(player);return s&&s->motion_supported;}
bool pad_player_set_motion(int player,bool enabled){
 struct pad_player_state *s=pad_state(player);if(!s||!s->motion_supported)return false;
 int rc=scePadSetMotionSensorState(s->handle,enabled);say("PS5_INPUT motion player=%d enabled=%d result=0x%x",player,enabled,(unsigned)rc);
 if(rc<0)return false;s->motion_enabled=enabled;return true;
}
bool pad_player_motion_enabled(int player){const struct pad_player_state *s=pad_state(player);return s&&s->motion_enabled;}

bool pad_player_has_rumble(int player){struct pad_player_state *s=pad_state(player);return s&&s->rumble_supported;}
bool pad_player_rumble(int player,uint16_t low,uint16_t high){
 struct pad_player_state *s=pad_state(player);if(!s||!s->rumble_supported)return false;
 if(!low&&!high&&!s->rumble_active)return true;
 unsigned char motors[2]={(unsigned char)(low>>8),(unsigned char)(high>>8)};
 int rc=prospero_pad_set_vibration_mode(s->handle,PAD_VIBRATION_COMPATIBLE);
 if(rc>=0)rc=scePadSetVibration(s->handle,motors);
 if(rc>=0)s->rumble_active=low||high;
 say("PS5_INPUT rumble player=%d low=%u high=%u result=0x%x",player,(unsigned)motors[0],(unsigned)motors[1],(unsigned)rc);
 return rc>=0;
}

static atomic_flag trigger_lock=ATOMIC_FLAG_INIT;
static void trigger_acquire(void){while(atomic_flag_test_and_set_explicit(&trigger_lock,memory_order_acquire)){}}
static void trigger_release(void){atomic_flag_clear_explicit(&trigger_lock,memory_order_release);}
static int trigger_submit(struct pad_player_state *s,int player,int index,const ProsperoTriggerCommand *command){
 unsigned bit=1u<<index;
 if((s->trigger_sent&bit)&&!memcmp(&s->trigger_applied[index],command,sizeof(*command)))return 0;
 ProsperoTriggerEffect native={0};native.mask=(uint8_t)bit;if(index==0)native.left=*command;else native.right=*command;
 int rc=scePadSetTriggerEffect(s->handle,&native);
 if(rc>=0){s->trigger_applied[index]=*command;s->trigger_sent|=bit;s->trigger_active=(s->trigger_active&~bit)|(command->mode?bit:0);}
 if((rc<0&&rc!=s->trigger_error[index])||(rc>=0&&!s->trigger_reported&&command->mode)){
  say("PS5_INPUT trigger native player=%d side=%d mode=%d position=%u strength=%u result=0x%x",player,index,command->mode,(unsigned)command->data[0],(unsigned)command->data[1],(unsigned)rc);if(rc>=0)s->trigger_reported=true;
 }s->trigger_error[index]=rc;return rc;
}
static bool trigger_apply(struct pad_player_state *s,int player,int index){
 unsigned bit=1u<<index;ProsperoTriggerCommand *profile=&s->trigger_profile[index];
 if((profile->mode==4||profile->mode==6)&&!(s->trigger_rejected&(1u<<profile->mode))){
  int rc=trigger_submit(s,player,index,profile);if(rc>=0){s->trigger_follow&=~bit;return true;}
  if((uint32_t)rc!=0x80920001u)return false;
  s->trigger_rejected|=1u<<profile->mode;
  say("PS5_INPUT trigger profile mode=%d rejected;using position-followed basic effects",profile->mode);
 }
 ProsperoTriggerCommand native;
 if(profile->mode==4||profile->mode==6){s->trigger_follow|=bit;prospero_trigger_follow(profile,index?s->last.r2:s->last.l2,&s->trigger_zone[index],&native);}
 else{s->trigger_follow&=~bit;native=*profile;}
 int rc=trigger_submit(s,player,index,&native);if(rc<0)s->trigger_follow&=~bit;return rc>=0;
}
// One OFF attempt per state change. A failed write is not retried every poll;
// cleared send state makes the next real request reach the pad again.
static int trigger_off(struct pad_player_state *s,int player,const char *why){
 int rc=0;
 if(s->trigger_active){ProsperoTriggerEffect off={0};off.mask=3;rc=scePadSetTriggerEffect(s->handle,&off);if(rc<0)say("PS5_INPUT trigger off player=%d reason=%s result=0x%x",player,why,(unsigned)rc);}
 s->trigger_active=0;s->trigger_sent=0;memset(s->trigger_applied,0,sizeof(s->trigger_applied));return rc;
}
bool pad_player_reset_triggers(int player){
 struct pad_player_state *s=pad_state(player);if(!s||!s->trigger_supported)return true;
 trigger_acquire();s->trigger_requested=s->trigger_follow=0;s->trigger_suspended=false;int rc=trigger_off(s,player,"reset");
 trigger_release();return rc>=0;
}
// System interception stops output but keeps the requested profiles, so the
// game's last effect returns with the pad instead of waiting for a new packet.
void pad_player_suspend_triggers(int player){
 struct pad_player_state *s=pad_state(player);if(!s||!s->trigger_supported||s->trigger_suspended)return;
 trigger_acquire();s->trigger_suspended=true;(void)trigger_off(s,player,"intercepted");trigger_release();
}
void pad_player_update_triggers(int player){
 struct pad_player_state *s=pad_state(player);if(!s||!s->trigger_supported||!s->connected||s->intercepted)return;
 trigger_acquire();
 if(s->trigger_suspended){
  s->trigger_suspended=false;
  for(int i=0;i<2;i++)if(s->trigger_requested&(1u<<i))(void)trigger_apply(s,player,i);
  if(s->trigger_requested)say("PS5_INPUT trigger restore player=%d sides=%u",player,(unsigned)s->trigger_requested);
 }else for(int i=0;i<2;i++)if(s->trigger_follow&(1u<<i))(void)trigger_apply(s,player,i);
 trigger_release();
}
bool pad_player_send_effect(int player,const void *data,int size){
 struct pad_player_state *s=pad_state(player);if(!s||!s->trigger_supported||!s->connected||s->intercepted)return false;
 ProsperoTriggerEffect effect;if(!prospero_trigger_packet(data,size,&effect))return false;if(!effect.mask)return true;
 trigger_acquire();bool success=true;for(int i=0;i<2;i++)if(effect.mask&(1u<<i)){
  const ProsperoTriggerCommand *command=i?&effect.right:&effect.left;
  if(memcmp(command,&s->trigger_profile[i],sizeof(*command)))s->trigger_zone[i]=-1;
  s->trigger_profile[i]=*command;s->trigger_requested|=1u<<i;
  if(!trigger_apply(s,player,i))success=false;
 }trigger_release();return success;
}
