# Client GPU Integration 01.000.004 — PS5 ALL PASS

Client004 combines the passing Java25/LWJGL core with the pinned RADV dependency in one native process. Its new eighth row runs a consumer-owned Java fixture that allocates actual LWJGL native buffers, loads a real resident JNI library and submits offscreen Vulkan copy/fill commands. Java verifies every returned word and the destination guard bytes. It also checks malformed buffers, thread ownership, stale handles and three actual Vulkan instance/device create/destroy cycles.

**All nine rows pass on the actual PS5**, confirmed by the human user on2026-10-23. Exact source, package and validation are frozen in `Client_GPU_Integration/`. Client000/001/002/003 remain frozen passing snapshots with exact package hashes. TitlePPSA99874 and the server/client content identity are retained, with independent client version01.000.004. Installing replaces the installed app; earlier packages are preserved. The server two-hour run stays deferred.

## Run on PS5

Install the complete `PPSA99874` folder from `dist/client-gpu/PPSA99874.zip`, also copied to the runtime workspace's current `dist/PPSA99874.zip`. Run **all nine rows in order**:

1. Initialize embedded runtime.
2. Create the real Java25 interpreter VM (128MiB, compact headers).
3. Verify54 original client/Java artifacts and noninitializing class loading.
4. Check the explicit PS5/x64 LWJGL platform/provider boundary.
5. Run JNI direct-buffer tests.
6. Run ordinary resident JNI loading/function lookup.
7. Run the actual LWJGL native memory/core/provider tests.
8. **Java + LWJGL: real GPU copy, fill and readback.** This performs12 transfers from8 to65536 bytes across three create/destroy cycles. Expected malformed operations must throw; real GPU failures must fail the row.
9. DestroyJavaVM; the native menu stays active.

Use D-pad and X as in client002. This test keeps the CPU-rendered probe menu; it does **not** repeat003's RGB presentation sequence. The graphics work is offscreen so it does not contend with the menu's VideoOut ownership. Leave the app open after the rows for reports at `http://<PS5-IP>:8765/`. After a crash, reopen at the menu without starting any rows to preserve the prior run's logs. No IP address or client-address filter is packaged.

Vulkan acquire is unnecessary for offscreen work. Submitted work uses a five-second fence wait; internal driver calls can still hang/fault. On an incomplete submission, the bridge retains possibly in-flight resources and refuses further use/cleanup until relaunch. Normal completed paths destroy both transfer buffers and their memory after every operation, then the device/instance at close. This does not establish arbitrary timeout recovery or low-memory robustness.

## Integration boundaries

This is a consumer fixture with a narrow JNI bridge, **not the full LWJGL Vulkan command binding or SDL/window integration**. It invokes actual Vulkan through the statically linked RADV entry point. The official Minecraft client/server JARs and54 upstream dependency JARs remain intact. The existing explicit BSD-licensed LWJGL dependency port is unchanged in scope. No game class is replaced and no game bytecode is rewritten. No shaders, Minecraft main/menu/world, SDL, audio or gameplay are launched.

The Java image/native modules, runtime SDK and JVM sources are unchanged. The graphics dependency uses the separately pinned SDK platform cache from003. Its C++ ABI/unwind archives are checked byte-for-byte against the runtime SDK before sharing those implementations.

The consumer link scopes Mesa's zlib and its platform providers to their own symbol names. Graphics-owned allocation/thread/libc calls bind to the actual scoped platform implementations; Java's global allocator, thread and DNS definitions retain their existing bindings. The shared SDK C++ ABI's optional TLS-destructor callback is now connected to the actual scoped platform implementation for this combined app, rather than the previous absent callback. This explicit integration boundary passes in the nine-row PS5 fixture; it is not a JVM source patch or a fake-success fallback.

Four real graphics constructors are retained and run exactly once by the resident library's JNI_OnLoad after VM creation. Legacy `.ctors.N` priorities are normalized, placing compiler-rt CPU detection at priority90 before the three normal-priority Mesa initializers. The existing359 JVM/core constructors remain deferred to the first row. No constructors execute automatically at application startup. Graphics dependency globals remain resident until app close; Vulkan session resources are explicitly torn down, while full module/global destructor lifecycle remains unvalidated.

`assets/java25/gpu-integration-audit.json` records scoped provider names, bindings, constructor priorities and actual support/bridge object hashes. The normal resident-library audit has three genuine groups: ps5clientgpu, ps5clientbridge and lwjgl. AGC link stubs describe real Sony module imports; no stub implementation is linked into or shipped with the app. Component licenses/notices are included. Downloaded sources, binaries and reports stay local/ignored.

## Build and checks

Use the pinned003 graphics setup and a working Java runtime workspace. The preparation/link tools remain consumer-owned; reusable runtime embedding tools are used without changing the runtime repository.

```sh
python3 tools/prepare_client_graphics.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/package_client_graphics.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/package_client_gpu.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25
python3 tools/test_client_gpu_package.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/test_client_gpu_host.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25
```

The004 packager first regenerates the standard002 runtime embedding inputs, then adds the actual constructor-free GPU JNI object to the existing resident registry and links its scoped native dependency separately. It preserves the runtime's original constructor guards, real native-libc adapters and wrapping policy. The final link checks deferred constructor ranges and performs native conversion/signing. Intermediate002 packages are preparation outputs, not newly inferred console passes; the frozen tested002 package stays intact.

The actual Java/LWJGL/JNI test passes on the Mac's physical GPU through the installed MoltenVK1.4.1 direct driver, with Java25 -Xint/-Xcheck:jni/-Xverify:all and UBSan. The host-only branch uses MoltenVK's actual direct entry point and portability-subset device extension; it does not spoof PS5 behavior. It uses the real host LWJGL core and a host-test JAR paired with that rebuilt native library's genuine hash. It does not disable hash verification or change production JARs. All12 GPU copy/fill/readback transfers, Java word/guard checks, negative controls and three create/destroy cycles pass. This does not validate the PS5 ABI, scoped platform providers or RADV behavior.

Target checks pass for real JNI/GPU symbols and system AGC imports, scoped zlib/allocation/thread providers, the actual TLS callback binding, four priority-correct retained graphics constructors,359 deferred core constructors and zero automatic startup constructors. Package CRC/signatures/shared identity,54 original artifacts, exact002 Java image/native library bytes, object inventories and frozen000-003/Fabric094/Paper108 full-package hashes pass. The package SHA256 is recorded in `client/gpu/status.json` and `dist/client-gpu/SHA256SUMS`.

Next: standard LWJGL Vulkan bindings, SDL/window integration and shader rendering, each with its own PS5 checks. Server endurance remains deferred.
