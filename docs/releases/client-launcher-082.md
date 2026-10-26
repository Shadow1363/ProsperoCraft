# ProsperoCraft 01.000.082 — native launcher for PS5

082 brings the native instance library, verified on-console downloads, expanded
DualSense controls, menu pointer/text picker and the accepted074 sound/performance
baseline to the public release. It adds the compact saved welcome checkbox,
horizontal focus, native left-stick navigation and bounded focus/press animation.
A verified clean Minecraft quit requests a fresh launcher process for safe device
and JVM ownership. Exact082 PS5 quit/relaunch and regression checks remain pending.

[Release and downloads](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/01.000.082) ·
[Build record](../validation/client082-launcher-build-2026-10-26.json) ·
[Release validation](../validation/client082-store-release-2026-10-26.json) ·
[Controls](../client-controls-081.md) · [082 changes and lifecycle](../client-launcher-082.md)

## Install and play

Download **PPSA99874.zip**, or install ProsperoCraft through ProsperoStore once
the catalog submission has merged and deployed. Extract the complete PPSA99874
folder to `/data/homebrew/` for ShadowMountPlus, following your existing native
homebrew installation workflow. Keep `sce_sys/param.json`: it requests4096MiB
for downloads. This release is an app-folder ZIP, not an ELF payload or PS4 PKG.

The package contains the launcher, native Java25 runtime and redistributable
bindings. **No Minecraft game JARs or assets are bundled. No desktop provisioning
is required.** Start the app, add a **26.3** instance and choose Download & Play.
The console downloads original publisher artifacts with pinned hash verification.
The first game download needs internet and available app download storage.
New installs have an empty library; existing instances/downloads/settings/worlds
under `/download0/ProsperoCraft` are retained. Do not delete that folder to update.

Only exact26.3 with an SDL receipt is eligible for demo launch. Other versions
can download but remain clearly unavailable for launch. Microsoft application-ID
approval is pending; full-account play remains blocked by normal ownership and
service checks. No other public ID, ownership bypass or game-JAR patch is used.
The demo's normal vanilla restrictions apply. Minecraft is not included, and the
project is unaffiliated with Mojang or Microsoft.

TitlePPSA99874 is shared with the Fabric/Paper server app: this client replaces
that installation. Keep existing server/world backups and the separate
[server release](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/Fabric-Paper-v01.000.108).
It does not provide simultaneous client/server installations under this title ID.

## Controls and limits

D-pad or left stick navigates the native launcher; L1/R1 selects the top bar.
X selects, Circle returns, and Options opens the controller guide. The welcome
uses LEFT/RIGHT between OK and the saved Show next time checkbox; X activates.
Settings can restore the notice and enable Reduced Motion.

In game, left stick moves and right stick looks; X jumps, Circle sneaks, Options
pauses, Triangle opens inventory, R2 attacks and L2 uses. In menus, right stick
moves the pointer; X/R2 and L2 click, L1/R1 scroll and Circle returns. Touchpad+R3
opens the text picker. The in-launcher guide lists the full081 temporary layout.
Controlify, full Unicode and touch-surface pointer tracking remain future work.

The publication request approves this exact082 for Store submission; it is not a
formal full-client ALL PASS. Exact082 launch → quit → library → relaunch, retained
worlds/sound/smoothness, stick/reconnect behavior and checkbox persistence still
need PS5 validation. The new quit path uses OS self-replacement, never another
Minecraft Main or JVM in the existing process. A rejected LoadExec remains an
explicit failure. Account credentials are memory-only and reset with the process.
The older074 sound/smoothness report does not establish an082 regression pass.

## Reproduction and source

The install ZIP is byte-for-byte the built082 package:
`ab49cad8977736be2be72230743232a270dba9bd17fa70a66b64a93c48230820`.
Its packaged consumer implementation is commit
a7b70eac899941f7d60eb2ece5f27257e9a8f4d1; the release tag also includes release
metadata and packaging documentation. The root `sce_sys/param.json` is an exact
copy of the branded manifest inside the published ZIP for catalog update checks.

`client082-openal-source-relink.zip` contains the exact native link inputs,
OpenAL corresponding original/modified source including the PS5 speaker backend,
SDK headers/build records, notices and editable replacement instructions. Both
unmodified relink and the accepted-library replacement reproduce the packaged
ELF. The included source builder and replacement link were exercised separately.
Modified binaries do not inherit any original console observations. Read the
included README and source licenses. SHA256SUMS covers every attached asset.

The matching reusable Java runtime source/patches are published at
[9afa03ad](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/9afa03adfb34dc1049f18de5839d762662b6c306).
Component license notices remain in the app and source kit. GitHub detects no
single repository license, so the catalog uses its Unlicensed classification;
this does not replace or remove upstream components' licenses.
Exact081 and accepted074 packages/symbols and all frozen milestones are preserved.
