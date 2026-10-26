/* SPDX-License-Identifier: MIT */
#include <stdlib.h>
#include <string.h>
/* Bound only to the startup-private OpenAL object. Other environment lookups,
 * the process getenv remains unchanged;startup defaults to the real PS5 backend. */
char *client_startup_openal_getenv(const char *name) {
 static char level[]="3";
 static char driver[]="ps5";
 static char app_local[]="/download0/mc-client";
 if(name&&strcmp(name,"ALSOFT_LOGLEVEL")==0)return level;
 if(name&&strcmp(name,"ALSOFT_DRIVERS")==0){char *configured=getenv(name);return configured&&*configured?configured:driver;}
 if(name&&strcmp(name,"ALSOFT_LOCAL_PATH")==0){
  char *configured=getenv(name);
  return configured&&*configured?configured:app_local;
 }
 return getenv(name);
}
