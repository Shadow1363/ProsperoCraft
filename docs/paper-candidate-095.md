# Paper 26.3 build 207 — first PS5 candidate (095)

The user reports satisfaction with Fabric and requests Paper next, then a
proper release before client work. Fabric094's full package and source commit
are retained as a development fallback; this report does not establish an exact
ALL PASS, completed endurance run or a newly frozen milestone. Vanilla083 and
frozen Server_Start058 remain intact.

## Distribution and isolation

The [Paper publisher metadata](https://fill.papermc.io/v3/projects/paper/versions/26.3/builds/207)
pins stable build207 and its 55,244,868-byte Paperclip artifact, SHA-256
`2df3b846f70716907d380915cc026667a9cadedf99b1ec680b0c5ff0e6132526`.
The original Paperclip runs in patch-only mode on the host against the existing
hash-verified Mojang bundle. All 105 resulting upstream runtime JARs must match
Paper's embedded inventories and source-controlled pins. No project game-JAR
rewrites, signature stripping, bytecode hooks or replacement game classes are
added. Paper is its own upstream distribution; it is not described as the
unmodified Mojang server. Game files/caches remain local, outside source Git.

The console launches upstream `org.bukkit.craftbukkit.Main` with this prepared
classpath, without running Paperclip/downloads/patching on PS5. It uses the
separate normal world `world-paper-v1`; existing Fabric/vanilla worlds remain.
View4/simulation3, structures, online authentication, whitelist, level4ops and
20 configured slots remain. No 20-player capacity claim. Music remains off.
`--nojline` and a Paper-only non-following console appender avoid redirect loops.
The initial Paper global config disables bundled spark through its supported
configuration; profiling and arbitrary native/plugin services are unvalidated.

Paper adds target-built java.net.http and jdk.security.auth classes (and module
closure dependencies). Native JAAS/GSS services are not embedded or ported.
Upstream Paper catches an unavailable native UnixSystem in its optional root/
admin check; there is no fabricated identity. Plugin-specific JNI/native services
and other native libraries remain subject to later compatibility work.

## Plugin and memory

PS5PaperSmoke1.0.0 compiles against the pinned upstream Paper API. It exercises
plugin enable, a scheduled main-thread task, `/ps5probe` and plugin disable.
The command is OP-only; console invocation verifies it before live monitoring.
It changes no gameplay. Source and plugin.yml are separate from the game JAR;
the generated plugin is SHA-256 checked before copying to the plugins directory.
Paper ERROR messages, including worker errors, fail the monitor.

The 224MiB Fabric heap runs out during normal Paper world generation on the
host. Paper therefore uses384MiB, with the existing C1/SerialGC/cache settings.
Fabric retains224MiB. Actual PS5 heap reservation, native headroom, latency and
long-run stability at384MiB remain unknown. Host success cannot establish them.

## Stop behavior

Paper calls System.exit when it stops. This is upstream behavior, so a successful
stop normally closes the app. The JNI exit callback reads only native files:
its fresh run-id marker, nonempty Paper level.dat, plugin-disable record, all
three dimension I/O scheduler completions, final RegionFile I/O completion and
exit code0. Missing/stale evidence, stop errors or nonzero exit reject success.
The callback does not call back into an exited VM. DestroyJavaVM is not a separate
completed row on this Paper path; no VM resurrection is attempted.

After joining and playing, press Circle in the PS5 probe to request save/stop.
The monitor first requires two tick-progress samples, then performs its final
flushed save and sends stop. Requests are checked at monitor intervals, so this
can take roughly a minute when requested very early. Reopen the probe afterwards
and leave it on the menu to retrieve the exit/session reports. A shortened play
check prints MC_PLAY_CHECK_COMPLETE, not MC_ENDURANCE_COMPLETE. It does not
claim the full7200-second target. Do not confuse the deliberate final app exit
with a crash while joining or playing; those are still failures.

## Validation and release gate

Host384MiB/C1/normal-world/25-forced-chunk run passes startup, 105-JAR preflight,
plugin enable/scheduler/command, actual NBT save operations/protocol templates,
60seconds of monitored ticks,28health checks,14flushed saves, saved regions and
normal upstream exit0. No player joined the host test. A second run passes the
controller-style shortened path (12seconds after readiness,4checks,3saves in
this sample), plugin disable, final saves and exit0. These are different random
worlds and not a performance benchmark. Native exit-classifier ASan/UBSan tests
reject missing/stale/partial/error/nonzero evidence, and replay actual Paper
shutdown output. Observer tests cover plugin markers and Paper-worker ERRORs.

Next actual PS5: initialize/create, verify, start, join; try `/ps5probe`, movement,
food/damage/grass/new chunks, death/respawn, saving and rejoining, then Circle
for a normal shutdown. Retrieve reports after reopening. Native pressure/new
module paths and Paper plugin lifecycle remain pending. Arbitrary plugins and
20-player load are not validated. Full two-hour run remains deferred.

Once the user confirms the exact Paper candidate passes those console checks,
freeze its matching source/checksum/validation and publish a proper release
before client work. Public compiled releases omit upstream game JARs and use
local provisioning as required by this repository's publication rules. No
passing Paper release or client milestone is claimed by this development build.

Final package checks pass: 105 publisher-pinned runtime artifacts, separate
plugin/hash, probe gates, target module classes, eight matching target native
libraries, linked JNI/allocator symbols and single ownership tables, signatures,
ZIP integrity, matching symbol/package copies, no Fabric artifacts or music, and
exact retained094/093/083/058 packages. Runtime native code matches094 apart from
build identification notes. Generated host test classes are excluded.

Local full development package SHA-256:
`858d488c8883273491bdd2efb2f9e8062c44331318f29bbcc9b59b56bcc97390`.
This is not a published passing release asset.
