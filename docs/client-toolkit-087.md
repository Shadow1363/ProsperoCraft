# Vulkan toolkit launcher — candidate01.000.087

Experimental Demo and Offline candidates for PPSA99874.
[Build/checksum/validation record](validation/client087-toolkit-build-2026-10-27.json). This is a development
migration, not a new console pass, frozen milestone, GitHub release or
ProsperoStore update. Published083/082 and exact local084/085/086 packages,
symbols and validation records remain preserved.

[Library preview](launcher/087/home.png) · [Offline detail](launcher/087/offline.png) ·
[All17 scripted preview states](launcher/087/contact-sheet.png). These use invented
fixture instance names and account text, not personal library/account data.

## What renders the launcher

PS5_VKHomebrewUI is pinned at
`2188642afbcc8d84d36149124f3d9e39dc1b1a05`, verified against upstream HEAD
on2026-10-27. `client/launcher/toolkit/upstream.json` records every vendored
file's SHA-256. The subset contains the original toolkit sources, Vulkan GLSL
and SPIR-V, fonts, notices and reproduction documentation. There are no local
upstream patches. The sample application, shell, designs, title assets and
audio devices are not adopted. Unused component/audio source is source material;
only the build script's explicit unit list is linked.

Credit belongs to BlackBearReloaded for the original ps5-homebrew-ui kit and
to mihawk-99/Mihawk for its Vulkan backend. GPL-3.0-or-later and font/third-party
notices are retained in source and both complete packages.

The focused consumer adapter sends the existing launcher layout through the
actual `hui::gfx::VkRenderer`: GPU SDF shapes, uploaded logo texture, upstream
Inter Regular/SemiBold font atlases, `PushButton` component faces/focus/press
motion and toolkit springs. The dark green library, centered top-bar labels,
icon choices, readable instance detail, welcome checkbox, guide and branch
identification remain connected to the existing model. Settings change real
saved preferences. Components are used for actions; the established grid,
keyboard and dialogs keep the Java model's navigation and selection policy.
This avoids introducing a second, conflicting focus or persistence model.
Reduced Motion disables movement and press scaling.

`native_menu.hpp` keeps a CPU drawing path for legacy host fixtures and a small
failure screen. The actual startup executable defines `PROSPERO_TOOLKIT` and
renders every normal launcher frame with Vulkan. It does not display a CPU
redesign and call that toolkit integration. Failure blocks gameplay.

## Device, display and thread ownership

1. The normal runtime initialization and existing early game-audio setup run
   first. The native UI thread has an explicit2MiB stack and runs the existing scoped graphics constructors
   through shared `pthread_once`, before any JVM or launcher Vulkan resource.
   Later JNI_OnLoad reuses that initialization. It still opens game WSI only
   after the launcher has closed. The toolkit's one glyph constructor has a
   separate retained linker range and explicit pre-use initialization.
2. The UI owns a private RADV Vulkan1.0 device/graphics queue, one offscreen
   RGBA8 image, render pass, command buffer, fence and coherent readback buffer.
   It creates no surface, swapchain, SDL window or VideoOut handle. Fonts/logo
   upload before the first frame; no upload occurs between prepare and draw.
3. Only the existing native presenter opens VideoOut. Each completed GPU image
   is copied into its cached tiled canvas using the runtime's bounds-checked
   `Canvas::blit_rgba`; the original SSE staging/VideoOut publication remains.
   Launcher, display, model/input and game coordinates stay1920×1080.
4. Before every `prepare(cmd,0)`, the single slot's fence must have completed.
   Prepare records outside the render pass. The pass's external dependencies
   order color writes and transfer reads. A transfer-to-host buffer barrier and
   completed fence precede every CPU read. No glass targets are requested.
5. Game selection asks the UI thread to stop. Each rendered frame has already
   completed its submission. The existing presenter closes VideoOut before
   unmapping/releasing scanout storage; the UI then waits for device idle,
   releases toolkit textures/pipelines and its own Vulkan resources/device,
   closes the controller and publishes completion. The JVM caller joins the UI
   thread and requires successful display **and** GPU cleanup before launch.
6. JNI stays entirely on the JVM caller's attached thread. The rendering thread
   exchanges only80bounded public fields and queued controller edges. Account,
   installer and Java tasks keep their existing worker/model behavior.

Private dispatch pointers obtain real commands from the resident ICD and its
device dispatch. They do not interpose global Vulkan symbols or change LWJGL's
loader. Existing scoped graphics allocation/thread/TLS providers remain;
toolkit C++ allocations use the already paired application new/delete bridge.
The target audit rejects automatic constructors and checks staged ranges.

