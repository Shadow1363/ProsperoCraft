<p align="center">
  <img src="docs/readme-banner.svg" alt="Minecraft Java on PS5 — server first, client next" width="1200">
</p>

<p align="center">
  <a href="#the-goal">The goal</a> ·
  <a href="#runtime-foundation">Java runtime</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="#follow-the-project">Follow the project</a>
</p>

# Minecraft Java on PS5

A homebrew project exploring **Minecraft Java Edition on PlayStation 5** — starting with a dedicated server, then working toward the client, controller support and mod compatibility.

> **Status: first Minecraft server bootstrap milestone passes on PS5.** Build **01.000.002** verifies all 40 official JARs and invokes Minecraft **26.3 / Java 25** `--help`. A ready server, world generation and player joins remain untested.

## The goal

Bring Java Edition's worlds and ecosystem to native PS5 homebrew through small, console-tested milestones.

| Direction | What we're aiming for |
| :--- | :--- |
| **Server first** | Start a vanilla server, create and reload a world, connect over the network and verify save integrity |
| **Client next** | Bring up native dependencies, a window, rendering, audio and controller input |
| **Mods later** | Validate Fabric and Forge against specific working game versions, then test individual mods |

Graphics exploration includes OpenGL and Vulkan possibilities. Backend availability, native bindings and renderer-mod compatibility still need to be established on PS5.

## Runtime foundation

