/* SPDX-License-Identifier: Zlib */
#ifndef PROSPERO_TRIGGER_FOLLOW_H
#define PROSPERO_TRIGGER_FOLLOW_H
#include "ps5_trigger_effect.h"
// A rejected per-zone command can be approximated with supported basic effects
// by following actual trigger travel. Hysteresis prevents boundary chatter.
static void prospero_trigger_follow(const ProsperoTriggerCommand *profile,uint8_t analog,int *previous,ProsperoTriggerCommand *out){
 if(profile->mode!=4&&profile->mode!=6){*out=*profile;return;}
 memset(out,0,sizeof(*out));const uint8_t *zones=profile->data+(profile->mode==6?1:0);
 int value=analog*10,zone=*previous;
 if(zone<0||zone>9||value>=(zone+1)*256+96||value<zone*256-96)zone=value/256;
 if(zone>9)zone=9;*previous=zone;
 int first=0;while(first<10&&!zones[first])first++;
 if(first==10||!zones[zone]||(profile->mode==6&&!profile->data[0]))return;
 out->mode=profile->mode==4?1:3;out->data[0]=(uint8_t)first;out->data[1]=zones[zone];
 if(profile->mode==6)out->data[2]=profile->data[0];
}
#endif
