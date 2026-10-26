/* Real Mesa context helper for host acceptance, never a fake GL provider. */
#include <jni.h>
#include <stdint.h>
#include <GL/osmesa.h>
JNIEXPORT jlong JNICALL Java_ClientOpenGL25_create(JNIEnv *env, jclass cls, jobject buffer) {
    (void)cls;
    void *pixels = (*env)->GetDirectBufferAddress(env, buffer);
    if (!pixels || (*env)->GetDirectBufferCapacity(env, buffer) < 8*8*4) return 0;
    const int attrs[] = {OSMESA_FORMAT, OSMESA_RGBA, OSMESA_PROFILE,
        OSMESA_CORE_PROFILE, OSMESA_CONTEXT_MAJOR_VERSION, 3,
        OSMESA_CONTEXT_MINOR_VERSION, 3, 0};
    OSMesaContext context = OSMesaCreateContextAttribs(attrs, NULL);
    if (context && !OSMesaMakeCurrent(context, pixels, GL_UNSIGNED_BYTE, 8, 8)) {
        OSMesaDestroyContext(context);
        return 0;
    }
    return (jlong)(uintptr_t)context;
}
JNIEXPORT void JNICALL Java_ClientOpenGL25_destroy(JNIEnv *env, jclass cls, jlong context) {
    (void)env; (void)cls;
    OSMesaMakeCurrent(NULL, NULL, GL_UNSIGNED_BYTE, 0, 0);
    OSMesaDestroyContext((OSMesaContext)(uintptr_t)context);
}

extern void client_gpu_stage(const char *, int);
JNIEXPORT void JNICALL Java_ClientOpenGL25_checkpoint(JNIEnv *env, jclass cls, jstring text) {
    (void)cls;
    const char *message = (*env)->GetStringUTFChars(env, text, NULL);
    if (message) {client_gpu_stage(message, 0); (*env)->ReleaseStringUTFChars(env, text, message);}
}
