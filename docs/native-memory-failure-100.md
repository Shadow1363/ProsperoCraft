# Paper startup native-memory failure in100

Current-run session, console, startup, native trace, abort and HotSpot fatal reports identify build 01.000.100. DNS/TLS online preflight and Paper's explicit experimental-Java opt-in complete. Paper initializes the plugin inventory, then HotSpot aborts while loading Bukkit EntityType classes: a 4 MiB non-class metadata reservation fails.

Immediately before failure the shared direct ledger holds0x7dd8000 bytes (125.84MiB) against 128 MiB; adding 4 MiB exceeds its policy cap. The reported kernel-failure counter is zero: policy refusals were not counted there. This establishes an exhausted software allowance, not exhausted PS5 physical memory. The2048-slot ledger is not full (0x119a mappings minus 0xfb0 releases).

Build 101 uses reusable runtime patch 0111: shared held-byte ceiling 256 MiB, same 2048 slots and exact ownership/cleanup, new separate policy-rejection counter. No preallocation, Java heap expansion or increased stack-owner limit. Paper/game/probe/plugin JARs and module image are unchanged. No project game-JAR transformation is added.

Host tests exercise mixed data/metadata allocations beyond 128 MiB, exact 256 MiB limit/refusal without kernel calls, release/reuse, concurrent owners, rollback and retained cleanup ownership under ASan/UBSan. Metadata, compact class-space and attached-worker stack ABI regressions and target HotSpot rebuild pass. These do not establish console backing availability or Paper readiness.

PS5 validation pending: CreateVM, VerifyJARs and Play; real readiness, plugin enable/scheduler/command, joined gameplay, save/stop and reload. Other native resource limits may still fail. Full 2h remains deferred. Preserve failed 100 and Fabric 094 fallback. No release/ALLPASS claim.
