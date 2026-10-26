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

Client_SPIRV_Cross is the frozen passing036 milestone,PPSA99874
01.000.036,human ALL5 PASS and saved session/detailed current-run startup
client-01.000.036-1792927908-979234410 on2026-10-25. Preserve exact
source/package/symbols/validation/release.3contexts/9GLSL450-HLSL5-MSL translations,
exact fingerprints,SSBO set0/binding0,push8/local64 reflection,malformed SPIR-V
error controls,384guards,allocation/context cleanup and JVM shutdown pass.
One PS5 locale adapter selects the real native localeconv API;original game JARs
and runtime implementation remain unchanged. Translated shader GPU execution,
MSL compiler validation,other features/callbacks/concurrency/non-C or changing
locales/floating literals/global teardown and Minecraft menu remain unvalidated.
The next original Main retry must combine036SPIRV-Cross and035VMA with the
previous accepted natives,and set Configuration.SPVC_LIBRARY_NAME to
System.mapLibraryName("ps5spvc") before original Spvc initializes. The original
default is spirv-cross;no Java overlay/game JAR change is required. Matching
OpenAL source/relink materials reproduce the accepted native ELF;original JARs
are omitted publicly. Continue outside frozen folders;server endurance deferred.

User branding update2026-10-25:the app name is ProsperoCraft. Use the supplied
PNG preserved in assets/branding,with its512RGBA nearest-neighbour icon,for
future development client/server packaging via tools/apply_branding.py. Do not
regenerate the artwork,rename repositories or change PPSA99874/content identity.
Preserve frozen snapshots/releases and already-built038. Keep future candidate
versions distinct as usual. Catalog rename/description update is PR737;its
reservation icon_url remains null per catalog rules until downloadable release.

Client039 failed check4 in original VulkanInstance validation-layer enumeration,
VK_ERROR_LAYER_NOT_PRESENT;the previous SDL/LWJGL pointer rejection was absent.
Exact039package/symbols/status are preserved locally;public failure record hashes
full saved exceptions.log (session/startup/run ID retrieval unavailable).
Client040 development loader reports truthful zero installed instance layers,
rejects named-layer extensions/enabled-layer creation,and delegates actual GPU
commands to resident ICD. Host MoltenVK/UBSan regressions pass;PS5 instance,
window/menu/gameplay remain pending. Original game JARs remain intact;do not
claim validation layers,menu success or a new passing milestone from host checks.

User artwork selection2026-10-25 supersedes the initial no-regeneration preference:
use the approved generated ProsperoCraft-icon-v3-source.png (complete dark-green
P/C outlines) in the next development build after040. Active icon0.png is its
512RGBA packaging resize;branding.json pins both checksums. Keep original/user
artwork and v2/v3 masters,frozen snapshots and already-built040 intact. Existing
client/server apply_branding.py hooks automatically consume the new icon.

Client040 original Main selected PS5 RADV Vulkan and logged SDL window creation,
then failed4MiB ByteBufferBuilder off-heap malloc. Exact040package/symbols/status
preserved;full exceptions/startup reports hashed in public failure record with
matching run ID. Client041 scopes only MemoryAccessJNI/LibCStdlib native objects
to existing clientgpu title-heap malloc/calloc/realloc/free/alignment family,with
audit and pre-Main checked large-buffer allocation/cleanup. No game JAR or JVM
global allocator changes. Approved v3 icon included. PS5 allocation/preflight,
render buffers/menu/gameplay and memory/performance remain pending;no new pass.

Client041 progressed through resource reload/renderFrame after scoped allocation
repair,then repeatedly failed4K swapchain creation;human reported crash/reopened.
Saved VM trace ends in shader compilation without captured fatal fault/abort.
Exact041package/symbols/status preserved. Client042 unifies SDL display and Vulkan
surface selection with actual enumerated1080p <=60Hz preference,plane/capability
checks and logging. Driver offers1080p/1440p/4K;never claim invented720p scanout.
PS5 swapchain/menu and later crash remain unresolved;host inventory regression
is synthetic policy validation,not GPU acceptance. Preserve frozen snapshots.

Client042 selected matching real1080p59.94 SDL/Vulkan surface but continued
VK_ERROR_INITIALIZATION_FAILED swapchain errors and human-reported crash.
Full native VM trace ends DONE:Metadata zeroing with no captured fatal signal.
Exact042package/symbols/status preserved. Client043 is explicitly diagnostic:
bounded64-event native Mesa WSI checkpoints identify initialization guards,
registration,image layout and host import errors without changing results or
parameters. A private RADV archive replaces one native WSI object;original pinned
source/archive unchanged. Original game JARs and frozen passes stay intact.
Driver rejection/crash/menu remain unresolved pending next PS5 diagnostic run.

