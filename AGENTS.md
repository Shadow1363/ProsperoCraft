# Minecraft project scope

This repository contains Minecraft-specific PS5 homebrew work. Java runtime
fixes and acceptance probes belong in mateo-cogeanu/ps5-java25-homebrew;
reference that project instead of copying its runtime development here.

The human user authorized this public repository and publishing its README.
Keep README status accurate: Java probe passes do not establish a Minecraft
pass. Freeze a game milestone only after the user confirms its tests passed
on the actual PS5 for the exact build. Preserve passing snapshots and record
versions, dependencies, console evidence and package SHA-256 checksums.

Keep the README and its docs/readme-banner.svg consistent with project status.
Preserve the Java runtime link. Commit and push completed, authorized changes,
verify successful publication and report any failures honestly. Keep generated
builds, dependency caches, credentials, logs and unrelated files out of source
control. Passing compiled packages belong in release assets.

After every completed Minecraft source, asset, documentation, configuration
or script change, run the relevant checks, then commit and push to this
repository before ending the turn. Development can be published before
console validation; mark results pending. The user explicitly authorized
these updates. Verify each push. Runtime fixes must be published separately
to ps5-java25-homebrew using its sync script; do not mix source ownership.
Keep official downloaded JARs in ignored caches/local build packages,
with source-controlled artifact metadata and checksums for reproduction.
The initial --help bootstrap probe must not auto-accept the EULA or claim
world/server readiness from host success.

Server_Bootstrap is the frozen passing 01.000.002 snapshot. Do not modify it.
The human accepted the Minecraft EULA for the server test on 2026-10-14,
recorded in server/eula-consent.json. Development server-start code lives
in server/ and tools/. Retain passing full packages under ignored
dist/milestones before replacing the current build. Public releases omit
official game JARs and document local provisioning and separate checksums.

## Unmodified Minecraft server JAR direction

The user requires future compatibility fixes and features to live in the Java
port or the separately maintained Minecraft harness/configuration. Do not add
or expand server-JAR transformations, bytecode hooks or replacement game classes.
Keep the official downloaded server JAR intact. Existing local derivative
transformations are temporary migration debt, not the preferred architecture.

Gradually remove the existing transformations as working replacements are
implemented and validated. Move runtime compatibility into the Java port; use
vanilla configuration, ops.json and supported administration mechanisms for
Minecraft policy where possible. Do not silently remove required workarounds
or claim an unmodified server while a derivative is still executed. Record
each remaining transformation and console validation needed for its removal.
Preserve frozen passing snapshots; migrate development only.

## Work order requested on 2026-10-19

Prioritize smooth, stable server gameplay and completion of the migration to
the original unmodified server JAR. Establish actual PS5 startup, player save/
rejoin persistence and the requested two-hour baseline. Then work on server-side
mod loaders and individually validated mods for compatible pinned versions.
Client graphics, native bindings and input come after server mods work.
Track mihawk-99/PS5_Vulkan as a client graphics candidate; it is not an adopted
or validated project dependency. Keep game/mod/client plans in this repository.

## User work-order update on 2026-10-20

The user reports lag-free joined gameplay on083 and explicitly defers the
full two-hour run until later. Proceed with Fabric server/mod validation, then
Paper server/plugin validation, before client work. This overrides the earlier
requirement to finish the two-hour run before beginning server loaders. Keep
083 as a vanilla fallback and keep endurance/persistence limitations explicit.
Fabric/Paper are separate server flavors; use isolated worlds and pinned upstream
distributions. Do not add project-specific game-JAR rewrites or game replacement
classes. Standard upstream loader/Mixin behavior is part of the authorized mod
experiment and must be disclosed. Paper executes its own upstream server rather
than claiming to execute an unmodified Mojang server. No new passing milestone
is established by the083performance report alone.

## User work-order update on 2026-10-21

