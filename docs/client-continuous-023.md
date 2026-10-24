# Client Continuous Direct Scene 01.000.023 — PS5 candidate

023 replaces022's static readback/upload/blit display path with real scene draws
into each acquired SDL BGRA swapchain image. Fifteen acceptance rows remain:
all earlier runtime/compiler/texture/perspective checks,then the new continuous
SDL presenter and JVM shutdown. Frozen022 package/source/symbols stay preserved.

ClientDirectScene25 borrows the actual SDL device/swapchain images. It creates
image views/framebuffers,a D32 depth attachment,a six-vertex position/UV buffer,
a real2x2sampled texture/descriptor,and three graphics pipelines. The texture
is uploaded once. Every acquired frame transitions the swapchain image to color
attachment layout,records three perspective/depth/blend draws directly into
that image,reads36pixel samples plus256guards,transitions to present layout
and FIFO-presents. There is no captured-scene upload,no blit and no CPU-generated
image. The older offscreen022 baseline still creates its readback for its own
acceptance row; the new presenter does not read it.

The display cycles three phases every60frames:pastel sampled panel with depth
rejection and white alpha blend,blue control with depth disabled for the farther
layer,then white control with blending disabled. Magenta remains outside the
panel. At least180frames must complete so all three phases run,plus physical
X/Circle/D-pad Left/strong left-stick event AND state masks15. Each frame's
actual pixel samples are checked within1UNORM rounding step per channel against
an independent perspective barycentric1/W reference at the actual display size.
This establishes a controlled direct rendering workload if it passes; there is
no camera movement/gameplay mapping yet.

One frame is submitted at a time and its completion fence is waited before
next-frame recording. The acquire wait stage is color-attachment output and
render-finished semaphores remain per swapchain image. Native display/renderer
resources are retained through JVM shutdown until app close; full destruction,
reacquisition/resize/focus/reconnect and timeout recovery remain unvalidated.

Host test uses the same ClientDirectScene25 record/setup code with real BGRA
offscreen targets. Original LWJGL3.4.3 command bindings,MoltenVK GPU and Java25
Xint/XcheckJNI/verification/core UBSan pass81draws/27full256x256BGRA images and
guards across3sessions/all3phases. Host completion is followed by renderer
resource cleanup. The host-specific fixture is excluded from the PS5 package.
Host offscreen targets do not exercise PS5 SDL/WSI/swapchain/display or native
resource retention. New shader compilation is not needed:the proven022 offline
vertex/fragment modules are reused; runtime shaderc controls remain a separate
acceptance row. Target all15 and visual phase checks remain pending.

Install PPSA99874 **01.000.023** from the runtime workspace's current
`dist/PPSA99874.zip` (consumer variant `dist/client-runtime_shader/PPSA99874.zip`).
Wait for Client023 ready,release X and press X once. After offscreen checks,
look for the panel cycling pastel/blue/white on magenta. When prompted,press X,
Circle,D-pad Left and move the left stick strongly. Confirm **ALL15 PASS** and
that the three visual phases appeared without corruption. The final image
stays visible; the app stops rendering after acceptance/JVM shutdown. If it
fails,leave it open;if it crashes,reopen without running again to preserve logs.

Same shared title ID;installing replaces the client/server app. No music.
Original54Java/game JARs,JVM/SDK source and prior native dependency ports remain
unchanged. Existing paired C++ allocation and compiler diagnostics stay active.
Camera controls,index buffers,filtering/mips,larger models/shaders,game startup,
complete SDL/Vulkan coverage,global teardown and prolonged/low-memory robustness
remain unvalidated. Server two-hour endurance stays explicitly deferred.

Target compile/link/package verification passes,including explicit direct
renderer companion,actual draw/vertex/renderpass bytecode and shader hashes,
absence of scene upload/blit references in the presenter,host-only fixture
exclusion,original JARs/exact runtime libraries,paired allocation and staged
constructors,CRC/signatures and all frozen022/earlier/server packages.
PS5 all15 and visible phase acceptance remain pending.
Package SHA-256: `846cd9adea6f9e6b04f80df461424c26b1fec6aa080ed641c35e7cfb16488ea4`.

## Human console acceptance2026-10-24

User “PASS” follows the explicit023 fifteen-check and pastel/blue/white phase
instructions. Exact source/package/symbols are frozen in Client_Continuous_Direct_Scene.
Current-run log downloads were refused;no independently corroborated run ID,
frame count or detailed stage completion is claimed. Human acceptance is kept
separate from host/package checks and the still-pending report retrieval.
