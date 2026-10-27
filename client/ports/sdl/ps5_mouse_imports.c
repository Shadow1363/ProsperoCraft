/* SPDX-License-Identifier: GPL-3.0-or-later
 * Link-time system import declarations only. These bodies never enter the app.
 * libSceMouse.sprx is supplied by the console, not shipped or emulated here.
 */
int sceMouseInit(void){return -1;}
int sceMouseOpen(int u,int t,int i,const void*p){(void)u;(void)t;(void)i;(void)p;return -1;}
int sceMouseRead(int h,void*p,int n){(void)h;(void)p;(void)n;return -1;}
int sceMouseClose(int h){(void)h;return -1;}