The user is satisfied with the Fabric experience and requests Paper next.
Validate the pinned upstream Paper distribution and a separate plugin on PS5;
once its exact candidate is confirmed passing, prepare and publish a proper
server release before client work. Do not infer a formal ALL PASS or full
two-hour completion from the satisfaction report. Preserve the Fabric094
candidate/package and vanilla083 fallback. Keep the two-hour test deferred.
Paper's upstream System.exit on shutdown is normal; report checked shutdown
evidence and distinguish a user-shortened play check from full endurance.

## User work-order update on 2026-10-22

The user reports Paper108 is much more than acceptable and by far the best yet,
after earlier satisfaction with Fabric094. The user now explicitly authorizes
client work while leaving the two-hour run pending, and requests a release
celebrating Fabric and Paper running before proceeding. Publish the accurately
qualified development prerelease and app-only artifacts; do not infer a formal
ALL PASS, completed lifecycle checklist or endurance result. Preserve exact
server packages/frozen milestones. Client work need not wait for those pending
server checks. Keep client code/artifact pins/graphics integration here and
reusable runtime fixes in the Java repository.

The user subsequently explicitly requested making Fabric-Paper-v01.000.108 a full
release, then continuing client work. Promote its GitHub release status without
inferring new console tests or ALL PASS. Keep endurance/lifecycle limitations
explicit and preserve the exact published app binaries and source tag.

The user requests reusing server title ID PPSA99874 and the same content identity
for client builds, but explicitly wants client versions to start at01.000.000
and advance independently of server versions. Do not continue the server build
counter for client packages.
Installing the client replaces the server app. Preserve tested server packages
and source snapshots for reinstalling; do not claim side-by-side installation.

Client_Foundation is the frozen passing client foundation milestone, PPSA99874
version01.000.000, user ALL PASS on2026-10-22. Preserve its source snapshot,
validation and matching compiled package. Its six foundation checks do not
establish game startup, GPU rendering, SDL/Vulkan/audio or controller gameplay.
Continue new client work in root client/, never inside Client_Foundation/.

Client_Native_Loading is the frozen passing client001 milestone, PPSA99874
version01.000.001, human ALL PASS for all seven rows on2026-10-22. Preserve
its source, validation and exact compiled package. It validates this resident
JNI loading/function-call integration, not full LWJGL/native graphics, arbitrary
ELF loading or Minecraft startup. Continue future work outside frozen folders.

Client_LWJGL_Core is the frozen passing client002 milestone, PPSA99874
version01.000.002, human ALL PASS for all eight rows on2026-10-23. Preserve
its source, validation and exact compiled package. It validates the tested
LWJGL native memory/JNI subset and PS5 resident provider; it does not establish
complete native bindings, arbitrary ELF loading, GPU/SDL/Vulkan or game startup.
Continue development outside frozen milestone folders.

Client_Native_Graphics is the frozen passing native-only client003 milestone,
PPSA99874 version01.000.003, human confirmation of all requested RGB/card checks
with no crash/corruption on2026-10-23. Preserve source, validation and exact
compiled package. It validates scoped RADV GPU clear/copy/readback and VideoOut
presentation, not Java/SDL integration, shader rendering, full Vulkan coverage
or game startup. No log retrieval was possible; evidence is the human report.
Continue development outside frozen folders.

Client_GPU_Integration is the frozen passing client004 milestone, PPSA99874
version01.000.004, user ALL PASS for all nine rows on2026-10-23. Preserve its
source, validation, exact package and symbols. It validates actual Java/LWJGL
plus resident JNI/RADV offscreen GPU copy/fill/readback, scoped provider/TLS
callback integration, three Vulkan session cycles and final JVM shutdown.
It does not establish full LWJGL Vulkan bindings, SDL/window integration,
shader/game rendering, full module cleanup or server endurance. Continue
development outside frozen folders.

