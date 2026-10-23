# Client Vulkan Bindings 01.000.006 — resident-name correction

Client005 failed its ninth row on PS5 with the human-reported exception:

`ClientVulkan25: java.lang.UnsatisfiedLinkError: PS5 resident library unavailable: ps5clientgpu`

The generated resident registry contains the exact key `libps5clientgpu.so`. The fixture used `System.loadLibrary("ps5clientgpu")` correctly, but then passed that same short logical name directly to `PS5Library`, whose native open consumes the actual mapped library name. Its registry lookup therefore failed before the new row could initialize Vulkan's command tables. This is a consumer bootstrap error, not evidence of a driver/GPU failure. The original005 package and matching symbols are preserved locally under ignored `dist/failures/Client_Vulkan_Bindings-01.000.005/`; its console record retains the failure.

Client006 corrects that call to `new PS5Library(System.mapLibraryName("ps5clientgpu"))`. The actual port's `System.mapLibraryName` uses its normal library prefix/suffix; on PS5 this matches the existing `libps5clientgpu.so` registry key. No alternate alias, fake loader success, Vulkan command change, runtime source/SDK patch or Vulkan/game JAR modification is introduced. The host-only override continues to open the exact MoltenVK library path using real host dlopen/dlsym; host GPU success does not validate the target registry path.

## Run

Install client **01.000.006**, title **PPSA99874**, from `dist/client-vulkan/PPSA99874.zip`, also copied to the runtime workspace's current `dist/PPSA99874.zip`. Run **all ten rows in order**. Row9 is the standard LWJGL Vulkan transfer/readback test; row10 is DestroyJavaVM. The CPU menu remains visible. Keep it open for logs after the rows. After a crash, reopen without running rows to preserve the reports. Same app/content identity as the server and earlier clients; installing replaces the installed app. Frozen000–004 remain untouched. Server endurance stays deferred.

All ten rows require a new PS5 result. The ninth row still checks original LWJGL Vulkan structs/capability tables/commands,12real GPU copy/fill/readback transfers from8 to65536bytes, all returned words/guard bytes, three instance/device create/destroy cycles, duplicate initialization rejection and loader cleanup. Full Vulkan API/extension coverage, SDL/window integration, Java presentation, shaders and Minecraft startup remain unvalidated. [The005 design and scope](client-vulkan-bindings-005.md) remain applicable except for the failed short-name call corrected here.

Host Java25 -Xint/-Xcheck:jni/-Xverify:all, real core UBSan and physical MoltenVK GPU checks pass for the corrected fixture. Target package checks verify that the actual compiled fixture calls mapLibraryName and that the generated registry contains its expected mapped key, along with existing real loader/ICD/JNI/GPU symbols, signatures/CRC, exact original JARs/moduleimage/native libraries, constructor ordering/scoped providers and frozen package checks. The corrected target lookup still requires PS5 console validation.

Rebuild using `tools/package_client_vulkan.py` and validate using `tools/test_client_vulkan_package.py` and `tools/test_client_vulkan_host.py`, with the same runtime workspace/JDK25 parameters documented for005. The package SHA256 is recorded in `client/vulkan/status.json` and `dist/client-vulkan/SHA256SUMS`. No new passing milestone/release is created for this candidate.
