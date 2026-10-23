# Client LWJGL Core — PS5 ALL PASS

Frozen milestone: title `PPSA99874`, client version `01.000.002`. The human user confirms **ALL PASS** for all eight rows on 2026-10-23. [Validation](validation.json) records the exact package, source/runtime pins and tested scope.

The actual upstream LWJGL3.4.3 native memory/JNI subset and PS5 resident SharedLibrary provider now pass on PS5: allocation, reallocation, calloc, aligned allocation, free, typed native views/copy, Unicode, MemoryStack, generic JNI malloc/free calls, actual symbol lookup/function invocation and missing/malformed/closed controls. The seven earlier runtime/JNI checks also pass.

The official game JAR and54 original client/Java JARs remain unchanged. The explicit BSD-licensed LWJGL dependency port and selected upstream native sources are disclosed in the frozen client sources and package audits. Full bindings/callbacks, arbitrary ELF loading, GPU presentation, SDL/Vulkan, audio/controller gameplay and Minecraft's menu/world remain ahead. Server two-hour endurance stays deferred.

`client/` is the frozen source/pin/acceptance snapshot. Use this release tag's root tools for reproduction. Preserve this folder and the exact compiled package; continue development outside it. The exact full local package and matching symbols are retained under ignored `dist/milestones/Client_LWJGL_Core-01.000.002/`.

## Download and local provisioning

The [Client_LWJGL_Core-v01.000.002 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_LWJGL_Core-v01.000.002) supplies the app-only ZIP, validation record, checksums and helper. The ZIP retains console-tested bytes without rebuilding and omits54 original upstream client/Java JARs for local provisioning.

1. Verify downloads against `SHA256SUMS` and extract the app-only ZIP.
2. In this release's checkout run `python3 tools/prepare_client.py`.
3. Restore exact original JARs with `python3 provision_client_release.py --manifest validation.json --app-dir /path/to/extracted/PPSA99874 --jars-dir /path/to/repository/build/client/jars`.
4. Install the complete PPSA99874 folder and run all eight rows in order.

Provisioning checks every retained file and original source JAR, reconstructing every file of the full tested package exactly. No account setup is required. This shares the server app identity; installing replaces the installed app. Earlier frozen client and server releases remain available.

Exact full tested package SHA-256: `d0b9f815ff68c5ad821b2166509879c623c813019d2f70bbacf53769f35e3971`.

Next: native GPU presentation, then SDL/Vulkan integration and Minecraft's real client menu.
