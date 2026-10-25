# ProsperoCraft client050 — presentation progress checkpoints

049 gets past048's diagnostic setup regression. Matching report run is
`client-01.000.049-1792947461-290571136`. The native FILE capture marker is present,
followed by actual entropy/device-UUID messages and successful1920x1080 buffer
registration (set0,buffers0-4). No GPU submit refusal/completion timeout appears.
Outer signal recording and positive VideoOut/three-image imports remain intact;
no signal/VM abort is captured and hs-error is unavailable.
[Hashed evidence](validation/client049-startup-failure-2026-10-25.json).

Retrieved046,047and049traces each contain390real compile entries and390returns.
The last shader return is therefore not evidence that this compile crashed.
Java reports end in resource reload/font loading. No new detailed visual result
or menu acceptance accompanied049log retrieval. The original later failure remains
unresolved;available reports do not identify a CPU instruction,GPU fault or a
failed native API. Do not turn missing diagnostics into proof of their absence.

050 adds patch0005 to the private native WSI adapter. It records:

- Raw C11 flip-thread creation status,without changing its existing failure return.
- First8 presentation enqueues,with buffer and in-flight count.
- First8 flip-worker fence waits,before the call and after its actual VkResult.
- First8 native SubmitFlip results,with buffer/argument/raw OS code.
- Non-success wait/flip results after those first8,subject to the same existing
 64-event/384-byte WSI logger cap shared with initialization evidence.

Counters are used under existing output ownership/locking (flip counter has one
worker). No new output,thread,timeout,memory allocation or resolution is introduced.
The same private WSI object replaces one archive member;original pinned Mesa source
and archive remain unchanged. All wait/OS calls and queue/buffer/argument updates
retain their order and behavior. Notably the pinned worker previously continued
to SubmitFlip even if WaitForFences returned failure;050logs that result without
claiming to repair its handling. This is an unresolved driver behavior to assess
against actual evidence,not a fabricated fence success. An accepted SubmitFlip
alone does not prove that the corresponding frame was shown.

An enqueue proves entry into native WSI queueing;fence begin without return narrows
a wait;successful return followed by submit status narrows OS presentation. No
queue markers could mean failure earlier in rendering/submission or a different
path;it is not proof of a queue-thread crash. The first8cap limits ongoing overhead
but does not locate an arbitrary later frame failure. Captured errors can be lost
if the existing64-event global budget is exhausted;inspect the full trace.

Preserve046early same-owner output,047outer delegating recorder and049native FILE
capture/nonfatal diagnostics. Original54JARs/5147assets,Java runtime/image/heap,
1080p mode and accepted components remain unchanged. Exact049full package,symbols,
status and evidence are retained. Frozen passes are untouched;no ALL PASS,new
passing milestone or release. Server2H endurance remains deferred.

Checks:

```sh
python3 tools/build_wsi_diagnostics.py
python3 tools/test_videoout_present_host.py
python3 tools/test_videoout_retry_host.py
python3 tools/test_videoout_resources_host.py
python3 tools/test_wsi_diagnostics_host.py
python3 tools/test_videoout_early_owner_host.py
python3 tools/test_shaderc_fault.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

The new host test compiles the exact patched flip worker with controlled fence/
OS responses,checking lock/call order,queue/buffer/argument changes,first8progress
and raw failure logging under ASan/UBSan. It terminates the infinite worker only
through a mock condition broadcast after one iteration. It checks the existing
failed-fence continuation rather than claiming hardware correctness. Other helper/
owner/retry/recorder/launch tests remain. Target/package audits pin patch0005,
its actual markers/object/archive and all original artifacts,SELF integrity and
historical checksums. None is a PS5 presentation pass.

Install runtime dist/PPSA99874.zip,launch and press X once. Report actual screen
behavior. After crash,reopen without X;collect full VM trace and native-stderr,
build/session/exceptions/startup/abort/fatal reports. Inspect queue/fence/flip
checkpoints with matching build/run. PS5 frame progression,crash mechanism/
resolution,menu and stable gameplay remain pending.

Full local ZIP SHA-256:
`ffc3b7d47132e7c426b42e1215033fd6649ca36f4a9c5c589bf44e59d935062f`.
Host exact-worker/helper/owner/retry/recorder/launch checks and target build pass.
Actual PS5 frame progression/crash resolution/menu remain pending.

Full-package validation passes,including actual presentation markers,private WSI
patch/object/archive hashes,original artifacts,SELF integrity and exact049preservation;
recorded in startup/status.json.
