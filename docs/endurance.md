# Online two-hour PS5 server endurance probe — build01.000.062

This development build extends the passing058 startup/save/stop fixture. The
Server_Start snapshot and exact passing package remain frozen. Runtime pin,
160MiB Java heap,8MiB native worker and interpreter mode are unchanged.

Run the five menu rows in order. Row4 first waits for real Minecraft readiness,
then runs for at least7200 seconds before a final flushed save, clean stop,
server-thread exit and nonempty world/level.dat check. Run Destroy Java VM only
after that row returns. Keep the app open and the console awake throughout.
If a row fails, leave the probe open for log collection before starting new rows.
The native menu timer includes startup; the Java health log measures the timed
endurance phase separately. Startup and shutdown can extend total elapsed time.

The server uses the existing isolated mc-server-start world/configuration.
Automatic pause when empty is disabled using pause-when-empty-seconds=0.
Every30 seconds the fixture sends time query gametime, waits for a fresh reply
and requires game time to advance. Every five minutes it requests save-all
flush and requires the completion acknowledgement. A final flushed save is
required even for a shortened host test. New server-thread ERROR logs, thread
exit, unresponsive commands or stalled game time cause failure. Command replies
have a120-second deadline; save work contributes to the endurance duration.

Log sharing remains on the existing runtime-selected address/port. Read
server.log for MC_ENDURANCE_BEGIN, MC_ENDURANCE_HEALTH and
MC_ENDURANCE_COMPLETE; these record elapsed time, actual game time, check/save
counts and Java heap usage. Success also requires MC_SERVER_ENDURANCE_OK and
the native row returning PASS, followed by VM destruction. Heap usage is Java
memory, not available native memory. A running menu or elapsed clock alone is
not proof of healthy ticks or a passing run.

The baseline workload uses low-distance flat-world settings without simulated
players. Build060 allows the configured account to join and records successful
join counts; it does not require a client to stay connected for the full run.
Loaded-chunk/client gameplay performance and multiplayer endurance need actual
client observations. Forced chunk loading is not added. No preset device IP or client filter is embedded.

For a short host regression after preparation:

```sh
python3 tools/test_server_start.py --endurance-seconds 75
```

The host run uses2-second checks and4-second saves so multiple real command
replies and flushes are exercised, including more than the usual60-second
empty-server pause threshold. It does not establish the requested two-hour
PS5 pass. Saved-world reload, player joins and longer performance/endurance
coverage remain separate validation work.


## Online login observation during059

The current059 console confirms that a LAN client reaches the listening server,
but discovery.minecraftservices.com fails with UnknownHostException. Authlib
then has no SESSION/verify endpoint and rejects login with its generic
Authentication servers are down message. This does not establish a global
service outage. The screenshot's server entry demonstrates status discovery,
not successful authenticated admission. Whitelist is also enabled.

The exact native resolver error is not present in the collected Java report;
that cause must be localized before claiming a DNS repair. No authentication,
whitelist, resolver settings or active console run were changed. The collected
snapshot shows real game-time progression through120seconds and the worker
remains RUN; the full two-hour outcome remains pending. Failed login is separate
from server-thread endurance checks and does not establish multiplayer support.


## Build060 online setup

Package with --join-player YOUR_ACCOUNT. The local app contains only that
account-name setting in a generated join-player.txt asset; the name is not in
source Git. Before server launch the fixture requires genuine DNS and verified
HTTPS responses from discovery/profile/session-profile/public-key services,
then merges the verified account into whitelist.json. Existing entries remain.
Online authentication and certificate validation remain enabled. This preflight
checks service reachability and profile identity, not a successful hasJoined
exchange; real admission is proved only when a client actually joins.

Install the complete060 folder with the current probe closed, then run rows in
order. After successful preflight and Done readiness, the7200-second timer
starts automatically. The configured account can try joining with the matching
Minecraft Java26.3 client. Whitelisting occurs before launch. Watch the console
log for MC_ONLINE_PREFLIGHT_OK and later actual player-join output. A preflight
failure reports DNS, HTTP/TLS or profile validation context and leaves the
native resolver stages available in vm-trace.log. No guessed endpoint IP,
offline identity or permissive TLS behavior is used.

Host integration can exercise real online preflight plus a short endurance:

```sh
python3 tools/test_server_start.py --endurance-seconds 75 --online-player YOUR_ACCOUNT
```

Host success cannot establish the PS5 resolver repair or authenticated client
admission. All060 console rows and the actual two-hour result remain pending.


Build060 also fails an online-enabled run if an authentication-thread ERROR is
observed; join/authentication-error counts are logged with health reports.
Monitoring that starts more than one poll interval after readiness is rejected,
so an unobserved readiness interval cannot silently count toward a pass.
The final host integration passes online preflight plus75seconds of live ticks,
36 checks,18 flushes, clean stop and saved metadata, with zero simulated joins.
Actual PS5 online admission and7200seconds remain unvalidated.


## Build061 trust-store repair

060 resolves DNS but TLS preflight fails with no trust anchors, before starting
the server/timer.061 adds genuine java.io descriptor metadata fallback and
relative File resolution for whitelist discovery. Look for MC_TLS_TRUST_FILE
and MC_TLS_TRUST_OK acceptedIssuers before MC_ONLINE_PREFLIGHT_OK. All certificate
and online-identity checks remain standard. The real host HTTPS preflight
passes under injected desktop metadata denial with the target111-root store;
console TLS/admission and the full7200second outcome remain pending.


## Build062 authentication discovery DNS repair

061 gets through standard TLS trust/preflight and real readiness, then its
Minecraft discovery thread cannot allocate a new DNS pool.062 retains one
bounded real pool/resolver pair from preflight and serializes fresh queries.
Expect DNS pool/resolver reuse stages in native trace. The harness now rejects
Minecraft discovery failures before the timed phase and checks discoveryErrors
alongside login errors afterward. This prevents a no-player endurance run
from passing after an observed discovery failure. A zero join count still does
not validate actual player admission. Host40second online readiness/save/stop
passes; PS5 admission and the full two-hour result remain pending. Install062,
run the normal rows and join after readiness; do not treat preflight or package
checks as a console pass. The frozen058 milestone is unchanged.
