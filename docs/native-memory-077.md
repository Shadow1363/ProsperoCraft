# Build 077 native compiler allocation failure and build 078 repair

The user reports near-perfect gameplay with some mob/damage lag, then a crash.
The current077fatal report captures97.573seconds JVM uptime: C1CompilerThread0
fails32664native bytes in Chunk::new while compiling SerializableChunkData.read
(808bytes). The32KiBraw fallback mapping fails with ENOMEM both before and after
unused arena pools are pruned. No Java heap OutOfMemoryError establishes the
cause; this is a native allocation abort. The generic JVM memory summary and
maxrss_raw520448 are not proof of a hard memory limit. No raw report/account
identity/address fields are published.

The vanilla compressed-NBT/SYNC/replacement/backup/readback probe passes on PS5.
That is file-pipeline evidence, not proof of player serialization or rejoin
persistence. Three health checks cover60seconds after readiness with one join
and zero completed scheduled world saves. Full-GC/tick bursts persist. This is
not ALLPASS, a passing milestone or completed7200seconds.

Runtime[0099](https://github.com/mateo-cogeanu/ps5-java25-homebrew/blob/main/Development/docs/java25-index-only-module-image.md)
keeps only the module image index resident in anonymous memory. Resource reads
use the upstream explicit-offset path, existing scoped buffers and checked ZIP
decode. Desktop behavior stays unchanged and no file-backed mapping is restored.
Currentimage28085766bytes,index1000498bytes;16KiBpage-rounded savings27082752bytes
(25.828125MiB). All modules stay available. This reduces a known persistent cost;
it is not a measured console peak-RSS reduction or a guarantee against future
native OOM. Resource file reads and temporary buffers can affect loading latency.

078retains the176MiBheap,NewRatio15,guardedC1/2MiBcompilationlimit,normalworld/view4/
simulation3/max20/OP4/authentication/certificatevalidation/7200sreadinessanchor.
No new game transformation or replacement class is introduced. Native compiler
allocation can still abort if memory is exhausted; no bailout implementation is
claimed. The generic runtime fix belongs in its own repository.

Actualrelease-reader ASan/UBSan verifies indexcopies under2MiB, zero file-backed
maps, resourceidentity forHTTPS/DTLS/SSL/Object/String/JFR/desktop, short/EINTR
reads, EIO/EOFfailurewithoutpublishingcompressedresourcebytes, both compressed
input/outputallocationrefusal, cleanup/recovery and earlierZIP/tinyterminal
controls. Targetnativebuild/exactpatchapplication pass. No new hostgame run is
needed for unchanged consumer helpers;077hostworld/save/stop controls remain
recorded with their comparison limits.

Pending078PS5: startup, index-onlytrace, nativeheadroomduringjoinedchunkloading,
readlatency/GC/tickgaps, mob/damagelag, respawn/food, playersave/rejoinpersistence,
full7200seconds and20playercapacity. Preserve frozen058. The failed077package
and matching symbols remain local for diagnosis.
