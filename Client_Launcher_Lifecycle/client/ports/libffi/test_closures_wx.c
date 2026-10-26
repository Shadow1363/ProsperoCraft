/* MIT. Fault/protection tests for allocation adapter only;not a libffi ABI test. */
#include <ffi.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <errno.h>
#include <unistd.h>
#include <sys/mman.h>
static int fail_map,fail_protect,fail_prep,maps,unmaps;
void*test_mmap(void*a,size_t n,int p,int f,int d,off_t o){if(fail_map){errno=ENOMEM;return MAP_FAILED;}assert(p==(PROT_READ|PROT_WRITE));void*r=mmap(a,n,p,f,d,o);if(r!=MAP_FAILED)maps++;return r;}
int test_mprotect(void*a,size_t n,int p){assert(p==(PROT_READ|PROT_EXEC));if(fail_protect){errno=EACCES;return -1;}return mprotect(a,n,p);}
int test_munmap(void*a,size_t n){int rc=munmap(a,n);if(!rc)unmaps++;return rc;}
ffi_status ps5ffi_prep_closure_loc_impl(ffi_closure*c,ffi_cif*cif,void(*fn)(ffi_cif*,void*,void**,void*),void*data,void*code){
 (void)c;(void)cif;(void)fn;(void)data;if(fail_prep)return FFI_BAD_TYPEDEF;
#if defined(__aarch64__) || defined(__arm64__)
 uint32_t bytes[]={0x52800320,0xd65f03c0};
#else
 unsigned char bytes[]={0xb8,25,0,0,0,0xc3};
#endif
 memcpy(code,bytes,sizeof(bytes));return FFI_OK;
}
static void note(ffi_cif*a,void*b,void**c,void*d){(void)a;(void)b;(void)c;(void)d;}
int main(void){
 void*code=(void*)1;assert(!ffi_closure_alloc(sizeof(ffi_closure),NULL));assert(!ffi_closure_alloc(0,&code)&&!code);code=(void*)1;assert(!ffi_closure_alloc((size_t)-1,&code)&&!code);
 fail_map=1;assert(!ffi_closure_alloc(sizeof(ffi_closure),&code)&&!code&&errno==ENOMEM);fail_map=0;
 ffi_cif cif;memset(&cif,0,sizeof(cif));
 for(int i=0;i<3;++i){ffi_closure*c=ffi_closure_alloc(sizeof(*c),&code);assert(c&&code==(void*)c);assert(ffi_prep_closure_loc(c,&cif,note,NULL,code)==FFI_OK);assert(((int(*)(void))code)()==25);assert(ffi_prep_closure_loc(c,&cif,note,NULL,code)!=FFI_OK);ffi_closure_free(c);}
 fail_protect=1;ffi_closure*c=ffi_closure_alloc(sizeof(*c),&code);assert(c&&ffi_prep_closure_loc(c,&cif,note,NULL,code)!=FFI_OK);ffi_closure_free(c);fail_protect=0;
 fail_prep=1;c=ffi_closure_alloc(sizeof(*c),&code);assert(c&&ffi_prep_closure_loc(c,&cif,note,NULL,code)!=FFI_OK);ffi_closure_free(c);ffi_closure_free(NULL);assert(maps==unmaps);
 printf("PASS W->X adapter:RW allocation/RX generated-code execution3cycles;NULL/zero/overflow/map/prep/protect failures,re-prep rejection and%d/%d mappings freed. This unit uses an explicit prep test double;real libffi/LWJGL ABI tested separately.\n",maps,unmaps);return 0;
}
