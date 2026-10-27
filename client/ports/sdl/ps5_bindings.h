/* SPDX-License-Identifier: GPL-3.0-or-later */
#pragma once
/* SDL USB-HID scancodes;513..515 are mouse buttons. Menu/typing slots0..7
 * stay fixed, while gameplay slots8..29 are user-configurable. */
static const unsigned short ps5_default_bindings[30]={82,81,80,79,40,41,43,42,26,22,4,7,44,8,225,224,9,20,62,58,59,60,23,56,15,68,30,38,513,514};
static bool ps5_parse_bindings(const char *text,unsigned short values[30]) {
    if(!text||!*text)return false;
    unsigned short parsed[30];
    for(int n=0;n<30;n++){
        unsigned value=0;int digits=0;while(*text>='0'&&*text<='9'){value=value*10+(unsigned)(*text++-'0');if(++digits>3)return false;}
        if(!digits||value>515||value==512||(n<8&&value!=ps5_default_bindings[n]))return false;
        parsed[n]=(unsigned short)value;
        if(n<29){if(*text++!=',')return false;}else if(*text)return false;
    }
    for(int n=0;n<30;n++)values[n]=parsed[n];return true;
}
