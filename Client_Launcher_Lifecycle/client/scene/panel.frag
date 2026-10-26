#version 450
layout(set=0,binding=0) uniform sampler2D sourceTexture;
layout(location=0) in vec2 textureUV;
layout(push_constant) uniform Parameters { vec4 rgba; float depth; uint mode; } p;
layout(location=0) out vec4 color;
void main(){color=p.mode==0u?texture(sourceTexture,textureUV):p.rgba;}
