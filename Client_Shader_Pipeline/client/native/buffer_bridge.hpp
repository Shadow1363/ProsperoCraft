/* SPDX-License-Identifier: GPL-3.0-or-later */
#pragma once
#include <jni.h>
#include <cstdint>
#include <cstring>
#include <unistd.h>
inline jlong client_bridge_page_size(JNIEnv*,jclass) {return sysconf(_SC_PAGESIZE);}
inline jlong client_bridge_fill(JNIEnv* env,jclass,jobject buffer,jlong seed) {
 if(!buffer) {jclass c=env->FindClass("java/lang/NullPointerException");if(c)env->ThrowNew(c,"direct buffer");return 0;}
 jlong capacity=env->GetDirectBufferCapacity(buffer);
 void* data=env->GetDirectBufferAddress(buffer);
 if(capacity<0 || (capacity>0&&!data)) {jclass c=env->FindClass("java/lang/IllegalArgumentException");if(c)env->ThrowNew(c,"direct ByteBuffer required");return 0;}
 // This synchronous call borrows the buffer only while its JNI reference is live.
 // No address escapes, no allocation/free ownership transfers and no GPU claim.
 auto* bytes=static_cast<unsigned char*>(data);std::uint64_t sum=0;
 for(jlong i=0;i<capacity;++i) {
  unsigned char value=static_cast<unsigned char>(static_cast<std::uint64_t>(seed)+static_cast<std::uint64_t>(i)*17);
  bytes[i]=value;sum+=value;
 }
 return static_cast<jlong>(sum);
}