Client043 WSI diagnostics identify negative VideoOut open before framebuffer
registration/image allocation;extent/count/import callback are valid. Native raw
OS error not captured;VM trace has no fatal signal. Exact043package/symbols/status
preserved. Client044 adds0002 native WSI patch:caches nonnegative handles only,
one delayed retry after2s before any buffers/current swapchain,max2OS attempts,
retains success and logs raw OS errors. Permanent refusal remains failure.
Private native archive only;original game JARs/Mesa archive and frozen passes
unchanged. Host exact-function tests use synthetic OS responses/clock. Initial
refusal/crash/menu/presentation need actual PS5 validation;server2H deferred.

When incrementing build versions,replace complete version/label tokens rather
than bare digits;historical SHA-256 strings must remain exact and unchanged.

Prospero Store status verified2026-10-25:rename PR737 is MERGED;upstream
apps/PPSA99874.json now says ProsperoCraft with updated client/server/native-Java
description. Reservation release/icon/source fields remain null. Do not duplicate
the rename PR or assume a downloadable listing/live website update. Detailed
continuation prompt:docs/handoff-prosperocraft-client044.md.

Client044 retrieved session client-01.000.044-1792941998-299539155 records two
actual sceVideoOutOpen results0x80020023 (kernel EAGAIN/resource unavailable).
Retry executed but registration/images/menu remain blocked;no fatal signal/VM
abort captured. Do not infer the unavailable resource or a crash stack. Exact044
package/symbols/status/evidence preserved. Client045 adds read-only configured/
available flexible memory and largest direct range with raw query statuses before/
after the same bounded open calls;no extra output,allocation,heap/resolution change.
Original game JARs/private source boundary/frozen passes preserved. Actual PS5
resources/open/presentation/menu and later crash remain pending;server2H deferred.
See docs/client-startup-045.md and matching044failure evidence. The044handoff
is historical;current candidate045 supersedes its version/status directions.

Client045 reports confirm both opens0x80020023 with324MiB flexible available and
>11.5GiB largest direct ranges. Earlier ordinary thread creates fail EAGAIN/ENOMEM
and succeed with direct stacks;libc/service pressure is a hypothesis,not confirmed
VideoOut cause. Exact045 artifacts/evidence retained.046 initializes the same WSI
output after GPU provider constructors/before original Main,under existing lock/
once;later swapchain reuses retained handle including0. No separate preflight
output or ownership handoff. Negative result fails JNI_OnLoad before Main;no fake
success. Startup-only macro leaves other build modes unchanged. PS5 early open/
registration/presentation/menu/later exit remain pending;server2H deferred.
Current046 supersedes historical044/045candidate instructions.

Client046 human reports visible original Mojang loading screen then crash/reopen.
Matching run client-01.000.046-1792944398-207378114 confirms early open0x4e100100,
prepare0 and3successful WSI image imports. Preserve this working same-owner early
initialization. No menu/gameplay/ALL PASS or new milestone;exact046retained.
No fatal signal/VM abort captured.047 holds an outer existing fault-recorder
reference across original startup JNI call,including gaps between shader compiles.
Existing recorder implementation/delegation unchanged;historical SHADERC FAULT
prefix no longer implies compiler origin and signals can be JVM-handled normally.
Requires4handlers/descriptor;RAII restores on returns. PS5 capture/crash cause/
menu/stability pending;server2H deferred. Current047supersedes earlier candidates.

Client047 reports show outer fault recorder4 and retained successful VideoOut/
3image imports,but no signal/VM abort/fatal report. Crash cause unknown;last shader
return is not crash-location evidence. Exact047retained.048 adds real native
stderr capture before constructors and fixed current/previous download endpoints.
Native driver submission/timeout diagnostics previously went only to stderr;
no such GPU failure is established yet. Preserve early owner/outer recorder.
Reopen without X after failure;collect native-stderr.log with VM/build/session/
exceptions/abort/fatal reports. PS5 descriptor capture/crash resolution/menu pending;
server2H deferred. Runtime helper/server/collector changes publish separately.
Current048supersedes earlier candidate instructions.

