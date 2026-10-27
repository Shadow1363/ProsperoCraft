# Fabric and Modrinth — development build 01.000.103

New instances offer Version, then Loader: Vanilla, Fabric and NeoForge
(coming soon). Existing libraries migrate missing loader fields to Vanilla.
Existing worlds and shared Mojang downloads stay in place. Only Minecraft26.3
can currently launch; other26.x downloads retain their existing coming-soon gate.

Instance Settings contains Mods, Shaders and Resource Packs. Each browser shows
six projects per page, ordered by downloads, with search above the list. X toggles
a checkbox. Download All processes the instance's persistent queue across all
three categories, including required mod dependencies. Queues survive navigating
between categories and restarting the app. Circle cancels work; verified staging
files and queued selections survive failures for retry. Resource packs go in
`game/resourcepacks`, shader packs in `game/shaderpacks`, mods in `game/mods`.
Packs still need to be selected in Minecraft; downloads do not enable them.

Modrinth search/version requests filter the exact game version; mod requests
require Fabric and exclude server-only results. Downloads use the publisher's
size/hash pins and bounded HTTPS host allowlists. Required dependencies are
resolved before downloads; every body is verified before any new file is
published. Optional dependencies are not silently installed. Incompatible project
metadata and duplicate filenames/installed versions are rejected. Existing files
with different bytes are preserved, with an error explaining the conflict.
Required pack dependencies that cannot be handled are reported rather than
silently ignored. No automatic mod update or delete/toggle-installed manager is
included in this candidate; existing files can block conflicting additions.

Fabric uses its official stable loader profile, Maven libraries/checksums and
KnotClient entrypoint. Its receipt pins the selected loader for repair/reuse.
Fabric's supported `fabric.systemLibraries` setting keeps PS5 LWJGL/OSHI providers
and the already-prepared native configuration in the parent classloader; the
original game and mods use upstream Knot/Mixin. There are no new project-specific
game-JAR rewrites. Standard upstream Fabric/Mixin transformations are part of mod
loading. The official client JAR remains intact. Game launch still requires the
existing owning account check. Original vanilla launch and clean-quit verification
remain; Fabric shutdown uses the actual Knot target classloader.

## Vitrail test direction

The requested shader engine is [Vitrail Shaders](https://modrinth.com/mod/vitrail-shaders),
project `oSIKhgz3`. The live Modrinth test resolves Fabric26.3 release
`0.13.0-beta+mc26.3`, version `Q3nKuPKJ`, with required Sodium project `AANobbMI`.
Fabric API and Chloride are optional in that release's Modrinth metadata and are
not silently added. The live test verifies both downloaded JAR hashes.

Vitrail runs OptiFine-format packs on Minecraft's native Vulkan renderer. It is a
beta; desktop support does not establish PS5 GPU compatibility or performance.
Install Vitrail through Mods, download a pack through Shaders and select it in
Vitrail's in-game screen (upstream default key I, with rebindable controls).
ProsperoCraft already requests the Vulkan graphics backend. No shader pack is
bundled or selected automatically.

## Validation and PS5 checklist

Host fixtures cover queue persistence, compatibility filters, sorting/paging,
required mod dependencies, checksum mismatch/cancel retention, no partial group
publication before all bodies verify, path/host/link rejection, library migration
and disabled NeoForge. Live HTTPS checks cover official Fabric profile/libraries,
Vitrail+Sodium downloads and real shader/resource searches. Actual upstream Knot
finds the intact26.3 game, initializes Mixin and executes a fixture mod's preLaunch
entrypoint, then intentionally stops before graphics. Its target shares the
parent's LWJGL Configuration class. These are host checks, not a PS5 game pass.
Native and real Vulkan toolkit previews exercise the actual new draw paths.

On the exact103 app:
1. Check visible01.000.103 and existing Vanilla instance/account/world behavior.
2. Create26.3 with Fabric; verify loader download and visible instance identity.
3. Open each content browser; check popular list/search/paging and queue ticks.
4. Cancel/retry a download and reopen the app to confirm queue persistence.
5. Search Vitrail Shaders in Mods, queue it and Download All; check Sodium appears
   as a required dependency. Pick a shader pack from Shaders and a resource pack.
6. Launch Fabric without a shader pack first, then test Vitrail/pack rendering,
   controls, audio, FPS, world save/reload and quit/relaunch. Leave open for logs
   if a loader/native/GPU failure occurs. Shader settings hotkeys may need rebinding
   to available controller inputs.

Keep accepted101 and all frozen snapshots. This candidate is not a Store update,
public release, formal ALL PASS or a new frozen milestone. Fabric, individual mods,
shader rendering and performance need actual PS5 validation before roadmap ticks.

References: [Modrinth search](https://docs.modrinth.com/api/operations/searchprojects/),
[project versions](https://docs.modrinth.com/api/operations/getprojectversions/),
[Fabric Meta](https://github.com/FabricMC/fabric-meta),
[Fabric system-library property](https://github.com/FabricMC/fabric-loader/blob/0.20.1/src/main/java/net/fabricmc/loader/impl/util/SystemProperties.java),
[Vitrail source/install notes](https://github.com/avpbynf/Vitrail-Shaders).

[Exact build validation](validation/client103-fabric-modrinth-build-2026-10-27.json).
Package SHA-256: `a2416025dc8d37b6e6de678ba5e3816d2f0279339fb332921ee03bb725b6f47a`.
