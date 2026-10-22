# Client Native Loading — PS5 ALL PASS

Frozen milestone: title `PPSA99874`, client version `01.000.001`. The human user confirms **ALL PASS** for all seven rows on2026-10-22. [Validation](validation.json) records the exact package/source/runtime pins and scope.

This adds real standard `System.loadLibrary`, a single `JNI_OnLoad`, ordinary JVM native-method lookup, scoped resident symbol lookup and calls to a genuine exported C function, with repeated handle use and missing/wrong-ABI/buffer error controls. The six foundation checks also pass. This does not initialize the LWJGL native core, load arbitrary ELF modules, create SDL/Vulkan presentation or launch Minecraft's menu/world. Server two-hour endurance remains pending.

`client/` is the frozen source/pin/acceptance snapshot. Use this release tag's root tools for reproduction. Preserve this folder and the exact compiled package; continue future changes in root `client/`. Full local package and symbols are preserved under ignored `dist/milestones/Client_Native_Loading-01.000.001/`.

## Download and local provisioning

The [Client_Native_Loading-v01.000.001 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Native_Loading-v01.000.001) provides an app-only ZIP, validation record, checksums and helper. The ZIP retains tested bytes without rebuilding, excludes54 original upstream client/Java JARs, and includes the project probes/resident JNI code plus the BSD-licensed dependency port. The original game JAR is unchanged.

1. Verify downloads against `SHA256SUMS` and extract the app-only ZIP.
2. In this release's checkout, run `python3 tools/prepare_client.py` to prepare the exact original artifacts locally.
3. Restore them with the attached helper:

   ```sh
   python3 provision_client_release.py \
     --manifest validation.json \
     --app-dir /path/to/extracted/PPSA99874 \
     --jars-dir /path/to/repository/build/client/jars
   ```

   Every retained file and source JAR is checked before copying. Provisioning reconstructs every file of the full tested package exactly; no account setup is required.

4. Install the complete PPSA99874 folder and run all seven rows in order. This shares the server app identity; installing it replaces that app. Earlier server releases and ClientFoundation000 remain available.

Next: actual LWJGL native core/function-provider integration and native presentation, then SDL/Vulkan and the real client menu. No GPU or gameplay result is inferred from this milestone.
