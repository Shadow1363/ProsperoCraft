# ProsperoCraft — playable Minecraft Java on PS5

![ProsperoCraft playable release](client-playable-066.svg)

**The world is playable. Native Java25 with guarded C1 compilation makes the difference.**

On 26 October 2026, the user reported that **01.000.066 is blazingly fast**,the world
is playable,game startup takes roughly 30 seconds,and world loading is much better.
These are real console observations,not a controlled benchmark or universal startup
promise. This full GitHub release preserves that exact build.

[Download](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/Client_Playable-v01.000.066) ·
[Human confirmation](../validation/client066-playable-confirmation-2026-10-26.json) ·
[Hashed reports](../validation/client066-playable-reports-2026-10-26.json).

## What's improved

066replaces interpreting every Java method with guarded C1 level 1 compilation:
onecompiler,16MiBcodecache,and bounded compilation arenas. A real integer-kernel
compilation and checksum gate passes before original Minecraft Main. Retrieved
PS5reports confirm that gate and playerjoin,with no captured heapOOM. The512MiB
uncompressed direct-backed heap and native RADV/Vulkan renderer remain.

The SDLrelative-mouse backend now permits capture,allowing temporary left-stick
WASD and right-stick look. Menu navigation remains available. This is still a
basic temporary mapping;Controlify remains the preferred future mod integration.
No game-JAR rewriting,bytecode hooks or replacement Minecraft classes are used.
All54originalJARs and5,147assetobjects remain intact.

**Sound is not implemented in this release.** OpenAL currently provides null and
loopback backends,and earlier launcher-created options mute music/master volume.
The next development candidate targets actual speaker output. Other limits:
full text entry/rebinding/controller polish,save/reload,repeated startup,hardware
utilization measurements and endurance remain pending. The retrieved run later
loggedMinecraftStoppingandreturnedtoharness;that is not a formal shutdown/endurance
pass. No FPS or full-hardware-utilization claim is made. Server2Hrun remains deferred.

## Install

Use a PS5 capable of this project's homebrew app format and your normal
homebrew launcher/installer. Desktop provisioning requires Python3.11+ and space
for a cache and full app. Use your legitimate Minecraft installation/entitlement.
The harness uses the supported offline demo path,multiplayer/chat disabled,and
collects no Microsoft credentials.

Download `ProsperoCraft-01.000.066-playable-app-only.zip`, `client066-install-manifest.json`,
`provision_client_menu.py`, `README-client066.md` and `SHA256SUMS`. Check each
SHA256 before use. With all listed assets downloaded,macOS/Linux can run
`shasum -a 256 -c SHA256SUMS`;individual hashes can be compared with
`shasum -a 256 filename`.

Extract the ZIP to obtain `PPSA99874/`,then restore every excluded original:

```sh
python3 provision_client_menu.py --manifest client066-install-manifest.json --app-dir PPSA99874 --cache-dir minecraft-originals --download
```

The helper name is retained for compatibility. It restores **all54JARs and5,147
assetobjects** from exact publisher URLs,verifies each file and the final inventory,
and refuses corruption. Already verified originals can be supplied with
`--jars-dir /path/to/build/client/jars --assets-dir /path/to/build/client-assets`.
Do not install the app-only ZIP before provisioning. A bad cached file is refused;
remove that specific damaged file and rerun. No game launch or login is performed.

Copy/install the complete `PPSA99874` folder using your normal workflow. If your
installer needs ZIP,zip that complete folder with `PPSA99874/` at the root. Launch,
pressXonce,andreleaseitduringloading. The C1gate must pass before Minecraft starts.

| Control | Menu | Captured in world |
| --- | --- | --- |
| D-pad | Arrows | Arrows |
| Left stick | Navigation | WASD |
| Right stick | — | Camera look |
| X | Select | Jump |
| Circle | Back | Pause/Escape |
| Triangle | Tab | Inventory |
| Square | Backspace | Backspace |
| R2/L2 | Mouse buttons | Punch/use |

If it crashes,reopen withoutX to preserve reports. Do not delete/reset worlds.
TitlePPSA99874 is shared with the server: this replaces that installation. Preserve
world backups and the [Fabric/Paper release](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/Fabric-Paper-v01.000.108).
Older [065world](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/Client_World-v01.000.065)
and [062menu](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/Client_Menu-v01.000.062)
checkpoints remain available. No Store submission/listing change is included.

## Reproduction and licensing

Tested consumer implementation `59c3d1018102c8662572d6179c7e489bbb7245b1`;
runtime `44fdf26ccb74cf8dd9127f1256b85416856981de`. The accepted app is not rebuilt
for publication. Full local ZIP hash (original downloaded files included locally,
not redistributed):

```text
0b549873222b155fd21b4a441535390660598096f3f32c27081a963d00ea7802
```

Public app-only hashes are in `SHA256SUMS`. Provisioning is checked against every
file/byte of the accepted full app,with actualJAR/assetdownload/corruption controls.
`client066-validation.json` records build/release checks.

A fresh `client066-openal-source-relink.zip` supplies exact native link inputs,
original/modifiedOpenALsources,scopeheader/envshim,SDKheaders/buildrecords and
editable replacement instructions. Unmodified relink and accepted-library
replacement reproduce the tested ELF. Read itsREADME;edited/rebuilt apps do not
inherit console acceptance. Existing component licenses/notices remain in the app.
Corresponding Java port sources/patches are at
[the matching runtime revision](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/44fdf26ccb74cf8dd9127f1256b85416856981de).

This release celebrates playable world performance. It does not establish a formal
full-client ALLPASS or remove the remaining audio,save/reload,polish and stability work.
