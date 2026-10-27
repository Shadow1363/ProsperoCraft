/* SPDX-License-Identifier: GPL-3.0-or-later */
#include "ps5_hid.h"
#include <string.h>
#include <stdio.h>
int sceSysmoduleLoadModule(uint16_t id);
int sceKernelGetModuleList(int *handles,size_t count,size_t *actual);
int sceKernelGetModuleInfo(int handle,void *info);
int sceKernelDlsym(int handle,const char *name,void **address);
int sceUserServiceGetInitialUser(int32_t *user);
struct hid_api {const char *module;const char *symbols[4];int ready;int(*init)(void);int(*open)(int,int,int,const void*);int(*read)(int,void*,int);int(*close)(int);};
static struct hid_api devices[2]={{"libSceKeyboard",{"sceKeyboardInit","sceKeyboardOpen","sceKeyboardRead","sceKeyboardClose"}},{"libSceMouse",{"sceMouseInit","sceMouseOpen","sceMouseRead","sceMouseClose"}}};
static int initialized;
static int find_module(const char *name){
 int handles[512];size_t count=0;if(sceKernelGetModuleList(handles,512,&count)!=0||count>512)return -1;
 const uint64_t sizes[]={0x160,0x1a8,0x1b0,0x158,0x200};
 for(size_t n=0;n<count;n++)for(size_t i=0;i<sizeof(sizes)/sizeof(sizes[0]);i++){
  struct {uint64_t size;char name[256];unsigned char extra[1024];} info={0};info.size=sizes[i];
  if(sceKernelGetModuleInfo(handles[n],&info)==0){info.name[255]=0;if(strstr(info.name,name))return handles[n];break;}
 }return -1;
}
void prospero_hid_preload(void){
 if(initialized)return;initialized=1;
 for(int n=0;n<2;n++){
  struct hid_api *api=&devices[n];int rc=sceSysmoduleLoadModule((uint16_t)(n?0x00a9:0x0106));int handle=find_module(api->module);void *symbols[4]={0};
  if(handle>=0)for(int j=0;j<4;j++)if(sceKernelDlsym(handle,api->symbols[j],&symbols[j])!=0)symbols[j]=0;
  api->init=(int(*)(void))symbols[0];api->open=(int(*)(int,int,int,const void*))symbols[1];api->read=(int(*)(int,void*,int))symbols[2];api->close=(int(*)(int))symbols[3];
  api->ready=api->init&&api->open&&api->read&&api->close;
  int init=api->ready?api->init():-1;fprintf(stderr,"PS5_INPUT %s moduleRc=0x%x handle=%d api=%d init=0x%x\n",n?"mouse":"keyboard",(unsigned)rc,handle,api->ready,(unsigned)init);
 }
}
int prospero_hid_open(int mouse,int index){
 if(mouse<0||mouse>1||index<0||index>=4)return -1;prospero_hid_preload();struct hid_api *api=&devices[mouse];int32_t user=-1;uint64_t param=0;
 if(!api->ready||sceUserServiceGetInitialUser(&user)<0||user<0)return -1;return api->open(user,0,index,&param);
}
int prospero_hid_read(int mouse,int handle,void *packets,int count){if(mouse<0||mouse>1||handle<0||count<=0||count>64||!devices[mouse].ready)return -1;return devices[mouse].read(handle,packets,count);}
void prospero_hid_close(int mouse,int handle){if(mouse>=0&&mouse<=1&&handle>=0&&devices[mouse].ready)(void)devices[mouse].close(handle);}
