# ProsperoCraft client046 — initialize the same WSI output before Main

[045 report evidence](validation/client045-startup-failure-2026-10-25.json) identifies
run `client-01.000.045-1792943278-134343222`. Both VideoOut opens still returned
0x80020023. Kernel resource queries succeeded:configured flexible448MiB,
available324MiB at both calls;largest direct range12622757888 bytes then
12373196800 bytes. Each open left these measurements unchanged. General depletion
of those pools is not supported by the evidence;this does not prove every
internal service allocation can succeed.

Earlier in the same trace,ordinary pthread_create fails32 times across8 Java
thread creation sequences with EAGAIN/errno ENOMEM. All8 direct-stack fallbacks
succeed,and9 ordinary creates succeed elsewhere. VM-native libc charged bytes
approach the existing2MiB allowance before the first failing thread creation.
These are concrete allocation-path failures despite available flexible memory.
They support a libc/service allocation-pressure hypothesis;they do **not** prove
VideoOut's internal failure path. There is no captured fatal signal/VM abort;
no crash instruction can be attributed from these reports.

046 adds `client_wsi_videoout_prepare` to the private WSI adapter. Startup-only
GPU provider JNI_OnLoad calls it after the existing GPU constructors and before
loading/executing original Main. In045 those constructors completed at trace
line1751,Main entered at1932,first ordinary thread failure was3784,and the first
VideoOut open was7151. Moving this service initialization earlier tests that
specific lifecycle/resource-pressure difference without changing memory limits.

This is the actual WSI output's initialization,not a separate display probe:

- The function uses the existing call_once,output lock,videoout_open_locked and
  static videoout_output. The same successful handle (including0) is retained.
- Later display enumeration and swapchain registration use that same state.
  No external handle is passed,no second output is opened,and no ownership
  transfer or close/reopen is implemented.
- No buffers/swapchain are allocated by preparation. No framebuffer or menu
  success is claimed from opening alone.
- A negative open result is logged and causes JNI_OnLoad to return JNI_ERR.
  Original Main then does not run. The native load failure is real;it is not
  replaced by a fabricated handle or success. In the actual startup path,an
  early load refusal stops that run before any delayed retry can be requested.
- The hook is compiled only when startup's private WSI diagnostics are selected.
  Other native milestone build modes retain their existing provider lifecycle.

The ordinary Java thread direct-stack fallback,Java256MiB heap,64MiB class space,
1080p display policy,original54 JARs/5147 assets and accepted native components
remain unchanged. Runtime source/SDK are not modified. Exact045 full package,
symbols,status and hashed report evidence were retained before building046.
Frozen passing snapshots/releases remain intact;046 is not a passing milestone.

Validation commands (resource/ownership tests use controlled OS responses):

```sh
python3 tools/build_wsi_diagnostics.py
python3 tools/test_videoout_retry_host.py
python3 tools/test_videoout_resources_host.py
python3 tools/test_wsi_diagnostics_host.py
python3 tools/test_videoout_early_owner_host.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

The new host test compiles the exact early-owner entry and open function under
ASan/UBSan,using pthread mutex/once primitives and controlled OS handles. Four
concurrent preparation calls result in one real mocked open;later normal opens
reuse positive/zero handles. Negative results and the existing delayed retry
limit stay unchanged. It does not validate real PS5 module allocation or GPU
presentation. Target/package audits pin patch0004 and startup-only hook in the
actual binary,plus original artifacts,constructors,SELF integrity and frozen hashes.

Install runtime `dist/PPSA99874.zip`,launch and press X once. Check the actual
screen;opening VideoOut alone is not menu acceptance. If it fails/crashes,reopen
without X to preserve reports. Retrieve full trace/build/session/exceptions and
abort/fatal reports. Look for early WSI open/resources and later registration,
images/presentation. Early initialization,remaining service allocations,original
menu/gameplay and later process-exit cause all require PS5 validation. Server2H
endurance remains deferred.

Host owner/retry/resource/helper and original launch/allocation checks pass.
Target build and full-package checks pass,including the actual early-owner
symbol/reference,all original artifacts,SELF integrity and historical package
checksums. Full local ZIP SHA-256:
`c4c8a11e8fb54dcf2e1fbb91759261aacb940ec1c85485a40ab225b138afbdb9`.
PS5 outcome remains pending.
