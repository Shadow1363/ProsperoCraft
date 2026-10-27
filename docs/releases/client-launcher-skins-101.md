# ProsperoCraft 01.000.101 — Clearer launcher, correct account actions and player skins

## What changed

- Sign-in and saved-account restoration take you straight to Instances.
- The account screen shows **Sign in** when signed out and **Sign out** when signed in.
- Brighter active tabs and a persistent underline make the current page easier to see.
- Resolution changes use the Settings dropdown; left/right no longer cycles the value.
- Snapshots start **off** for new libraries. Existing saved preferences are retained.
- In-game menus use cursor selection without D-pad or left-stick arrow-key navigation. The text keyboard and gameplay bindings retain their own controls.
- Fix a Java socket-availability error that prevented custom player skins from downloading on PS5. Original Minecraft files remain unmodified.

These changes passed functional PS5 testing. This release preserves the exact tested build101 package and retains the smoother gameplay and up-to-120 Hz output introduced in100.

## Install or update

Install the complete **PPSA99874.zip** folder through your usual PS5 homebrew workflow, or update through ProsperoStore after the catalog deployment completes. The installed version is **01.000.101**.

Back up worlds and preserve `/download0/ProsperoCraft` when updating. Client and server share PPSA99874, so installing one replaces the other. New installations start with an empty library; the launcher downloads verified original publisher files on the console. Java Edition ownership and a valid Minecraft profile are required for full-game play. No official game JARs or asset objects are bundled.

## Compatibility and testing

Minecraft **26.3** is the playable native baseline. Other 26.x releases and snapshots can be downloaded, but launch support is still in development. Client mod loaders and full Controlify integration remain planned; LAN hosting is deferred.

Use a compatible 120 Hz display and PS5 output configuration for high-refresh play. Set Minecraft's Maximum Framerate to 120 or higher and disable VSync. FPS depends on the scene and settings; presentation follows the active display refresh rather than being fully uncapped. The earlier high-refresh test reached 119 FPS; no new frame-time or FPS measurement is claimed for 101.

Broader account recovery, save/reload, repeated world/server changes, reconnect and extended endurance remain under testing. The existing GC policy defers class/code cleanup from concurrent remarks while retaining full-GC unloading; longer-session memory and code-cache pressure still need testing. Authentication retains the existing experimental account flow.

## Credits and source

GUI: **mihawk-99/PS5_VKHomebrewUI**, based on BlackBearReloaded's ps5-homebrew-ui. Instance icons: **MultiMC and Prism Launcher contributors**, with original licenses and attribution retained. Runtime: **PS5 Java 25**, with OpenJDK, Mesa/RADV, SDL, LWJGL and OpenAL Soft.

Matching OpenAL corresponding source, relink materials, validation and SHA-256 checksums accompany this release. ProsperoCraft is unofficial and is not affiliated with Mojang, Microsoft or Sony.
