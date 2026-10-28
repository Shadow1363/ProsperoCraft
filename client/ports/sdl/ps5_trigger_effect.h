/* SPDX-License-Identifier: Zlib
 * Independently authored conversion of Controlify/SDL's 47-byte DualSense
 * packet into native pad effect parameters. No raw HID reports reach hardware.
 */
#ifndef PROSPERO_TRIGGER_EFFECT_H
#define PROSPERO_TRIGGER_EFFECT_H
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
typedef struct {int32_t mode,reserved;uint8_t data[48];} ProsperoTriggerCommand;
typedef struct {uint8_t mask,reserved[7];ProsperoTriggerCommand left,right;} ProsperoTriggerEffect;
_Static_assert(sizeof(ProsperoTriggerEffect)==120,"native trigger ABI");
_Static_assert(offsetof(ProsperoTriggerEffect,right)==64,"R2 command offset");
static bool prospero_trigger_decode(const uint8_t *p,ProsperoTriggerCommand *out){
 memset(out,0,sizeof(*out));if(p[0]==0x05||p[0]==0)return true;
 unsigned mask=p[1]|((unsigned)p[2]<<8);if(mask&~0x3ffu)return false;
 if(p[0]==0x25){
  int first=-1,last=-1,count=0;for(int i=0;i<10;i++)if(mask&(1u<<i)){if(first<0)first=i;last=i;count++;}
  if(count!=2||first<2||first>7||last<=first||last>8||p[3]>7)return false;
  out->mode=2;out->data[0]=(uint8_t)first;out->data[1]=(uint8_t)last;out->data[2]=p[3]+1;return true;
 }
 if(p[0]!=0x21&&p[0]!=0x26)return false;
 if(!mask||(p[0]==0x26&&!p[9]))return true;
 uint32_t packed=p[3]|((uint32_t)p[4]<<8)|((uint32_t)p[5]<<16)|((uint32_t)p[6]<<24);
 uint8_t zones[10];int first=0;while(!(mask&(1u<<first)))first++;
 bool uniform=mask==(0x3ffu&~((1u<<first)-1));
 for(int i=0;i<10;i++){zones[i]=(mask&(1u<<i))?((packed>>(3*i))&7)+1:0;if(i>=first&&zones[i]!=zones[first])uniform=false;}
 if(uniform){out->mode=p[0]==0x21?1:3;out->data[0]=(uint8_t)first;out->data[1]=zones[first];if(p[0]==0x26)out->data[2]=p[9];}
 else if(p[0]==0x21){out->mode=4;memcpy(out->data,zones,10);}
 else{out->mode=6;out->data[0]=p[9];memcpy(out->data+1,zones,10);}
 return true;
}
static bool prospero_trigger_packet(const void *data,int size,ProsperoTriggerEffect *out){
 if(!data||size!=47)return false;const uint8_t *p=data;memset(out,0,sizeof(*out));
 if(p[0]&8){out->mask|=1;if(!prospero_trigger_decode(p+21,&out->left))return false;}
 if(p[0]&4){out->mask|=2;if(!prospero_trigger_decode(p+10,&out->right))return false;}
 return true;
}
#endif
