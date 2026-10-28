# ProsperoCraft 01.000.117

Minecraft Java Edition running natively on PlayStation 5, powered by a Native Java 25 Runtime. Sign in, create separate instances, and play Minecraft Java 26.3 with native graphics, audio, DualSense controls and keyboard/mouse support. Java Edition ownership is required.

## Changelog

- Add Duplicate Instance with separate worlds, mods, packs and settings, unique names and IDs, progress and cancellation.
- Refresh instance and content buttons with the Settings-style appearance, animated focus and press feedback. Arrange Mods, Shaders, Resource Packs and Duplicate in a 2×2 grid, with a green Done button and matching navigation.
- Preinstall Controlify and its required dependencies when setting up new Fabric instances. Existing instances and later uninstalls are preserved.
- Add native DualSense gyro, compatible vibration and HD haptic audio integration. Translate Controlify adaptive-trigger effects, with a trigger-travel fallback for rejected per-zone commands. Physical adaptive-trigger behavior still needs console verification.
- Fix world access, chunk saving/loading and world deletion failures caused by open-file pressure. Preserve audio output across resource reloads.
- Resolve exact dependency pins consistently, upgrade outdated managed dependencies when required and continue unrelated queued downloads when a mod fails. Failed mods and their dependents report errors.
- Accept safe Unicode resource-pack filenames, including formatted C418 music-pack names.
- Explain Iris incompatibility before launch: OpenGL is not available in the current Vulkan renderer. Use Vitrail for shaders. Distant Horizons compatibility remains work in progress; NeoForge is not enabled.

## Install and compatibility

Install PPSA99874.zip through your usual homebrew workflow or update through ProsperoStore once its catalog deployment completes. Preserve /download0/ProsperoCraft and back up worlds. Client and server use the same title ID, so installing one replaces the other.

The launcher downloads and verifies original Minecraft files on the console; official game JARs and assets are not bundled. Minecraft 26.3 is the playable baseline. Other downloadable versions are not yet claimed launchable. NeoForge and LAN hosting remain planned.

This release preserves the exact build117 package. Host, native input/UI and package checks pass. Earlier console feedback confirms keyboard input, haptics and world play/reload after the file-handle repair. Adaptive-trigger feel, the latest launcher changes and extended endurance still require console testing. Microphone capture is not included. Earlier high-refresh testing reached119FPS on compatible120Hz output; no constant-FPS or shader-performance guarantee is made.

## Credits and source

GUI: **mihawk-99/PS5_VKHomebrewUI**, based on BlackBearReloaded's ps5-homebrew-ui. Instance icons: **MultiMC and Prism Launcher contributors**, with original licenses and attribution retained. Runtime: **PS5 Java 25**, with OpenJDK, Mesa/RADV, SDL, LWJGL and OpenAL Soft. Project thumbnails belong to their respective mod and pack authors; image decoding uses libwebp and STB.

Matching OpenAL corresponding source, relink materials, validation and SHA-256 checksums accompany this release. ProsperoCraft is unofficial and is not affiliated with Mojang, Microsoft or Sony.
