/* SPDX-License-Identifier: MIT */
#include <stdlib.h>
#include <string.h>
/* Bound only to the startup-private OpenAL object. Other environment lookups,
 * the process getenv and backend selection retain their existing behavior. */
char *client_startup_openal_getenv(const char *name) {
 static char level[]="3";
 if(name&&strcmp(name,"ALSOFT_LOGLEVEL")==0)return level;
 return getenv(name);
}
