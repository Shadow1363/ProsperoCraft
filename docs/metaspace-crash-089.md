# Build089: startup metadata reservation abort;090audio removal

The retrieved session identifies089and a VM ABORT. Its current fatal report
records a4MiB ordinary native mapping refusal (ENOMEM) while reserving more
non-class metaspace, at17.511seconds elapsed on Worker-Main-1. Metaspace is about
94MiB used/95MiB committed, including about17MiB class metadata within the32MiB
compressed class-space reservation. Java heap is not full; reducing it to176MiB
already caused severe GC thrashing in088. Readiness/player join are not reached
in this089capture. The smoke-mod entrypoint did execute. Raw logs stay local.

0103's VM-owned libc cap is observed just below2MiB; it does not fix this distinct
ordinary virtual-memory reservation failure.090retains224MiB heap and0103while
adopting runtime0104for ordinary non-fixed/non-executable mtMetaspace ENOMEM.
It can reserve through the existing shared128MiB/2048slot direct ledger with
requested alignment. New backing is zeroed and PROT_NONE, NMT reserve is recorded,
existing RWcommit remains, and metadata uncommit zeroes unused subranges then
protects NONE. Physical backing stays owned/budgeted until exact whole release.
Heap/compressed class-space/executable/fixed/other-tag requests stay excluded.
This is not unlimited memory, a guaranteed native reserve or a completed PS5 fix.

At the user's request090also removes this app's menu_audio include, startup/stop,
selection calls and audio status UI. The consumer sets menu_audio=false in the
external probe spec, so the runtime packager omits menu music/selection PCM.
No app music playback thread or AudioOut call remains. Shared audio sources and
frozen passing apps are preserved; this is not an audio rewrite or a claim that
music caused the metadata abort.

Host validation uses actual reservation/ledger/helpers/release code over real
aligned storage and controlled kernel calls under ASan/UBSan:4MiB alignment,
nonzero backing zeroed before first commit, PROT_NONE faults, subrange zeroed
recommit/adjacent data, purpose/error/fixed/executable gates, NMT reserve event,
rollback and exact release/cleanup retention. Existing allocator/NMT/direct
fault/concurrency, metadata-hint and historical-prefix controls pass. Exact0104
patch and targetHotSpot build pass. Full target VM lifecycle is not tested on host.
No new host game run: all game/probe/loader/smoke JAR bytes stay unchanged, retaining
089's224MiB host Fabric60second/27check/14save/25forced-chunk/save-stop evidence.
That evidence cannot validate the target memory mapping repair.

Next console checks: silent app/menu, startup metadata reservation/commit,
short joined exploration with damage and tall-grass updates, player save/rejoin,
GC/direct-held/native-thread reports and stability. Full two-hour run is deferred;
Paper/plugins/arbitrarymods/20-player load pending. Preserve058frozen and083
vanilla fallback, and retain exact089failed package locally. No ALL PASS claim.
