# Client Graphics Pipeline — PS5 ALL PASS

Frozen milestone: **PPSA99874**, client **01.000.010**, user **ALL PASS** on
**2026-10-24** in response to the twelve-row and visible-preview checklist.
Retrieved reports corroborate nine graphics draws, every pixel/guard check,
three graphics sessions, readback publication and DestroyJavaVM.
[Validation](validation.json) separates automated evidence from visual acceptance
and records exact source, package, shader/compiler and dependency hashes.

Original LWJGL Vulkan bindings create vertex/fragment modules, a graphics
pipeline, optimal-tiled RGBA8 image/view and render pass/framebuffer. A fullscreen
triangle produces colored tiles, a black border and white diagonal. Three
push-constant phases change the palette. Java verifies every256x256 image pixel
and all256 readback guard bytes across three normal pipeline/image/device
lifecycles. Earlier Java/core/Vulkan transfer/compute rows also pass.

After verification, consumer JNI copies actual GPU readback bytes into the
existing CPU-menu preview. The CPU display does not recreate the reference
pattern. The human ALL PASS response accepts the instructions to confirm that
preview appears and remains after JVM shutdown; no separate screenshot or image
description was supplied. Logs alone prove rendering/readback/publish, not human
perception. The CPU menu remains the display owner.

SDL/window integration, Java-owned VideoOut/direct GPU swapchain presentation,
Minecraft startup/gameplay, broader graphics features such as textures/depth/
blending, runtime shaderc, full module/global destruction and timeout recovery
remain unvalidated. Server two-hour endurance stays deferred. Original game/
Vulkan JARs and runtime implementation/SDK are unchanged. Frozen000–004 and008–009
remain preserved. This milestone does not launch Minecraft.

`client/` is the frozen source/pin/result snapshot; use this release tag's root
tools for reproduction and continue development outside this folder. Exact full
ZIP and matching symbols are preserved locally under ignored
`dist/milestones/Client_Graphics_Pipeline-01.000.010/`.

## Download and local provisioning

The [Client_Graphics_Pipeline-v01.000.010 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Graphics_Pipeline-v01.000.010)
provides the app-only ZIP, validation.json, SHA256SUMS and provisioning helper.
Tested files are preserved without rebuilding;54 original upstream client/Java
JARs are omitted for local provisioning. Fixtures, dependency ports, shader
source/SPIR-V and component notices remain included.

1. Verify SHA256SUMS and extract the app-only ZIP.
2. In the tagged source checkout run `python3 tools/prepare_client.py`.
3. Run `python3 provision_client_release.py --manifest validation.json --app-dir /path/to/extracted/PPSA99874 --jars-dir /path/to/repository/build/client/jars`.
4. Install the complete PPSA99874 folder; run all twelve rows in order. Row11 renders/verifies the graphics image; row12 destroys the JVM. Confirm the colored preview remains at the lower right.
5. Leave it open for logs at `http://<PS5-IP>:8765/`; after a crash reopen without running rows.

Provisioning verifies every retained file and original JAR, reconstructing all
tested package files exactly and rejecting invalid checksum inputs. No account
setup is required. Installing replaces the shared-ID server/client app. Embedded
audit fields remain console pending because tested bytes are unchanged; the
external validation records the later human pass and retrieved evidence.

Full tested package SHA256:
`514205b2940c8e7044aa034b820846758d5442f9f19dee4875c59aa9ec3089ef`.

Next: SDL/window and direct GPU display integration, with separate PS5 checks
before Minecraft startup.
