# Client Visible Perspective Scene 01.000.022 — candidate

022 retains the021 offscreen texture/depth/blend row and runtime compiler/GPU
baselines,adds a perspective/vertex-buffer row,and replaces the final SDL tile
presenter with a visible display of the verified GPU scene. Fifteen checks run:
earlier baselines,actual runtime shaderc,021 texture controls,new scene,SDL
physical input/presentation,then JVM shutdown. Frozen021 is preserved unchanged.

The scene uses six vertices in an actual host-visible Vulkan vertex buffer:
vec3 position and vec2 UV at a20byte stride. A tilted world-space panel has
camera-space Z2on the left and4on the right. The vertex shader performs a
positive-Z perspective projection (near1/far10,then a bounded depth remap for
the near/far controls). Ordinary perspective interpolation supplies UVs to a
nearest sampled2x2RGBA texture. An independent CPU barycentric1/W reference
checks all pixel centers in both triangles. This verifies perspective-correct
texture coordinates,not merely pre-divided positions or a procedural shader.
The inherited depth rejection,disabled-depth,alpha blend and disabled-blend
phases produce27draws/9full256x256images+256guards over3 sessions. All pixels
are checked within1UNORM rounding step per channel; no edge pixels are skipped.

After the normal phase of the final session is verified,its actual GPU readback
is copied into a Java byte array. The SDL fixture uploads those exact RGBA bytes
once into a real transfer image,then uses nearest vkCmdBlitImage into the BGRA
swapchain. This is an explicit GPU-render/readback/re-upload/blit handoff. No
CPU-rendered reference image is displayed,and this is not continuous scene
rendering directly into the swapchain. The scene is static; physical input is
still an acceptance check,not camera/gameplay control.

The visible image should be a pastel four-color perspective-textured panel
centered on a magenta background. It remains visible after PASS. The presenter
checks36actual swapchain samples and256guards each frame against the exact
source readback,at least90FIFO presents and both physical event/state masks15.
Full Vulkan blit capability/transfer-destination surface support is required;
unsupported capabilities produce an explicit failure. SDL/native display,image
and memory resources stay retained until app close as in the passing baseline.

Host validation: actual original LWJGL3.4.3 command bindings,MoltenVK GPU,
Java25 Xint/XcheckJNI/verification and native core UBSan. Three scene sessions/
27draws/9full-image+guard checks pass. A host-only hook additionally scales the
actual rendered image to128x96BGRA on the GPU and verifies every pixel against
actual source bytes. The hook changes only the host fixture after verification;
its SceneBlitHost25 companion is excluded from the target package. It validates
real conversion/scaling but does not exercise PS5 SDL/surface/WSI or signal that
console acceptance has occurred. New graphics shaders are compiled offline
and spirv-val validated; the separate existing shaderc row still compiles GLSL
at runtime with real error controls and18GPU dispatches.

Install PPSA99874 **01.000.022** from the runtime workspace's current
`dist/PPSA99874.zip` (consumer variant `dist/client-runtime_shader/PPSA99874.zip`).
Wait for Client022 ready,release X and press X once. Initial screen may be blank
while offscreen checks run. When prompted,press X,Circle,D-pad Left and move the
left stick strongly. Confirm **ALL15 PASS** and the textured panel on magenta.
If it fails,leave the app open; if it crashes,reopen without starting another
run to preserve reports. Installing replaces the shared-ID client/server app.

No music. Original54Java/game JARs,JVM/SDK source and previous native dependency
ports are unchanged. Existing paired C++ allocation and compiler diagnostics are
retained. Index buffers,filtering/mips,continuous/direct swapchain scene rendering,
camera movement,larger models/shaders,game startup and full native teardown remain
unvalidated. Server two-hour endurance stays explicitly deferred.

Target compile/link/package checks pass,including15-row order and packaged
companions,real vertex-buffer/blit native exports,scene shader hashes,host-only
verifier exclusion,paired C++ allocator/staged constructors,original54 JARs/
exact runtime libraries,CRC/signatures and preserved021/020/earlier/server
packages. PS5 all15 and visible scene acceptance remain pending.
Package SHA-256: `9d49135a4dcbd66e93ef496e442c7845964e08aa6664c9dc26546a94196e450e`.
