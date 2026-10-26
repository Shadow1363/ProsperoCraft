# Fixed1080p pointer alignment — candidate01.000.083

The user reports that the Store-installed082can display Minecraft but X/R2
cannot activate the demo-world/menu controls, and identifies resolution mismatch
as the cause. Source inspection finds that082defaults to1280×720logical game
size while the native Vulkan path normally selects1920×1080. That mismatch is
consistent with misaligned GUI hit testing. No current-run logs independently
corroborate the coordinate values. The earlier082human pass remains a historical,
scoped result; this later regression report adds a resolution-specific limitation.

083locks game size to **1920×1080** throughout launch arguments, native SDL
window creation/resize and actual enumerated Vulkan display-mode selection.
A display without a real1080pmode is rejected rather than silently selecting
another size. Normal refresh is preferred among available1080pmodes.
The native Settings row reads **1920 x1080(locked)** and has no edit arrow.
X, LEFT and RIGHT cannot change it. Old saved0/1/2resolution choices normalize to
legacy index2and are saved with an exact prior-library backup. No instances,
downloads, worlds, game options or sound settings are deleted/reset.

[Actual native Settings preview](launcher/083/settings-locked.png) ·
[Build and checksum record](validation/client083-1080p-build-2026-10-26.json)

The SDL window callback reports1920×1080and fixed bounds even when a game asks
for an older size, keeping logical input coordinates and the physical surface
in the same space. The cursor/input adapter and official Minecraft JARs remain
unchanged; no game hooks or transformations are added. Existing082Quit/relaunch,
controller/notice/animation behavior and074audio/performance configuration remain.
The new package also includes the projectGPLv3license and attribution notice.

Java fixtures cover old preferences, migration/backups/world retention, locked
controls and launch dimensions. Actual SDL callback and display/surface fixtures
cover forced logical size,1080pselection and no1080prejection. Existing native
preview/JNI/input/cursor/startup/lifecycle/audio/options checks and full target/
package audits pass. These host checks do not establish actual083PS5clicks.

Install the **complete083folder** from `dist/client-startup/PPSA99874.zip`
(mirrored to runtime `dist/PPSA99874.zip`), including param.json. Keep the existing
`/download0/ProsperoCraft` folder; the4096MiBrequest and title identity remain.
On exact083, check that the pointer aligns with buttons, X/R2activate menu items,
the demo world opens, settings/worlds/downloads survive, sound/smoothness remain
and Quit returns to the library with relaunch. No083ALLPASS is claimed yet.

For an existing082installation, choosing1920×1080in launcher Settings before
launch is the resolution workaround. This candidate makes that selection fixed.
The published082package/tag and Client_Launcher_Lifecycle snapshot are preserved.
Root sce_sys/param.json now mirrors the published083brandedmanifest;
client/startup/param.json remains the083buildsource manifest. The user subsequently explicitly requested publication:083is now a public
GitHubrelease and its Store update is PR819. Console results are still pending;
see docs/releases/client-resolution-083.md for the current publication state.
