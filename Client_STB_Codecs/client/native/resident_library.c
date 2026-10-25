/* SPDX-License-Identifier: GPL-3.0-or-later */
#include <jni.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <dlfcn.h>
static int load_count;
#ifdef __PROSPERO__
extern void* __dlopen(const char*,int);
extern void* __dlsym(void*,const char*);
extern int __dlclose(void*);
#define OPEN __dlopen
#define SYMBOL __dlsym
#define CLOSE __dlclose
#else
#define OPEN dlopen
#define SYMBOL dlsym
#define CLOSE dlclose
#endif
JNIEXPORT uint64_t ps5_client_checksum(const unsigned char* bytes,size_t count) {
 uint64_t sum=0;for(size_t i=0;i<count;++i)sum+=bytes[i]*(uint64_t)(i+1);return sum;
}
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm,void* reserved) {
 (void)reserved;JNIEnv* env=NULL;
 if((*vm)->GetEnv(vm,(void**)&env,JNI_VERSION_1_8)!=JNI_OK)return JNI_ERR;
 __atomic_add_fetch(&load_count,1,__ATOMIC_RELAXED);return JNI_VERSION_1_8;
}
JNIEXPORT jint JNICALL Java_ClientLibrary25_loadCount(JNIEnv* env,jclass type) {
 (void)env;(void)type;return __atomic_load_n(&load_count,__ATOMIC_RELAXED);
}
static void failure(JNIEnv* env,const char* type,const char* message) {
 jclass c=(*env)->FindClass(env,type);if(c)(*env)->ThrowNew(env,c,message);
}
static void* self_library(void) {
#ifdef __PROSPERO__
 return OPEN("libps5clientbridge.so",RTLD_LAZY);
#else
 Dl_info info;
 if(!dladdr((const void*)&ps5_client_checksum,&info))return NULL;
 return OPEN(info.dli_fname,RTLD_LAZY);
#endif
}
JNIEXPORT jlong JNICALL Java_ClientLibrary25_resolvedChecksum(JNIEnv* env,jclass type,jstring name,jobject buffer) {
 (void)type;
 if(!name||!buffer){failure(env,"java/lang/NullPointerException","symbol and buffer required");return 0;}
 if((*env)->GetStringUTFLength(env,name)>128){failure(env,"java/lang/IllegalArgumentException","symbol too long");return 0;}
 jlong size=(*env)->GetDirectBufferCapacity(env,buffer);void* bytes=(*env)->GetDirectBufferAddress(env,buffer);
 if(size<0||(size>0&&!bytes)){failure(env,"java/lang/IllegalArgumentException","direct buffer required");return 0;}
 const char* symbol=(*env)->GetStringUTFChars(env,name,NULL);if(!symbol)return 0;
 // Only this known function has the signature invoked below. Other symbol
 // names are looked up solely as absence controls, never cast and executed.
 int known=strcmp(symbol,"ps5_client_checksum")==0;
 void* library=self_library();void* address=library?SYMBOL(library,symbol):NULL;
 (*env)->ReleaseStringUTFChars(env,name,symbol);
 if(!library){failure(env,"java/lang/UnsatisfiedLinkError","resident client library unavailable");return 0;}
 if(!address||!known){CLOSE(library);failure(env,"java/lang/UnsatisfiedLinkError","checksum export unavailable");return 0;}
 uint64_t (*checksum)(const unsigned char*,size_t)=(uint64_t(*)(const unsigned char*,size_t))address;
 uint64_t result=checksum(bytes,(size_t)size);
 int closed=CLOSE(library);
 if(closed!=0){failure(env,"java/lang/UnsatisfiedLinkError","resident handle close failed");return 0;}
 return (jlong)result;
}
