# Build 092: ready at 20 TPS, then selector wakeup fails

The downloaded current session identifies build 01.000.092 and reports FAIL in
the live-server monitor. Server readiness and Fabric smoke checks succeed.
Five unjoined health samples cover 0–121 seconds; measured intervals report
20 TPS, low GC time, and about 0.1 ms average ticks. This does not measure joined
movement, damage or chunk generation. No successful player login is recorded.

At about 147 seconds, a connection reaches the acceptor, but registration fails
because KQueueSelectorImpl.wakeup calls IOUtil.write1 and receives IOException:
Cannot allocate memory. Multiple Netty event loops then terminate; the monitor
correctly fails and requests shutdown. The exception reports about 100 MiB free
Java heap. The last direct-memory sample holds 0xff8000 bytes out of 128 MiB
with zero reported allocator failures. Neither proves why the pipe write fails.
The 091 directory failure does not recur; full directory/persistence validation
is still incomplete. Raw logs and account/network details stay local.

Build 093 adopts runtime 0107: a PS5 selector registers a kernel user event once
and triggers it for wakeups, avoiding pipe writes on that backend. Existing
interrupt locking/coalescing and real-error propagation remain. Unsupported
user-event kernels retain a diagnosed pipe fallback, so the same memory failure
can still occur there. Other native allocation pressure remains unresolved.

Actual patched selector/new JNI bodies pass macOS kqueue tests with
-Xcheck:jni/UBSan: 1,200 wake-before/blocking/coalescing rounds, socket readiness
and cancellation, 100 close races, EINTR retry, unsupported fallback, registration
ENOMEM and trigger EIO. Target Java classes and native libraries compile.
These are host controls, not proof that PS5 firmware supports this event filter.
Original game, probe, Fabric loader and smoke-mod JARs remain unchanged. The
module image and libnio change for the runtime selector repair. Music stays off.

Next PS5: start the server and try joining. Inspect the backend marker and any
network exception, then check movement, damage, grass, new chunks, save/rejoin
and clean stop. Keep the full two-hour run deferred until joined stability is
confirmed. No ALL PASS, mod compatibility or 20-player load claim is made.
Frozen 058 and vanilla 083 remain intact; exact failed 092 is preserved locally.

Package validation passes: ZIP CRC, version/options, seven current native
libraries, pinned artifacts/original-game audit, linked new JNI methods and
backend markers, signatures and matching package/symbol copies. Compared with
092, exactly the two selector classes and four checked incremental-build
metadata resources change in the module image. Other native code and all game/
probe/loader/smoke JARs match. No new host game run was performed; earlier 089
host evidence remains separate from console results.

Local 093 package SHA-256:
`43c0cdcec805a309852d60b37ade34473f1d6a55cc1f0031924e3427a137c69d`.
It is a development candidate, not a passing release asset.
