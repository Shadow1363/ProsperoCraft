# ProsperoCraft 01.000.108

Minecraft Java Edition running natively on PlayStation 5, powered by a Native Java 25 Runtime. Sign in, create separate instances, and play Minecraft Java 26.3 with native graphics, audio, DualSense controls and keyboard/mouse support. Java Edition ownership is required.

## Changelog

- Add Fabric instance support and a Modrinth browser for mods, shaders and resource packs, with search, download queues and verified downloads.
- Download required mod dependencies automatically, including Fabric API modules declared by mods. Repair missing dependencies before launch and report incompatible requirements in the launcher.
- Add Installed lists and per-file Uninstall buttons with confirmation. Worlds, settings and unrelated files are preserved.
- Show larger project icons, including WebP and indexed PNG artwork, with clearer selection checkboxes and roomier lists.
- Add saved controller remapping and physical keyboard/mouse input. Correct launcher navigation and use a QWERTY launcher keyboard.
- Improve audio startup by reserving the output port before JVM/GPU allocation. Share the resident SDL library under SDL3 for Controlify integration; full Controlify compatibility remains experimental.
- Add native image support used by shader packs, reduce metadata/code-cache pause pressure, and offer an optional Vitrail shadow-map scale setting. Shader FPS depends on the pack and settings.

## Install and compatibility

Install PPSA99874.zip through your usual homebrew workflow or update through ProsperoStore once its catalog deployment completes. Preserve /download0/ProsperoCraft and back up worlds. Client and server use the same title ID, so installing one replaces the other.

The launcher downloads and verifies original Minecraft files on the console; official game JARs and assets are not bundled. Minecraft 26.3 is the playable baseline. Other downloadable versions are not yet claimed launchable. NeoForge and LAN hosting remain planned.

This release preserves the exact build108 package. Host/package and live dependency-download tests pass; keyboard operation is confirmed on PS5. Broader dependency repair, mouse, Controlify, audio/lifecycle, save/reload and extended endurance testing remain incomplete. Earlier high-refresh testing reached119FPS on compatible120Hz output; no constant-FPS or shader-performance guarantee is made.

## Credits and source

GUI: **mihawk-99/PS5_VKHomebrewUI**, based on BlackBearReloaded's ps5-homebrew-ui. Instance icons: **MultiMC and Prism Launcher contributors**, with original licenses and attribution retained. Runtime: **PS5 Java 25**, with OpenJDK, Mesa/RADV, SDL, LWJGL and OpenAL Soft. Project thumbnails belong to their respective mod and pack authors; image decoding uses libwebp and STB.

Matching OpenAL corresponding source, relink materials, validation and SHA-256 checksums accompany this release. ProsperoCraft is unofficial and is not affiliated with Mojang, Microsoft or Sony.
