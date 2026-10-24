# Client SDL Window/Input — PS5 automated, input and visual PASS

Frozen milestone: **PPSA99874**, client **01.000.014**, accepted on
**2026-10-24**. The user reports **“tiles nice, inputs all accepted.”** The saved
session confirms ALL12 PASS; logs show real SDL eventMask15/stateMask15,
537 graphics/sample/guard/FIFO frames and DestroyJavaVM complete.
[Validation](validation.json) records exact source/package/dependency hashes,
automated evidence, human acceptance and limits of this result.

Actual SDL3 release3.4.2 uses a public PS5 video/joystick backend, with consumer
adaptations for the resident Vulkan ICD, real display-mode discovery and SDL
Vulkan surface hooks. The original LWJGL SDL Java JAR creates a fullscreen
window and surface and accepts real DualSense X, Circle, D-pad Left and strong
left-stick movement via both events and polled state. No virtual input is used
on the console. Graphics render directly through the tested swapchain path;
36 readback samples and256 guard bytes are checked per frame. Earlier runtime/
core/Vulkan/compute checks also pass.

The SDL backend derives from the independently Zlib/MIT-licensed files in
[PS5_Dusklight](https://github.com/griches/PS5_Dusklight) at the pinned revision;
no game/artwork/Dawn/audio code is included. Attribution and licenses are kept
in client/ports/sdl. The port reuses bootstrap-owned pad service initialization,
waits up to10seconds for real discovery and records native diagnostics. Explicit
fixture companion loading avoids the earlier probe lookup failure; its original
classpath/deployment cause remains unresolved. Original game/SDL/Vulkan Java
JARs, JVM implementation and SDK remain unchanged.

SDL/native window, gamepad and GPU resources remain alive until app close,
including after DestroyJavaVM. This pass does not establish SDL_Quit/window
teardown, resize, reconnect/focus behavior, handoff/reacquisition, timeout recovery,
libffi callbacks, audio, rumble/LED, keyboard/mouse mapping or Minecraft gameplay.
Complete SDL/Vulkan coverage and prolonged load remain unvalidated. Server
two-hour endurance stays deferred. Frozen000–004 and008–011 are preserved.

`client/` is the frozen source/pin/result snapshot; use the release tag's root
tools for reproduction, continuing development outside this folder. Exact full
ZIP and matching symbols are preserved locally under ignored
`dist/milestones/Client_SDL_Window_Input-01.000.014/`.

## Download and local provisioning

The [Client_SDL_Window_Input-v01.000.014 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_SDL_Window_Input-v01.000.014)
provides an app-only ZIP, validation.json, SHA256SUMS and provisioning helper.
Tested files remain unchanged;54 original upstream client/Java JARs are omitted
for local provisioning. Fixtures, ports, shaders/SPIR-V and notices remain included.

1. Verify SHA256SUMS and extract the app-only ZIP.
2. In the tagged source checkout run `python3 tools/prepare_client.py`.
3. Run `python3 provision_client_release.py --manifest validation.json --app-dir /path/to/extracted/PPSA99874 --jars-dir /path/to/repository/build/client/jars`.
4. Install PPSA99874. Wait for Client014 ready, release X, then press X once. Twelve automatic checks run; the initial screen may be blank.
5. At Input ready, briefly hold X, Circle and D-pad Left, then move the left stick strongly. Confirm the automatic PASS notification and visible pattern. Keep it open for logs; after a crash reopen without pressing X.

Provisioning validates all retained files and original JARs, restores every tested
package file exactly and rejects invalid checksum inputs. No account setup is
required. Installing replaces the shared-ID client/server app. Embedded audit
fields stay console pending because tested bytes are unchanged; external
validation records the later acceptance and retrieved evidence.

Full tested package SHA256:
`dfa391acfe93a63330b6c98616237906859287bb6ad21e380265a240151dbd1b`.

Further client work must separately validate missing renderer features,
keyboard/mouse or controller mapping, runtime shader compilation and actual
Minecraft startup.
