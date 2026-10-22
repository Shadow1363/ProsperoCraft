# Client Foundation — PS5 ALL PASS

Frozen milestone: title `PPSA99874`, client version `01.000.000`. The human user reports **ALL PASS** for all six foundation rows on2026-10-22. [Validation record](validation.json) identifies the matching package, source revision, runtime pin, dependency port and exact scope.

This proves the foundation probe: runtime initialization, interpreter VM creation, original client-artifact verification/noninitializing class loading, explicit LWJGL PS5/x64 platform identification with honest unported-native-loader handling, real JNI direct-buffer handoff and VM destruction. It does not launch Minecraft's main/menu, initialize SDL/Vulkan/audio or render a game frame. Server two-hour endurance remains pending.

`client/` is the frozen source/pin/acceptance snapshot. Use the release tag's root `tools/` for reproducible preparation/build and host checks; those tools were used with these source inputs. Preserve this snapshot; continue subsequent changes in the root `client/` development directory. The exact full tested package and symbols are preserved locally in ignored `dist/milestones/Client_Foundation-01.000.000/`.

## Public app-only download

The [Client_Foundation-v01.000.000 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Foundation-v01.000.000) includes the app-only ZIP, `validation.json`, `SHA256SUMS` and a provisioning helper. The ZIP preserves every included tested byte without rebuilding. It omits54 official client/Java JARs; the project probe and BSD-licensed LWJGL dependency port remain included. The original game JAR is unchanged. No account configuration or login is required for this foundation probe.

1. Verify the release downloads against `SHA256SUMS`, then extract the app-only ZIP.
2. Check out this release tag and run `python3 tools/prepare_client.py` to download/hash-check the pinned original artifacts locally. They remain in ignored caches and `build/client/jars/`.
3. Restore the excluded artifacts:

   ```sh
   python3 provision_client_release.py \
     --manifest validation.json \
     --app-dir /path/to/extracted/PPSA99874 \
     --jars-dir /path/to/repository/build/client/jars
   ```

   The helper checks every retained app file and every required JAR before writing. It retains the tested compiled dependency port, rather than rebuilding it.

4. Install the completed PPSA99874 folder and run all six rows in order. This shares the server app ID and replaces the installed server application. Server release packages remain available for reinstalling; client numbering starts independently at zero.

Future work: actual native LWJGL function resolution/core bindings, native presentation and SDL/Vulkan integration, then the real client menu. No further graphics or game acceptance is inferred from this milestone.
