# ProsperoCraft client044 — bounded VideoOut open retry

043run client-01.000.043-1792940581-168525309 identified a concrete WSI branch:
requested1920x1080 matches its mode,images3/max5,host-import callback present,
format44/usage0x2/FIFO2. It fails initialization-guard-477 and register/ownership
with VK_ERROR_INITIALIZATION_FAILED. That guard is videoout_open_locked's refusal,
before framebuffer registration/image allocation. This is not an image extent,
count or memory-import rejection. The raw OS error was printed only to native
stderr,not captured in043's report. Later exit has no captured fatal signal.

The pinned driver sets opened=true before sceVideoOutOpen and retains it even
on negative return. Every later call therefore returns the cached negative
without another OS attempt.044fixes that state:opened=true only on a nonnegative
actual handle. One retry is permitted at least2seconds after the first refusal,
only before any buffers or current swapchain exist. There are at most two OS
open attempts per process. A successful handle,including0,is retained and never
reopened/closed by this adapter. Permanent failure remains failure;no raw OS error
or Vulkan result is rewritten. The first refusal's underlying cause could still
be permanent,resource pressure or another issue;the patch does not establish
that it is transient. Initial refusal/crash/presentation still need PS5 testing.

The additional native patch0002-videoout-open-retry.patch layers over043's bounded
WSI checkpoints in an ignored private source export. Open attempt and raw hex
OS result now reach the existing report logger. Original pinned Mesa source and
archive remain unchanged;one recompiled WSI object is substituted in a private
RADV archive selected for development startup only. The audit pins both patches,
patched source/object and original/private archives. Original game JARs,JVM-global
allocators,1080p selection,256MiB heap,other accepted native components and the
approved icon remain intact. Exact043package/symbols/status preserved.

Checks/build:

```sh
python3 tools/build_wsi_diagnostics.py
python3 tools/test_videoout_retry_host.py
python3 tools/test_wsi_diagnostics_host.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

The retry host test compiles the exact patched open function with controlled
OS responses/clock under ASan/UBSan. It covers negative-result logging,deadline,
failed-then-successful retention,valid0handle,two permanent failures and no retry
with existing resources. High-frame-rate behavior is unchanged and not exercised
by that test. The existing diagnostic helper test checks bounded formatting,
error preservation and concurrency. These are host state-machine/helper checks,
not real PS5 OS/GPU acceptance. Target/package checks verify selected patches,
private native object/archive,original archive preservation,original54JARs/5147
assets,exact runtime,other accepted components,constructors,icon and integrity.

Install dist/client-startup/PPSA99874.zip or runtime dist/PPSA99874.zip,launch
and press X once. Report failure promptly. After a crash,reopen without X for
preserved reports. The next log should show actual open attempt/result codes.
PS5 VideoOut retry/presentation/menu,initial OS refusal/later crash,memory and
performance/network/teardown remain pending. Server2H endurance stays deferred.

Host retry/helper/launch/allocation checks,target WSI compile and full-package
checks pass. Full local ZIP SHA-256:`3a940fa1e3280b8f665f065ce5af50a00b1b9d2884b608a5a123f41666670443`.
PS5 open/retry/presentation and initial refusal/crash remain pending.
