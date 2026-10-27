/* SPDX-License-Identifier: GPL-3.0-or-later
 * Bounded ProsperoCraft project-icon thumbnails. No game or ImageIO loading.
 * STB and libwebp retain their upstream licenses in the packaged notices.
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <webp/decode.h>
#define STB_IMAGE_STATIC
#define STB_IMAGE_IMPLEMENTATION
#define STBI_ONLY_PNG
#define STBI_ONLY_JPEG
#define STBI_NO_STDIO
#define STBI_NO_SIMD
#define STBI_NO_HDR
#define STBI_NO_LINEAR
#define STBI_MAX_DIMENSIONS 1024
#include "stb_image.h"
int prospero_content_thumbnail(const uint8_t *data,size_t size,char out[6145]){
 if(!data||size<12||size>1024*1024)return 0;
 int w=0,h=0,channels=0;uint8_t *pixels=0;int webp=!memcmp(data,"RIFF",4)&&!memcmp(data+8,"WEBP",4);
 if(webp){if(!WebPGetInfo(data,size,&w,&h)||w<1||h<1||w>1024||h>1024)return 0;pixels=malloc((size_t)w*h*4);if(!pixels)return 0;if(!WebPDecodeRGBAInto(data,size,pixels,(size_t)w*h*4,w*4)){free(pixels);return 0;}}
 else{if(!stbi_info_from_memory(data,(int)size,&w,&h,&channels)||w<1||h<1||w>1024||h>1024)return 0;pixels=stbi_load_from_memory(data,(int)size,&w,&h,&channels,4);if(!pixels)return 0;}
 const char hex[]="0123456789abcdef";size_t at=0;
 for(int y=0;y<32;y++)for(int x=0;x<32;x++){const uint8_t *p=pixels+((size_t)(y*h/32)*w+x*w/32)*4;for(int c=0;c<3;c++){int v=(p[c]*p[3]+24*(255-p[3])+127)/255;out[at++]=hex[v>>4];out[at++]=hex[v&15];}}
 out[at]=0;if(webp)free(pixels);else stbi_image_free(pixels);return 1;
}
#ifndef PROSPERO_ICON_NO_JNI
#include <jni.h>
JNIEXPORT jstring JNICALL Java_ProsperoContentImages_nativeDecode(JNIEnv *env,jclass owner,jbyteArray bytes){
 (void)owner;if(!bytes)return NULL;jsize size=(*env)->GetArrayLength(env,bytes);if(size<12||size>1024*1024)return NULL;
 uint8_t *data=malloc((size_t)size);if(!data)return NULL;(*env)->GetByteArrayRegion(env,bytes,0,size,(jbyte*)data);if((*env)->ExceptionCheck(env)){free(data);return NULL;}
 char out[6145];int good=prospero_content_thumbnail(data,(size_t)size,out);free(data);return good?(*env)->NewStringUTF(env,out):NULL;
}
#endif
