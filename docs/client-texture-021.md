# Client Texture/Depth/Blend 01.000.021 — PS5 candidate

021 retains every020 runtime/compiler/GPU/SDL/JVM acceptance row and adds one
real Vulkan texture/depth/blend row. Fourteen checks run in this order: earlier
runtime/native/GPU baselines,actual runtime GLSL compiler,new texture workload,
SDL display/physical inputs,then JVM shutdown. The new row uses offscreen GPU
readback; the visible SDL tiles and input prompts remain the passing baseline.
It does not display a textured game scene or launch Minecraft.

The fixture uploads an original2x2 RGBA test texture through a host-visible
staging buffer into a real optimal-tiled sampled image. An actual combined
image/sampler descriptor is bound to a fragment shader using texelFetch. A
D32_SFLOAT depth image is attached to the render pass. Three pipelines exercise
LESS depth testing/writes,disabled depth,and standard source-alpha blending.

Each of three phases draws the sampled texture at depth0.25,then a farther
solid-blue layer at0.75,and a half-alpha white layer. Phase0 must retain the
near texture through depth rejection,then blend white. Phase1 disables depth
for the farther blue draw and must yield blended blue. Phase2 disables blending
for the white draw and must produce white with half alpha. Every pixel in each
256x256 image and256 guard bytes is verified; at most1 UNORM rounding step is
allowed per channel. Texture quadrants,depth and blend controls differ so a
missing descriptor/depth/blend effect cannot silently pass.

Three upload/device/resource lifecycles produce27 draws and9 fully verified
images. Explicit buffer/image dependencies cover upload,shader sampling,color/
depth writes and host readback. Resources are destroyed after completed GPU
work; incomplete submissions remain retained rather than freed while active.
Two new vertex/fragment GLSL modules are compiled offline with glslangValidator
and checked by spirv-val. The existing020 row separately retains real runtime
shaderc compilation/error controls and18 GPU output checks. This new row does
not claim runtime compilation of its graphics shaders or filtering coverage.

Host validation uses the real original LWJGL Vulkan bindings and actual
MoltenVK GPU on this Mac under Java25 Xint/XcheckJNI/verification with core
UBSan. All3 uploads/27draws/9full-image and guard checks pass. Target PS5 build
and console validation are separate; no new passing milestone is established.

Install PPSA99874 **01.000.021** from the runtime workspace's current
`dist/PPSA99874.zip` (consumer build path `dist/client-runtime_shader/PPSA99874.zip`).
The existing runtime_shader development variant now includes the texture row;
no passing020 package is replaced. Wait for Client021 ready,release X and press
X once. Offscreen compiler/texture tests run first. At SDL Input ready,press X,
Circle,D-pad Left and move the left stick strongly. Confirm the final PASS
notification and visible tiles. If it fails,leave it open; if it crashes,reopen
without running another test to preserve reports.

Same shared title ID PPSA99874; installing replaces the client/server app.
Music remains absent. Original54 Java/game JARs,JVM/SDK source and prior native
dependency ports remain unchanged; existing020 paired C++ allocation and native
compiler diagnostics are retained. Frozen020 exact package/source/symbols stay
preserved. Texture filtering/mips,vertex buffers,indexing,perspective,larger
workloads,SDL teardown,actual game startup and deferred server endurance require
separate validation.

Target package/CRC/signature checks pass,including texture shader module hashes,
real native exports,14-row order and explicit companion loading,paired C++
allocation and staged constructors,54original JARs/exact runtime libraries and
frozen020/earlier/server package preservation. PS5 validation remains pending.
Package SHA-256: `5adbcd8dda4e355c69ab027c4630c0603bb095250e9afb2251e678ce9e58bc81`.

## Console acceptance2026-10-24

Human “nice pass!” and retrieved run client-01.000.021-1792844052-984973201
confirm ALL14 PASS:3uploads/27draws/9full images+guards,depth/blend controls,
existing runtime compiler baseline,SDL318frames/event/state masks15 and JVM stop.
The exact source/package/symbols are frozen in Client_Texture_Depth_Blend.
Earlier pending statements describe the pre-test candidate; the frozen
validation record establishes the subsequent pass and its limits.