Client_Vulkan_Bindings is the frozen passing client008 milestone, PPSA99874
version01.000.008, user ALL PASS for all ten rows on2026-10-24. Retrieved current-run
logs corroborate12 standard LWJGL Vulkan GPU transfers,3 instance/device lifecycles,
loader cleanup and DestroyJavaVM. Preserve source, exact package and symbols.
This validates the tested original LWJGL Vulkan command/struct/capability-table
path and diagnostic storage recovery, not complete Vulkan coverage, SDL/window
integration, Java presentation, shaders or game startup. Continue development
outside frozen folders; server two-hour endurance remains deferred.

Client_Shader_Pipeline is the frozen passing client009 milestone, PPSA99874
version01.000.009, user ALL PASS for all eleven rows on2026-10-24. Retrieved logs
confirm18 actual LWJGL/RADV compute shader dispatches, output/guard verification,
three shader/device lifecycles and DestroyJavaVM. Preserve source/package/symbols.
This is offscreen compute, not SDL/window integration, visible graphics/fragment
rendering, Java display presentation or game startup. Continue development outside
frozen folders; server two-hour endurance remains deferred.

Client_Graphics_Pipeline is the frozen passing client010 milestone, PPSA99874
version01.000.010, user ALL PASS on2026-10-24 after the twelve-row and colored
preview checklist. Retrieved logs corroborate9 graphics draws, full pixel/guard
checks,3 image/pipeline/device lifecycles, GPU readback publication and JVM stop.
Actual readback is displayed by the existing CPU menu; preserve this distinction
from SDL/window, Java-owned VideoOut/direct GPU swapchain presentation and game
startup, which remain unvalidated. Preserve exact source/package/symbols; continue
development outside frozen folders. Server two-hour endurance remains deferred.

Client_Direct_Presentation is the frozen passing client011 milestone, PPSA99874
version01.000.011, human automated-notification and explicit visual PASS on
2026-10-24. Retrieved logs confirm all12 checks,90 ordered direct graphics/FIFO
presents,36 pixel samples plus256 guards per frame and DestroyJavaVM. Native
GPU display/resources remain retained until app close; CPU display is not opened.
Preserve source/package/symbols. Teardown/handoff/resize/timeout recovery, SDL
window/input and game startup remain unvalidated. Continue outside frozen folders;
server two-hour endurance stays deferred.

Client_SDL_Window_Input is the frozen passing client014 milestone, PPSA99874
version01.000.014, human tiles/input acceptance and saved ALL12 PASS on2026-10-24.
Reports confirm real SDL3 PS5 window/Vulkan surface, physical DualSense events
and state for X/Circle/D-pad Left/left stick,537 graphics/sample/guard/FIFO frames
and DestroyJavaVM. Preserve exact source/package/symbols. SDL/native display
resources remain retained until app close; teardown/resize/focus/reconnect,
audio/callbacks/keyboard-mouse mapping and game startup remain unvalidated.
Continue outside frozen folders. Server two-hour endurance remains deferred.

Client_Runtime_Shader is the frozen passing client020 milestone,PPSA99874
version01.000.020,human nice pass on2026-10-24. Saved ALL13 PASS confirms actual
shaderc GLSL compilation/error controls across3 compiler lifecycles,18 real
runtime-SPIR-V RADV dispatches/full output+guards,SDL252frames/eventMask15/
stateMask15 and DestroyJavaVM. Preserve exact source/package/symbols. Consumer
app C++ operators use paired existing graphics heap providers; SDK/JVM/game/Java
JARs remain unchanged. Target dependency checkpoint patches and scoped fault
recorder remain disclosed. Includes/callbacks/HLSL/larger shader workloads,
textures/depth/blending/game startup/global teardown and server endurance remain
unvalidated. Continue development outside frozen folders.

