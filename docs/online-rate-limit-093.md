# Build 093: profile lookup rate limit before server startup

The current 093 session fails during verified online preflight. Discovery HTTPS
succeeds, then api.mojang.com returns HTTP 429 for the account profile lookup.
The server never starts and the new runtime selector backend is not exercised.
This capture neither confirms nor rejects the selector repair. Raw reports and
account details stay local.

094 avoids the redundant name lookup when the configured account already has a
valid UUID in the world's whitelist. That UUID is still checked against the
remote HTTPS session profile, including both UUID and account name. Missing
entries use the original remote name lookup. Invalid or conflicting identities
fail. Existing whitelist entries are not treated as proof of an authenticated
login: online-mode, the server's actual login verification, TLS certificate
validation and whitelist enforcement remain enabled.

All preflight JSON reads now retry HTTP 429 at most twice. Retry-After numeric
seconds and HTTP dates are supported, with a five-second default for missing or
malformed headers. A request for more than 30 seconds of waiting fails with an
explicit retry-later message rather than retrying early. Other HTTP statuses,
I/O errors and malformed responses remain failures; interruption propagates.
Each response disconnects before any wait. Persistent throttling still fails;
this is not a claim that an unavailable external service can always be bypassed.

Host checks run the actual response/retry/cleanup methods using controlled HTTPS
responses, without contacting Mojang: 429 then success, exhausted retries,
Retry-After forms, 401/404/500, malformed/oversized bodies and interruption.
Whitelist reuse/missing/malformed/conflicting identities and remote session
UUID/name checks pass, along with the existing HTTPS-only/UUID/schema tests.
The runtime and original game/Fabric/smoke JARs are unchanged. Only the separate
probe's online-bootstrap classes change. Music remains removed.

Next console: verified online preflight, startup and joining, followed by the
selector backend marker and short joined stability/save/rejoin checks. Actual
093 selector support and native pressure remain unvalidated. The full two-hour
run is deferred. No ALL PASS or 20-player capacity claim. Frozen 058, vanilla083
fallback and exact failed093 package are preserved.

Final package checks pass: CRC/version/options, current native libraries and
module image, all pinned JARs/original-game audit, linked selector methods and
markers, signed-container integrity and matching package/symbol copies. Runtime
and module image are identical to 093; other than the online-bootstrap probe
classes, game/probe/Fabric/smoke JAR entries match. Online mode is still enabled,
and host test doubles are excluded. Frozen/fallback packages remain intact.

Local 094 package SHA-256:
`97ec74c40b9c495884130f9dae0ab10bf393e521265cbe82177f06190176df2d`.
This development candidate still needs actual PS5 validation.
