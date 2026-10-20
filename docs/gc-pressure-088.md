# Build088: joined GC thrashing and delayed updates

Current-run088 remains RUN at collection. It admits the player and runs beyond
121seconds after readiness; the captured client leaves at about84seconds.
There is no current native thread-creation crash or player-save warning in this
capture. This is a short observation, not persistence/stability acceptance.

Health at30seconds shows20TPS and3.727seconds of GC during the interval. At
61seconds it reports18.36TPS/21.540seconds interval GC and near-full heap. At
91seconds it reports9.97TPS/29.072seconds interval GC. The game warns that it is
13.817seconds behind. The latest100tick sample at61seconds has44.9ms mean,
299.2msP95/377.3msP99. Actual GC log contains259full pauses (258Allocation Failure,
oneCodeCache GC Threshold),72.839seconds combined, max373.038ms. Repeated full
collections reclaim only173MiB->171MiB within a174MiB effective heap. Short
post-leave tick samples can look healthy while generation/GC backlog clears.
Averaged tick samples alone did not capture this problem in earlier short tests.

This establishes severe Java heap pressure in088. It is consistent with delayed
fall damage, delayed tall-grass neighbor updates and missing/slowly arriving
chunks in the user's screenshot. It does not prove every client artifact has
that cause. These are real vanilla server behaviors delayed by execution; no
project damage/block-update hooks are present. Raw logs/identities stay local.

089 raises the heap cap from176MiB to224MiB (48MiB), keeping view4/simulation3,
normal world/Fabric isolation, spawn-protection0,20configured player slots and
online whitelist/level4ops policy. To address the earlier087pthread refusal
without shrinking Java heap again, runtime0103limits VM raw allocator ownership
of libc to2MiB including prefixes/in-flight requests, then uses existing
page/slab/direct backends. It does not reserve or guarantee SDK memory; other
native allocations and map/resource budgets can still fail. Thread stacks remain
512KiB and C1/SerialGC/NewRatio/cache/direct budget settings are unchanged.

Verbose thrown-exception logging is disabled for089: the capture shows expected
packet-thread control-flow exceptions on ordinary client traffic. Standard
os+thread=info stays in the existing bounded8MiB active/one8MiB rotated VM log.
Its legacy exceptions.log filenames/routes remain for collection. Actual future
player-save warnings may require another focused diagnostic run if they recur.
Game/probe/loader/smoke JARs stay unchanged. No game rewrites or replacement
classes, executor changes or disabled errors are added.

Host allocator/NMT/pre-init/budget/concurrency/failure ASan/UBSan and direct-ledger
regressions pass; exact0103forward patch and targetHotSpot build pass. Host
Fabric224MiB normal-world generation/save/stop evidence is recorded separately.
Host GC/SDK models cannot establish PS5 speed or thread headroom. Next: short
joined PS5 chunk exploration, damage/grass updates, native/thread/GC reports and
leave/rejoin persistence. Full two-hour run remains deferred; arbitrary mods,
Paper/plugins,20-player load and actual render-distance increases are pending.
Preserve058frozen and083vanilla fallback plus exact087/088candidates locally.
