# Build091: threads start, player-directory listing fails

The current091session is FAIL before readiness. It records a successful4MiB
metadata reservation,3successful512KiB direct-backed thread creations and2join/
release pairs with result0. Server initialization reaches key generation and
binding port25565. It then throws NullPointerException in vanilla
OldUsersConverter.convertPlayers because java.io.File.list returned null.
Current-run native startup output reports `PS5 java.io list open failed errno=12`.
That old message does not identify whether fd open, context mapping or64KiB
record-buffer mapping failed. No JVM-abort claim is made. Raw logs remain local.

092adopts runtime0106for the remaining directory-buffer allocation route. The
shared java.io/NIO helper retries ordinary context/data mapping ENOMEM through
the existing bounded VM direct-memory C ABI/ledger. Each allocation records its
backend; context length is rounded to16KiB and the record buffer remains64KiB.
Partial initialization and close release matched backends, preserving genuine
errors rather than fabricating empty or incomplete results. PS5libnio declares
its direct VM dependency. Diagnostics now distinguish1=fd,2=context,3=buffer;
fd-level ENOMEM is not repaired by buffer fallback. Actual target cause/repair
therefore remain pending rather than assumed from the old message alone.

Host validation uses actual File.list/listFiles JNI with -Xcheck:jni/UBSan and
the actual VM C ABI/shared ledger over controlled real storage. With ordinary
buffer mappings refused, it returns351exact Unicode names, converter-style.dat
filters and empty listings across repeated lifetimes. Partial direct-budget
refusal returns null and rolls back resources. Existing fd/read/partial-read/
close/map failures, array growth, child/symlink paths and recovery pass. Actual
NIO JNI/Files.walk normal controls and malformed/error/EOF parserASan/UBSan
controls pass. Exact0106patch and targetjava.base native builds pass. This is a
controlled host adapter, not full PS5 kernel/VM behavior.

No new host game run: game/probe/loader/smoke JARs remain byte-identical, retaining
089's224MiB60s/27checks/14saves/25forced-chunk/save-stop host evidence separately.
224MiB, metadata/thread-stack/libc fixes, view4/simulation3/normal world/security/
OP policy and music removal remain. No project game-JAR rewrite/replacement,
legacy-directory rename/deletion or skipped conversion is introduced.

Next PS5: startup and actual directory enumeration, then short joined movement/
new chunks/damage/grass/save/rejoin; inspect staged errors if startup still fails.
Reaper/guard/TLS/NMT under sustained load and actual player persistence remain
unvalidated. Full two-hour run stays deferred; arbitrarymods/Paper/plugins/
20-player load pending. Preserve058frozen and083vanilla fallback plus exact failed
091package locally. No new ALL PASS claim.
