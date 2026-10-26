# Fabric and Paper running on PS5

Release: [Fabric-Paper-v01.000.108](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/Fabric-Paper-v01.000.108).

Minecraft Java 26.3 now has positive PS5 playtest reports with both Fabric and Paper on the native Java 25 port. The user was very satisfied with Fabric094 and describes Paper108 as much more than acceptable and by far the best build yet. This full release celebrates those results and preserves downloadable app binaries. It does not establish a new ALL PASS milestone. The two-hour endurance run remains explicitly pending, and client work is now authorized.

- Fabric app: 01.000.094, loader 0.19.5, source `d43c3bd2fa044e40ce334a70a41769770b3244d7`.
- Paper app: 01.000.108, upstream Paper 26.3 build207, tested source `3a793f13e6459166bdfbccd71fb7e708946cb097` (the release adds documentation/provisioning only).
- Both alternatives use title PPSA99874: install one at a time. Keep your existing saved worlds backed up and retain the working local server package.
- The port adds no game-JAR rewrites or replacement game classes. Fabric uses its standard loader/Mixin mechanisms. Paper executes the upstream Paper distribution, rather than an unmodified Mojang server.
- Normal worlds, a configured 20-player limit and OP for admitted players are included. Twenty simultaneous players, arbitrary mods/plugins, complete plugin lifecycle/save/rejoin/stop acceptance and two-hour stability are not certified.

## Downloads and local setup

The two app-only ZIPs retain their tested bytes without rebuilding. They omit upstream game/dependency/loader JARs and personal `join-player.txt`. The project's probe and smoke mod/plugin remain included. The attached `validation.json` records each retained file and each excluded JAR, source commits, full local package hashes, public package hashes and evidence limits. Verify the downloaded files against the attached `SHA256SUMS`.

1. Download and extract the app-only ZIP for your chosen flavor, plus `validation.json` and `provision_release.py` from this release.
2. In a separate checkout of this repository, select the flavor's source commit above. Obtain the separately maintained [Java runtime workspace](https://github.com/mateo-cogeanu/ps5-java25-homebrew). The current preparation scripts expect the host Java 25 toolchain at `/opt/homebrew/opt/openjdk@25/bin/`; this preparation flow currently targets the project's macOS build host.
3. Prepare pinned upstream artifacts locally with the selected source checkout:

   ```sh
   python3 tools/prepare_server.py --runtime-workspace /path/to/PS5_Homebrew --flavor paper
   ```

   Use `--flavor fabric` for Fabric. Paper uses original upstream Paperclip on the host to prepare the pinned Paper distribution. This does not add project game transformations.

4. Restore only the excluded, exact-hash JARs to the extracted app and provision your own online account:

   ```sh
   python3 /path/to/provision_release.py \
     --manifest /path/to/validation.json \
     --flavor paper \
     --app-dir /path/to/extracted/PPSA99874 \
     --jars-dir /path/to/source/build/assets/java25/jars \
     --join-player YOUR_ACCOUNT
   ```

   Select `fabric` for the Fabric download. The helper verifies every retained app file and every required source JAR before writing. It retains the included probe/mod/plugin rather than substituting newly compiled versions. It writes the account only to your local app folder. Authentication and TLS remain enabled.

5. Close the existing PS5 app and install the complete provisioned PPSA99874 folder. Run initialization, CreateVM and VerifyJARs before Play. After a normal Paper stop, reopen the app for reports. Full endurance remains a later test.

The server baseline remains available while client graphics/native-binding work begins. No playable PS5 client is claimed by this release. Frozen ALL PASS snapshots remain unchanged.