Missing initialization/font resources produce a native diagnostic and block
Java/game launch. Frame fence waits are bounded at five seconds. A failed
submit or timeout poisons the surface; uncertain GPU allocations are retained
until process exit, never freed under potentially running work. Close failure
blocks game handoff. Native stderr records `PS5_UI` initialization and cleanup.
Upstream synchronous pipeline/upload/idle operations still use Vulkan's normal
blocking calls; hardware hangs cannot be ruled out by the host fixtures.

Quit keeps the existing original-Main clean-return gate and OS LoadExec process
replacement. This candidate never re-enters Main/JVM or reopens launcher
VideoOut under retained game WSI resources in the old process.

## Preserved behavior and data

No Java launcher/model/auth/install/lifecycle source, official game JAR, game
class, OSHI provider or public verification key changes. Same UUID game paths,
worlds, options, shared verified cache, account import and4GiB storage request
under `/download0/ProsperoCraft`. Delete remains Cancel-first, busy-protected
and recoverable through persistent Triangle Undo. No purge or data migration.

Demo embeds Demo channel identity and omits the Offline verification key; it
ignores personal proofs. Offline retains the signed ownership/profile lease,
signature/time/expiry checks and existing key. `--offline` still means cached
build dependencies; `--launcher-channel` selects gameplay policy. Both variants
replace the same installed title and use the same data. Mods remain planned.

## Reproduction and verification

Use the existing packaging command for each channel:

```sh
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew \
  --java-home /path/to/JDK25 --offline --startup --launcher-channel demo
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew \
  --java-home /path/to/JDK25 --offline --startup --launcher-channel offline
```

The runtime must contain `Canvas::blit_rgba`, published separately through its
sync workflow (runtime commit `d05f68d`). Toolkit sources are vendored and verified before compilation;
`prepare_launcher_toolkit.py` reproduces the subset directly from the exact
upstream Git revision. Shader arrays remain byte-for-byte upstream. The baker
and font licensing are retained; original font TTFs are obtainable from the pin.

Run the existing launcher/model/CPU/startup/package tests, plus
`test_launcher_toolkit.py` and `preview_launcher_toolkit.py` after generating
the original preview fixture with `preview_launcher.py`. The new preview uses
the actual Vulkan backend and host lavapipe; VideoOut/controller/JNI are host
fixtures. On ARM64 only the fixture's x86 SSE publication copy becomes memcpy;
target compilation keeps the original SSE code. The host goes directly through
the ICD, so Khronos validation layers are **not** enabled. No layer-clean claim
or PS5 performance result is made. `test_launcher_toolkit_shaders.py` validates
all seven original arrays with spirv-val for Vulkan1.0 and compares the exact
SPIR-V words against local compilation. Upstream's literal shader `--check`
differs only in the glslang16.4 versus16.6 version comment; binary words match.
No upstream shader source or array is modified.

The deliberate conservative limit is a GPU-to-CPU readback for every changed
launcher frame, one in-flight frame and a subsequent tiled upload. Console
startup delay, memory pressure, animation smoothness and handoff must be
measured on PS5; host rendering does not establish those properties. The game
continues to use its established SDL/Vulkan graphics path after cleanup.

## Exact087 PS5 checklist

Install the complete chosen package folder, retaining existing download data.
Keep086 available to reinstall if native pre-JVM RADV or handoff fails.

1. Cold launch each channel: visible toolkit UI before Java readiness, no black
   screen or failure popup; busy account/catalog/download work stays responsive.
2. Check TV typography, centered labels, focus/stick repeat, grid selection,
   keyboard/name/icon, dialogs, welcome checkbox and guide. Toggle Reduced
   Motion/startup notice and reopen to confirm persistence.
3. Add/download/cancel/retry/repair. Unsupported selected versions stay blocked.
   Demo never offers Offline, including with an imported personal record.
   Offline requires the existing valid unexpired signed record.
4. Delete with default Cancel, confirm deletion, restart, Triangle Undo; reopen
   the same saved world/options. Attempt deletion while busy.
5. Launch26.3 in each allowed mode: aligned1080p pointer/clicks, controls/audio,
   original CPU/GPU debug text, world save/reload and gameplay.
6. Quit → library → relaunch at least three cycles, checking sound, cursor,
   saved data and no stuck display. Collect current-run `PS5_UI`/WSI/session
   diagnostics if anything fails. Responsiveness, transitions, game handoff,
   repeated cycles and Delete/Undo remain console-only pending tests.
