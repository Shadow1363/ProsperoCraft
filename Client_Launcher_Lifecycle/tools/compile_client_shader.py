#!/usr/bin/env python3
"""Compile the consumer canary GLSL to validated SPIR-V and Java fixture data."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def compile_shader():
    out=ROOT/'build/client-shader';out.mkdir(parents=True,exist_ok=True)
    source=ROOT/'client/shader/workload.comp';binary=out/'workload.spv'
    subprocess.run(['/opt/homebrew/bin/glslangValidator','-V','--target-env','vulkan1.1','-o',str(binary),str(source)],check=True)
    subprocess.run(['/opt/homebrew/bin/spirv-val','--target-env','vulkan1.1',str(binary)],check=True)
    data=binary.read_bytes();assert len(data)%4==0 and data[:4]==b'\x03\x02\x23\x07'
    words=[int.from_bytes(data[i:i+4],'little')for i in range(0,len(data),4)]
    java=out/'ClientShaderCode25.java'
    java.write_text('import java.nio.*;import org.lwjgl.system.MemoryStack;\npublic final class ClientShaderCode25 {\n private static final int[] WORDS={'+','.join('0x%08x'%v for v in words)+'};\n public static ByteBuffer code(MemoryStack stack){ByteBuffer b=stack.malloc(WORDS.length*4).order(ByteOrder.nativeOrder());for(int v:WORDS)b.putInt(v);return b.flip();}\n}\n')
    audit={'glsl_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'spirv_sha256':hashlib.sha256(data).hexdigest(),'spirv_bytes':len(data),'compiler':subprocess.check_output(['/opt/homebrew/bin/glslangValidator','--version'],text=True),'validation':'spirv-val --target-env vulkan1.1 PASS','scope':'Offline GLSL->SPIR-V fixture; actual SPIR-V->GPU compilation remains in target RADV vkCreateComputePipelines; no shaderc/game launch'}
    (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');return java
if __name__=='__main__':compile_shader()
