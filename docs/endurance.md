# Two-hour PS5 server endurance probe — build01.000.059

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

This is an unattended no-player server test with low-distance flat-world
settings. It does not generate player activity or establish loaded-chunk,
network-client, gameplay performance or multiplayer endurance. Forced chunk
loading is not added. No preset device IP or client filter is embedded.

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
