/* Real host-JVM regression for the PS5 harness's DefineClass/method-lookup path. */
#include <jni.h>
#include <cassert>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iterator>
#include <string>
#include <vector>
int main(int argc,char **argv){
 assert(argc==4);bool present=std::strcmp(argv[3],"present")==0;
 std::string cp="-Djava.class.path="+std::string(argv[1]);
 JavaVMOption options[]={{const_cast<char*>("-Xint"),nullptr},{cp.data(),nullptr}};
 JavaVMInitArgs args{};args.version=JNI_VERSION_24;args.nOptions=2;args.options=options;
 JavaVM *vm=nullptr;JNIEnv *env=nullptr;assert(JNI_CreateJavaVM(&vm,reinterpret_cast<void**>(&env),&args)==JNI_OK);
 jclass lc=env->FindClass("java/lang/ClassLoader");auto get=env->GetStaticMethodID(lc,"getSystemClassLoader","()Ljava/lang/ClassLoader;");
 jobject loader=env->CallStaticObjectMethod(lc,get);assert(loader&&!env->ExceptionCheck());
 std::ifstream file(argv[2],std::ios::binary);assert(file);std::vector<char> bytes((std::istreambuf_iterator<char>(file)),{});
 jclass fixture=env->DefineClass("ServerStart25",loader,reinterpret_cast<const jbyte*>(bytes.data()),static_cast<jsize>(bytes.size()));assert(fixture&&!env->ExceptionCheck());
 auto method=env->GetStaticMethodID(fixture,"main","([Ljava/lang/String;)V");
 if(present){if(env->ExceptionCheck())env->ExceptionDescribe();assert(method&&!env->ExceptionCheck());}
 else {assert(!method&&env->ExceptionCheck());auto error=env->ExceptionOccurred();env->ExceptionClear();
  jclass throwable=env->FindClass("java/lang/Throwable");auto str=env->GetMethodID(throwable,"toString","()Ljava/lang/String;");auto message=static_cast<jstring>(env->CallObjectMethod(error,str));
  const char *text=env->GetStringUTFChars(message,nullptr);assert(std::strstr(text,"NoClassDefFoundError")&&std::strstr(text,"ServerStart25$Observer"));env->ReleaseStringUTFChars(message,text);
 }
 assert(vm->DestroyJavaVM()==JNI_OK);std::puts(present?"PASS: DefineClass main-method lookup resolves Observer from probe JAR":"PASS: absent helper reproduces exact ServerStart25$Observer lookup failure");
}
