# Client Vulkan Bindings 01.000.005 — console failure recorded

**Console result:** row9 failed with `PS5 resident library unavailable: ps5clientgpu`. The fixture used an unmapped logical name in the SharedLibrary provider. [Client006](client-vulkan-bindings-006.md) corrects that lookup;005 is not a passing milestone. The following records the005 design and original candidate scope.

Client005 exercises the original upstream LWJGL3.4.3 Vulkan Java bindings, structures and instance/device capability tables against the actual statically resident RADV driver. It builds on frozen Client_GPU_Integration004 ALL PASS. **All ten PS5 rows are pending for this exact build**; host GPU success is not a console pass.

The Vulkan JAR is unchanged. LWJGL's supported `VK.create(FunctionProvider)` entry accepts the existing PS5 resident SharedLibrary provider. The consumer adds one standard `vkGetInstanceProcAddr` C entry which forwards directly to the real ICD's `vk_icdGetInstanceProcAddr`. The original generic core JNI functions execute upstream VK10 command bindings; the new test does not route GPU commands through004's hand-written `transfer` JNI function. No Vulkan-JAR transformation, replacement Vulkan Java class, game-JAR rewrite, desktop-OS spoof or fabricated driver result is introduced.

## Run on PS5

Install the complete `PPSA99874` folder from `dist/client-vulkan/PPSA99874.zip` (also copied to the runtime workspace's current `dist/PPSA99874.zip`). Same app/content identity, client version **01.000.005**. Installing replaces the existing app; frozen000–004 and server packages stay preserved.

Run **all ten rows in order** using D-pad and X:

1. Initialize the embedded runtime.
2. Create the Java25 interpreter VM,128MiB and compact headers.
3. Verify54 original client/Java artifacts and noninitializing classes.
4. Check the explicit PS5/x64 platform/provider boundary.
5. JNI direct buffers and errors.
6. Resident JNI library loading and actual function lookup.
7. Actual LWJGL native memory/core/provider tests.
8. The passing004 Java/JNI GPU copy/fill/readback fixture, now part of this exact build.
9. **LWJGL Vulkan: standard commands and GPU readback.** The new test creates real upstream VkInstance/VkDevice capability tables and uses standard Vulkan structures/commands. It checks12 GPU copy/fill/readback transfers,8 through65536bytes, full returned-word and remaining-buffer guard checks, three instance/device lifecycles, duplicate VK loader initialization rejection and loader cleanup.
10. DestroyJavaVM; the native probe menu stays active.

The menu remains CPU-rendered. This test uses offscreen buffers and does not repeat003's RGB display sequence. Leave the app open for reports at `http://<PS5-IP>:8765/`. After a crash, reopen without running any rows to preserve prior reports. No device addresses or client filters are packaged. A failure should retain its exception details/checkpoints; a successful host build does not establish that the PS5's class verification and capability initialization will pass.

## GPU and lifecycle scope

The Java fixture uses original VK10 allocation/mapping, queue/command-pool, buffer-copy/fill, pipeline-barrier, fence and resource-destruction commands. Source/destination host writes are flushed, GPU writes are fenced and invalidated before Java reads them. Each completed transfer checks the entire requested result and every remaining destination byte. Buffers/memory, command pools/fences, devices and instances are destroyed on normal completed paths; the VK loader/provider is closed and a repeated destroy is checked.

The implementation requests a five-second GPU fence timeout. If the wait does not complete, possibly in-flight allocations and their context remain resident until relaunch; their mappings are deliberately not freed while the GPU may still use them. This is fail-and-relaunch behavior, not full timeout recovery. Broader failure/low-memory cleanup, global native destructor lifecycle, prolonged GPU load and full Vulkan API coverage remain unvalidated.

This validates selected **standard LWJGL Vulkan command bindings**, not every Vulkan command/extension or the whole renderer. SDL/window integration, Java-driven presentation, shader pipelines, audio/controller gameplay and Minecraft main/menu/world remain ahead. The separately passing native003 display result is preserved, not inferred to pass through Java. Server two-hour endurance remains deferred.

## Build, provenance and checks

The005 packager composes the existing client002 JVM embedding and004 scoped native GPU support, adding only the new resident loader object and Java fixture. The shared link helper accepts the consumer variant/version while retaining004 defaults. Runtime SDK/HotSpot source/module image and all54 original client/Java artifacts are unchanged. The existing disclosed BSD LWJGL core/platform port remains; the upstream Vulkan JAR is bit-identical to the pinned original. The005 GPU audit records the loader object's SHA256 and Java fixture source SHA256 in addition to the004 scoped-provider, constructor and native-object audit.

```sh
python3 tools/prepare_client_graphics.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/package_client_graphics.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25
python3 tools/test_client_vulkan_package.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/test_client_vulkan_host.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25
```

The host test executes the same Java Vulkan fixture on the Mac's physical GPU using installed MoltenVK1.4.1, real core JNI and the resident-provider class backed by real host `dlopen`/`dlsym`. The host-only provider opens the actual MoltenVK path and enables its reported portability-subset device extension. It does not run the PS5 registry/ABI or claim RADV validation. No desktop dynamic-loader JNI methods are added to the core subset. The core host-test JAR carries the actual locally rebuilt native-library hash; checking remains enabled. The original Vulkan JAR is SHA256-checked before and after the run, with no host-only rewrite.

Host checks pass under Java25 `-Xint -Xcheck:jni -Xverify:all` and actual core UBSan: standard global/instance/device command-table construction,12 GPU transfers and full readback/guard verification, three real instance/device lifecycles, duplicate initialization rejection and idempotent loader teardown. There are no missing-native-method, JNI-checker or UBSan errors. These results do not validate target compilation's PS5 ABI at runtime.

Target checks pass for native conversion/signatures, shared title/version, actual loader/ICD/JNI/GPU exports and system AGC imports,359 deferred core constructors, four correctly ordered explicit graphics constructors and no automatic startup constructors. Object audits, resident groups, scoped zlib/allocator/thread/TLS providers, exact original Vulkan/all54 JAR hashes,002 moduleimage/native-library bytes and frozen000–004/Fabric094/Paper108 package hashes are verified. Raw reports and build outputs remain local/ignored. No new milestone/release is frozen before human console ALL PASS.

Next after acceptance: SDL/window integration and shader rendering through the standard Vulkan bindings, with their own console checks before game startup.
