# ProsperoCraft 0.98 — Play at up to 120 FPS

## New in 0.98

- Enable 120 Hz output on compatible displays, lifting the previous 60 FPS presentation ceiling. Minecraft reached **119 FPS** in PS5 testing of the high-refresh update.
- Prefer supported refresh rates up to 120 Hz, with automatic 60 Hz fallback when high-refresh output is unavailable.
- Fix the launcher footer so it displays the installed build version correctly.
- Reduce background diagnostic logging while retaining GC and safepoint pause summaries.

## Playing at 120 FPS

Use a 120 Hz-capable display and enable 120 Hz output in your PS5 settings. In Minecraft, set Maximum Framerate to 120 FPS or higher and disable VSync. Actual FPS depends on the scene, settings and display configuration. Presentation remains synchronized to the active display refresh rate; fully uncapped presentation is not implemented.

## Install or update

Install the complete **PPSA99874.zip** folder through your normal PS5 homebrew workflow, or update through ProsperoStore once its catalog update is deployed. The app and console version is **01.000.098**.

Back up your worlds and preserve `/download0/ProsperoCraft` when updating. Installing the client replaces the server app because both use PPSA99874. New installations start with an empty instance library; download Minecraft through the launcher. An account with Java Edition ownership and a valid Minecraft profile is required for full-game play. Official game JARs and assets are downloaded from the publisher, verified on the console and remain unmodified.

## Compatibility and testing

Minecraft **26.3** is the playable native baseline. Other 26.x releases and snapshots can be downloaded, but launch support is still in development. Client mod loaders and full Controlify integration remain planned; LAN hosting is deferred.

The 119 FPS result was reported on build 01.000.097. Version 01.000.098 includes the same high-refresh changes plus the visible-version correction and quieter diagnostic logging. Its target build, package checks and source/relink verification pass; a separate console regression test of the exact 098 package is still pending. Brief GC-related hitches remain under investigation: captured build097 pauses commonly exceed the 8.3 ms budget for 120 FPS. Reduced logging is not a confirmed stutter fix. Frame-time consistency, long-session endurance and broader save/reload and lifecycle coverage remain under testing. Authentication retains the existing experimental account flow.

## Credits and source

GUI: **mihawk-99/PS5_VKHomebrewUI**, based on BlackBearReloaded's ps5-homebrew-ui. Instance icons: **MultiMC and Prism Launcher contributors**, with original licenses and attribution retained. Runtime: **PS5 Java 25**, with OpenJDK, Mesa/RADV, SDL, LWJGL and OpenAL Soft.

Matching OpenAL corresponding source, relink materials, validation records and SHA-256 checksums accompany this release. ProsperoCraft is unofficial and is not affiliated with Mojang, Microsoft or Sony.
