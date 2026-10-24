#version 450
layout(push_constant) uniform Parameters { uint phase; } parameters;
layout(location=0) out vec4 color;
void main() {
    uvec2 p=uvec2(gl_FragCoord.xy);
    if(p.x<16u||p.y<16u||p.x>=240u||p.y>=240u) color=vec4(0,0,0,1);
    else if(abs(int(p.x)-int(p.y))<3) color=vec4(1,1,1,1);
    else {
        uint index=((p.x/32u)+(p.y/32u)+parameters.phase)%4u;
        color=index==0u?vec4(1,0,0,1):index==1u?vec4(0,1,0,1):index==2u?vec4(0,0,1,1):vec4(1,1,0,1);
    }
}