Client_Texture_Depth_Blend is the frozen passing client021 milestone,PPSA99874
version01.000.021,human nice pass on2026-10-24. Saved ALL14 PASS confirms3real
texture uploads,combined sampled-image descriptors,D32 depth and alpha-blend
controls with disabled-feature comparisons,27draws/9full256x256images+guards,
existing runtime compiler baseline,SDL318frames/eventMask15/stateMask15 and JVM
shutdown. Preserve exact source/package/symbols. The texture workload is
offscreen,new graphics shaders compiled offline; visible SDL tiles remain the
baseline. No game/Java JAR or JVM/SDK changes. Visible textured scene,perspective/
vertex buffers,larger shaders,game startup,global teardown and endurance remain
unvalidated. Continue development outside frozen folders.

Client_Visible_Perspective_Scene is the frozen passing client022 milestone,
PPSA99874 version01.000.022,human all pass on2026-10-24. Saved ALL15 PASS
confirms real vertex-buffer/perspective-correct sampled scene27draws/9full
images+guards,actual verified GPU readback/upload/blit through SDL295FIFO
frames with physical event/state masks15,and JVM shutdown. Preserve exact
source/package/symbols. Static visible panel uses explicit readback/re-upload/
blit handoff,not continuous scene rendering directly into swapchain or camera
control. No game/Java JAR/JVM/SDK changes. Direct/continuous rendering,index
buffers/camera,larger workloads,game startup,global teardown and endurance
remain unvalidated. Continue development outside frozen folders.

Client_Continuous_Direct_Scene is the frozen client023 milestone,PPSA99874
version01.000.023,human PASS on2026-10-24 after explicit all15/direct scene
phase instructions. Current-run log endpoint refused connections;no session ID
or precise frame count independently corroborated. Preserve exact source/package/
symbols and distinguish human acceptance from pending log retrieval. Shared
renderer draws into each acquired SDL BGRA color attachment;requires minimum180
frames/all3phases,36samples+256guards/frame and physical masks15. No captured
scene upload/blit. Native display/renderer retained;camera controls/indexing,
larger workloads,game startup,global teardown and endurance remain unvalidated.
Continue development outside frozen folders.

Client023 follow-up:Safari native UI retrieved the saved reports on2026-10-24
while shell requests still returned No route to host. Run
client-01.000.023-1792846440-446670267 corroborates ALL15 PASS,494consecutive
direct frames/1482scene draws,all3phases,physical masks15 and JVM shutdown.
Keep the original frozen source/validation and four release assets unchanged;
docs/validation/client023-log-follow-up-2026-10-24.json and additive release
follow-up assets record this later evidence. Raw logs stay local. Camera,
game startup,full teardown and endurance limitations remain.

User work-order update2026-10-24:try actual original Minecraft client startup
now,before camera controls. Development024 calls unmodified26.3Main through
consumer harness,full5147original asset objects and supported demo arguments;
no credentials or game class transformations. Native client coverage remains
incomplete;four startup rows are not an automatic menu pass. Original game
Main return/process exit is diagnostic evidence,not menu/world acceptance.
Preserve frozen023/earlier packages and actual-console validation boundaries.

User update2026-10-24:work on genuine callbacks/libffi and OpenAL after025
reaches original Main and exits during native bootstrap.026 is a five-row
native acceptance candidate,not a game launch. Preserve original game JARs,
failed024/025 packages and frozen023. Host passes do not establish PS5 callback
ABI,mixer or shutdown;freeze only exact human console acceptance. Before a
public OpenAL-linked binary release,provide corresponding sources and exact
relink inputs/instructions with its LGPL notices. Speaker output,remaining
client dependencies and Minecraft menu remain unvalidated;endurance deferred.

