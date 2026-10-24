# Client Shader Pipeline — PS5 ALL PASS

Frozen milestone: **PPSA99874**, client **01.000.009**, all eleven rows confirmed
passing by the user on **2026-10-24**. Retrieved current-run logs confirm18 real
compute dispatches, all output/guard checks, three shader/device lifecycles and
final DestroyJavaVM. [Validation](validation.json) records tested source, package,
shader/compiler hashes, dependencies, public assets and limits of this result.

The original LWJGL Vulkan3.4.3 JAR creates the shader module, storage-buffer
layout/descriptors, push constants and compute pipeline, then dispatches through
actual RADV. GLSL is compiled offline to validated SPIR-V; RADV compiles that
SPIR-V into GPU code during vkCreateComputePipelines on the PS5. Java verifies
every output and guard word for1,63,64,65,1024,4096-word workloads in each of
three sessions. Partial64-thread workgroups exercise shader bounds checks.
Earlier Java/native/core/Vulkan transfer rows also pass.

This is offscreen compute, with the CPU menu staying visible. SDL/window
integration, graphics/fragment shader pipelines, Java display presentation,
Minecraft startup/gameplay, runtime shaderc, full module/global destruction,
timeout recovery and broad Vulkan/device coverage remain unvalidated. Server
two-hour endurance remains deferred. Original game/Vulkan JARs and the Java
runtime implementation/SDK are unchanged. Frozen000–004 and008 remain preserved.

`client/` is the frozen source/pin/result snapshot. Use this release tag's root
tools for reproduction; continue development outside this folder. The exact full
ZIP and matching symbols are preserved locally under ignored
`dist/milestones/Client_Shader_Pipeline-01.000.009/`.

## Download and local provisioning

The [Client_Shader_Pipeline-v01.000.009 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Shader_Pipeline-v01.000.009)
provides the app-only ZIP, validation.json, SHA256SUMS and provisioning helper.
Tested files are preserved without rebuilding;54 original upstream client/Java
JARs are omitted for local provisioning. Fixtures, dependency ports, shader
source/SPIR-V and component notices remain included.

1. Verify attached SHA256SUMS and extract the app-only ZIP.
2. In the tagged source checkout run `python3 tools/prepare_client.py`.
3. Run `python3 provision_client_release.py --manifest validation.json --app-dir /path/to/extracted/PPSA99874 --jars-dir /path/to/repository/build/client/jars`.
4. Install the complete PPSA99874 folder and run all eleven rows in order. Row10 is compute shader/readback; row11 destroys the JVM. The screen stays on the CPU menu.
5. Leave it open for logs at `http://<PS5-IP>:8765/`; after a crash reopen without running rows.

Provisioning checks every retained file and original JAR, reconstructing every
tested package file exactly. Bad checksum inputs are rejected. No account setup
is required. Installing replaces the shared-ID server/client app. Embedded
console-pending audit fields are retained because tested bytes are unchanged;
external validation records the later human pass and retrieved evidence.

Full tested package SHA256:
`e26c108d72dfe139c5f53cd2c2620685a9e918dcc801cb82878b920a6cd9bebb`.

Next: window/display integration and visible graphics shader rendering, each
with separate PS5 validation before attempting Minecraft startup.