Client048 black screen was diagnostic setup FAIL check1/code1 before JVM;matching
run client-01.000.048-1792946164-359674616/native header only. PS5 title dup2EPERM
is documented by inspected SDK source. Do not treat stale VM traces as048. Exact
048retained.049uses open/fdopen/unbuffered FILE then stderr pointer replacement,
no dup2/no pipe/thread;raw descriptor2 remains unchanged/not captured. Optional
capture failure now logs/notifies and continues startup. Preserve early WSI owner/
outer recorder/original artifacts. PS5 FILE capture/loading/crash/menu pending;
server2H deferred. Current049supersedes earlier candidate instructions.

Client049 matching run client-01.000.049-1792947461-290571136 confirms real native
FILE capture and1080p framebuffers registered set0/buffers0-4.048setup regression
passed;no GPU submit/timeout diagnostic or signal/VM abort captured.046/047/049
have390compile entries/returns each,last compile is not a known crash location.
Exact049retained.050adds first8present/fence/flip checkpoints plus raw failures,
within existing64event cap,in private WSI object. Behavior/results unchanged,
including existing failed-fence continuation (logged,not repaired/claimed success).
No new output/thread/timeout/resolution/heap change. PS5 frame progression/crash/
menu/stability pending;server2H deferred. Current050supersedes earlier candidates.

Latest continuation handoff:docs/handoff-prosperocraft-client051.md. It contains
current051package/source/checksum,latest retrieved051snapshots,all prior fixes,
Safari retrieval/publication boundaries and eventual release/store requirements.
050/044handoffs are historical. ProsperoCraft PR737 was verified MERGED;reservation
fields were null in that verified state. Do not infer a downloadable client listing.

Client050 human reports Mojang loading then crash;matching run
client-01.000.050-1792949111-939372034 confirms8successful fence waits/8accepted
native flips and390shader entries/returns,no captured signal/VM abort/driver error.
Cause remains unknown,not the last compile. Exact050package/symbols/status retained.
051 adds optional bounded startup Java thread-stack/heap snapshots:90samples/1s,
32printed threads/24frames,Main/resource workers first;one daemon requesting256KiB.
Setup/sampler failure disables diagnostics and continues original Main. Safepoints,
allocation and timing effects require PS5 validation. No game-JAR changes/menu pass/
new milestone. Current051 supersedes050 candidate instructions;see
docs/client-startup-051.md and050 validation record. Server2H remains deferred.

051retrieved run client-01.000.051-1792950523-73596505 confirms90complete snapshots
8-89147ms and normal observer completion. Samples63-90render waits in pipeline
future join while resource worker has changing RUNNABLE texture/font/model stacks.
This is not a proven deadlock/crash cause.390shader entries/returns,first8fences/
flips succeed;no captured fatal signal/VM abort/driver error/OOM. Allocation reserve
failures/null metadata attempts require retry/fallback context. No explicit human051
final visual outcome supplied;050Mojang/crash remains a separate report. No binary
changed for documentation handoff;051console/menu/crash mechanism remain unresolved.
See docs/validation/client051-startup-observations-2026-10-25.json and the current
051handoff before work. Preserve051exact artifacts before any changed052candidate.

Current continuation update:docs/handoff-prosperocraft-client053.md supersedes052
candidate instructions. Human confirms052Mojang loading near completion then crash
before menu fade around1½minutes. Matching reports end after91complete snapshots,
last94195ms,with render joining pipeline future and worker baking resource models.
No fatal context/OOM/driver error captured;cause unknown. Exact052retained before053.
053adds consumer native resource/handler-ownership observations around Java samples,
first120at1s then60at5s;no handler replacement,no speculative game/runtime/heap/GPU
repair. Console validation remains pending. Server2H stays deferred. Read prior051
complete release/store/provisioning/OpenAL requirements before any client release.

Current054update supersedes053candidate directions:see docs/handoff-prosperocraft-client054.md.
053crash/reopen reports contain98snapshots through97185ms and native pairs through
97186ms;pipeline wait resolves,Main entersMinecraft.run and language-resource apply.
No permanent deadlock/menu/crash cause is established. Four recorder handlers match,
flexible availability remains>=324MiB;raw RSS units/process policy unknown.054adds
read-only process limits/direct availability and dense transition sampling;no
limit/heap/graphics/game repair claimed. Exact053retained;054console pending.

