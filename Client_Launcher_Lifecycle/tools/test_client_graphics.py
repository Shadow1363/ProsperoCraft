#!/usr/bin/env python3
"""Check native003 real package/ELF/imports, CPU card memory safety and frozen baselines.
GPU and VideoOut calls require the PS5 and are not simulated as a pass here.
"""
import argparse,hashlib,json,subprocess,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args();runtime=a.runtime_workspace.resolve()
sha=lambda data:hashlib.sha256(data).hexdigest()
package=ROOT/'dist/client-graphics/PPSA99874.zip';work=ROOT/'build/client-graphics'
with zipfile.ZipFile(package)as z:
 assert z.testzip()is None
 prefix='PPSA99874/';names=z.namelist()
 assert not any(n.endswith(('.jar','.so','.pcm','.at9'))for n in names)
 assert not any('/sounds/'in n or '/jars/'in n for n in names)
 param=json.loads(z.read(prefix+'sce_sys/param.json'));server=json.loads((ROOT/'server/param.json').read_text())
 assert param['contentVersion']=='01.000.003'
 assert all(param[k]==server[k]for k in ['titleId','contentId','conceptId'])
 assert z.read(prefix+'eboot.bin')==(work/'PPSA99874/eboot.bin').read_bytes()
 assert z.read(prefix+'sce_module/libc.prx')==(runtime/'build/native/libc.prx').read_bytes()
 audit=json.loads(z.read(prefix+'assets/graphics-audit.json'))
 assert audit['source_pins']==json.loads((ROOT/'client/graphics/sources.json').read_text())
 assert not audit['runtime_sdk_replaced'] and audit['console']=='pending'
 for name,path in [('radv_archive_sha256',ROOT/'build/graphics-radv/src/amd/vulkan/libvulkan_radeon.a'),('platform_archive_sha256',ROOT/'.tools/graphics-sdk/target/lib/libps5platform.a'),('host_recipe_sha256',work/'radv-link-host.sh')]:assert audit[name]==sha(path.read_bytes())
 for name,digest in audit['objects_sha256'].items():assert digest==sha((work/name).read_bytes())
 assert any('LLVM-LICENSE' in n for n in names) and any('Mesa-MIT' in n for n in names)
 assert b'Client003 ready: press X'in z.read(prefix+'eboot.bin')
 assert b'AUTOMATED CHECKS PASS:91 frames'in z.read(prefix+'eboot.bin')
 assert b'Human confirmation'in z.read(prefix+'eboot.bin')
 assert b'JNI_CreateJavaVM'not in z.read(prefix+'eboot.bin')
 assert (runtime/'dist/PPSA99874.zip').read_bytes()==package.read_bytes()
 assert (ROOT/'dist/client-graphics/SHA256SUMS').read_text().split()[0]==sha(package.read_bytes())
for path in [work/'PPSA99874/eboot.bin',work/'PPSA99874/sce_module/libc.prx']:
 out=subprocess.check_output([str(runtime/'build/native/host/ps5-native-tool'),'self','--inspect','--file',str(path)],text=True);assert 'integrity: valid'in out
elf=work/'llvm-pie.elf';llvm=Path('/opt/homebrew/opt/llvm/bin')
symbols=subprocess.check_output([str(llvm/'llvm-nm'),'--defined-only',str(elf)],text=True)
for name in ['vk_icdGetInstanceProcAddr','radv_CreateInstance','radv_CreateDevice','radv_CmdClearColorImage','vk_common_QueueSubmit','graphics_run','graphics_report','__cpu_indicator_init','__cpu_model','ps5_fp_ieee']:
 assert any(line.endswith(' '+name)for line in symbols.splitlines()),name
for name in ['sceAgcInit','sceAgcDriverSubmitDcb']:
 assert not any(line.endswith(' '+name)for line in symbols.splitlines()),'Accidentally linked executable AGC stub: '+name
needed=subprocess.check_output([str(llvm/'llvm-readelf'),'-d',str(elf)],text=True)
for library in ['libSceAgc.prx','libSceAgcDriver.prx','libSceVideoOut.sprx','libScePad.sprx']:
 assert library in needed,library
for folder,digest in [('Client_Foundation-01.000.000','e2eb90a727fc670418437937b292b152c5177e3e02077aa114049bc6c9c11fbf'),('Client_Native_Loading-01.000.001','abc6aef0f162d9d134dec298742f27dfdb91a80345bb81ac54498239d34fd890'),('Client_LWJGL_Core-01.000.002','d0b9f815ff68c5ad821b2166509879c623c813019d2f70bbacf53769f35e3971')]:
 assert sha((ROOT/'dist/milestones'/folder/'PPSA99874-full-local.zip').read_bytes())==digest
for version,digest in [('094','97ec74c40b9c495884130f9dae0ab10bf393e521265cbe82177f06190176df2d'),('108','18dc7f06d59ff11b33c7e96b85f813a28a2cb19638fe0d6eacfd4224513781e7')]:
 assert sha((runtime/'build/java25'/f'PPSA99874-{version}-full-local.zip').read_bytes())==digest
# Exercise actual card/text pixel writer with address/undefined sanitizers at
# its minimum, normal,4K and maximum accepted extents; guards catch overruns.
with tempfile.TemporaryDirectory(prefix='graphics-card-')as tmp:
 tmp=Path(tmp);source=tmp/'card.c'
 source.write_text('#include "'+str(ROOT/'client/graphics/presentation.c')+'"\n'+r'''
#include <assert.h>
void graphics_report(const char *name,int result){(void)name;(void)result;}
int main(void){
 const unsigned sizes[][2]={{640,480},{1920,1080},{3840,2160},{7680,4320}};
 for(unsigned n=0;n<4;n++){
  extent.width=sizes[n][0];extent.height=sizes[n][1];
  size_t bytes=(size_t)extent.width*extent.height*4;
  unsigned char *allocation=malloc(bytes+128);assert(allocation);
  memset(allocation,0xa5,bytes+128);mapped=allocation+64;card();
  for(unsigned i=0;i<64;i++)assert(allocation[i]==0xa5&&allocation[bytes+64+i]==0xa5);
  for(size_t i=3;i<bytes;i+=4)assert(mapped[i]==255);
  assert(mapped[0]==128&&mapped[1]==96&&mapped[2]==16);
  assert(mapped[bytes-4]==24&&mapped[bytes-3]==48&&mapped[bytes-2]==16);
  if(n==1){
   FILE *f=fopen("card.ppm","wb");assert(f);fprintf(f,"P6\n%u %u\n255\n",extent.width,extent.height);
   for(size_t i=0;i<bytes;i+=4){fputc(mapped[i+2],f);fputc(mapped[i+1],f);fputc(mapped[i],f);}fclose(f);
  }
  free(allocation);
 }
 return 0;
}
''')
 subprocess.run([str(llvm/'clang'),'-std=c11','-O1','-g','-fsanitize=address,undefined','-ffunction-sections','-fdata-sections','-Wl,-dead_strip','-I'+str(ROOT/'.tools/PS5_Mesa/include'),str(source),'-o',str(tmp/'test')],check=True)
 subprocess.run([str(tmp/'test')],cwd=tmp,check=True)
 import shutil
 shutil.copyfile(tmp/'card.ppm',work/'card.ppm')
print('PASS native003 CRC/signatures/shared title/real RADV exports and AGC imports/no game or Java/no shipped stubs/source-object hashes/frozen000-002/Fabric094/Paper108; actual card ASan/UBSan at640x480 through8K. GPU/PS5 console pending. SHA256',sha(package.read_bytes()))
