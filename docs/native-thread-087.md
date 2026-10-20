# Build087: native worker creation failure after join

The current-run087session is FAIL. The server is ready and records nine health
checks through241seconds at20TPS with no joined players. It admits an
authenticated player, then fails about two seconds later. The first fatal game
error is OutOfMemoryError: unable to create native thread, from ForkJoinPool
compensation while chunk generation waits in IOWorker.isOldChunkAround.
The resulting worker exception reaches the server and it stops, disconnecting
the client. Authentication is not the rejection in this capture.

The native VM trace records38successful pthread_create calls and8failures
(two groups of four retries). Failure result is35 (target EAGAIN), errno12,
requested stack512KiB. Attribute acquisition succeeds; no attribute-pool
exhaustion is shown. This is not evidence of an OS thread-count cap. The
Java exception reports about30.5million bytes free within the200081408-byte
maximum heap after failure; native memory and Java heap are distinct resources.
The exact SDK allocation that failed is not identified. The bounded direct
fallback covers selected VM/ZIP/image allocations, not pthread internals or
thread stacks. Its zero failure counter does not establish pthread headroom.
Raw logs remain local; no identity/address is published.

087 passes the new actual players/data java.io/NBT file preflight before join.
This does not establish a real player save/rejoin. It also does not establish
that spawn-protection=0 fixed the previously reported block corrections; the
short connection did not permit acceptance of that change.

088 is a controlled memory-budget candidate: cap Java heap at176MiB rather than
192MiB, leaving16MiB more potential process memory for native use when Java
would otherwise expand to its old cap. This does not preallocate or guarantee
a native reserve, and it can increase GC pressure or cause a real Java heap
refusal. Keep512KiB thread stacks, processor count2, C1/SerialGC/cache/direct
ledger and game/loader/mod artifacts unchanged. Add standard os+thread=info to
the existing bounded VM exception log for thread names/count/failure context.
No errors are suppressed and no game executor or JAR is replaced or rewritten.

Validate host Fabric chunk generation and saves at176MiB, then short PS5 join,
movement into new chunks, disconnect and rejoin. Inspect native thread creation
and GC together before deciding whether the tradeoff helps. This is not a proven
SDK allocation fix or a capacity/performance claim. Player persistence/block
corrections remain pending; full two-hour test is still deferred.058frozen and
083vanilla fallback, plus the exact failed087package, are preserved.
