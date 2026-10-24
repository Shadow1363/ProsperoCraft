#version 450
layout(location=0) in vec3 position;
layout(location=1) in vec2 uv;
layout(location=0) out vec2 textureUV;
layout(push_constant) uniform Parameters { vec4 rgba; float depth; uint mode; } p;
void main(){
    // Perspective divide by positive camera-space Z. Near1/far10 projection,
    // with bounded depth remap for the inherited near/far control draws.
    float z=(10.0/9.0)*position.z-10.0/9.0;
    gl_Position=vec4(position.xy,z*0.2+p.depth*position.z,position.z);
    textureUV=uv;
}