Minecraft needs a working Java runtime before the game can be brought up. That work lives in **[ps5-java25-homebrew](https://github.com/mateo-cogeanu/ps5-java25-homebrew)**.

The repositories have separate responsibilities:

- **Java port:** OpenJDK, PS5 platform adaptations, JNI and runtime acceptance probes.
- **This project:** Minecraft dependencies, launch flow, server/client integration, input, graphics and game-specific tests.

The runtime project has these **console-tested Java milestones** on PS5 firmware **13.60**:

| Runtime milestone | What passed | Source & results |
| :--- | :--- | :---: |
| **JVM startup** | Java 25 VM creation, arithmetic, Java thread start/join and shutdown | [JVM_Startup](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/JVM_Startup) |
| **File I/O** | Private-file creation, UTF-8 write/read, size and deletion | [IO_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/IO_Probe) |
| **ZIP / JAR** | Archive reads, manifest parsing, JAR class loading and UTF-8 resources | [ZIP_JAR_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/ZIP_JAR_Probe) |
| **Networking** | TCP/UDP IPv4 loopback, Java worker echo, nonblocking NIO channels and selector readiness | [Network_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/Network_Probe) |
| **LAN / DNS** | Outbound TCP/UDP echo between PS5 and Mac, forward DNS lookup and VM lifecycle | [LAN_DNS_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/LAN_DNS_Probe) |
| **Inbound LAN** | External IPv4 TCP accept and UDP receive/reply | [Inbound_LAN_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/Inbound_LAN_Probe) |
| **HTTPS / IPv6** | Verified HTTPS, IPv6 loopback and concurrent/repeated local traffic | [Advanced_Network_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/Advanced_Network_Probe) |
| **LAN endurance** | Actual IPv6 link-local LAN and 60-second external TCP/UDP workloads | [LAN_Endurance_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/LAN_Endurance_Probe) |
| **Dependencies / JNI** | Manifest-linked JARs, services/resources, system class path and real resident JNI calls | [Dependency_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/Dependency_Probe) |

The runtime now has **nine passing console milestones**, including inbound IPv4, verified HTTPS, IPv6 loopback/link-local LAN, 60-second external load, manifest-linked dependencies, actual system class-path loading and resident JNI calls. The first Minecraft-specific bootstrap probe also now passes on PS5. The current Java bootstrap uses interpreter mode, and JIT performance remains future work.

## Roadmap

### 1 · Prove the server foundation

- [x] Validate the Java runtime's TCP/UDP loopback and NIO selector probes on PS5.
- [x] Validate outbound Java LAN TCP/UDP and forward DNS on PS5.
- [x] Validate inbound LAN and multi-JAR/system class-path loading on PS5.
- [x] Pin official Minecraft 26.3 / Java 25 artifacts and inventory its 40 JARs.
- [x] Verify the inventory and official `--help` entry point on the host.
- [x] Pass the first Minecraft server bootstrap probe on PS5.
- [ ] Launch a vanilla dedicated server and reach a ready state.
- [ ] Create, save, stop and reload a test world.
- [ ] Connect from another device and verify sustained ticks and clean shutdown.

### 2 · Bring up the client

- [ ] Port the required native libraries and window/input interfaces.
- [ ] Establish a working rendering backend and audio path.
- [ ] Reach the main menu and load a vanilla test world.
- [ ] Add usable controller navigation and gameplay controls.
- [ ] Measure performance, memory use and stability on the console.

### 3 · Explore the mod ecosystem

- [ ] Validate Fabric and Forge separately for selected game versions.
- [ ] Check each mod's Java, native-library and graphics requirements.
- [ ] Test individual mods before attempting larger mod sets.
- [ ] Publish exact tested versions, results and reproducible builds.

## First server bootstrap probe

**Passing snapshot:** `PPSA99874`, version `01.000.002`. [Frozen source](Server_Bootstrap/server/native/bootstrap.cpp) · [Pinned artifacts](Server_Bootstrap/server/26.3.lock.json) · [Validation](Server_Bootstrap/validation.json)

Run all five rows in order:

1. Initialize the embedded Java runtime.
2. Create the Java 25 interpreter VM (128 MiB maximum heap).
3. Verify all 40 official JAR hashes, the server’s Java 25 bytecode and representative dependency/module classes.
4. Invoke the real, unmodified Minecraft 26.3 `net.minecraft.server.Main --help` and check its option-parser output.
5. Destroy the VM.

No Mac networking helper is needed. This build does not accept the EULA, generate a world, listen for players or establish server tick performance. Long exception messages wrap and support D-pad left/right paging.

The official server bundle is downloaded from Mojang’s metadata-pinned URL. Its SHA-1, size and SHA-256 are checked; each contained library/server JAR is checked against the bundle’s SHA-256 inventory. Game files remain in ignored caches and local packages, rather than source commits. See the [official 26.3 release](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3).

## Current development: server start probe 01.000.003

The five rows initialize the runtime, create a 256 MiB interpreter VM, check official artifacts, start/save/stop a flat test world, and destroy the VM. Human EULA acceptance for this test is [recorded](server/eula-consent.json); the wrapper writes `eula=true` only when its explicit acceptance property is enabled.

The world and configuration live under the application-visible `/download0/mc-server-start`. The test preserves that directory across launches, writes its controlled low-distance server properties, listens on available interfaces without a preset IP, waits up to ten minutes for the real `Done` message, sends `stop`, awaits server-thread exit and reads the saved `world/level.dat`. The menu waits while this row runs. The host test passes; **PS5 server startup/save/stop remains pending**. This development build includes target-built `jdk.zipfs` for Minecraft datapacks, in addition to the bootstrap module set. It does not establish player-join support or sustained performance.

### Build and verify

With the pinned Java port/toolchain available:

```sh
python3 tools/package_server_probe.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/test_server_start.py
```

The preparation script creates the class-path header and external probe specification under `build/`. The Java repository supplies the reusable runtime builder and extra target-built Java modules. No host native binaries are included. Optional module natives and server-specific native dependencies still need console validation.

Install the complete `PPSA99874` folder from the generated ZIP through ShadowLoader. Keep any existing app closed while replacing files.

## Milestones & releases

| Minecraft milestone | Console result | Snapshot | Release |
| :--- | :--- | :--- | :--- |
| **Server Bootstrap · 01.000.002** | ALL PASS on PS5 13.60: VM lifecycle, 40-JAR preflight and official server `--help` | [Frozen source & validation](Server_Bootstrap) | [Download](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Server_Bootstrap-v01.000.002) |

The public release contains the console-tested app/runtime, with official game/dependency JARs excluded. To provision those, run `tools/prepare_server.py --runtime-workspace /path/to/PS5_Homebrew`, then copy the generated `build/assets/java25/jars/` into the extracted app's `assets/java25/jars/`. The regular packaging command above produces the full local app automatically. Exact full-package and release-asset hashes are recorded separately in [validation](Server_Bootstrap/validation.json).

Earlier build failures remain recorded in [console results](server/console-results.json). This milestone establishes bootstrap/help only. World creation, a ready dedicated server, player joins and sustained ticks are next.

## Follow the project

Runtime fixes and reusable tools are published to [ps5-java25-homebrew](https://github.com/mateo-cogeanu/ps5-java25-homebrew). Minecraft harnesses, artifact pins, preparation scripts and console results are published here. The current development probe attempts real vanilla startup/save/stop; client and mod work follow their own prerequisites.
