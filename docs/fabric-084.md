# Fabric server candidate 01.000.084

Update:084 PS5 loader/mod/readiness/join are confirmed, followed by a native C1
allocation abort. See [085 follow-up](native-memory-084.md); pending sections below
record the original084plan and are superseded by that measured result.

The user reports absolutely no lag during083joined gameplay and defers the full
two-hour run until later. Preserve the local083vanilla package and its source
commit35f45706c00e4e562531f70f43cc29b301f73264. This is a human gameplay report,
not ALL PASS, a validated capacity limit or a completed endurance milestone.
The user now requests Fabric, then Paper, before the client.

## Scope

Use Minecraft26.3 with Fabric Loader0.19.5 from the official
[Fabric metadata](https://meta.fabricmc.net/v2/versions/loader/26.3/0.19.5/server/json).
The [26.3 announcement](https://fabricmc.net/2026/09/15/263.html) documents this
loader line. server/fabric-26.3.lock.json pins seven upstream loader/ASM/Mixin
artifacts by URL, size and SHA-256. Loader's nested JARs are covered transitively
by its exact artifact hash. All40Mojang game/library pins remain unchanged.
Downloaded game/loader artifacts stay in ignored caches and local packages.

A small separate server-only mod, ps5-fabric-smoke1.0.0, implements the actual
Fabric ModInitializer entrypoint. It needs no Fabric API and has no game hooks,
mixins or replacement game classes. Its marker is required before probe success.
This proves loader/mod entrypoint execution, not compatibility with arbitrary
third-party mods, Fabric API, networking mods or native libraries.

The downloaded Minecraft server JAR remains byte-for-byte original. Fabric
Knot/Mixin can transform classes in memory as part of standard upstream mod
loading; do not describe that process as wholly unmodified runtime game code.
No project-specific game-JAR rewrite, signature stripping or replacement game
class is introduced. Monitoring stays outside game classes.

## Launch and worlds

Prepare or package with --flavor fabric. Vanilla remains an explicit supported
--flavor vanilla path. The generated launcher header carries the matching
flavor property, label and classpath. Fabric uses world-fabric-v1; vanilla keeps
world-normal-v1 and the historical flat world directory. Fabric config/mod/cache
files share the existing server working directory, but no vanilla world is
converted or opened by the Fabric test. Keep backups before later content mods.

Before Knot launches, copy the hash-verified, probe-owned smoke mod into mods/.
Other mods are not deleted. After launch, require a non-system target classloader
and require MinecraftServer to load through that loader. NBT save/protocol checks
explicitly use the same target loader, avoiding a parallel vanilla game copy in
the system loader. Preflight verifies47pinned JARs and the original server bytecode.

Keep083memory settings:192MiB maximum heap, SerialGC/NewRatio15, C1level1/one
compiler/2MiB arena limit,16MiB code cache, SweeperThreshold50 and MetaspaceSize128m.
Keep authenticated admission/TLS/whitelist, OPlevel4 without player-limit bypass,
normal terrain/view4/simulation3 and configured20-player limit. Mod-loader memory
overhead and actual20-player capacity remain unvalidated on PS5.

## Validation

Host checks exercise the exact preflight-then-start sequence, loading all47pins,
real Fabric/Knot initialization, smoke-mod entrypoint, readiness, NBT file probe,
protocol templates, tick queries, saves and clean stop. Exact measurements and
package checks are recorded in server/build-status.json. Original40JAR signatures,
vanilla OSHI error handling and vanilla ops.json controls remain checked.

Pending on PS5: initialization, Verify JARs, loader/mod marker, joined vanilla
26.3client play, mob/damage latency, food/respawn, player save/rejoin and native
memory/GC observations. The first test is a short compatibility/play session.
The monitor can remain open up to7200seconds and saves every300seconds, but no
full two-hour run is requested now or inferred from a shorter session. Relaunch
the probe to make reports available after a crash as before. No milestone freezes.

## Next: Paper

[Paper26.3](https://papermc.io/news/26-3/) is the next separate server flavor for
plugin compatibility. The official download API observed stable build207 on
2026-10-20; server/paper-26.3.candidate.json records its URL/size/checksum for the
next stage. It is researched, not downloaded, built or PS5 validated here.
Paper plugins and Fabric mods use separate server ecosystems; Paper will execute
its upstream server distribution in a separate world, not claim unmodified Mojang
execution. Establish Fabric console startup/mod execution before that integration.
Client work follows the requested server-loader/mod/plugin experiments.
