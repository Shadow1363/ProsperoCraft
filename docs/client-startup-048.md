# ProsperoCraft client048 — capture actual native stderr

Matching047 reports identify run `client-01.000.047-1792945285-415061738`.
The outer startup fault recorder installed all4 handlers. VideoOut again opens
with0x4e100100,prepare returns0,and all3swapchain host-image imports succeed.
No SHADERC FAULT/signal/VM abort is captured;hs-error is unavailable. The trace
ends after a shaderc return during resource reload/font loading. Saved RUN does
not prove liveness. No new human menu acceptance or detailed visual outcome was
supplied with this log request. [Evidence](validation/client047-startup-failure-2026-10-25.json).

047's longer signal scope did not yield a crash record. That does not prove
handler delivery,or exclude process kill,GPU/system termination or another cause.
Do not infer a fatal instruction or label the last successful compile the failure.

A separate concrete report gap remains:the pinned RADV driver writes native
errors to stderr. These include submission refusal (`radv_ps5_cs.c`) and a GPU
completion timeout (`radv_ps5_winsys.c`). Java System.setErr does not capture
those native FILE/descriptor writes,and JNI's vfprintf hook is only JVM output.
Those possible driver messages were not present in the downloaded reports.
This is an observation gap,not evidence that either GPU condition occurred.

048 uses the reusable runtime native_stderr.hpp helper before embedded/native
constructors. After explicit session initialization,it creates a separate
identity-stamped `/download0/probe-native-stderr.log`,redirects real descriptor2
onto that file for append,and makes stderr unbuffered. It verifies setup and
fails check1 if report creation/duplication/buffering fails. A first native stdio
marker confirms the stream write path when present in the report. Capture stays
active for this title's lifetime;there is no background watcher or new listener.
stdout and original Java console redirection remain unchanged.

Runtime log sharing adds fixed current/previous allowlisted endpoints:
`/native-stderr.log` and `/previous-native-stderr.log`. A new explicit session
archives prior native output before clearing it;reopening without X preserves
the crashed run's report. The collector includes both files. Old/nonparticipating
apps can return404. Runtime changes are generic report tooling;no JVM implementation,
SDK or image is changed. The consumer harness chooses when to enable capture.

Keep046's working early same-owner output and047's extended signal recorder.
No GPU submission/fence/result,display ownership,resolution,heap,game JAR or
native driver behavior is changed. The54original JARs/5147asset objects and
frozen passing snapshots remain intact. Exact047 package/symbols/status and report
evidence are retained locally. No ALL PASS,new passing milestone or release.

Checks:

```sh
# Runtime workspace
python3 tools/test_native_stderr.py
python3 tools/test_probe_log_share.py
python3 tools/test_probe_report_writer.py
# Consumer workspace
python3 tools/test_shaderc_fault.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

Host capture checks use actual native stdio/raw descriptor2 writes and _exit,
append/open returning2,stdout/errno preservation,and failed-open behavior under
ASan/UBSan. Server checks verify native-report archiving,current/previous routes
and ZIP collection alongside existing allowlist/large/disconnect tests. Existing
recorder delegation/outer-scope and original launch/allocation checks remain.
Target/package checks verify actual native capture marker/endpoints,original pins,
WSI/fault symbols,audits,constructors,SELF integrity and exact047preservation.
None establishes PS5 descriptor/driver output capture or crash resolution.

Install runtime dist/PPSA99874.zip,launch and press X once. After failure/crash,
reopen without X. Retrieve native-stderr.log **in addition to** full VM trace,
build/session/exceptions/startup-tail/abort/hs-error. First verify matching build/run
and native stream marker. Inspect actual driver messages without assuming a GPU
fault in advance. Actual PS5 native logging,crash mechanism/resolution,menu and
stable presentation/gameplay remain pending. Server2H endurance stays deferred.

Full local ZIP SHA-256:
`ede64e69349767fa6dcf425155e5b00210eb20ce48408c6c5c36c7e59179dca4`.
Runtime report-helper changes are published separately at12b03cd in
ps5-java25-homebrew;the runtime image remains the exact accepted baseline.
Host capture/server/recorder/launch/allocation checks and target build pass.
Actual PS5 capture/crash resolution/menu remain pending.

Full-package verification passes,including actual native-capture marker/routes,
original pins,SELF integrity and preserved047checksum;recorded in startup/status.json.

## Console regression and superseding049

048stopped before the JVM:live session FAIL Initialize embedded runtime/code1,
native report only identity. PS5 refuses dup2EPERM;native-active marker absent.
Earlier host descriptor tests did not establish title capability. This run did
not test the original crash. [Evidence](validation/client048-diagnostic-setup-failure-2026-10-25.json).
[049](client-startup-049.md) removes dup2,uses a configured replacement stderr FILE
and makes optional diagnostic failure nonfatal. Raw descriptor2 is not captured.
