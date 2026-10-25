# ProsperoCraft client049 — repair diagnostic setup regression

The human reported a prolonged black screen in048. Live report retrieval identifies
run `client-01.000.048-1792946164-359674616`;session is FAIL Initialize embedded
runtime/code00000001. The native file contains its matching build/run header but
not the native-active marker. It stopped before constructors/JNI_CreateJavaVM,
so this run did not exercise original Main,rendering or the previous crash.
[Evidence](validation/client048-diagnostic-setup-failure-2026-10-25.json).
Do not attribute old VM traces still on disk to this048 run.

This is a diagnostic regression introduced in048. Its helper calls dup2 to redirect
descriptor2;the PS5 title returns EPERM1. Header creation/open succeed on the same
path,and setvbuf errors are mapped toEIO5. The inspected upstream SDK explicitly
documents title dup2 refusal and uses stderr stream replacement instead:
[platform/src/klog.c at7a82030](https://github.com/mihawk-99/PS5_PayloadSDK/blob/7a82030dcff6457936d75be97f52aa509b770e1f/platform/src/klog.c).
This is source reference evidence,not a dependency upgrade. The048host checks
passed because host descriptor duplication is allowed;they did not establish
PS5 syscall capability. Preserve exact048package/symbols/status/evidence.

049 changes the generic runtime helper to open/fdopen the append file and make
the new FILE unbuffered **before** assigning it to stderr. It never calls dup2.
Open/fdopen/setvbuf failure leaves the previous stderr pointer in place and closes
unpublished resources. The old stream/descriptor2 remain owned and are not closed.
Native fprintf(stderr,...) driver messages can now use the replacement stream;
raw write(2,...) and libraries caching the old FILE retain their original output.
The helper is called before native services;no concurrent pointer update/thread
or pipe is introduced. This is title-lifetime capture with no automatic restore.

Consumer startup also makes this optional diagnostic setup nonfatal. Header or
helper failure is notified and logged with its exact code,then existing runtime
startup continues. Setup success writes `Client049 native stderr stream active
before embedded constructors`;startup log records FILE-capture status and explicitly
notes raw descriptor2 is unchanged. No capture success is fabricated. This avoids
another black-screen startup block merely because optional logging is unavailable.

Keep046early WSI ownership and047outer delegating fault recording. No Java heap,
resolution,GPU driver/runtime implementation or official game JAR changes. Original
54JARs/5147assets and all frozen passing milestones remain intact. Runtime helper
repair is published separately;no JVM image change. No new pass/release is claimed.

Validation:

```sh
# Runtime
python3 tools/test_native_stderr.py
python3 tools/test_probe_log_share.py
python3 tools/test_probe_report_writer.py
# Consumer
python3 tools/test_shaderc_fault.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

Host tests exercise actual native stdio/unbuffered _exit/append,raw descriptor2
and stdout unchanged,errno preservation,failed open and injected fdopen failure
with unpublished-fd cleanup/old-stream preservation under ASan/UBSan. HTTP tests
retain native-report session archiving/routes/ZIP collection. Target/package audit
requires fdopen and absence of dup2 in the startup main object,actual marker/routes/
nonfatal status text,original pins,audits,SELF integrity and exact048checksum.
Host success still does not prove PS5 FILE replacement or resolve original crash.

Install runtime dist/PPSA99874.zip,launch and press X once. If capture fails,the
app now continues and notifies. After a crash,reopen without X;collect current
native-stderr.log plus matching build/session/full VM/exceptions/startup/abort/
fatal reports. Verify matching identity and native-stream marker. Actual PS5
stream capture,return to original loading screen,crash mechanism/resolution,
menu/gameplay/stability remain pending. Server2H endurance stays deferred.

Full local ZIP SHA-256:
`b8edd18c63a6572c483c7c6e203e772bf48c974c50b56a1199fe7d2151d11b40`.
Runtime helper repair published separately at6382528 in ps5-java25-homebrew;
no runtime image change. Host stream-capture/server/recorder/launch/allocation
checks and target build pass. Actual PS5 behavior remains pending.

Full-package validation passes,including fdopen/no dup2 in actual startup main,
nonfatal diagnostic marker,all original pins,SELF integrity and exact048preservation;
recorded in startup/status.json.
