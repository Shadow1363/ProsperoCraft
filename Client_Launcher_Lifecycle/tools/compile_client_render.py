#!/usr/bin/env python3
"""Compile the consumer canary GLSL to validated SPIR-V and Java fixture data."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def compile_render():
    out=ROOT/'build/client-render';out.mkdir(parents=True,exist_ok=True)
    files=[];methods=[]
    for name,method in [('fullscreen.vert','vertex'),('pattern.frag','fragment')]:
        source=ROOT/'client/render'/name;binary=out/(name+'.spv')
        subprocess.run(['/opt/homebrew/bin/glslangValidator','-V','--target-env','vulkan1.1','-o',str(binary),str(source)],check=True)
        subprocess.run(['/opt/homebrew/bin/spirv-val','--target-env','vulkan1.1',str(binary)],check=True)
        data=binary.read_bytes();assert len(data)%4==0 and data[:4]==b'\x03\x02\x23\x07'
        words=[int.from_bytes(data[i:i+4],'little')for i in range(0,len(data),4)]
        methods.append('public static ByteBuffer '+method+'(MemoryStack stack){int[] words={'+','.join('0x%08x'%v for v in words)+'};ByteBuffer b=stack.malloc(words.length*4).order(ByteOrder.nativeOrder());for(int v:words)b.putInt(v);return b.flip();}')
        files.append({'source':name,'glsl_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'spirv_sha256':hashlib.sha256(data).hexdigest(),'spirv_bytes':len(data)})
    java=out/'ClientRenderCode25.java';java.write_text('import java.nio.*;import org.lwjgl.system.MemoryStack;\npublic final class ClientRenderCode25 {\n'+'\n'.join(methods)+'\n}\n')
    audit={'files':files,'compiler':subprocess.check_output(['/opt/homebrew/bin/glslangValidator','--version'],text=True),'validation':'Both SPIR-V modules pass spirv-val --target-env vulkan1.1','scope':'Offline GLSL->SPIR-V; actual graphics-pipeline GPU compilation occurs in RADV. Image readback is shown through existing CPU menu; no SDL or swapchain integration.'}
    (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');return java
if __name__=='__main__':compile_render()
