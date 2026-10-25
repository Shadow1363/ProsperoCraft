/* Project explicit resident initialization adapter. MIT license. */
#include <jni.h>
typedef void(*Initializer)(void);
extern Initializer __client_openal_init_start[],__client_openal_init_end[];
extern void client_gpu_stage(const char*,int);
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM*vm,void*reserved){
 (void)vm;(void)reserved;static int initialized;
 if(!initialized){for(Initializer*p=__client_openal_init_start;p!=__client_openal_init_end;++p)if(*p)(*p)();initialized=1;client_gpu_stage("Actual OpenAL Soft retained constructors initialized",0);}
 return JNI_VERSION_1_8;
}
