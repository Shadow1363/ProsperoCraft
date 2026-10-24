# Client Runtime Shader Compilation 01.000.019 — parser fault capture

018 fully crashed during run `client-01.000.018-1792841874-781253561`.
Current-run reports confirm real native compile entry, result allocation,
C++ diagnostic stringstream construction, Compiler::Compile and TShader
construction. The last checkpoint is immediately before glslang parse.
No Java exception or VM abort was captured. This rules out those earlier
initialization boundaries for this run, but does not identify the parser fault.

019 keeps the actual compiler and all thirteen acceptance checks. A second
observational native dependency patch logs thread pool assignment, deferred
processing, version scanning, built-in table generation and user-shader parsing.
The exact pinned glslang source is exported into the ignored build tree before
applying the patch; original caches and Java/game JARs remain unchanged.

During the actual compile call, a scoped fault recorder appends signal number,
code, reported address and96 raw context words to the existing VM trace.
The raw context range follows the pinned SDK's signal probe; desktop FreeBSD
register offsets are not assumed to match PS5. This may allow identification
of the faulting instruction against the matching symbols. It cannot capture
faults that the platform does not deliver as these signals.

The recorder preserves and delegates to prior SIGSEGV/SIGBUS/SIGILL/SIGABRT
handlers, including the JVM's existing handler. It does not modify the context,
catch/recover a compiler error or fabricate a successful result. Original
handlers are restored after normal compilation. Nested install/restoration,
mask preservation, bounded context writes and both one-argument and SA_SIGINFO
handler delegation pass real host child-process tests. Target signal delivery,
context capture and compiler execution remain unvalidated.

Install PPSA99874 **01.000.019** from `dist/client-runtime_shader/PPSA99874.zip`
(or the runtime workspace's current `dist/PPSA99874.zip`). Wait for the ready
notification, release X and press X once. The compiler runs before SDL. If it
passes, follow the X/Circle/D-pad Left/left-stick prompts and confirm the final
result and tiles. If it crashes, reopen without starting another run.

This is a diagnostic candidate, not a demonstrated crash repair or new passing
milestone. Three invalid/valid GLSL compilation cycles,18 actual RADV output/
guard workloads, SDL physical input/display and JVM shutdown remain required.
JVM/SDK/game/Java JARs are unchanged. Failed018 package/symbols and frozen014
and earlier milestones are preserved. Includes/callbacks/HLSL, global teardown,
textures/depth/blending, game startup and two-hour server endurance remain pending.

Host fault recorder and actual unpatched host compiler/MoltenVK regression checks
pass. Target build/link, package signatures/CRC, native patch/source hashes and
checkpoint strings, resident exports and constructor ordering, original54 JARs,
exact002 image/native libraries and preserved milestone/package checks pass.
Target precompiled headers are disabled to avoid stale headers after source
export. These checks do not prove target parser or signal capture success.
Package SHA-256: `772e23900036ede31d7aa32cb6552d99309472aa9a7a7889db69c2a7c8df9e43`. PS5 validation is pending.
