# Fabric stutters, shader image loading and launcher controls — 01.000.104

The human reports Fabric103 loads, but has severe short stutters and crashes
when selecting a shader. They request spatial left/right launcher navigation,
normal styling for content buttons and QWERTY for the launcher keyboard only.
This is partial Fabric console feedback, not an ALL PASS or shader acceptance.

## Retrieved103 evidence

Safari computer use confirmed open build103/current session and downloaded the
current/previous diagnostic links after the app had reopened. Previous native
stderr identifies run `client-01.000.103-1793122052-873759368`; current run is
`client-01.000.103-1793122360-573968131`. Previous Java/GC files have no separate
session header; their previous-run rotation is collected alongside that native
report. Raw logs remain local; public observation records hashes and summaries.

The previous exception report shows Fabric/Mixin, a running integrated world,
Vitrail0.13.0-beta and BSL_v10.1.8. Shader noise decoding fails at
`MemoryCacheImageInputStream -> sun.java2d.Disposer`, caused by
`UnsatisfiedLinkError: no awt in system library path`. The later
NoClassDefFoundError is the failed initializer being reused. This is a Java image
runtime gap; no captured native GPU fatal report establishes a shader-driver
crash. Graphics compatibility after fixing decoding remains untested.

The JIT log's32MiBcode cache approaches95percent use, with repeated explicit
code-cache-triggered aggressive GC from roughly274–298s. GC reports also contain
metadata-threshold full collections of92–105ms and four System.gc full pauses
near shader reload/crash,177–364ms. These are observed latency/pressure sources;
there is no frame-timestamp correlation or proof they explain every hitch.

World saves also fail with `Too many open files`. Exact FD limits/counts were not
captured for that prior gameplay run; the available current resource file is only
a header. Do not claim a measured limit, a proven leak owner or successful save.

## 104 changes

- Reserve96MiBcode cache instead of32MiB, keeping the existing C1 compiler policy.
- Set initial metadata GC threshold128MiB; this does not cap metadata or precommit
  that entire amount. Keep heap128MiBinitial/1536MiBmax and prior G1 policy.
- Honor explicit GC through concurrent G1 cycles, preserving collection requests
  rather than disabling them. Full collection remains available when required.
- Add the Java repository's opt-in genuine OpenJDK ImageIO raster/Disposer/Unix
  IDs/Trace and LCMS resident natives. Original game/mod JARs stay untouched.
  The Java component is an image-data subset, not full GUI/fonts/printing/JPEG.
- Configure standard JAR URL streams without the global resource cache before
  Fabric starts. This avoids an extra retained descriptor per resource JAR in a
  real host test:40 retained with cache, zero with scoped streams. Classloader
  handles remain owned normally; actual PS5 FD/save behavior needs confirmation.
- Instance Settings moves horizontally between Mods/Shaders and Done/Delete;
  vertical moves follow screen rows. Content browsers likewise navigate
  Search/Download All and Previous/Next horizontally, results vertically.
- Mods/Shaders/Resource Packs use standard secondary buttons; focus indication
  remains distinct. Delete is secondary as well; confirmation remains required.
- Launcher keyboard has number row, QWERTY, ASDFGHJKL and ZXCVBNM rows, with
  existing case/space/backspace/confirm/cancel controls. The in-game keyboard is
  unchanged.

The code cache reserves64MiBmore native address space than103. Long mod sessions
can still grow metadata/code/heap pressure; this candidate is not an endurance
fix or a promise that every mod/shader works. The lower-pause100remark policy is
preserved, including its longer class/code retention tradeoff.

## Verification and PS5 follow-up

Host tests force the new native image subset, prove no stock AWT/LCMS fallback,
match all PNG pixel hashes against stock JDK for RGBA/indexed/grayscale/RGB,
and exercise ICC conversion. Actual upstream Fabric/Mixin still reaches a test
mod's preLaunch entrypoint and shares parent LWJGL state. Real JAR streams prove
the scoped-handle behavior. JVM controls prove96MiBcode-cache capacity and128MiB
metadata threshold, retained heap contents, and concurrent explicit-GC cycles;
old-policy control produces full pauses. Host tests omit only x86 UseAVX/UseSSE
flags on the ARM host. Native and actual Vulkan UI previews were inspected.

The target native link initially exposed missing J2dTraceImpl; adding intact
upstream Trace.c resolved it. The final native link, package signatures/CRC,
ImageIO export/images/audit, source/fixture equality and preserved dependency
checks pass. Test expectations now reflect spatial navigation and QWERTY keys.
No frozen core/dependency equality assertion is weakened.

On exact104, test launcher arrows/style/QWERTY; launch Fabric without shaders,
compare stutters in the same scene, then retry the shader. Check world save/reload
explicitly because103 had save errors. Check audio, controls and quit/relaunch.
Keep open for logs on failure. Native decoder behavior, shader rendering/GPU
features, frame-time improvement, file-handle headroom and save reliability are
all pending actual PS5 validation. Preserve101/103 and all frozen milestones.
No Store/public binary release or new milestone is requested.

[103 observation](validation/client103-stutters-shader-observation-2026-10-27.json) ·
[104 build validation](validation/client104-stutters-shaders-controls-build-2026-10-27.json).
Package SHA-256: `3cfffdbdc17c8858f17dc060c53fcfd5048cb2335e08ae653a0fa19781e9aadc`.
