<p align="center">
  <img src="docs/readme-banner.svg" alt="ProsperoCraft — Minecraft Java client and server development on PS5" width="1200">
</p>

<p align="center">
  <a href="#downloads">Downloads</a> ·
  <a href="#current-status">Current status</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="CHANGELOG.md">Changelog</a>
</p>

# ProsperoCraft

<img src="assets/branding/icon0.png" alt="ProsperoCraft crafting-table PC icon" width="160">

**A native PlayStation 5 port of Minecraft Java Edition — no Wine.**

The original Minecraft Java code runs on our PS5-native OpenJDK 25 port, with
native PS5 graphics, audio and input integration. There is no Windows build or
Wine compatibility layer involved.

ProsperoCraft brings Java Edition worlds, servers and the modding ecosystem to
PS5 homebrew. The goal is a polished client with responsive controls, smooth
rendering, working sound, reliable saves and an easy-to-use launcher.

> **Sound works and gameplay feels buttery smooth on PS5.** The latest
> **01.000.074** playtest confirms both, with native Java 25 and G1 GC.
> [Playtest evidence](docs/validation/client074-smooth-audio-confirmation-2026-10-26.json) ·
> [Published playable release066 →](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Playable-v01.000.066)

## Downloads

| Release | What to expect | Get started |
| :--- | :--- | :--- |
| **Playable client · 01.000.066** | Minecraft Java 26.3, playable worlds and temporary DualSense controls. Sound and smoother gameplay are confirmed in development074; this release remains066. | [Download](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Playable-v01.000.066) · [Setup](docs/releases/client-playable-066.md) |
| **Fabric / Paper servers · 01.000.108** | Separate server builds with positive console playtests. Full lifecycle and endurance checks remain pending. | [Download](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Fabric-Paper-v01.000.108) · [Setup](docs/releases/fabric-paper-108.md) |

Follow the matching release's provisioning instructions to obtain and verify the
official game files. Public app-only downloads exclude Minecraft JARs and game
asset objects; matching source, checksums and licensing details accompany each
release.

The client and server share title ID **PPSA99874**: installing one replaces the
other. Keep your world backups and the matching server package for reinstalling.

## Current status

| Area | Status |
| :--- | :--- |
| **Native Java 25** | Runs on PS5, with guarded C1 compilation used by the playable client. |
| **Client gameplay** | The user reports buttery-smooth gameplay on exact build074. FPS has not been benchmarked. |
| **Controls** | Temporary DualSense keyboard/mouse mapping works. Full Controlify integration is planned. |
| **Sound** | The user confirms very good game sound on exact build074. |
| **Validation ahead** | Save/reload, controller polish, measured frame pacing and extended play remain to be checked. |

Development078 keeps the native launcher separate from Minecraft startup and adds
clearer sign-in errors. Full PS5 authentication is still being validated.
[Launcher guide](docs/client-launcher-077.md) · [Sign-in diagnostics](docs/client-auth-078.md).

Development074 now has positive PS5 sound and smoothness feedback, with no active quality caps.
See the [freeze investigation and candidate guide](docs/client-audio-pacing-074.md).
The published release remains066; this074playtest does not create a new public release.
For individual fixes, console evidence and earlier milestones, read the detailed
**[CHANGELOG.md](CHANGELOG.md)**.

## Roadmap

### Required for store release

- [ ] **Microsoft login** for official downloads.
- [ ] **Launcher menu with instances**, full settings and instance management.
- [ ] **All Minecraft 26.x releases**, including snapshots.
- [ ] **Fabric, Forge and NeoForge instances** within the current 26.x releases.
- [ ] **SDL3 support for Controlify** integration.
- [ ] **Performance good enough for shaders.**

These are planned release requirements. Loader, mod and shader compatibility
will need validation for each supported game version.

### Later

- [ ] **Custom menu music by CogiArt.**
- [ ] **`.mrpack` imports.**
- [ ] **USB keyboard and mouse controls.**
- [ ] **Themes.**
- [ ] **JVM 21** for broader Minecraft support.
- [ ] **JVM 17** for even broader Minecraft support.

## Runtime foundation

ProsperoCraft is powered by the separate
**[PS5 Java 25 runtime project](https://github.com/mateo-cogeanu/ps5-java25-homebrew)**.
That repository maintains OpenJDK, PS5 platform adaptations and reusable runtime
tools. This repository maintains Minecraft integration, artifact pins, native
dependencies, launch configuration, controls and game-specific validation.

Official game JARs and assets stay intact in current development. Frozen historical
workarounds and their migration history are documented in the changelog.

## Follow the project

- **[Releases](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases)** — downloads, setup and checksums.
- **[Detailed changelog](CHANGELOG.md)** — build-by-build changes, results and known issues.
- **[Milestone archive](CHANGELOG.md#milestones--releases)** — frozen source snapshots and console validation.
- **[Java runtime](https://github.com/mateo-cogeanu/ps5-java25-homebrew)** — the native Java foundation.
- **[Project artwork](assets/branding/README.md)** — branding and graphics.

ProsperoCraft is an independent homebrew project, unaffiliated with Mojang,
Microsoft or Sony.
