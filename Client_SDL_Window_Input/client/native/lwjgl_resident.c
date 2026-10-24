/* SPDX-License-Identifier: BSD-3-Clause */
#include <jni.h>
#include <stdint.h>
#include <dlfcn.h>
#ifdef __PROSPERO__
extern void* __dlopen(const char*,int);extern void* __dlsym(void*,const char*);extern int __dlclose(void*);
#define OPEN __dlopen
#define FIND __dlsym
#define CLOSE __dlclose
#else
#define OPEN dlopen
#define FIND dlsym
#define CLOSE dlclose
#endif
JNIEXPORT int ps5_lwjgl_pointer_size(void){return sizeof(void*);}
JNIEXPORT jlong JNICALL Java_org_lwjgl_system_ps5_PS5Library_nOpen(JNIEnv* env,jclass cls,jstring name){
 (void)cls;if(!name)return 0;const char* text=(*env)->GetStringUTFChars(env,name,NULL);if(!text)return 0;
 void* handle=OPEN(text,RTLD_LAZY);(*env)->ReleaseStringUTFChars(env,name,text);return (jlong)(uintptr_t)handle;
}
JNIEXPORT jlong JNICALL Java_org_lwjgl_system_ps5_PS5Library_nFind(JNIEnv* env,jclass cls,jlong handle,jstring name){
 (void)cls;if(!name||!handle)return 0;const char* text=(*env)->GetStringUTFChars(env,name,NULL);if(!text)return 0;
 void* address=FIND((void*)(uintptr_t)handle,text);(*env)->ReleaseStringUTFChars(env,name,text);return (jlong)(uintptr_t)address;
}
JNIEXPORT jint JNICALL Java_org_lwjgl_system_ps5_PS5Library_nClose(JNIEnv* env,jclass cls,jlong handle){(void)env;(void)cls;return CLOSE((void*)(uintptr_t)handle);}
