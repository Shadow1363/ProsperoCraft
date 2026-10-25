/* Project PS5 platform allocation adapter for genuine libffi. MIT license. */
#include <ffi.h>
#include <stdint.h>
#include <stddef.h>
#include <errno.h>
#include <unistd.h>
#include <sys/mman.h>
#include <string.h>
#define MAGIC UINT64_C(0x5053354646495758)
#define OFFSET 64u
struct Header {uint64_t magic;size_t length;int prepared;};
extern ffi_status ps5ffi_prep_closure_loc_impl(ffi_closure*,ffi_cif*,void(*)(ffi_cif*,void*,void**,void*),void*,void*);
static struct Header* header(void*p){return (struct Header*)((char*)p-OFFSET);}
void* ffi_closure_alloc(size_t size,void**code){
 if(!code){errno=EINVAL;return NULL;}*code=NULL;
 long page=sysconf(_SC_PAGESIZE);if(page<=(long)OFFSET||size==0||size>(size_t)page-OFFSET){errno=EINVAL;return NULL;}
 void*base=mmap(NULL,(size_t)page,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANON,-1,0);if(base==MAP_FAILED)return NULL;
 struct Header*h=base;h->magic=MAGIC;h->length=(size_t)page;h->prepared=0;void*p=(char*)base+OFFSET;*code=p;return p;
}
void ffi_closure_free(void*p){if(!p)return;struct Header*h=header(p);if(h->magic!=MAGIC)return;(void)munmap(h,h->length);}
void* ffi_data_to_code_pointer(void*p){return p;}
int ffi_tramp_is_present(void*p){(void)p;return 0;}
ffi_status ffi_prep_closure_loc(ffi_closure*c,ffi_cif*cif,void(*fun)(ffi_cif*,void*,void**,void*),void*data,void*code){
 if(!c||!cif||!fun||code!=(void*)c)return FFI_BAD_TYPEDEF;
 struct Header*h=header(c);if(h->magic!=MAGIC||h->prepared)return FFI_BAD_TYPEDEF;
 ffi_status result=ps5ffi_prep_closure_loc_impl(c,cif,fun,data,code);if(result!=FFI_OK)return result;
 h->prepared=1;__builtin___clear_cache((char*)c,(char*)c+sizeof(*c));
 if(mprotect(h,h->length,PROT_READ|PROT_EXEC)!=0){h->prepared=0;return FFI_BAD_TYPEDEF;}
 return FFI_OK;
}
