# Play-test failure in 101: first DNS query

Current-run session, exception, console, startup tail and native trace all identify build 01.000.101. The test fails normally without a new VM abort. Trust-store validation, DRBG and default TLS setup complete, but the first discovery lookup fails. Early pool/resolver preparation succeeds and both handles are reused. The real query returns 0x804101E2 with neterrno226. The native direct trace reports 256 MiB allowance and zero policy refusals/kernel failures. Paper does not start; the new native-memory allowance has not been exercised through Paper readiness.

Build 102 pins the runtime's scoped resolver repair: up to three synchronous default-policy attempts after completed timeout226 only. The same pool/resolver lease remains held; no cached/preset answers or new resolver resources. The existing timeout/retry arguments are retained. Success publishes a real answer; exhaustion propagates the last real failure. Other errors stop immediately, and nondefault timeout/retry/flag calls pass through once. This may extend startup delay and cannot fix a persistent network outage. No authentication or TLS validation change.

Host ASan/UBSan tests execute the actual adapter and SHA-pinned SDK conversion/cleanup bodies: recovery on attempts 2/3, persistent timeout exactly 3 calls, timeout then permanent failure, permanent error no-retry, explicit timeout/async flags passthrough, failed-answer isolation, errno, lease cleanup/recovery and 400 cross-thread fresh lookups with late allocation refusal. These inject network results and do not establish PS5 DNS behavior.

Package checks require all 105 upstream Paper JARs, probe/plugin JARs, module image and native libraries unchanged from 101, with only the scoped adapter and build label changing in the application. Actual PS5 recovery, online preflight, Paper readiness, plugin lifecycle, joined play/save/stop/reload remain pending. Keep failed 101 and Fabric094/vanilla083/frozen058 fallbacks. Full 2h remains deferred; no ALL PASS/release claim.

## Console result for102

The next actualPS5 run fails at the same discovery lookup, before Paper. All three queries return0x804101E2/neterrno226; retry2/3 diagnostics and lease cleanup establish that the bounded retry path executes. The run reports no direct-memory policy or kernel failures.

The user confirms both manual DNS slots point to one Pi-hole. During investigation its host answers ping, but direct UDPDNS queries time out, TCP53 refuses connections, and the adminHTTP page is unreachable. The Mac's normal resolver answers the discovery hostname. This supports investigating resolver identity/service availability; it does not establish a Minecraft block-list match, nor prove behavior from the PS5 once service is restored. Keep device addresses and raw reports local. Retain candidate102 and retry it after resolver availability is confirmed. No additional runtime/game change is supported by these reports alone.
