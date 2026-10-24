#version 450
layout(push_constant) uniform Parameters { vec4 rgba; float depth; uint mode; } p;
void main(){vec2 positions[3]=vec2[](vec2(-1,-1),vec2(3,-1),vec2(-1,3));gl_Position=vec4(positions[gl_VertexIndex],p.depth,1);}
