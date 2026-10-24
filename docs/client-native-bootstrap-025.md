# Client025 native-bootstrap failure and development dispatch port

The PS5 now creates the VM with128MiB and executes original Minecraft Main.
Run client-01.000.025-1792850495-314186228 ends in the game's native-library
crash report and System.exit(-3). The memory report shows46MiB used of123MiB;
there is no observed025 heap reservation/OOM failure. This is later than024.
The game has not created a window/renderer/menu. Frozen023 remains intact.

Original LWJGL VK.create() and ALC.create() switch on Platform.get();the core
port's appended PS5 enum reaches their default IllegalStateException paths.
The original game sets Vulkan explicit initialization before calling VK.create;
this is not a duplicate-initialization error. OpenAL is the first fatal entry
in this run's shuffled load order. OSHI warnings are caught system-report
limitations,not the fatal cause. Full reports remain local;the tracked evidence
contains checksums and a scoped summary only.

Development adds a separate pinned-source LWJGL module overlay. VK's PS5 branch
loads the configured genuine resident ps5clientgpu provider. ALC's PS5 branch
uses the normal OpenAL name/configuration path and genuine resident resolver.
All upstream lifecycle,capability creation and missing-library rejection stay
in place. No fake exports,game-JAR edits,game replacement classes or runtime
implementation changes. The downloaded54original JARs remain intact. This
explicit dependency overlay is not part of025 or any frozen milestone.

Build with tools/build_lwjgl_module_platform.py --java-home JAVA_HOME --offline.
The two official3.4.3 source archives,patches,emitted classes and hashes are
recorded in client/ports/lwjgl/modules.json and generated build audit. Output
is an ignored overlay JAR,not a new app/install candidate. Cache/source archives
and compiled outputs are not committed. The upstream BSD license is included.

Host validation runs the original and patched actual module classes with the
real built native core under Xint/XcheckJNI/verification/UBSan. A host-only
Unsafe control selects the actual PS5 enum branch after host-core initialization;
it is never packaged. Original VK/ALC reject PS5. Patched VK resolves the actual
MoltenVK provider and reports a real supported Vulkan version,then upstream's
VkAllocationCallbacks preinitialization reaches the missing native
LibFFI.FFI_TYPE_DOUBLE method. This is an expected negative boundary control,
not a successful complete Vulkan bootstrap or a PS5 GPU result. Duplicate
creation rejection and destroy retain upstream semantics. Patched ALC reaches
the real missing-library UnsatisfiedLinkError with no fabricated OpenAL provider.

Real libffi callback and OpenAL native implementations are required next.
OpenGL is also unconditionally loaded by this original client's native
bootstrap even with the Vulkan backend;STB,FreeType,VMA,SPIRV-Cross and further
SDL callbacks remain incomplete. Muting audio does not remove its bootstrap
requirement. The dispatch repair is built/tested separately and deliberately
not promoted into a new console app while these known blockers persist.
No additional025 console test is needed. No026 app/menu pass is claimed;
server two-hour endurance stays deferred.
