/* Project JNI callback acceptance helper. MIT license. */
#include <jni.h>
#include <stdint.h>
#include <pthread.h>
typedef int32_t(*Callback)(int32_t,int32_t,const void*,void*);
struct Work{Callback callback;int32_t sum;};
static void*work(void*ptr){struct Work*w=ptr;w->sum=0;for(int i=0;i<32;++i)w->sum+=w->callback(7,11,(void*)(uintptr_t)0x35,(void*)(uintptr_t)0x1234);return NULL;}
JNIEXPORT jint JNICALL Java_ClientNativeBootstrap25_invokeCallback(JNIEnv*e,jclass c,jlong address,jboolean threaded){
 (void)e;(void)c;if(!address)return -1;struct Work w={(Callback)(uintptr_t)address,0};
 if(threaded){pthread_t thread;int err=pthread_create(&thread,NULL,work,&w);if(err)return -err;err=pthread_join(thread,NULL);if(err)return -err;}else work(&w);
 return w.sum;
}
