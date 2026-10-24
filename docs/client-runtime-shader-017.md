# Client Runtime Shader Compilation 01.000.017 — initialization boundaries

Client016 crashed after SDL input/display passed196 frames and event/state masks15.
Retrieved run `client-01.000.016-1792840821-503202597` remains RUN at the compiler
row. Actual retained shaderc/glslang/C++ constructors completed. The last Java
checkpoint preceded first Shaderc class initialization and native compiler entry;
loader realpath attempts followed. No Java exception, VM abort or fatal report
was captured. These reports do not isolate the fault to class loading or native
shaderc initialization, and a repaired compiler is not claimed.

017 adds Java checkpoints before/after original Shaderc class initialization,
before native compiler/options allocation and before invalid-source compilation.
An observational native wrapper logs entry/return around the actual upstream
shaderc_compiler_initialize symbol, renamed only for forwarding. The original
function is still called with identical arguments/results; no success is
fabricated and no Java dependency JAR is changed.

The compiler row now runs before the SDL display/input row, so it does not
compete with the retained SDL/GPU display context and a compiler failure does
not require repeating manual controller input. Within each compiler/GPU cycle,
GLSL compilation happens before creating that cycle's Vulkan device/buffers.
This reduces simultaneous resources; it is not proof of the crash's cause.
All valid/invalid GLSL controls, three compiler lifecycles and18 GPU output/
guard workloads remain required. Host real compiler/MoltenVK checks pass the
reordered fixture; target console execution remains unvalidated.

Install **PPSA99874 01.000.017** from `dist/client-runtime_shader/PPSA99874.zip`,
also copied to the runtime workspace's current `dist/PPSA99874.zip`. Wait for
Client017 ready, release X then press X once. The compiler test now comes BEFORE
the tiles and SDL Input ready prompt. If it passes, complete X/Circle/D-pad Left/
left-stick inputs and confirm the final PASS notification and visible tiles.
If it crashes, reopen without pressing X to preserve reports. If it stalls for
several minutes, record the behavior and reopen without starting another run.

Thirteen automatic checks still run; numeric fixture12 (compiler) precedes11
(SDL display/input), then13 destroys the JVM. All console acceptance remains
pending. Failed016 package/symbols and frozen passing milestones stay preserved.
Original game/SDL/Vulkan/shaderc JARs and JVM/SDK implementation are unchanged.
Runtime includes/callbacks/HLSL, teardown, larger rendering/game integration and
server two-hour endurance remain unvalidated. This candidate provides narrower
fault evidence if the crash persists; it is not a new passing milestone.
