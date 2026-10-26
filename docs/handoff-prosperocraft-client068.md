# ProsperoCraft068 continuation

The human confirms067sound works beautifully and now requests fixing intermittent
freezes, suspected GC. The current partial067logs confirm15fullGCpauses, maximum
647.647ms:7allocation,7codecachethreshold,1aggressivecodecache. Old space is almost
full even after collection. Sound continuity during a freeze is unknown.
See [evidence](validation/client067-audio-freezes-2026-10-26.json) and the
[068 investigation/test guide](client-gc-068.md).

068 uses NewRatio7 inside the unchanged512MiB SerialGC heap and32MiB codecache
instead of16MiB. It retains C1 level1 and its correctness gate, cleanup safety,
working audio/input/graphics and all original game bytes. No runtime implementation
change. More old space and a larger code cache target observed pressure, but the
host occupancy fixture shows only modest improvement and more young collections;
actual PS5 latency and native headroom remain unvalidated.

Local install: `dist/client-startup/PPSA99874.zip`, titlePPSA99874/version01.000.068,
SHA256`24e65f1020e97437b4ce0316e53f41aa1c56b8732bd9768663f2208ac7531efb`.
The exact067package/symbols are preserved in `dist/accepted/Client_Audio-01.000.067/`.
Its SHA256is`95f0af47359b48493afab6e9af23e81de1097796332c4b32e64d03123030397f`.
The public full release remains066; do not rebuild or relabel accepted binaries.
No new release requested. Server fallback packages and frozen milestones remain.

Next: obtain actual068same-world pause/performance/audio feedback and current-run
GC/JIT reports. Do not assume all freezes are GC, claim ALL PASS or save/endurance
acceptance, or expand into loader/shader/performance changes without evidence.
If crashed, ask to reopen without X before report retrieval. Safari read-only
log-share download links work when shell network access fails; derive current
UI labels/indices, collect a fresh timestamped set, and keep raw logs local.

Keep the README concise; build history belongs in CHANGELOG.md. Minecraft source
belongs in this repo and must be checked/committed/pushed; reusable runtime fixes
belong in ps5-java25-homebrew via its sync script. Official JARs/assets stay intact.
Runtime pin44fdf26ccb74cf8dd9127f1256b85416856981de. No Store work. Roadmap remains
in README; this step addresses pauses while preserving the playable client.
