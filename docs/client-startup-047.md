# ProsperoCraft client047 — retain native fault recording across original startup

046 produced the original visible Mojang loading screen on the actual PS5,then
crashed according to the human,who reopened the app without starting another run.
Saved build/session identify `client-01.000.046-1792944398-207378114`.
[Hashed report evidence](validation/client046-loading-screen-crash-2026-10-25.json).
This is loading-screen progress,not menu/gameplay acceptance or ALL PASS.

The early same-owner VideoOut open returns the actual positive handle0x4e100100,
with prepare result0. Later WSI creates the real1920x1080/3image swapchain;
images0/1/2 each require8847360 bytes aligned65536 within10485760-byte buffers,
and each host import returns0. The old initialization/registration rejection is
absent. Human visual evidence corroborates actual presentation beyond opening.
Keep046's early same-owner initialization;no new display owner/handoff is needed.
This run establishes that the lifecycle change worked,not the precise internal
cause of045's late-open refusal.

The later crash still has no captured fatal signal or VM abort. hs-error.log is
unavailable;vm-trace ends after shaderc returns,with resource reload/font loading
in the Java report. Narrator unsupported-platform and offline service errors are
logged,but there is no fatal stack tying them to this crash. Do not label one
of those recoverable logged messages the crash cause or invent a crash instruction.

A concrete diagnostic gap exists:the native signal recorder is scoped to each
shaderc_compile_into_spv call. Its final end restores earlier JVM handlers and
closes its append descriptor between compilations. Thus a crash after a compiler
return can escape this recorder.047 holds one outer reference around the complete
ClientStartup25 JNI invocation,including native provider initialization and the
original reflective Main call. Nested compiler begin/end calls reuse its handlers
and descriptor;ending one compile cannot remove the outer recording scope.

The recorder implementation and its signal forwarding are unchanged. It records
SIGSEGV/SIGBUS/SIGILL/SIGABRT through the existing preopened raw-write path,
including raw bounded96-word context,then delegates to the prior JVM handler.
The historical `SHADERC FAULT` prefix now also applies to faults outside compilation;
that prefix does not identify the faulting component. Raw context words have no
assumed PS5 register layout. A signal handled normally by the JVM is not by itself
a fatal crash. No signal recovery,context rewrite or fabricated success is added.
The wrapper requires all4 handlers and a valid descriptor;otherwise check4 fails
explicitly before Main. RAII releases its reference on ordinary/Java-exception
returns,including partial-install failure,restoring prior handlers when last.
Process-kill/GPU/system faults may still leave no signal report;capture is pending.

Only the consumer startup harness lifetime changes. The fault source,shaderc,
WSI adapter,original54JARs/5147assets,Java runtime,heap/class limits and approved
branding stay intact. Exact046 full package,symbols,status and failure evidence
are preserved locally. No passing milestone/release is created from this partial
progress;frozen passing snapshots remain untouched. Server2H remains deferred.

Checks/build:

```sh
python3 tools/test_shaderc_fault.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

The real recorder host test now exercises SIGILL and SIGSEGV after a nested
compiler scope ends while an outer reference remains,as well as existing handler
restoration/mask and one-argument/SA_SIGINFO forwarding. Prior handlers determine
child exit;this is diagnostic delegation validation,not PS5 recovery. Desktop
context coverage is4words;PS5 keeps its existing96-word raw capture. Package checks
verify actual recorder symbols and startup diagnostic marker plus original pins,
native audits,constructors,SELF integrity and preserved exact046 checksum.

Install runtime dist/PPSA99874.zip,launch and press X once. Observe the actual
loading/menu screen. After a crash,reopen without X to preserve reports. Retrieve
full native trace/build/session/exceptions/abort/fatal reports and inspect any
raw fault context against matching047symbols. Actual PS5 signal capture,crash
cause,menu/presentation stability and gameplay still need validation.

Full local ZIP SHA-256:
`52cc98ea6b779f8bdf9b8a2b185a555f5e9bba5a970e33e55fd1bde3907f54f3`.
Host recorder delegation/lifetime tests and original launch/allocation checks pass;
target build and full-package verification pass,including original pins,SELF
integrity,recorder symbols/marker and exact046preservation;recorded in startup/status.json.
Actual PS5 crash capture/resolution and menu remain pending.

## Retrieved console evidence

Matching047run client-01.000.047-1792945285-415061738 confirms outer recorder4,
early VideoOut0x4e100100/prepare0 and3successful imports. No signal/VM abort;
hs-error unavailable. Trace ends after shaderc return,not proof of crash location.
[Evidence](validation/client047-startup-failure-2026-10-25.json) ·
[048native-stderr follow-up](client-startup-048.md).
