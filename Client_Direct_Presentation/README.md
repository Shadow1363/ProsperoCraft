# Client Direct Presentation — PS5 automated and visual PASS

Frozen milestone: **PPSA99874**, client **01.000.011**, confirmed on
**2026-10-24**. The user reports **“PASS by notification and pass by my eyes.”**
Retrieved session reports ALL12 PASS; startup confirms90 ordered FIFO presents,
pixel-sample/guard checks and DestroyJavaVM. [Validation](validation.json) records
exact tested source/package, shaders/compiler, dependency pins and evidence.

Original LWJGL KHR_display/surface/swapchain bindings discover the actual PS5
display, create a compatible surface and BGRA8 FIFO swapchain, render with real
vertex/fragment shaders into acquired images and present through RADV/VideoOut.
Each of90 frames verifies36 readback samples and256 guard bytes. Three palette
phases show colored tiles, a black border and white diagonal. Earlier runtime/
core/Vulkan/compute fixtures also pass. The CPU renderer does not open VideoOut.

The native display context is intentionally retained until app close; the last
frame stays visible after JVM shutdown. This establishes direct Java/Vulkan GPU
presentation, not display teardown, CPU-menu handoff, reacquisition, resize or
timeout recovery. SDL/window integration, Minecraft startup/gameplay, audio/
controller gameplay, runtime shaderc, broad graphics/device coverage and full
module/global destruction remain unvalidated. Server two-hour endurance stays
deferred. Original game/Vulkan JARs and runtime implementation/SDK are unchanged.
Frozen000–004 and008–010 remain preserved.

Host validation used a separate offscreen MoltenVK companion for the presentation
shader/BGRA/push-constant/pixel logic. It did not exercise PS5 WSI. The actual PS5
run and explicit human confirmation establish the presentation result here.
The target checks36 samples per frame, not every full-resolution pixel; frozen010
separately verified every256x256 offscreen pixel.

`client/` is the frozen source/pin/result snapshot; use the release tag's root
tools for reproduction and continue development outside this folder. The exact
full ZIP and matching symbols are preserved locally under ignored
`dist/milestones/Client_Direct_Presentation-01.000.011/`.

## Download and local provisioning

The [Client_Direct_Presentation-v01.000.011 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Direct_Presentation-v01.000.011)
contains an app-only ZIP, validation.json, SHA256SUMS and provisioning helper.
Tested files are preserved without rebuilding;54 original upstream client/Java
JARs are omitted for local provisioning. Fixtures, dependency ports, shader
source/SPIR-V and component notices remain included.

1. Verify SHA256SUMS and extract the app-only ZIP.
2. In the tagged source checkout run `python3 tools/prepare_client.py`.
3. Run `python3 provision_client_release.py --manifest validation.json --app-dir /path/to/extracted/PPSA99874 --jars-dir /path/to/repository/build/client/jars`.
4. Install PPSA99874. Wait for Client011 ready; the screen may be blank. Release X, then press X once. Twelve checks run automatically; there is no CPU test menu.
5. Confirm full-screen colored tiles/white diagonal remain after the automatic PASS notification and JVM shutdown. Keep it open for logs at `http://<PS5-IP>:8765/`; after a crash reopen without pressing X.

Provisioning checks all retained files and original JARs, reconstructing every
tested package file exactly and rejecting bad checksum inputs. No account setup
is required. Installing replaces the shared-ID server/client app. Embedded audit
fields remain console pending because tested bytes are unchanged; external
validation records the later human pass and retrieved evidence.

Full tested package SHA256:
`1cc3e1f62a6495e1d110ab3eed80d2e1b73231b23bc428045383e2d47e41d86b`.

Next: SDL window/input integration, retaining separate PS5 checks before
Minecraft startup.
