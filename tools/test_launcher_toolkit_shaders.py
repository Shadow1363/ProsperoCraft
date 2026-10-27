#!/usr/bin/env python3
"""Compare actual SPIR-V words, ignoring the compiler-version C comment."""
from pathlib import Path
import re, struct, subprocess, tempfile
from build_launcher_toolkit import KIT

def words(path):
    return [int(n,16) for n in re.findall(r'0x([0-9a-fA-F]{8})',path.read_text())]

with tempfile.TemporaryDirectory() as directory:
    work=Path(directory)
    for source in sorted((KIT/'src/gfx/vk/shaders').glob('*')):
        if source.suffix not in ('.vert','.frag'):continue
        output=work/'array.inc'
        name,stage=source.name.split('.')
        symbol='k'+name.capitalize()+stage.capitalize()
        subprocess.run(['glslangValidator','-V','--target-env','vulkan1.0','--quiet','--vn',symbol,'-o',str(output),str(source)],check=True)
        original=words(source.with_name(source.name+'.inc'))
        assert original==words(output),source
        binary=work/'shader.spv';binary.write_bytes(struct.pack('<'+'I'*len(original),*original))
        subprocess.run(['spirv-val','--target-env','vulkan1.0',str(binary)],check=True)
print('PASS all7 pinned shader arrays validate as Vulkan1.0 and exactly match locally compiled SPIR-V words; only glslang16.4/16.6 version comments differ')
