/* SPDX-License-Identifier: Zlib */
#pragma once
#include <stdint.h>
static int16_t prospero_haptic_sample(float value)
{
    if(!__builtin_isfinite(value))return 0;
    if(value>=1.0f)return INT16_MAX;
    if(value<=-1.0f)return INT16_MIN;
    return (int16_t)(value*32767.0f);
}
static void prospero_haptic_pcm(const float *quad,int16_t *stereo,int frames)
{
    for(int i=0;i<frames;i++){
        stereo[2*i]=prospero_haptic_sample(quad[4*i+2]);
        stereo[2*i+1]=prospero_haptic_sample(quad[4*i+3]);
    }
}