Latest054retrieval/handoff update:docs/handoff-prosperocraft-client054.md is now a
complete self-contained continuation guide,with docs/fresh-context-prompt-client054.md.
054run client-01.000.054-1792954563-796299341 confirms120snapshots through96992ms,
120native phase pairs96993ms;pipeline join resolves,Main applies language resources,
worker idle. AS/RSSreported infinite,data32GiB,flexible>=324MiB,largest direct range
>=12124160000bytes;RSSunits unverified,no1GiBlimit/exhaustion diagnosis. No fatal
context/OOM/driver error. No explicit054human final outcome/timing supplied. This
handoff turn changes docs/evidence only,054binary unchanged. Preserve exact054before
changed055;read complete saved logs and establish actual outcome before assumptions.

## Client product goal clarified on2026-10-26

The user wants a polished,playable Minecraft Java client on native Java25forPS5,
including responsive controls,smooth rendering,working audio,world gameplay,
saving/reloading and stability. A working menu is an intermediate debugging
checkpoint,not the final product or sufficient full-client release acceptance.
Continue beyond startup while keeping exact-build console scope/results honest.

## User menu confirmation and GitHub release authorization — 2026-10-26

The user confirms the visible Minecraft Java menu on exact client01.000.062
and explicitly requests a polished GitHub release with no Prospero Store work.
Tested implementation f3349a1fb90a9304d7aa808b339bd37738607d14; full-local ZIP
26f31cc26bc960d3c7e35205c0280e8b83bc6e475a17b8383c778583cf952b88. Preserve
these accepted bytes/symbols/source. This accepts visible menu startup only,
not formal ALL PASS, menu interaction, world gameplay, speaker audio, save/reload,
full teardown or stability. Publish a full release accurately qualified to that
scope; retain server fallbacks. No Store/catalog changes are authorized here.
Do not rebuild or change the accepted binary under the same version. Public
app-only artifacts exclude original JARs AND asset objects; provision both with
verified publisher pins. Include exact startup OpenAL source/relink/shim inputs.

## User control and menu performance direction — 2026-10-26

After the062menu release, the user requests temporary functional controls and a
menu-lag fix. The user prefers upstream Controlify for the eventual modded client,
on an exactly compatible Fabric/NeoForge build. Do not treat desktop mod support
as PS5 acceptance. Temporary063SDL keyboard/mouse translation is opt-in through
PS5_TEMPORARY_CONTROLS and must hand off to real gamepad/mod support without double
input. Preserve the raw SDL joystick path. No game JAR rewrites/replacement classes.
The observed gradual idle slowdown has a supported vanilla AFK policy alternative;
GC stutter remains distinct. Preserve accepted062release bytes/tag and continue
candidates at063or later;no Store updates or new release without separate request.

## First world and performance work — 2026-10-26

The user confirms065world loads and punching works,but movement fails and severe
lag/verylongloading make it unplayable. They request a GitHub release of this exact
checkpoint and then a speed candidate. Publish accurately scoped fullworld-entry
release;do notinferformalALLPASS,playableperformance,movement,save/reload,audio or
stability. Preserve065accepted bytes/symbols/source/tag. No Store work.
Proceed with performance investigation and a new066candidate;guardedC1 and SDL
relative-input repair are in scope. Fullhardwareutilization is the goal,not a
claim justified by enabling flags. No gameJAR transformations/replacementclasses.

## Playable066release and audio work — 2026-10-26

The user confirms066is blazinglyfast,worldplayable,startuproughly30seconds,and
requests release then sound before further instructions. Publish exact066asfull
GitHubplayableworldrelease,accuratelyqualified humanresult—notFPS/ALLPASS/save/
audio/enduranceguarantee. Preserve exactZIP/symbols/source/tag. NoStorework.
Next067isrealPS5AudioOut/OpenALspeakerbackendplusbacked-upunmutingoflegacy
launcherdefaults. Keep gameJARs/assetsintact,working066fallback andspeedsettings.
No further performance-tuning scope beyond maintaining working C1 is requested.

## Audio confirmation and intermittent freezes — 2026-10-26

The user confirms067sound works beautifully on PS5 and now authorizes investigating
and fixing intermittent freezes. Preserve exact067package/symbols as the working
audio fallback. Current-run GC evidence confirms full pauses; do not assume every
freeze is GC or claim a latency pass from host tests. Continue at068or later,
retain working audio/input/C1 and untouched game files. No new release or Store
publication requested. Keep build history in CHANGELOG.md; README stays concise.

068follow-up:human reports escalating stutters then complete freeze. Same-run
reports confirm Java heap OOM and chunk-save failure, repeated499M->499MfullGC.
Preserve068as failed GC candidate; do not claim save success.069requests768MiB
heap/NewRatio3 using separate runtime0119bounded ceiling; console reservation/
headroom/sufficiency/stability pending. Current continuation:docs/handoff-prosperocraft-client069.md.

