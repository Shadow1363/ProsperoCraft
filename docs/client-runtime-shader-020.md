# Client Runtime Shader Compilation 01.000.020 — C++ allocation route

019 crashed in run `client-01.000.019-1792842526-244118770` while glslang
started generating/parsing built-in symbol tables. The fault recorder installed
all4 handlers and captured SIGILL code5 at runtime address0x408579. The title
load base is0x400000, independently corroborated by the checkpoint address
0x406090 against its ELF symbol0x6090. ELF offset0x8579 is precisely the UD2
instruction in application operator new[] after __wrap_malloc returns null.
This is a deliberate allocation-failure trap, not evidence of unsupported GPU
instructions or a glslang parser bug. Requested allocation size and overall
available memory are not established by the report.

The app's unchanged minimal SDK C++ allocation operators call raw libc through
the existing trace wrapper, bypassing the graphics heap already used by RADV's
C allocation references.020 scopes only cpp_runtime.o's malloc/free/
posix_memalign references to the existing genuine clientgpu heap providers.
Ordinary,array,nothrow,aligned and sized C++ allocation/deallocation paths stay
paired. The existing graphics allocator uses its direct-memory heap and retains
its real libc fallback/foreign-pointer ownership handling. No successful
allocation or compiler output is fabricated; true exhaustion still fails.

This selects providers for this consumer title's shared application C++
operators. It does not change the SDK source or libraries, JVM-specific
allocation implementations, raw process libc symbols or global linker wraps.
The package includes cpp-allocation-audit.json with exact source/raw/scoped
object hashes and the three bindings. Target object references are checked
against the real existing graphics providers. Other candidate builders and all
frozen snapshots keep their original behavior.

Host tests compile the unchanged SDK operator source with matching provider
bindings and exercise1MiB new[]/write/delete[],zero-size,nothrow success/failure,
256/4096-aligned new/delete and balanced ownership. Host providers use actual
host allocation; this verifies operator pairing, not PS5 direct memory. The
original actual host shaderc/MoltenVK workload remains applicable: only Java
stage/version text changed. Target runtime compiler execution subsequently passed the captured020 console run.

Install PPSA99874 **01.000.020** from `dist/client-runtime_shader/PPSA99874.zip`
(or the runtime workspace's current `dist/PPSA99874.zip`). Wait for the ready
notification, release X and press X once. The compiler runs before SDL. If it
passes, complete X/Circle/D-pad Left/left-stick inputs and confirm the final
PASS notification and visible tiles. If it crashes, reopen without starting
another run to preserve the fault report.

All thirteen checks remain required: three actual invalid/valid GLSL compiler
cycles,18 actual runtime-SPIR-V GPU dispatches/output+guards,SDL physical input/
display and JVM shutdown. Parser checkpoints/fault forwarding remain enabled.
No game/Java JAR transformations. Exact failed019 package/symbols are preserved.
This is a targeted repair candidate, not a console pass or new milestone.
Includes/callbacks/HLSL/global teardown,later rendering/game startup and deferred
server two-hour endurance remain unvalidated.

Target package checks pass, including actual scoped C++ object references/hashes,
existing real providers, original JARs/runtime libraries, constructor counts/
order, resident exports, native fault capture/patch audits, CRC/signatures and
preserved milestone/server packages. Package SHA-256: `4573723d3947f005f7389d82737505b17581fc36ba0f2c1b3ba0b42dca2bb552`.
PS5 compiler/repair validation passed on2026-10-24: human “nice pass!” and saved ALL13 PASS. See ../Client_Runtime_Shader/validation.json for exact evidence and remaining limits.
