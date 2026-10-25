# ProsperoCraft client045 — VideoOut resource evidence

The retrieved044 session is `client-01.000.044-1792941998-299539155`,build
01.000.044. Both actual VideoOut open attempts returned `0x80020023`.
The retry executed but did not recover. WSI repeatedly rejected registration
before framebuffer allocation;1920x1080,3 images/max5 and the host-import callback
were valid. [Hashed report evidence](validation/client044-startup-failure-2026-10-25.json).
Saved RUN is not a liveness assertion. There is no new human acceptance report.
The trace ends during shader compilation without a captured fatal signal;
abort.txt says no VM abort,hs-error.log says unavailable. This does not identify
why the process later stopped or establish a crash instruction.

An inspected upstream SDK reference maps kernel0x8002xxxx errors to their low16-bit errno
in platform/src/libc.c:kernel_errno;target/include/sys/errno.h defines35 as
EAGAIN/EWOULDBLOCK (resource temporarily unavailable). Inspected reference commit:
`b5efad528e0ac1b8289f39d72a0e890ff68ff0a6` (not a dependency upgrade).
[Kernel mapping source](https://github.com/mihawk-99/PS5_PayloadSDK/blob/b5efad528e0ac1b8289f39d72a0e890ff68ff0a6/platform/src/libc.c).
That mapping does not establish which resource VideoOut could not obtain or
whether waiting longer would help. No confirmed memory-exhaustion diagnosis.

045 adds a third patch to the existing private WSI source/archive adapter.
Immediately before and after each of its at-most-two OS open calls,it records:

- Configured flexible-memory budget and available flexible bytes,with each raw
  query result.
- Reported direct-memory size and largest available64KiB-aligned range,its
  physical start and query result. The largest range is not total free memory.

Each query output starts at0/start-1;failure statuses remain explicit,so do not
interpret an errored query's0 as proof of exhaustion. A nonpositive direct total
skips the range query. The helper preserves errno,uses the existing384-byte stack
logger/64-event bound,and does not allocate,create threads,open an extra output
or change a result. Native successful handles stay with the same WSI owner.
It does not add a preflight display or an ownership handoff.

Source/ELF audit finds the native sceVideoOutOpen import remains external;
the startup main does not enter the CPU renderer. There is no new output owner
in this change. System-module internal resource allocation and the source of
EAGAIN remain unknown. No module unload/reload,arbitrary delay,heap or resolution
change is attempted. The original54 JARs/5147 asset objects,256MiB Java heap,
64MiB compressed class space,1080p mode selection and branding remain intact.
Exact044full package,symbols,status and evidence are retained locally before build.
Frozen passing milestones are unchanged;045 is diagnostic development.

Checks:

```sh
python3 tools/build_wsi_diagnostics.py
python3 tools/test_videoout_resources_host.py
python3 tools/test_videoout_retry_host.py
python3 tools/test_wsi_diagnostics_host.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

The new host test compiles the exact resource helper with controlled kernel
responses,checking arguments,success/error fields,invalid total and errno
preservation under ASan/UBSan. Existing retry/helper regressions still apply.
These checks do not validate real PS5 query behavior,VideoOut or rendering.
The package audit verifies the third patch,private archive/object hashes and
resource format in the actual SELF,plus existing original-artifact/integrity checks.

Install runtime `dist/PPSA99874.zip`,launch and press X once. After failure/crash,
reopen without pressing X so reports remain available. Retrieve full vm-trace.log
along with build/session/exceptions/abort/fatal reports. Inspect WSI resources and
open results first;available memory alone cannot prove display ownership or
internal module health. Actual VideoOut open/registration/presentation and original
menu still need PS5 validation. Later crash and full game stability remain
unresolved. No passing milestone or release;server2H endurance remains deferred.

Full local package SHA-256:
`df6978569980e567cf2ce269f29e2854dfebb7fc4df75d29709991a8e9aeeffd`.
Host resource/retry/helper/original launch checks and target build pass.
Full-package verification passes,including original artifact pins,SELF integrity,
private WSI audit and preserved historical checksums;recorded in startup/status.json.

## Retrieved console outcome

Run client-01.000.045-1792943278-134343222 confirms both opens still fail0x80020023,
with324MiB flexible available and >11.5GiB direct ranges. Queries succeed;no VM
abort/fatal report. Ordinary thread allocations fail EAGAIN/ENOMEM earlier and
recover with direct stacks. [Evidence](validation/client045-startup-failure-2026-10-25.json).
[046early WSI-owner follow-up](client-startup-046.md);resource-pressure cause and
actual menu/presentation remain unresolved.
