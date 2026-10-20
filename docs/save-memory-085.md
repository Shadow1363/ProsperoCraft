# Build085 native save-allocation failure and086candidate

The supplied Prism client log reaches the game, later reports Server closed,
then gets Connection refused on reconnect. Its process exits with code0. This
log does not show a client JVM crash; the current085PS5reports establish the
server-side cause. Raw client/probe logs and accounts/addresses remain local.

## Console evidence

085reaches Fabric/mod/Knot/world readiness, passes the NBT file-pipeline probe
and admits an authenticated player. Latest health is91seconds after readiness,
4checks/0scheduledsaves/1join. The direct backend records2064mappings and2000
releases at the final sample,3309568held bytes,10059776peak observed held bytes
and zero reported direct failures. C1's previous native allocation abort is not
observed in this run; this does not prove universal native-memory stability.

The new failure is java.util.zip.Deflater.init native OutOfMemoryError on an
IO worker while constructing RegionFile chunk-save compression. Minecraft reports
an exception on the worker, stops the server and disconnects the client. Player
save warnings and stats/advancement failures follow; cold image resource
java/nio/file/Path$1.class fails reading/decompression. The probe fails its save
checks instead of reporting success. This run does not validate saved inventory,
player location, scheduled world saves or rejoin persistence. The UI survives;
no current JVM fatal/abort report is available.

## Runtime repair0102 / build086

[Runtime0102](https://github.com/mateo-cogeanu/ps5-java25-homebrew/blob/main/Development/docs/java25-zip-image-direct-memory.md)
extends ZIP stream/zlib and temporary image-resource allocations to use the same
VM direct-memory ledger after libc and anonymous pages refuse allocation. It
exposes two native C ABI helpers; per-allocation backend tags preserve exact
libc/page/direct ownership. The existing2048slot/128MiB held-byte budget is
shared across raw HotSpot, ZIP and image buffers, not duplicated per library.
No128MiB preallocation occurs. Java heap/metaspace/code-cache mapping stays the
same, as do the192MiB heap, C1/GC policies and all game/loader/probe/mod JARs.

The generic helper test uses the actual exported VM functions, actual ledger and
real aligned host storage with controlled kernel responses. Complete actual ZIP
JNI tests force libc and anonymous allocation failure, then perform raw/wrapped
roundtrips and compressed ZipFS create/read operations through direct memory.
Partial initialization with direct refusal retains genuine OOM and cleanup.
Actual image tests cover input/output/zlib direct buffers, partial-budget failure
without publishing caller bytes and exact Path$1/HTTPS/DTLS bytes. ASan/UBSan,
existing read/decode/corruption controls and actual Java/native/JNI image handoff
pass. Target HotSpot/java.base natives rebuild and two exports are verified.
These checks are not PS5 kernel/cache/latency or game-persistence proof.

086also calls the menu row Server play test rather than2-hour endurance to
match the requested short compatibility work. The monitor's existing7200second
maximum/readiness anchor and300second saves remain unchanged; full endurance is
still deferred. All game/loader/probe/mod bytes and separate Fabric world policy
remain unchanged. No client setting, game-JAR rewrite or Fabric patch is added.

Pending086PS5: joined play under compression/image pressure, shared counters,
actual player/world saves, rejoin/food/respawn, native headroom and stability.
Other native-library allocations and pool/budget exhaustion remain possible.
Keep083vanilla fallback and failed085package/symbols. Continue short Fabric
validation before Paper/plugins and later client work. No new ALL PASS milestone.
