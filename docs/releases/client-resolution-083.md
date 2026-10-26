# ProsperoCraft01.000.083 — fixed1080p menu alignment

083addresses the reported Store082menu-click misalignment by locking the game
and native display to1920×1080. Previously, the launcher could request720p/900p
while Vulkan presented1080p, leaving logical GUI/input coordinates mismatched.

[Release/downloads](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/01.000.083) ·
[Implementation and Settings preview](../client-resolution-083.md) ·
[Build record](../validation/client083-1080p-build-2026-10-26.json) ·
[Release validation](../validation/client083-release-2026-10-26.json)

## Changes

- Always launches with1920×1080dimensions.
- Migrates existing saved resolution choices to1080p with a previous-library backup.
- Shows the resolution as locked; X/LEFT/RIGHT cannot change it.
- Forces SDL logical window creation and resize to1080p with fixed bounds.
- Selects only real enumerated1080pVulkan modes; normal refresh is preferred.
- Includes the projectGPLv3license and mateo-cogeanu — ProsperoCraft attribution.

## Install/update

Use the exact **PPSA99874.zip** from the083release. Once the Store catalog update
has merged and deployed, ProsperoStore will offer083as an update to082. Manual
installation: extract the complete PPSA99874folder to `/data/homebrew/` using your
existing ShadowMountPlus workflow. Keep sce_sys/param.json and all assets.
It requests4096MiBof download storage with the existing title/content identity.

Preserve `/download0/ProsperoCraft`; do not clear instances, cache, options or
worlds. The first083launcher open normalizes old resolution settings and saves
an exact prior-library backup. The app ZIP contains no official Minecraft game
JARs/assets. Downloads still come from verified original publisher artifacts on
the console; no desktop provisioning is required.

Only exact26.3SDLdemo is eligible for launch. Microsoft application approval and
full-account access remain pending; no ownership bypass or game-JAR modification.
An actual enumerated1920×1080mode is required. The app rejects unsupported output
sizes instead of silently accepting a misaligned fallback. Other game video/audio
options and the082controls, lifecycle and accepted074configuration are retained.

This title ID is shared with the server app, so installing the client replaces
that app installation. Preserve separate server packages and world backups.

## Validation and source

The user explicitly requested Store publication of this exact083build. Host
migration/control/dimension tests, actual SDL window/display fixtures, native
previews/input/cursor/lifecycle tests, target/package/signature/CRC/source audits
and matching OpenAL source/relink checks pass. **Exact083physical pointer alignment,
X/R2menu activation, demo-world startup, retained sound/smoothness and Quit/relaunch
are still awaiting PS5 confirmation.** No new ALLPASS or frozen milestone is claimed.
The earlier082human acceptance and later resolution regression remain recorded.

The public ZIP is byte-for-byte the083candidate:
`8fcbdc8cb9cc8065aa0eaac26457a834fffb15098725e987df1d33257a76444e`.
Implementation commit97d2b14c7e3f0ee35e5d63750d743bf0149fe594; runtime source
9afa03adfb34dc1049f18de5839d762662b6c306. The release tag also includes publication
metadata and the exact branded source sce_sys/param.json for catalog version checks.

Attached SHA256SUMS covers the app, validation records and fresh
client083-openal-source-relink.zip. That kit includes exact native link inputs,
original/modified OpenAL sources, PS5 speaker backend, headers/build records and
editable replacement instructions. Unmodified relink and accepted-library
replacement reproduce the exact packaged ELF. The included source builder and
replacement link were exercised. Changed binaries do not inherit console acceptance.

Original ProsperoCraft code is GPL-3.0-or-later; preserve copyright/license notices
and meet corresponding-source obligations. Root LICENSE/NOTICE and their copies
inside the ZIP identify mateo-cogeanu — ProsperoCraft and upstream contributors.
Upstream components keep their own licenses; official game files are not relicensed.
Exact082package, tag, source snapshot and validation remain unchanged as a fallback.
