# Client Vulkan Bindings — PS5 ALL PASS

Frozen milestone: **PPSA99874**, client **01.000.008**, all ten rows confirmed
passing by the user on **2026-10-24**. [Validation](validation.json) records the
exact tested source, full-package hash, dependencies and scope. Retrieved logs
corroborate12 standard LWJGL GPU submissions, three complete instance/device
cycles, loader cleanup and final DestroyJavaVM.

The original LWJGL Vulkan3.4.3 JAR now drives actual RADV GPU copy/fill/readback
using its structs, supported VK.create(FunctionProvider), upstream VkInstance/
VkDevice capability tables and selected standard commands. Java verifies all
returned words and destination guard bytes for transfers from8 to65536bytes.
Earlier Java/core/resident-JNI/GPU checks also pass. The scoped graphics providers
and genuine SDK TLS-destructor callback remain disclosed in package audits.
The official game and54 client/Java artifact JARs stay intact.

008 also recovers from007's diagnostic ENOSPC failure by retaining bounded old
startup/VM log tails at explicit new-run initialization. Runtime ENTER/DONE
checkpoint sampling and quiet native-call context reduce diagnostic IO. The
runtime change is opt-in probe support; its JVM implementation and SDK are
unchanged. Menu-only reopening preserves logs. Full low-storage/IO-failure
robustness is not established by this successful run.

Complete Vulkan/extension coverage, SDL/window integration, Java-driven display
presentation, shaders, Minecraft startup/gameplay, full module/global destruction
and timeout recovery remain unvalidated. The server two-hour run stays deferred.
This milestone does not launch Minecraft. Frozen000–004 are preserved.

`client/` is the frozen source/pin/result snapshot; use this release tag's root
tools for reproduction. Continue development outside this folder. Exact tested
ZIP and matching symbols are preserved locally under ignored
`dist/milestones/Client_Vulkan_Bindings-01.000.008/`.

## Download and local provisioning

The [Client_Vulkan_Bindings-v01.000.008 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Vulkan_Bindings-v01.000.008)
contains an app-only ZIP, validation.json, SHA256SUMS and provisioning helper.
The app-only ZIP preserves tested files without rebuilding and omits54 upstream
client/Java JARs for local provisioning. Fixtures, dependency ports and license
notices remain included.

1. Verify downloaded files against SHA256SUMS and extract the ZIP.
2. In the tagged source checkout run `python3 tools/prepare_client.py`.
3. Run `python3 provision_client_release.py --manifest validation.json --app-dir /path/to/extracted/PPSA99874 --jars-dir /path/to/repository/build/client/jars`.
4. Install the complete PPSA99874 folder; run all ten rows in order. Row9 tests standard LWJGL Vulkan commands; row10 destroys the JVM.
5. Keep the app open for logs at `http://<PS5-IP>:8765/`; after a crash reopen without running rows.

Provisioning verifies every retained file and original JAR and reconstructs all
tested package files exactly. Corrupt retained/JAR checksum inputs are rejected.
No account setup is required. Installing replaces the shared-ID server/client
app. Embedded audit records remain console pending because tested bytes are
unchanged; the external validation records the later console pass.

Full tested package SHA256:
`d6132b1f56fbbc892577019ec3b86a6abcd31b2dc50b670543afa5cb9596ddb4`.

Next: SDL/window integration and shader rendering, each with separate PS5 checks
before attempting game startup.
