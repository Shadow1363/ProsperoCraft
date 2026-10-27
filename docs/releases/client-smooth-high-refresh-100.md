# ProsperoCraft 01.000.100 — Smoother high-refresh gameplay

## What changed

- Reduce short gameplay hitches with smaller garbage-collection batches and less class/code cleanup during regular concurrent-GC remarks.
- Enable up to 120 Hz output on compatible displays, with automatic 60 Hz fallback. The high-refresh update reached 119 FPS in PS5 testing.
- Correct the in-app version display and reduce background diagnostic logging while retaining GC pause summaries.

This update has received positive PS5 gameplay feedback for noticeably improved smoothness. FPS still depends on the scene, settings and display; this is not a guarantee of constant 120 FPS or zero stutter.

## Playing at 120 FPS

Use a 120 Hz-capable display and enable 120 Hz output in your PS5 settings. In Minecraft, set Maximum Framerate to 120 FPS or higher and disable VSync. Presentation follows the active display refresh rate; fully uncapped presentation is not implemented.

## Install or update

Install the complete **PPSA99874.zip** folder through your normal PS5 homebrew workflow, or update through ProsperoStore once its catalog update is approved and deployed. The installed app version is **01.000.100**.

Back up your worlds and preserve `/download0/ProsperoCraft` when updating. Client and server apps share PPSA99874, so installing one replaces the other. New installations start with an empty library. Download Minecraft through the launcher; an account with Java Edition ownership and a valid Minecraft profile is required for full-game play. Official game JARs and assets are downloaded from the publisher, verified on the console and remain unmodified.

## Compatibility and testing

Minecraft **26.3** is the playable native baseline. Other 26.x releases and snapshots can be downloaded, but launch support is still in development. Client mod loaders and full Controlify integration remain planned. LAN hosting is deferred.

The release preserves the exact tested build100 package. Gameplay smoothness has been accepted in PS5 testing; broader save/reload, account recovery, reconnect, repeated world/server changes and extended endurance still need testing. The 119 FPS result was reported on the earlier high-refresh build097, not as a new measurement of100.

The GC policy keeps full-GC class unloading enabled but defers cleanup from concurrent remarks. Unused classes and compiled code can remain in memory longer, so long-session memory and code-cache pressure remain under review. Authentication retains the existing experimental account flow.

## Credits and source

GUI: **mihawk-99/PS5_VKHomebrewUI**, based on BlackBearReloaded's ps5-homebrew-ui. Instance icons: **MultiMC and Prism Launcher contributors**, with original licenses and attribution retained. Runtime: **PS5 Java 25**, with OpenJDK, Mesa/RADV, SDL, LWJGL and OpenAL Soft.

Matching OpenAL corresponding source, relink materials, validation records and SHA-256 checksums accompany this release. ProsperoCraft is unofficial and is not affiliated with Mojang, Microsoft or Sony.
