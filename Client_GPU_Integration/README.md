# Client GPU Integration — PS5 ALL PASS

Frozen milestone: **PPSA99874**, client **01.000.004**, user **ALL PASS** for all nine rows on **2026-10-23**. [Validation](validation.json) records the exact source/package/runtime pins and tested scope. Acceptance is the direct human report; no console logs were retrieved for this freeze.

Actual Java25, LWJGL native memory and a resident JNI bridge now submit RADV offscreen GPU copy/fill commands in one process. Java verifies all returned words and guard bytes for12 transfers from8 to65536bytes, plus malformed-buffer, thread-ownership and stale-handle controls. Three Vulkan instance/device create/destroy cycles, repeated close and final DestroyJavaVM pass alongside the seven earlier runtime/core checks.

This uses a narrow consumer JNI fixture, not full LWJGL Vulkan command bindings. SDL/window integration, shader rendering, Minecraft main/menu/world and combined presentation from Java remain unvalidated. Native003's separate GPU presentation snapshot remains preserved. Full module/global destruction, timeout recovery, broader GPU coverage and server two-hour endurance remain unvalidated/deferred.

The official game JAR and54 original client/Java JARs remain intact. Scoped graphics providers and a real shared-ABI TLS callback are disclosed in source and package audits; the runtime source and its SDK were not replaced. `client/` is the frozen source/pin/result snapshot. Use this release tag's root tools for reproduction and continue development outside frozen folders. Exact full ZIP and matching symbols are preserved under ignored `dist/milestones/Client_GPU_Integration-01.000.004/`.

## Download and local provisioning

The [Client_GPU_Integration-v01.000.004 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_GPU_Integration-v01.000.004) provides an app-only ZIP, validation.json, SHA256SUMS and helper. The ZIP retains tested bytes without rebuilding and omits54 original upstream client/Java JARs for local provisioning. Project fixtures, the BSD-licensed LWJGL port/native core, scoped RADV/platform and component notices remain included.

1. Verify the downloads against SHA256SUMS and extract the app-only ZIP.
2. In the tagged release checkout run `python3 tools/prepare_client.py`.
3. Restore the original files using `python3 provision_client_release.py --manifest validation.json --app-dir /path/to/extracted/PPSA99874 --jars-dir /path/to/repository/build/client/jars`.
4. Install the complete PPSA99874 folder and run all nine rows in order. Row8 is Java/GPU integration; row9 destroys the VM. The CPU menu remains visible; this does not repeat003's RGB sequence.
5. Leave the app open for logs at `http://<PS5-IP>:8765/`. After a crash, reopen without running any rows.

Provisioning verifies all retained files and source JARs, reconstructing every tested full-package file exactly. No account setup is required. This shared app identity replaces the installed server/client app; earlier packages remain available. Embedded audit records remain console pending because tested bytes are unchanged; the external validation records the later human pass.

Full tested package SHA-256: `0077d9f72e7a468e16bacfc075527c096d68decab1849e1252ba18405cf444b5`.

Next: standard LWJGL Vulkan bindings, SDL/window integration and shader rendering, with separate console checks before game startup.
