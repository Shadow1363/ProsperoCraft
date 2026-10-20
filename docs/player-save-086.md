# Build086: disconnect save failure and block corrections

The retrieved current-run086 reports show Fabric, the smoke mod, readiness and
an authenticated join. At120seconds after readiness the monitor reports20TPS,
five checks and zero scheduled saves. The latest100-tick sample reports4.9ms
mean/26.2ms P99; that window does not exclude earlier spikes. After the player
leaves, vanilla prints `Failed to save player data for ...`. The harness stops
on that warning and fails the run. No current native VM abort is established.
The earlier085Deflater allocation/image decode exceptions are absent from this
capture; that is not proof they can never recur. Raw logs remain local.

Repeated block-position mismatches and force-sent blocks occur around spawn.
Default spawn protection is a possible explanation for rejected breaks, but the
warnings alone do not establish the cause.087 explicitly sets vanilla
`spawn-protection=0`, consistent with unrestricted building in this test world.
Existing online authentication, whitelist and level4 ops.json remain enabled.
Actual in-game OP permissions still need PS5 confirmation.

Inspection of the original26.3 PlayerDataStorage shows that its save method
catches Exception and logs only the player name. It does not print the caught
exception. Its data directory is `players/data`. The previous synthetic NBT
check created its files directly beneath the world, so it did not check that
exact directory.087 uses java.io mkdirs/isDirectory for the real directory,
then runs its existing compressed NBT temp/write/replace/backup/read test in a
probe-owned temporary child. It never edits player files, and cleans its child.
This also ensures the directory exists; whether that fixes the observed warning
is unresolved. The Java port already anchors relative java.io File operations
against user.dir; no duplicate runtime path patch was added.

087 additionally enables standard HotSpot thrown-exception logging to a separate
8MiB active file and one8MiB rotated file. The read-only log server/collector
expose both, preserving them across reopen and archiving them on a new run.
Expected caught exceptions will appear too. Diagnostic logging may add I/O;
087 is not a benchmark or a completed save fix. All original game/loader/smoke
JARs are unchanged. Standard Fabric runtime loading remains disclosed; no
project game rewrites/replacement classes are introduced.

Next PS5 checks: break grass/dirt near spawn; check a vanilla OP command; leave
and reconnect to verify inventory/location persistence. If player save still
fails, keep the failed result or reopen at the menu so both exception logs can
be collected. Confirm the directory check and exact thrown cause before another
runtime repair. Full two-hour run, arbitrary mods, Paper/plugins and20-player
load remain deferred/unvalidated. Preserve058frozen and083vanilla fallback.