069follow-up:768MiBstartup works but stutters recur; retrieved console showsview16/
simulation12and continued fullGC/live-setgrowth.070uses backed-up once-only vanilla
options caps6/5, preserving lower values/later choices; heap/runtime unchanged.
Do not infer a stable live set or GCpass from hostchecks. Current070handoff applies.

Userclarification:target is smooth highsettings, not quality cuts as finalfix.
070was diagnostic only; userdidnoteditsettings, butreportsstill16/12andstutters.
071disablesactive070cap,preservesexistingconfiguration,andusesboundedretainedheap
diagnostics/runtime0120. No claim of a lower-distancecomparison orperformancefix.
Currentcontinuation docs/handoff-prosperocraft-client071.md.

071retentionfollow-up:3PS5histogramsconfirmgrowingchunk/longarraycategories,stable
modelquadcount;notleakproof.072preservesqualityandtestsG1/1536MiB/2GCworkers+
1concurrentworker/processorhint4,withoutdiagnostichistograms. Runtime0121bounded
heapceiling;actualPS5G1startup/nativeheadroom/pausespending. Current072handoff.

072follow-up:humanreportsverysmallstuttersbutnosound. PartialG1logs:92pauses,
median20.8335ms/max49.747ms/nofullGC;qualifiedimprovement,notformalpass. Audioinit
0x80260002failsbeforeportopen.073boundedBusyactual-portprobe/retry/AlreadyInit
handlingonly;preserveG1/heap/quality. AudiblePS5recoverypending. Current073handoff.

073audiofixfailed(all20Busy/NotInit),smallstuttersannoying.074testsAudioOutinit
onthenativestartupthreadbeforeVM/heap,validatesrealearlyresultandrealport;no
forcedservicereset. G1goal8/workers4anddefaultstackobserveroff;quality/heapretained.
ActualPS5audibility/initorder/GCworkers/latency pending. Current074handoff.

074humanconfirmation2026-10-26:verygoodsoundandbuttersmoothgameplay. Preserveexact
074package/symbols/testedsource72eca7fccf79c81c2cb7a057afdffcad51207b90; no rebuild
ofacceptedbytes. Subjectiveaudio/smoothnessacceptanceonly,nomeasuredFPS/save/
endurance/formalALLPASS. No newrelease or furtherimplementationrequested.

## Native launcher and MSA direction — 2026-10-26

The user requests a beautiful launcher with Microsoft account login and supplied
public application ID f0c7635e-8d50-4d7e-afa3-d15db4a0a3d3. Candidate075 adds
native UI, device-code authentication and original Main session arguments. No
client secret or token persistence. One Vanilla26.3 instance; settings informational.
Host and target checks do not establish live authentication or display handoff.
Continue from docs/handoff-prosperocraft-client075.md. Preserve accepted074 bytes
and performance/audio/settings. No new release or Store publication requested.

076branding update: user supplies Downloads/ProsperoCraft2.png for packaged app
icon and ProsperoCraftTransparent.png for native launcher corner. Source copies
and hashes belong in assets/branding; generated bitmap from prepare_launcher_branding.py.
Keep075exact package/symbols preserved during MSA tests. Candidate076 changes
branding/version only; inherited live-login/display handoff checks remain pending.
Current guide docs/client-launcher-076.md. No release requested.

## Launcher startup separation — 2026-10-26

User reports GUI never loads (075/076exact version unspecified) and requires
separation from MC graphics.077native UI starts/presents before VM creation,
with account/model work on the JVM startup thread and mailbox-only UI exchange.
Defer artifact inventory/game native loads/C1/Main until Play. Preserve early
AudioOut init on original startup thread. See docs/handoff-prosperocraft-client077.md.
Host threading/JNI-table/order tests do not establish PS5 GUI/liveMSA/handoff.
Keep raw auth secrets out of diagnostics; preserve074/075/076packages. No release.

## Authentication rejection follow-through — 2026-10-26

077user passes public-client setup/code approval but returns to Not signed in
with generic REGISTRATION text. No full MSA/MC acceptance. Exact later endpoint
is unresolved; no proven Minecraft403.078preserves HTTP401bodies with bounded
bufferedPOSTs and adds endpoint/status UI errors and allowlisted diagnostics.
Never log raw responses, token/code values, headers or exception/cause text.
Read docs/handoff-prosperocraft-client078.md. Preserve077and earlier packages.
Use actual078PS5_AUTH logs to identify the failing stage before service changes.
No new release/Store publication or auth/entitlement bypass.