Client_Callbacks_OpenAL is the frozen passing026 milestone,PPSA99874
01.000.026,human ALL5 PASS and retrieved run
client-01.000.026-1792852721-557017669 on2026-10-24. Preserve its exact
source,full package,symbols,validation and release assets.192real Java
callbacks across calling/native threads,3OpenAL loopback mixer lifecycles
with PCM/frequency/guard/silence controls,Vulkan loader/FFI bootstrap and JVM
shutdown pass. No PS5 speaker output,full callback coverage or game menu pass.
The release includes original OpenAL corresponding source and exact relink
objects/helper;unmodified relink reproduces the frozen native ELF. Original
game JARs are omitted publicly and reprovisioned locally. Continue development
outside the frozen folder;server two-hour endurance remains deferred.

Client_OpenGL_Provider is the frozen passing029 milestone,PPSA99874
01.000.029,human ALL5 PASS and saved session/startup for
client-01.000.029-1792919308-523542436 on2026-10-25. Preserve exact
source/package/symbols/validation and release assets.3real Mesa softpipe/OpenGL
JNI contexts verify192RGBA pixels/768guards and JVM shutdown. This validates
software GL bootstrap and tested PS5 dependency dispatch,not hardware OpenGL,
Minecraft startup or broad GL coverage. Vulkan remains the game renderer plan.
The release includes matching OpenAL source/relink materials;unmodified relink
reproduces the accepted native ELF. Game JARs remain original and are omitted
publicly. Continue development outside the frozen folder;endurance deferred.

Client_STB_Codecs is the frozen passing031 milestone,PPSA99874
01.000.031,human ALL5 PASS and matching saved session
client-01.000.031-1792921801-581678467 on2026-10-25. Detailed startup
download was incomplete;do not claim independent per-cycle log verification.
Accepted fixture covers3real PNG encode/read/decode/free cycles,768RGBA bytes/
384input guards,truncated PNG/invalid Vorbis controls,Perlin/native structs
and JVM shutdown. Preserve exact source/package/symbols/validation/release.
This is not valid Vorbis decode,font/resize/DXT/callback coverage or game startup.
Release includes exact matching OpenAL source/relink materials;unmodified relink
reproduces the accepted native ELF. Game JARs are omitted publicly and remain
original locally. Continue development outside the frozen folder;endurance deferred.

Client_FreeType_Fonts is the frozen passing033 milestone,PPSA99874
01.000.033,human ALL5 PASS and saved session/detailed current-run startup
client-01.000.033-1792924441-82563672 on2026-10-25. Preserve exact
source/package/symbols/validation/release.3real FreeType2.14.1 library/face
lifecycles verify9Abel glyphs at16/24/32px plus repeats,expected FNV64
fc260d7c9d8a2036,384guards,metadata/metrics,space/invalid font controls,
face/library cleanup and JVM shutdown. Other font features/formats,optional
compressed/color font dependencies,callbacks/concurrency/global teardown and
Minecraft startup remain unvalidated;server endurance deferred. Release includes
matching OpenAL source/relink materials reproducing the accepted native ELF.
Original game JARs remain intact locally and are omitted publicly. Continue
outside the frozen folder;next original Main retry must combine accepted natives.

Client_VMA_Allocator is the frozen passing035 milestone,PPSA99874
01.000.035,human ALL5 PASS and saved session/detailed current-run startup
client-01.000.035-1792926499-461213821 on2026-10-25. Preserve exact
source/package/symbols/validation/release.12real RADV copy/fill transfers across
3VMA3.4.0 allocator/instance/device lifecycles use two mapped65536-byte buffer
suballocations each;exact source/output/guards,NEVER_ALLOCATE controls,
map/flush/invalidate/unmap/free and JVM shutdown pass. Images,custom pools,
defragmentation,budgets,virtual allocations,allocation callbacks,concurrent/large
workloads/global teardown and Minecraft startup remain unvalidated. SPIRV-Cross
is still a known missing native bootstrap component;server endurance deferred.
Release includes exact matching OpenAL source/relink materials reproducing the
accepted native ELF. Original game JARs stay intact locally and are omitted
publicly. Continue outside the frozen folder;do not infer a Minecraft menu pass.
