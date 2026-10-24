# Client Runtime Shader Compilation 01.000.018 — native compile boundaries

017 fully crashed during saved run `client-01.000.017-1792841350-700258348`.
Retrieved reports prove original Shaderc Java class initialization, actual
shaderc_compiler_initialize entry/return and options allocation/configuration
completed. The final checkpoint precedes the first invalid-GLSL compile. SDL
was not opened. No Java exception or VM abort was captured. These reports
narrow the fault to the compilation call; they do not prove a stack, memory,
locale, TLS, JNI or parser defect.

018 adds target-only checkpoints inside the pinned native shaderc dependency:
actual compile API entry/return, real result allocation, C++ diagnostic stream
construction, Compiler::Compile, TShader/thread-local pool setup, parser entry
and diagnostic formatting. The real upstream compiler still executes all work;
no output, error or successful return is substituted. The source patch is
explicitly recorded and hashed in shaderc-audit.json. Original downloaded source
caches, all Java/game JARs, JVM and shared SDK stay unchanged. This is a diagnostic
candidate, not a demonstrated repair or passing milestone.

Compilation still precedes each Vulkan device allocation, and the compiler row
precedes SDL display/input. Three invalid/valid GLSL compilation cycles, runtime
SPIR-V creation,18 actual GPU dispatches with full output/guards, the existing
SDL physical input/display workload and JVM shutdown remain required. Native
callbacks/includes/HLSL, teardown, full game integration and server two-hour
endurance remain unvalidated.

Install PPSA99874 **01.000.018** from `dist/client-runtime_shader/PPSA99874.zip`
(or the runtime workspace's current `dist/PPSA99874.zip`). Wait for the ready
notification, release X and press X once. If compilation passes, follow the SDL
X/Circle/D-pad Left/left-stick prompts and confirm the final result and tiles.
If it crashes, reopen without starting another run to preserve reports.
Failed017 package/symbols and all frozen passing milestones are preserved.

Host actual compiler/MoltenVK regression passes all3 compiler cycles and18 GPU
workloads. Target compile/link, package CRC/signatures, checkpoint patch hash and
embedded strings, resident exports, constructor counts/order, original54 JARs,
exact002 runtime image/native libraries and frozen package checks pass. Host
compiler is unpatched; these checks do not validate target native compilation.
Package SHA-256: `44ee853dd7a8a914fc49db3cfd5632ac8fd9dff55a390968623ea926ac6a68ee`. PS5 console validation is pending.
