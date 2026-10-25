# ProsperoCraft client041 — scoped native render-buffer allocation

040run client-01.000.040-1792935600-381088939 selected the Vulkan backend,
identified the PS5 GPU and extensions,and logged creation of an SDL ps5 window.
GameRenderer subsequently failed in RenderBuffers/SectionBufferBuilderPack:
ByteBufferBuilder's system MemoryAllocator.malloc(4194304) returned0. The game
reported off-heap allocation failure,returned,and the harness correctly failed.
The Java heap's last collection used130MiB/247MiB committed;increasing Java heap
is not justified by this error. No visible menu/rendering pass is established.

Inspection of original ByteBufferBuilder bytecode and original LWJGL JNI shows
the allocator uses native malloc pointers. Those core JNI objects currently bind
to process libc,whereas graphics/SDL/C++ use the dependency's scoped real title
heap. Exact libc refusal cause/console-wide pressure remains unmeasured.

041changes only startup packaging of the two original LWJGL allocation JNI
objects:MemoryAccessJNI and LibCStdlib. Their malloc,calloc,realloc,free,
posix_memalign/aligned_alloc references bind to the existing clientgpu title-heap
family. Both allocation and release/grow paths stay paired;no global/JVM symbol
is replaced. The title heap's real direct-memory allocator and libc fallback
are reused;no fabricated success is returned. Other native components,original
JARs,Java heap256MiB and frozen snapshots stay intact. New
lwjgl-allocation-audit.json records exact scoped objects and all bindings.

Before original Main,a real LWJGL system-allocator preflight holds3x4MiB,grows one
to8MiB,checks preserved pages/tail and the new extent,checks64KiB calloc zeroes,
checks4096-aligned4MiB memory,and frees all allocations through paired functions.
Failure stops with a specific allocation error. Successful preflight does not
establish sufficient memory for all game workloads.

The user-approved generated v3 icon with complete P/C outlines is included as
512RGBA packaging artwork. Existing040package and frozen artifacts are preserved.

Checks/build:

```sh
python3 tools/build_lwjgl_native.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --host --offline
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

Host preflight executes actual original LWJGL JNI with host libc under
-Xcheck:jni;this validates allocation/check/cleanup logic,not the PS5 heap.
Target package checks verify scoped object hashes and undefined allocator
references against the real graphics binding map,all54original JARs/5147assets,
exact runtime/accepted native inputs,constructors/signatures and corrected icon.

Install local dist/client-startup/PPSA99874.zip or runtime dist/PPSA99874.zip,
launch and press X once. Inspect actual screen;report failure promptly and keep
open for logs,or reopen without X after a crash. No automatic menu PASS exists.
PS5 allocator preflight,render buffers,visible menu/gameplay,memory adequacy,
performance/network/teardown remain pending. Server2H endurance stays deferred.

Host preflight/launch checks and full-package checks pass. Full local ZIP SHA-256:
`c252c4ce4f454025c6f0930e5c2e2395ff778a3cbe86f7cc71599a94f15fd98c`. PS5 validation remains pending.

Console outcome:render buffers no longer refuse4MiB;original resource reload
and render loop reached,but4K swapchain repeatedly fails and user reports crash.
See[041evidence](validation/client041-startup-failure-2026-10-25.json) and
[042mode retry](client-startup-042.md). No visible menu pass.
