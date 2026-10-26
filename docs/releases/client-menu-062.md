# ProsperoCraft — the first Minecraft Java menu on PS5

![ProsperoCraft first menu release](client-menu-062.svg)

**Minecraft Java's menu is here, running on native Java 25 on PS5.**
On 26 October 2026, the user confirmed that client **01.000.062** reached the
visible menu. This release preserves that exact executable and celebrates the
first menu checkpoint after the native graphics, shader, font, codec and
callback milestones.

[Download the GitHub release](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/Client_Menu-v01.000.062)
· [Console confirmation](../validation/client062-menu-confirmation-2026-10-26.json)
· [Release validation](../validation/client062-release.json)

## What you get

- The menu-confirmed PS5 app, native Java 25 runtime and resident native ports.
- Original Minecraft 26.3 startup through its original Main class, using the
  Vulkan graphics backend. No replacement game classes or rewritten game JARs.
- A standalone Python helper that restores **all 54 pinned original JARs and
  all 5,147 asset objects**, with checksums checked before installation.
- SHA-256 checksums, validation details, and matching OpenAL corresponding
  sources and native relink materials.

This is a full GitHub release with a deliberately narrow acceptance scope:
**the visible menu on the actual console**. It is an experimental client build.
Menu interaction, controller gameplay, worlds, saves/reloads, repeated startup,
full teardown and long-run stability have not been accepted. The OpenAL port
currently provides null/loopback backends; **PS5 speaker output is not implemented**.
New options files mute sound; existing options files are preserved.

## Install

You need a PS5 capable of running the project's homebrew app format, your usual
homebrew launcher/installer, a desktop with **Python 3.11 or newer**, and enough
space for the download cache and reconstructed app. Use your legitimate Minecraft
installation/entitlement; this release does not collect Microsoft credentials or
provide an account login. The current harness launches the supported offline
demo path with multiplayer and chat disabled.

1. Download these assets into one working directory:
   `ProsperoCraft-01.000.062-menu-app-only.zip`, `client062-install-manifest.json`,
   `provision_client_menu.py`, `SHA256SUMS` and `README-client062.md`.
   `client062-validation.json` records the detailed checks. Developers can also
   download `client062-openal-source-relink.zip`.
2. Check the downloaded files against `SHA256SUMS`. On macOS/Linux, run
   `shasum -a 256 -c SHA256SUMS` after downloading all listed assets. To verify an
   individual file, compare its `shasum -a 256 filename` output with that line.
3. Extract the app ZIP. It creates a `PPSA99874` directory. The public ZIP omits
   downloaded game/dependency JARs and asset objects, so provision them **before**
   copying/installing the app:

   ```sh
   python3 provision_client_menu.py --manifest client062-install-manifest.json --app-dir PPSA99874 --cache-dir minecraft-originals --download
   ```

   The helper downloads missing files from the exact pinned publisher URLs,
   verifies every retained app file and every restored file, and checks the
   final file inventory. It never launches the game or asks for credentials.
   Keep the cache for retries. A corrupted cached file is refused; remove that
   specific damaged cache file and rerun to download it again.

   If you already prepared this repository's pinned originals, use:

   ```sh
   python3 provision_client_menu.py --manifest client062-install-manifest.json --app-dir PPSA99874 --jars-dir /path/to/ps5-minecraft-java/build/client/jars --assets-dir /path/to/ps5-minecraft-java/build/client-assets
   ```

4. Install/copy the **fully provisioned** `PPSA99874` directory using your normal
   homebrew workflow. If your installer needs an app-folder ZIP, zip that complete
   directory with `PPSA99874/` at the archive root. The release app-only ZIP is not
   ready to launch until the originals have been restored.
5. Launch the app and press **X once** at its startup screen. Allow resource and
   shader loading to finish. There is no measured startup-time guarantee.
   If it crashes, reopen without pressing X to preserve the reports for diagnosis.

**Shared title ID: PPSA99874. Installing this client replaces the server app.**
Keep the [Fabric/Paper server release](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/Fabric-Paper-v01.000.108)
and your server/world backups for restoration. No side-by-side installation is claimed.
This release does not add a Prospero Store listing or change its reservation.

## What changed in 062

061's final native trace was inside OpenAL's app-local current-directory lookup
during HRTF discovery. 062 passes the existing game-data directory explicitly
through OpenAL's supported `ALSOFT_LOCAL_PATH` setting, avoiding that default
lookup. Existing nonempty explicit settings are respected and real file discovery
is retained. The exact preceding PS5 crash mechanism remains unproven.

The accepted executable retains the existing diagnostic logging and bounded
startup observer. These can affect timing and are part of the tested bytes.
Java runs in interpreter mode with the existing 256 MiB heap; this release makes
no world performance or frame-rate claim. There is no SDK, game-JAR or asset rewrite.

## Reproduction and source

Tested implementation:
[`f3349a1`](https://github.com/mateo-cogeanu/ProsperoCraft/commit/f3349a1fb90a9304d7aa808b339bd37738607d14).
The release tag adds packaging, provisioning and documentation without rebuilding
the accepted app. The complete tested local package has SHA-256:

```text
26f31cc26bc960d3c7e35205c0280e8b83bc6e475a17b8383c778583cf952b88
```

That full local ZIP contains original downloaded game files and is not published.
The public ZIP has a different hash, recorded in `SHA256SUMS` and release validation.
Provisioning was tested against **every file and byte** of the accepted package.
Actual pinned JAR/asset downloads, corrupted JAR/asset refusal and retained-file
tampering refusal were also checked.

The matching `client062-openal-source-relink.zip` contains original OpenAL Soft
1.25.2 sources, the modified startup sources, scope header, explicit-path/trace
shim source and object, build records, SDK headers and exact native link inputs.
Its README describes rebuilding, editing and replacing OpenAL. Both an unmodified
relink and the accepted-library replacement path reproduce the tested native ELF:

```text
df5074be95daae364f7f49fc8e7a91749e41e1888042ef59fe04b18ef02b43f2
```

Building a replacement directly from the included modified sources and linking
it was also checked; source rebuilds can differ in bytes and do not inherit
console acceptance. Normal homebrew ELF-to-SELF packaging instructions are linked
from the kit. Original native dependency notices remain in the app and source
materials. OpenAL is LGPL-2.0-or-later; other bundled components retain their
respective licenses. Project sources/pins are in the release tag, and reusable
Java port sources are in
[ps5-java25-homebrew](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/1e9fb4f23a2e84e26c50fe67cc4e746ff371dfa2).

## What comes next

The goal remains a polished, playable Minecraft Java client on native PS5 Java 25:
responsive controls, rendering, real audio, world gameplay, saving/reloading and
stability. This menu release is a real step toward that goal. It does not replace
those remaining console tests or establish a formal full-client ALL PASS.
Server two-hour endurance remains deferred.
