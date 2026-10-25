# Client035 — real VMA allocator,PS5 ALL5 PASS

Original Minecraft034 reports missing liblwjgl_vma.so at bootstrap index5.
The earlier shaderc,SDL,FreeType,STB and OpenAL entries loaded in that Main run.
The window was not initialized;OpenGL/spvc were later in this run's randomized
order. Native startup ends VM EXIT -3. No separate native JVM fault or heap OOM
is established. The exact failed034 full ZIP/symbols/candidate status and raw
reports are preserved locally;the validation JSON publishes report hashes only.

035 builds the original two generated LWJGL3.4.3 C++ units and embedded VMA3.4.0
header from the pinned LWJGL commit. Its Vulkan headers and common headers are
pinned from that same source. No implementation stubs,game transformations or
replacement game classes are added. Original LibVma.setupMalloc initializes
private clientvma_org_lwjgl_* slots;core allocator globals remain untouched.
Other C++/thread/heap references bind to the same existing scoped graphics
providers. Native Vulkan functions are supplied through the original LWJGL
VmaVulkanFunctions table;static and dynamic Vulkan lookup are disabled by the
upstream generated source. All54 downloaded game/Java JARs remain unchanged.

The five-row probe initializes runtime/VM,verifies original artifacts,performs
real allocation/GPU work,then destroys the VM. Three allocator/instance/device
lifecycles each allocate two mapped65536-byte buffers through vmaCreateBuffer.
The preferred large heap block size is bounded at1MiB;allocation offsets and
sizes are logged. Four copy/fill submissions per cycle cover8,256,4096 and65536
bytes. Exact destination/source bytes and remaining destination guards are
verified after actual GPU fence completion,VMA flush/invalidate and barriers.
NEVER_ALLOCATE before a pool exists must fail with VK_ERROR_OUT_OF_DEVICE_MEMORY
and null output handles. Map/unmap,destroyBuffer,destroyAllocator and Vulkan
cleanup are actual native calls. A5second incomplete fence retains resources
until app close;unsafe cleanup is not attempted. No game window or music opens.

```sh
python3 tools/build_lwjgl_vma_native.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline
python3 tools/build_lwjgl_vma_native.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --host
python3 tools/test_vma_bootstrap_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --vma-bootstrap
python3 tools/test_client_vma_package.py --runtime-workspace /path/to/PS5_Homebrew
```

Omit --offline for a first verified dependency fetch. Host checks use real
MoltenVK/VMA/JNI with UBSan,Xcheck:jni and Xverify:all,both normal Mac and a
host-only PS5 enum selector. Host-only paired JAR metadata contains the host
native hash;target/cached original JARs are untouched. The exact main and nested
allocation fixture bytecode are compared against the console package. A host
pass does not establish PS5 driver/VMA compatibility or menu success.

Install local dist/client-vma_bootstrap/PPSA99874.zip or runtime workspace
dist/PPSA99874.zip. PPSA99874 replaces the existing app. Launch and press X
once;report all five rows. After failure leave the app open for reports,or reopen
without pressing X if it closes. No device IP/filter is embedded in the app.

Human ALL5 PASS and matching saved session/detailed startup on2026-10-25
establish the tested
PS5 VMA/JNI/GPU transfer/cleanup workload. Images,
custom pools,defragmentation,budgets,virtual allocations,allocation callbacks,
concurrent/large workloads and full native teardown remain unvalidated.
SPIRV-Cross and broader SDL integration are incomplete;Minecraft startup/menu/
world/gameplay and server two-hour endurance remain unvalidated. Endurance is
deferred. Preserve all frozen milestones and failed034/032/030 packages.

Original VMA MIT notice/implementation and LWJGL BSD/Vulkan header licenses
are bundled under vma-licenses. A future public OpenAL-linked binary release
must include matching corresponding-source and exact relink materials first.

Host and full package checks pass. Full local package SHA-256:
`7e62bc9b982a48f0ffbb9fe384b40f100d132fcd6be271fdc1df13c1738d46fd`.
Human PS5 ALL5 PASS and matching saved session/detailed startup recorded
on2026-10-25. All12RADV transfers,3allocator/device lifecycles,source/output/guards,
NEVER_ALLOCATE controls,cleanup and DestroyJavaVM are corroborated in the current run.
Client_VMA_Allocator preserves the accepted source/package/validation/release.
Continue development outside the frozen folder.
