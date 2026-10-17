<p align="center">
  <img src="docs/readme-banner.svg" alt="Minecraft Java on PS5 — server first, client next" width="1200">
</p>

<p align="center">
  <a href="#the-goal">The goal</a> ·
  <a href="#runtime-foundation">Java runtime</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="#follow-the-project">Follow the project</a>
</p>

# Minecraft Java on PS5

A homebrew project exploring **Minecraft Java Edition on PlayStation 5** — starting with a dedicated server, then working toward the client, controller support and mod compatibility.

> **Status: first Minecraft server bootstrap milestone passes on PS5.** Build **01.000.002** verifies all 40 official JARs and invokes Minecraft **26.3 / Java 25** `--help`. A ready server, world generation and player joins remain untested.

## The goal

Bring Java Edition's worlds and ecosystem to native PS5 homebrew through small, console-tested milestones.

| Direction | What we're aiming for |
| :--- | :--- |
| **Server first** | Start a vanilla server, create and reload a world, connect over the network and verify save integrity |
| **Client next** | Bring up native dependencies, a window, rendering, audio and controller input |
| **Mods later** | Validate Fabric and Forge against specific working game versions, then test individual mods |

Graphics exploration includes OpenGL and Vulkan possibilities. Backend availability, native bindings and renderer-mod compatibility still need to be established on PS5.

## Runtime foundation

Minecraft needs a working Java runtime before the game can be brought up. That work lives in **[ps5-java25-homebrew](https://github.com/mateo-cogeanu/ps5-java25-homebrew)**.

The repositories have separate responsibilities:

- **Java port:** OpenJDK, PS5 platform adaptations, JNI and runtime acceptance probes.
- **This project:** Minecraft dependencies, launch flow, server/client integration, input, graphics and game-specific tests.

The runtime project has these **console-tested Java milestones** on PS5 firmware **13.60**:

| Runtime milestone | What passed | Source & results |
| :--- | :--- | :---: |
| **JVM startup** | Java 25 VM creation, arithmetic, Java thread start/join and shutdown | [JVM_Startup](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/JVM_Startup) |
| **File I/O** | Private-file creation, UTF-8 write/read, size and deletion | [IO_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/IO_Probe) |
| **ZIP / JAR** | Archive reads, manifest parsing, JAR class loading and UTF-8 resources | [ZIP_JAR_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/ZIP_JAR_Probe) |
| **Networking** | TCP/UDP IPv4 loopback, Java worker echo, nonblocking NIO channels and selector readiness | [Network_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/Network_Probe) |
| **LAN / DNS** | Outbound TCP/UDP echo between PS5 and Mac, forward DNS lookup and VM lifecycle | [LAN_DNS_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/LAN_DNS_Probe) |
| **Inbound LAN** | External IPv4 TCP accept and UDP receive/reply | [Inbound_LAN_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/Inbound_LAN_Probe) |
| **HTTPS / IPv6** | Verified HTTPS, IPv6 loopback and concurrent/repeated local traffic | [Advanced_Network_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/Advanced_Network_Probe) |
| **LAN endurance** | Actual IPv6 link-local LAN and 60-second external TCP/UDP workloads | [LAN_Endurance_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/LAN_Endurance_Probe) |
| **Dependencies / JNI** | Manifest-linked JARs, services/resources, system class path and real resident JNI calls | [Dependency_Probe](https://github.com/mateo-cogeanu/ps5-java25-homebrew/tree/main/Dependency_Probe) |

The runtime now has **nine passing console milestones**, including inbound IPv4, verified HTTPS, IPv6 loopback/link-local LAN, 60-second external load, manifest-linked dependencies, actual system class-path loading and resident JNI calls. The first Minecraft-specific bootstrap probe also now passes on PS5. The current Java bootstrap uses interpreter mode, and JIT performance remains future work.

## Roadmap

### 1 · Prove the server foundation

- [x] Validate the Java runtime's TCP/UDP loopback and NIO selector probes on PS5.
- [x] Validate outbound Java LAN TCP/UDP and forward DNS on PS5.
- [x] Validate inbound LAN and multi-JAR/system class-path loading on PS5.
- [x] Pin official Minecraft 26.3 / Java 25 artifacts and inventory its 40 JARs.
- [x] Verify the inventory and official `--help` entry point on the host.
- [x] Pass the first Minecraft server bootstrap probe on PS5.
- [ ] Launch a vanilla dedicated server and reach a ready state.
- [ ] Create, save, stop and reload a test world.
- [ ] Connect from another device and verify sustained ticks and clean shutdown.

### 2 · Bring up the client

- [ ] Port the required native libraries and window/input interfaces.
- [ ] Establish a working rendering backend and audio path.
- [ ] Reach the main menu and load a vanilla test world.
- [ ] Add usable controller navigation and gameplay controls.
- [ ] Measure performance, memory use and stability on the console.

### 3 · Explore the mod ecosystem

- [ ] Validate Fabric and Forge separately for selected game versions.
- [ ] Check each mod's Java, native-library and graphics requirements.
- [ ] Test individual mods before attempting larger mod sets.
- [ ] Publish exact tested versions, results and reproducible builds.

## First server bootstrap probe

**Passing snapshot:** `PPSA99874`, version `01.000.002`. [Frozen source](Server_Bootstrap/server/native/bootstrap.cpp) · [Pinned artifacts](Server_Bootstrap/server/26.3.lock.json) · [Validation](Server_Bootstrap/validation.json)

Run all five rows in order:

1. Initialize the embedded Java runtime.
2. Create the Java 25 interpreter VM (128 MiB maximum heap).
3. Verify all 40 official JAR hashes, the server’s Java 25 bytecode and representative dependency/module classes.
4. Invoke the real, unmodified Minecraft 26.3 `net.minecraft.server.Main --help` and check its option-parser output.
5. Destroy the VM.

No Mac networking helper is needed. This build does not accept the EULA, generate a world, listen for players or establish server tick performance. Long exception messages wrap and support D-pad left/right paging.

The official server bundle is downloaded from Mojang’s metadata-pinned URL. Its SHA-1, size and SHA-256 are checked; each contained library/server JAR is checked against the bundle’s SHA-256 inventory. Game files remain in ignored caches and local packages, rather than source commits. See the [official 26.3 release](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3).

## Current development: server start probe 01.000.051

The five rows initialize the runtime, create a 160 MiB interpreter VM, check official artifacts, Java null recovery and vanilla asset ZipFS, start/save/stop a flat test world, and destroy the VM. Human EULA acceptance for this test is [recorded](server/eula-consent.json); the wrapper writes `eula=true` only when its explicit acceptance property is enabled.

The world and configuration live under the application-visible `/download0/mc-server-start`. The test preserves that directory across launches, writes its controlled low-distance server properties, listens on available interfaces without a preset IP, waits up to ten minutes for the real `Done` message, sends `stop`, awaits server-thread exit and reads the saved `world/level.dat`. Row 4 runs on a dedicated JNI-attached native worker with an 8 MiB stack. The menu redraws elapsed seconds while test selection and VM destruction remain disabled until the worker joins. The ten-minute readiness deadline starts after the synchronous server main method returns; it does not bound that initial call. The current host readiness/save/stop test passes at 160 MiB (earlier runs passed at 192 MiB); **PS5 server startup/save/stop remains pending**. Build 01.000.003 failed during JVM creation after a 64 MiB native reservation returned ENOMEM with its 256 MiB heap setting. A host attempt at 128 MiB exhausted Java heap during world generation. Build 01.000.004 also failed at JVM creation with an 80 MiB reservation failure. Build 01.000.005 retains the 192 MiB Java heap and includes a PS5 runtime adaptation: non-class metaspace reserves 16 MiB nodes instead of 64 MiB, growing through the existing allocator as needed. Build 01.000.005 now passes real VM creation at 192 MiB, official JAR checks and VM destruction on PS5. The server row then failed on `ServerStart25$Observer` lookup before execution. Build 01.000.006 puts all consumer probe classes in `ps5-server-probe.jar` on the system class path; the matching JNI lookup regression and real host readiness/save/stop test pass. The console memory limit and earlier signal cause remain unestablished. Build 01.000.006 executes the wrapper, but did not reach ready and exposed a partial Log4j initialization stack. Build 01.000.007 uses headless console-only logging and preserves error headings, cause chains, initial output and recent output separately. Native text capacity now holds the report instead of truncating it to 1.5 KiB. Its host readiness/save/stop and long-error diagnostic tests pass; the actual prior exception is not yet identified. This development build includes target-built `jdk.zipfs` for Minecraft datapacks, in addition to the bootstrap module set. It does not establish player-join support or sustained performance.

### Build and verify

With the pinned Java port/toolchain available:

```sh
python3 tools/package_server_probe.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/test_server_start.py
```

The preparation script creates the class-path header and external probe specification under `build/`. The Java repository supplies the reusable runtime builder and extra target-built Java modules. No host native binaries are included. Optional module natives and server-specific native dependencies still need console validation.

Install the complete `PPSA99874` folder from the generated ZIP through ShadowLoader. Keep any existing app closed while replacing files.

## Milestones & releases

| Minecraft milestone | Console result | Snapshot | Release |
| :--- | :--- | :--- | :--- |
| **Server Bootstrap · 01.000.002** | ALL PASS on PS5 13.60: VM lifecycle, 40-JAR preflight and official server `--help` | [Frozen source & validation](Server_Bootstrap) | [Download](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Server_Bootstrap-v01.000.002) |

The public release contains the console-tested app/runtime, with official game/dependency JARs excluded. To provision those, run `tools/prepare_server.py --runtime-workspace /path/to/PS5_Homebrew`, then copy the generated `build/assets/java25/jars/` into the extracted app's `assets/java25/jars/`. The regular packaging command above produces the full local app automatically. Exact full-package and release-asset hashes are recorded separately in [validation](Server_Bootstrap/validation.json).

Earlier build failures remain recorded in [console results](server/console-results.json). This milestone establishes bootstrap/help only. World creation, a ready dedicated server, player joins and sustained ticks are next.

## Follow the project

Runtime fixes and reusable tools are published to [ps5-java25-homebrew](https://github.com/mateo-cogeanu/ps5-java25-homebrew). Minecraft harnesses, artifact pins, preparation scripts and console results are published here. The current development probe attempts real server startup/save/stop with PS5 diagnostic compatibility; client and mod work follow their own prerequisites.

Build 01.000.007 reached block/registry initialization and reported an
OutOfMemoryError from the legacy verifier while checking JOML Matrix3f,
plus a separate logging configuration lookup failure. Build 01.000.008
uses an explicit 8 MiB code-cache reservation in interpreter mode, loads
the logging XML through the probe JAR URL, and includes native verifier
failure-site/errno/JNI-state diagnostics and Java heap counters. The host
server reaches ready/save/stop with about 1 MiB of code cache used. The
PS5 failure is not yet confirmed resolved.


## Download diagnostic logs (01.000.009)

Keep the probe open and visit **`http://<PS5-IP>:8765/`** from a browser on the
same LAN. Use the console's current IPv4 address; none is compiled into the app.
The menu shows listener status. This native service runs independently of the JVM
and serves the app's own files, avoiding FTP sandbox access restrictions. It stays
available while the server test is running. After a process crash, relaunch and
download the saved logs before running a new test.

Download **Startup log**, **Native VM trace**, **Full Minecraft console**,
**Last JVM abort**, and **Latest probe exception** as available. The Minecraft
console file is replaced per server attempt and capped at 32 MiB with an explicit
marker; the existing on-screen report remains bounded. Other logs retain their
existing append/truncation behavior. Missing files return 404.

To collect a ZIP with checksums, use the Java runtime workspace helper:

```sh
python3 /path/to/PS5_Homebrew/tools/fetch_probe_logs.py <PS5-IP> --output probe-logs.zip
```

The read-only page exposes only named logs, with no file browser, upload or
commands. It is unencrypted LAN access without authentication; keep it on the
intended network and do not forward port 8765. Nothing is uploaded automatically.
See the [runtime log-sharing documentation](https://github.com/mateo-cogeanu/ps5-java25-homebrew/blob/main/Development/docs/probe-log-sharing.md).

The downloaded 01.000.008 startup log confirms native verifier allocation failure
at site 3586 with no pending JNI exception, and a missing native `management`
library. These remain unresolved in 01.000.009; this build improves collection.
**PS5 log downloads and server readiness/save/stop remain pending.**


Build **01.000.009 log sharing is confirmed working by the user**; the downloaded
console identifies native verifier scratch allocation failure during
`Matrix3f.rotateLocal`, with 58,800,432 Java heap bytes still free. Build
**01.000.010** includes the Java port's PS5-only method-scratch lifetime fix:
non-root verifier scratch blocks are released at each method reset instead of
retaining oversized allocations until class verification finishes. All bytecode
checks remain active. The patched complete verifier validates Matrix3f, Matrix4f
and Quaternionf through host JNI, and a constrained allocator sanitizer test
passes 600 methods where the original retention exhausts its budget. The packaged
target library was rebuilt and verified byte-for-byte.

This addresses a demonstrated native allocation pattern; **PS5 resolution is
pending**. The missing native management library and unsupported optional OS
telemetry are separate remaining issues. No ready server or world save on PS5 is
claimed. Log sharing remains available on port 8765 in this build.


The 01.000.010 console logs show progress past Matrix3f verification, followed
by another native scratch allocation failure in `MemUtil$MemUtilNIO.copy4x4`
(site 3600, no pending JNI exception), with 58,020,336 Java heap bytes free.
Build **01.000.011** keeps method scratch cleanup and adds a PS5-only fallback:
if libc refuses a verifier pool block, request real anonymous read/write OS pages.
Each block records its allocation backend and is released with `free` or `munmap`
as appropriate. If both backends fail, the verifier still reports OOM; no checks
are bypassed. The startup log records requested bytes, malloc errno, mapped bytes
and mmap errno for fallback attempts, even with verbose native tracing disabled.

Host sanitizer checks cover forced heap rejection, writable real mappings,
matching cleanup and both-backend exhaustion. The complete patched verifier
checks the actual MemUtilNIO class as well as Matrix3f, Matrix4f and Quaternionf.
The target library was rebuilt and verified against the packaged copy.
**PS5 validation is pending.** Management-library and OS-telemetry warnings remain
separate unresolved issues; the server has not yet reached ready on PS5.


## Current fixes in 01.000.012

- **JVM management:** the real target `libmanagement` is embedded and connected
  to HotSpot's management interface. Preflight now queries actual heap/non-heap
  memory and VM input flags rather than only resolving the class name.
- **Verifier memory:** the method scratch cleanup and real OS-page allocation
  fallback from 01.000.011 remain included, with allocation diagnostics in the
  startup log. Console confirmation is still required.
- **PS5 system reports:** unsupported OSHI hardware/software readings are marked
  explicitly unavailable. The accurate PS5 OS identity and real JVM memory/flags
  are retained; no physical hardware readings are invented or warnings globally
  hidden. Full OSHI support is not claimed.

The last item is a narrowly scoped **Minecraft diagnostic adaptation**. The
original signed server JAR remains unchanged and hash-verified. A separate local
unsigned derivative executes with only the two optional `SystemReport` telemetry
methods adapted; every other server class/resource is byte-identical. Original
desktop behavior is retained. No global signature checks are disabled. The
execution artifact is therefore not described as an unmodified signed server.
See [scope, provenance, and validation](docs/platform-diagnostics.md). Generated
game artifacts, including the diagnostic derivative, are not committed or
published as binary release assets. The frozen bootstrap release is unchanged.

Host management, diagnostic adaptation, restricted-module preflight/help, and
real server readiness/save/stop checks pass. **PS5 testing remains pending** for
management, the verifier fallback and real server ready/save/stop. Use the log
page on port 8765 to collect results after the attempt.


## Class loading and log identity in 01.000.013

The latest console attempt reached MobEffects initialization, then reported a
bare OOM through `ClassLoader.defineClass1`. Its startup tail ended in VM ABORT;
the supplied exception file still described the older MemUtilNIO attempt.
Build **01.000.013** adds PS5-only native class-byte/UTF scratch allocation
fallback to real anonymous RW pages, with matching backend cleanup. Bytecode
checks and JVM definition entry points remain unchanged. Startup diagnostics
record allocation sizes/results and distinguish failure after entering the JVM.
The exact origin of the console OOM remains unproven until this build is tested.

The log page now separates **Open app build** (`build.txt`) from **Recorded run
status** (`session.txt`). Relaunching preserves the failed run's logs; these
identifiers can differ after a crash. Initializing a new run archives the prior
exception, VM abort and server output before writing current-run placeholders.
Prior reports have their own download links. Archive failure preserves the
current source report and is recorded in session status. Startup history has
explicit build/run markers, and the ZIP collector includes build/session files.

The actual native class-loader host test loads and executes classes using heap
and forced mapping paths, exercises hidden/direct definitions and long UTF
sources, and checks cleanup after malformed input, invalid ranges and real OOM.
Log archive/collector checks also pass. **PS5 validation and real server readiness
remain pending.** If it aborts again, include `abort.txt`, `session.txt`,
`startup.log` and `server.log`; the current exception file may correctly state
that no Java exception was captured before the process aborted.

## Native worker in 01.000.014

The user confirms build 013 exits the whole app during row 4. Its latest startup log shows successful class-byte scratch mappings, but no current abort report, server output or console crash code. Those mappings do not identify what terminated the app.

Build **01.000.014** moves the long JNI call off the UI thread and supplies a dedicated 8 MiB pthread stack. The worker attaches to the existing VM and owns its `JNIEnv`; the creating thread keeps its own environment. The Java fixture sets the system context class loader before server initialization. The UI hides worker-written result/exception buffers until completion and join, then enables subsequent tests. It shows elapsed seconds once per second while the worker is active. Read-only log sharing on port 8765 remains available.

The actual server fixture reaches `Done`, saves `world/level.dat` and stops on a native-attached host worker at 192 MiB; the main loop continues during that test. Target linking, package integrity and library/JAR identity checks also pass. **PS5 validation is pending.** This change addresses UI blocking and stack ownership, but does not establish the original crash cause or isolate native fatal errors from the process.

For the attached-worker host regression, first build the fixture runner with `python3 tools/test_jni_worker.py` in the runtime workspace, then run here:

```sh
python3 tools/test_server_start.py --worker-runner /path/to/PS5_Homebrew/build/java25/jni-worker-test/jni-worker-check
```

Build 014 console follow-up: the user reports a whole-app crash at 19 seconds. Retrieved logs confirm worker attachment and contain a current signal 11 record matching the 014 handler address. The server console is empty, the current exception remains a placeholder and the abort endpoint is unavailable. The exact native fault site remains unresolved; this build has **not** passed startup/save/stop on PS5. Raw diagnostic files remain local.

## Native crash capture in 01.000.015

Build **01.000.015** repairs the missing native-call evidence in row 4. The harness previously disabled call tracing before invoking the server. It now uses quiet mode: caller, pointers, byte count and completion status remain in memory without per-call disk writes. Allocation wrappers also cover calloc, realloc and free while preserving the original functions.

The runtime stores call/stage/recursion state separately for each thread in a preallocated table. This prevents cross-thread overwrites without using allocating emulated TLS in an allocator wrapper or signal handler. Table exhaustion suppresses new capture and leaves existing records intact. The attached worker, live elapsed counter and read-only log sharing remain.

Host sanitizer tests, target code checks, the HotSpot rebuild and package integrity checks pass. **The underlying build 014 SIGSEGV is still unresolved; build 015 is awaiting PS5 validation.** It does not claim a completed native crash fix. Repeat the test sequence, then leave the probe open on its menu after relaunch so the current logs can be retrieved.

Build 015 console follow-up: quiet capture now records a completed 128-byte native malloc returning null. The retained caller resolves to HotSpot `os::malloc` in the matching 015 ELF. The same subsequent SIGSEGV remains, with no Java exception and an empty server console. This identifies an allocation failure, but does not establish the reason it failed or the later faulting instruction. Actual server startup/save/stop has not passed.

## Native allocation fallback in 01.000.016

Build **01.000.016** includes a Java runtime fix for the confirmed failed 128-byte HotSpot allocation. When libc refuses native storage, HotSpot now falls back to real writable anonymous OS pages. Small allocations share mappings through eight size classes; larger ones use direct mappings. Backend-aware resize/free preserves existing bytes on failure and releases mappings when no longer needed. The raw storage prefix also covers early NMT allocations so they remain compatible after initialization. Existing native-memory tracking checks and the 192 MiB Java heap setting remain.

The actual allocator passes sanitizer tests with forced failures, resize migration, alignment, pooled sharing, concurrency and complete cleanup. The actual HotSpot API bodies also pass checks against a narrow NMT contract model, including failed-resize header revival and allocation limits. Target rebuild and package/library identity checks pass. **PS5 validation is pending:** this addresses the observed allocation failure, but does not yet prove the subsequent SIGSEGV or server startup/save/stop is resolved.

## Bulk file-I/O buffer fallback in 01.000.017

Build 016 logs confirm successful HotSpot native-page fallbacks, then report
`OutOfMemoryError` in `RandomAccessFile.readBytes0` while loading a dependency
JAR. Its trace has no captured signal record and no abort report; this does not
prove the prior native crash is resolved. Server readiness/save/stop has not passed.

Build **01.000.017** consumes a separate Java runtime fix for bulk file-read/write
temporary buffers: libc first, then real writable OS pages, with matching
cleanup even after partial writes and exceptions. Both allocation failures
still produce the original error. JNI/UBSan host checks and target/package
checks are recorded in [build status](server/build-status.json).
**PS5 validation of build 017 remains pending.**

## Native platform strings in 01.000.018

Build 017 confirms the file-I/O mapping fallback works, then fails in
`FileInputStream.open0` while Java logging loads its configuration. The error
"requested array size exceeds VM limit" comes from a failed native platform-string
allocation and can occur for a normal-sized path. Build **01.000.018** consumes
the Java runtime's platform-string fallback: libc first, then real OS pages,
with matched normal/error cleanup and unchanged encoding/NUL checks.
The JNI/UBSan host checks and target/package validation are recorded in
[build status](server/build-status.json). **PS5 validation remains pending**;
no successful world readiness/save/stop or resolution of prior native crashes
is claimed.

## Verifier class-hash memory in 01.000.019

Build 018 logs confirm successful platform-string/file-I/O mappings, then
report verifier OOM at class-hash initialization for `org/joml/Matrix3fc` and
a separate native SeedGenerator thread-creation failure. Build **01.000.019**
extends the runtime fallback to all verifier-owned native allocations,
including the class-hash calloc arrays and their matched cleanup. Complete
host verifier checks pass with libc allocation refused and with mapping
failures injected during initialization. Thread creation now logs its exact
failure stage/return code; **the seed-thread cause remains unresolved**.
PS5 server readiness/save/stop and clean shutdown remain pending.

## Thread attributes and metaspace alignment in 01.000.020

Build 019 identifies the seed-thread failure as `pthread_attr_init` returning
ENOMEM before thread creation. Later native reservations fail while trying to
align another metaspace region, followed by a signal crash; the subsequent
fault's causal chain remains unproven. Build **01.000.020** consumes two Java
runtime fixes: a bounded, exclusively leased pool of real thread-attribute
objects initialized early, and exact-size non-replacing aligned mapping hints
before the larger metaspace reservation attempt. Security seed behavior,
verification and the 192 MiB Java heap setting remain.

ASan/UBSan host checks cover actual pthread creation/reuse and safe host mappings;
target/package checks are recorded in [build status](server/build-status.json).
**PS5 thread success, crash resolution and real server ready/save/stop remain
pending.** No completed Minecraft server milestone is claimed.

## Crash evidence and diagnostic overhead in 01.000.021

The user reports build 020 crashed and was reopened. Its logs confirm a
successful exact-size aligned metaspace reservation, but contain no captured
signal/abort and no server console output. The cause remains unrecorded.
Build **01.000.021** is a diagnostic build: routine metadata disk tracing is
sampled while every last-stage update remains in memory; native call tracing
uses quiet mode throughout VM/server execution. It adds thread startup phase
markers and a fixed-name HotSpot fatal report linked as `hs-error.log` on the
log page. Reports are archived before a new run; relaunch preserves them.
A report is available only if HotSpot generates it. Host/target/package checks
are recorded in [build status](server/build-status.json).
**The crash is unresolved; PS5 server ready/save/stop remains pending.**

## Stack discovery and thread initialization in 01.000.022

The 021 crash trace records successful native thread creation and child entry, then stops before stack recording/current-thread setup finishes. No signal or fatal report was saved. The remaining fresh attribute allocation in stack discovery now uses an early initialized query pool, separate from creation attributes so live stack addresses cannot contaminate new threads. Actual OS stack queries and real failures remain in place. Intermediate stack/TLS markers narrow any continuing failure. Host sanitizer stress and target compilation pass; **022 console validation and actual server ready/save/stop remain pending**. The exact 021 fault is unproven.

## Current-thread TLS in 01.000.023

The 022 trace confirms stack discovery succeeds, then the new child stops between compiler TLS assignment checkpoints. This target uses compiler TLS emulation, which may allocate on a thread's first access. Build 023 removes that dependency for HotSpot's current-thread pointer and uses its existing native pthread TLS backend, including guarded pre-init lookups and JNI destructor semantics. Host sanitizer tests cover 1600 concurrent initialization/clear cycles and signal lookups; target IR checks native key access without compiler TLS emulation. The trace provides no exact crash PC; **023 console validation and actual server ready/save/stop remain pending**.

## Native key failures and crash evidence in 01.000.024

Build 023 passes native TLS setup, handshake and Java thread entry before a later SIGSEGV. Its saved JVM fatal report is useful, but the reported registers are inconsistent; no exact crash location is established. Build 024 fixes ignored native key update failures in product builds: checked return/readback, a bounded allocation-free override for failed updates, explicit null on refused clear, and destructor handling that cannot resurrect a detached Thread. Normal native TLS remains the primary path. The fallback supports 1024 distinct failed thread identities per process and fails explicitly on exhaustion. New diagnostics record any actual key refusal and raw signal context without changing ABI offsets. **Native-key failure as the 023 cause, crash resolution, and real PS5 server ready/save/stop remain unconfirmed.**

## Direct native termination diagnostics in 01.000.025

The 024 console log confirms native pthread TLS returns ENOMEM and the fallback lets affected threads enter Java and later clear/return. The later whole-app crash produces no signal or current fatal report. Build 025 adds direct linked `abort`/`exit`/`_exit` hooks that save caller/status and previous native context, then preserve original termination behavior. This is a diagnostic build; kernel kills and calls internal to separately loaded modules can still bypass the hooks. **The later crash cause and real PS5 server ready/save/stop remain unconfirmed.**

## Progress and resource logs in 01.000.026

The 025 capture has no native termination or fatal signal marker, so the exact cause remains unknown. Its current startup log contains 272930 verifier mapping messages (over 21MiB). Build 026 samples repetitive successful messages while retaining mmap failures; allocation/verification behavior is unchanged. The log page adds **Class loading progress** and **Native resource samples**, archived on a new run. Native samples use actual OS getrusage without JNI and report raw counters or an explicit query error. Raw maximum RSS is not available memory or a proven container limit; the last loaded class is progress evidence. **All PS5 rows, diagnostic evidence and real server ready/save/stop remain pending.**

## Compiler TLS allocation repair in 01.000.027

Build 026 crashed after approximately 46 seconds. Its native termination trace and matching executable identify an abort in compiler-rt's emulated TLS setup after a 128-byte address-array allocation returned null. Build 027 uses the Java project's scoped compiler-TLS allocator adapter: libc first, then actual OS RW pages, with matched growth and release. The Java heap remains 192 MiB. This fixes the confirmed allocation path; console execution must establish whether later startup succeeds.

The harness also honors the JVM print hook's requested FILE stream. Build 026 redirected class-loading output into startup.log and left class-load.log empty; build 027 preserves separate class/fatal log files while retaining console capture. Resource samples remain available. Compiler-TLS native key update failures now have a distinct diagnostic marker; its setter semantics are unchanged, so a refusal remains a separate issue. **All five rows and real server readiness/save/stop require PS5 testing.**

## Compiler TLS key retention in 01.000.028

Build 027 confirms that mapped TLS allocation works, but its native key setter returns ENOMEM. That loses the storage pointer and repeats allocation: 247 refused key updates and 495 mappings precede another compiler-rt abort. Class loading is now captured separately as intended.

Build 028 pins a Java runtime repair that retains compiler-rt's canonical array independently of the native setter. Native destructors use the current array instead of a potentially stale native pointer. Thread creation/join adapters reclaim retained storage after actual thread death, with generation checks protecting reused identities. A detached or unjoined thread with refused native registration retains its array until identity reuse or process exit. Host sanitizer tests cover real pthread destructor order, stale pointers, concurrent isolation, failure paths and cleanup. The heap remains 192 MiB. **All five PS5 rows and actual server ready/save/stop remain pending.**

## Verifier repair and synchronization checks in 01.000.029

Build 028 closed around 20 seconds. The capture ends during a child thread's startup handshake; no signal, abort, fatal report or Java exception identifies the fault. Class loading reached JOML Matrix4x3f. Testing that class with the actual verifier reproduced signed-shift undefined behavior, now corrected by the Java runtime. That finding does not prove the PS5 crash cause.

Build 029 also records native synchronization errors in the product VM instead of compiling those checks away, and adds parent/child monitor-handshake checkpoints. Host sanitizer regressions cover the verifier, decoding boundaries and failed native synchronization initialization. The Java heap remains 192 MiB. **The crash cause, all five PS5 rows and actual ready/save/stop remain pending.**

## Native synchronization allocation in 01.000.030

Build 029 captured `pthread_mutex_init` returning ENOMEM, followed by a signal during fatal reporting. No Java exception or completed fatal report was captured. Build 030 uses the Java port's bounded early pools of real native mutexes and conditions, with exclusive stable-address leases and separate relative/absolute clock attributes. Exhaustion still attempts real native initialization and preserves failures. The Java heap remains 192 MiB. Host sanitizer checks pass with late initialization refused, native wait/signal/timeout behavior and 8,000 concurrent lease lifetimes. **All five PS5 rows and actual server ready/save/stop remain pending.**

Build 030 target compilation, signed-container integrity, ZIP checks and target-library identity checks pass. Package SHA-256: `04abef711724a49249dbf306f5bcba32f3dc7c49d70a561c4ff2c40852c24bca`. PS5 testing remains pending.

## Mutex reserve follow-up in 01.000.031

Build 030 initialized every early pool entry successfully, but still closed after a later mutex-init ENOMEM. Its capture does not record pool occupancy or identify the constructor. The generated-class workload can require additional metadata locks, making the 512-mutex reserve a plausible bottleneck. Build 031 expands the runtime mutex reserve to 4096 and reports exact pool occupancy, attribute matching and caller on native init failure, plus distinct event/parker/monitor labels. Condition capacities and the 192 MiB Java heap are unchanged. Host sanitizer checks cover all 4096 entries, exhaustion/reuse, incompatible attributes and the actual emitted failure fields. **This is a capacity adjustment and diagnostic build; PS5 server ready/save/stop is still unvalidated.**

Build 031 target compilation, signed-container integrity, ZIP checks and target-library identity checks pass. Package SHA-256: `5817e19dfe2405a911d70e5cc9db031ef341b1249470243efd85835952b66a43`. PS5 testing remains pending.

## Condition reserves in 01.000.032

Build 031 initializes all 4096/512/256 native primitives and reaches 12,884 class records, compared with 4,245 in build 030. Its later failure is native condition initialization ENOMEM; no mutex fallback failure is recorded. Build 032 expands relative/absolute condition reserves to 4096/2048 and records occupancy, requested clock domain and caller on failed native initialization. Event/monitor condition checks have distinct labels; parker retains relative/absolute labels. Mutex capacity 4096 and Java heap 192 MiB remain. Host tests cover each full condition reserve, exhaustion/reuse and the actual failure fields. **PS5 startup/save/stop remains unvalidated; condition-pool exhaustion is not established by the 031 capture.**

Build 032 target compilation, signed-container integrity, ZIP checks and target-library identity checks pass. Package SHA-256: `8e758fd3d6c76419b48d7f5913ae5bc907b626fca3d30374016439f76c78ae33`. PS5 testing remains pending.

## World metadata blocker in 01.000.033

Build 032 reaches the official server's world-directory validation, which fails reading `/download0/mc-server-start/world` attributes with Operation not permitted. The pinned server bytecode uses `NOFOLLOW_LINKS`. The native trace records no synchronization-init failure in this capture; a later signal occurs on another Java thread, whose exact crash cause remains unresolved.

Build 033 pins the Java port's nofollow descriptor-metadata repair: genuine file/directory attributes and missing-path errors, while final symlinks remain rejected when native lstat cannot describe them. The official validator is unchanged. The harness checks the required root/world metadata operation before loading Minecraft, allowing an early contextual failure. Shared exception/session reports use descriptor IO, with write failures recorded in the native trace. Heap and synchronization reserves are unchanged. **All five PS5 rows, actual ready/save/stop and resolution of the later native crash remain pending.**

Build 033 target compilation, signed-container integrity, ZIP checks and target-library identity checks pass. Package SHA-256: `d808a0cdd89f0828eb6265ea5bd4d265f7cf1405e93caf37df5c7b91995fe9f2`. PS5 testing remains pending.

## Signal recovery and vanilla assets in 01.000.034

Build 033 passed the earlier world metadata blocker, then reported native realpath EPERM while mounting the vanilla asset JAR. The complete native trace also exposed a signal ABI mismatch: HotSpot read a stack address as the interrupted PC because the SDK outer context lacks 48 reserved PS5 bytes. Runtime patches correct register reads and continuation writes, and add a descriptor-verified path fallback after EPERM. Link-dependent paths remain refused when native realpath cannot resolve them; the official game validator is unchanged.

Build 034 adds early preflight checks that catch a Java null access and mount/read the actual vanilla asset JAR through ZipFS. Its log page offers a compact startup tail (last512KiB), preserving full historical downloads. Host replay, actual JNI/ZipFS tests, HTTP tests, target compilation and package integrity/library checks pass. **Live signal recovery, all five console rows and actual ready/save/stop remain pending.** Heap remains192MiB. Package SHA-256: `848e02fc6672db599c851cfdd5045eee2a0a533335afb04808d1299ea2a4b7b1`. No new passing milestone is claimed.

## Null preflight crash in 01.000.034

Build034 crashes during the deliberate Java null check in row3, before verifying JARs or mounting assets. The console confirms corrected interrupted-PC reads, but no continuation is recorded. The inherited FreeBSD signal handler queries desktop kernel stack-gap controls before exception handling; disassembly confirms the linked procctl uses a raw desktop syscall. The exact terminating instruction is still unknown.

Build035 excludes that desktop-specific workaround on PS5 while preserving JVM stack guards and normal exception selection. Additional checkpoints narrow any remaining failure to stack triage, state/interpreter classification or continuation selection. The null preflight stays enabled. Actual-block host regressions and the target rebuild/package checks pass; **PS5 exception recovery, all five rows and real server ready/save/stop remain pending**. Package SHA-256: `17d71f2c4a4fe50407670a2ca46fdbfab3ffbfc5f90f4a38eeefba24bcc2572a`.

## Signal recovery confirmed; asset lookup in 01.000.036

Build035 confirms normal implicit Java null exception recovery on the PS5 and passes all40 pinned JAR checksum stages. It then crashes in the combined vanilla asset canonicalize/mount stage without a subsequent signal record. The new register layout and desktop stack-gap exclusion therefore have direct console evidence, but a full server pass is still unestablished.

The previous path fallback called an SDK openat function that issues a raw desktop syscall. Build036 pins a runtime repair that verifies each unelided path component with resident open/close, refusing link-dependent fallback paths and preserving actual errors. Optional desktop directory-at capabilities are no longer advertised on PS5; a secure anchored directory backend remains unported. Native realpath/fallback/component checkpoints and separate canonicalization/mount/read/close stages narrow any next failure. Heap remains192MiB.

Actual host JNI/ZipFS tests, capability checks, target compilation and package integrity/library checks pass. **All five PS5 rows and actual ready/save/stop remain pending.** Package SHA-256: `dfe1565747b98ffa1bed235c38bb8ca72fe57fc2281040bba729861afd40f772`.

## Java failures without app termination in 01.000.036

Build036 survives both verification and server-start failures, with the log service still available. The asset JAR canonicalization completes. Verification then reports EPERM during ZipFS mounting; server startup reports EPERM enumerating the existing world through the official DirectoryValidator. World readiness/save/stop remains unestablished.

Build037 pins resident libkernel directory enumeration with bounded record parsing and actual errors, plus descriptor-based read/write access checks after native EPERM. Execute/search permissions are never inferred; official world validation remains unchanged. Preflight separates readable-access, actual directory iteration and ZIP mounting. Verification and server exceptions now have separate links on the log page, preserving both when subsequent tests run. They are archived/reset for an explicitly initialized new run and retained on relaunch.

Host actual JNI/directory/ZipFS tests, malformed-record sanitizer tests, HTTP/archive checks, target compilation and package checks pass. **All five PS5 rows and real server ready/save/stop remain pending.** Package SHA-256: `f081c082bdc1a1f0c872935207cc21756e8a3ccde37e8bbb80f651d58f1ba343`.

## Directory ABI and native compression in 01.000.038

Build037 confirms readable asset access and canonicalization. Verification fails directory iteration with Invalid argument. The server reaches datapack loading, then native Inflater.init throws OutOfMemoryError through compressed ZipFS input. This is a native allocation path; the Java heap still reports free space. Minecraft service discovery also reports a separate DNS failure, which remains unresolved. Independent verification/server reports are now captured successfully.

Build038 tries the alternate resident directory API only after an initial unsupported-call response and successful rewind, with no entries delivered; it never replays after delivery. PS5 Inflater/Deflater stream and private zlib allocations gain a libc-first mapped fallback with overflow checks and matched cleanup. Both backends failing remains genuine OOM. Preflight now checks a real native compressed roundtrip before assets. Heap remains192MiB; authentication, game code and archive checks remain intact.

Actual JNI/zlib/ZipFS and sanitizer tests, target compilation and package checks pass. **All five PS5 rows, actual server ready/save/stop and the discovery DNS result remain pending.** Package SHA-256: `12dbc7f95c20837c314af3950e7c5780e8eb956f089fadcb8b564ee850985e25`.

## Native crash evidence in 01.000.039

Build038 fails directory verification with Invalid argument after the early compression check, and the user reports a whole-app crash59seconds into server startup. The saved trace records a native-state signal with PC and fault address0x100026c946 outside the app image, then another signal during error handling. The prior completed memset record is not the faulting call. No completed fatal report or native caller stack was available. The server page begins with discovery DNS failure; full server/startup files could not be saved this turn.

Build039 separates directory bytes into a dedicated page-aligned64KiB mapping and records which directory API enters/retries/fails. This removes a buffer-layout assumption; alignment/size is not yet proven the cause of EINVAL. New signal diagnostics sample saved stack words and monotonic frame links within the actual thread bounds, with nested-signal sampling skipped. They are bounded best-effort evidence, not protection from every corrupt/unreadable stack page. **The native crash cause remains unresolved; this is a diagnostic development build.**

Host sanitizer/target-code tests, target rebuilds and package checks pass. All five PS5 rows, directory enumeration, native caller capture and real ready/save/stop remain pending; DNS remains separate. Heap stays192MiB. Package SHA-256: `f6c68ef2fcadbcccb7f6547f79af1b5ee0ecfd2f92e760e015b1ae419cb2f506`.

Build039 console update: verification now **passes on PS5**, but flat-world startup still crashes. The reopened session records a native VM abort for run `01.000.039-1792229683-675501422`. The full native trace has not yet been retrieved because Firefox’s Save dialog is disabled; the caller and a repair remain unresolved. This establishes verification progress only; server readiness, save and stop remain unvalidated.

## Native OOM and fatal-reporting repair in 01.000.040

Build039 verification passes on PS5. Its saved native frame chain identifies a native allocation failure in the class dictionary, followed by a signal in the desktop core-path query during fatal reporting. Small allocations were refused64KiB slabs; the console memory limit remains unknown.

Build040 pins a runtime repair that reports no desktop core path on PS5, allowing normal fatal reporting to continue, and retries a minimal real mapped slab when the64KiB request is refused. If both mappings fail, native OOM remains a real failure. Actual-body host sanitizer tests and target compilation pass. **PS5 startup, real readiness/save/stop and failure-report survival require retesting.** No heap increase or game validation changes are included.

The subsequently saved039 trace confirms native OOM followed by a current-directory query fault during fatal reporting. Build040 package SHA-256: `42caf2dc57df38b7b8348f3bafdcda0abb0c8f4c81391b1a92d05d5560e17502`. Console results remain pending.


## Build040 console failure and build041 follow-up

The user reports a crash on flat-world startup in040. Retrieved current-run
reports identify `01.000.040-1792230582-556842474`. The server console reports
`OutOfMemoryError: PS5 class-byte scratch allocation failed (malloc and mmap)`
while defining a command lambda during datapack loading. A later native request
for8256bytes fails its16384-byte mapping with ENOMEM, then the VM aborts. This
trace has no signal marker; the previous secondary fatal-query crash did not
recur in this capture. Native resource capacity and the final allocation site
remain unknown. The last resource sample is58s, `maxrss_raw=504352`; its units
and the console's limit are not inferred. Service discovery also still reports
`UnknownHostException`. No ready/save/stop milestone passed.

Build041 supplies explicit flat-world biome/layers, correcting the independent
`No key layers in MapLike[{}]` configuration error. Server-thread lookup now
enumerates platform threads without requesting every thread's native stack
trace during readiness/failure cleanup. This removes avoidable native work;
it does not establish that stack collection caused the abort. The runtime pin
adds raw native fatal size/file/line/type/detail diagnostics before the full
error reporter. Heap size, online authentication and official datapack checks
are retained. Existing worlds are preserved; generation settings apply when
creating a world.

Host tests pass for a real Done/stop/saved level.dat run at192MiB without the
missing-layers error, plus absent/live/exited thread lookup with more than64
threads. Runtime fatal-entry ASan/UBSan contract test and target build pass.
**Build041 remains an experimental follow-up: PS5 native resource exhaustion,
all console rows and actual readiness/save/stop require validation.**

Build041 package SHA-256: `d95e4458cc35bf2cd3009bbaca15268a3c4b9df10c98e7157538c93d7bb90df2`.


## Build041 console failure and build042 allocator mitigation

The current-run reports for `01.000.041-1792232186-809546025` confirm a failed
16-byte native AllocateHeap request. Both64KiB and minimal16KiB slabs were
refused with ENOMEM; fatal-site tracing identifies `allocation.cpp:42`. A second
16-byte fatal request and24-byte refusal precede VM ABORT/_exit1, without a
captured signal. The startup tail also records a failed433-byte class scratch
allocation. The server reached new-world creation without the previous
missing-layers error, but never reported Done. Discovery DNS remains unresolved.
Last resource sample:57s, `maxrss_raw=504576`; units and process limit remain
unproven. Raw logs are retained locally.

Build042 pins a runtime mitigation: after mapping refusal, a small allocation
may borrow an available slot from a larger compatible size class. Ownership,
free/realloc behavior and real exhaustion failure are preserved. Complete
failure now records mapped bytes/live/free slots for each fallback class.
These counters cover fallback slabs only. Build041 does not establish that
compatible spare slots existed at its failure; this addresses a concrete
allocator limitation and needs console evidence for its effect. It is not a
confirmed fix for overall native exhaustion. Heap remains192MiB.

Actual-header ASan/UBSan tests pass for forced mapping refusal with larger-slot
reuse, exhaustion, owner-first release, undersized-slot rejection, failed resize
and concurrent lifetimes; os.cpp/NMT contract-model checks and target build pass.
The consumer Java harness is unchanged from the host-tested041 source.
**All042 console rows and real server readiness/save/stop remain pending.**

Build042 package SHA-256: `3005ff93a3d8098148e3232e6419480877a293ada83381959d805abd94332a48`.


## Build042 returned failure; build043 class scratch mitigation

The human reports042 failed at58 seconds without crashing. Current-run session
`01.000.042-1792232967-506149971` records a returned server-row FAIL. The server
console still identifies class-byte scratch OOM while generating an ExecuteCommand
lambda during datapack loading. Its native trace records115 successful compatible
larger-slot borrows, then normal worker return, with no captured fatal OOM,
VM ABORT or signal marker. The short server-exception report is BootstrapMethodError;
it does not supersede the detailed console cause. No ready/save/stop pass.

Build043 pins a PS5 runtime change that uses a bounded4KiB native stack buffer
for small byte-array class definitions, including hidden generated classes.
Larger files retain libc/mmap scratch and genuine allocation failure. JNI copying,
range checks, JVM class definition and bytecode verification remain enabled.
Each active definition uses4KiB more stack; recursive stack demand and later
metadata/native exhaustion remain console concerns. Heap192MiB and worker8MiB
stack are unchanged. This removes the observed temporary-buffer mapping need,
not a claim that the native resource limit is solved.

Actual ClassLoader.c JNI tests with UBSan and full host bytecode verification
pass small ordinary/hidden classes with BOTH backends denied, large heap/mmap
success and OOM, zero/4096/4097 boundaries, malformed/range cases, long UTF
source and direct-buffer cleanup. Target build passes. **All043 PS5 rows and
real readiness/save/stop remain pending.** Discovery DNS remains unresolved.

Build043 package SHA-256: `f523a0dceb4fc068fcee45af35dd6a3304b30c396c7751a42b3be92eb6bf761c`.


## Build043 medium class scratch failure; build044 reusable storage

The user reports043 failed without crashing. Live session
`01.000.043-1792234015-586564080` confirms a returned server-row failure.
Its saved console advances beyond the earlier lambda-definition failure to
`ExecuteCommand.addConditionals`, where an ordinary class triggers class-byte
scratch OOM. The startup tail records20257bytes with a refused32768-byte mapping
(ENOMEM). The wrapper then reports a Java fixture exception; server readiness,
save and stop did not pass. Full native trace was not retrieved for this run.
The separate discovery DNS failure remains.

Build044 pins four exclusive reusable32KiB scratch leases in the PS5 classloader.
Libc remains first; after refusal, eligible requests try an atomic lease before
mmap. Pool exhaustion and >32KiB requests retain real mmap and OOM behavior.
The4KiB local small-class buffer remains. This adds about128KiB fixed BSS plus
headers; recursive/concurrent definitions cannot share an active lease. Normal
JNI copy/range checks and JVM verification are retained. Native resource limits,
BSS backing on console and later metadata exhaustion remain unproven.

Actual-helper ASan/UBSan tests cover simultaneous20257-byte leases, exclusivity,
exhaustion, actual mmap fallback, size boundaries, reuse and concurrent ownership.
Actual JNI UBSan/full-verification tests execute medium ordinary/hidden classes
with both backends refused and retain >32KiB allocation/OOM checks. Target build
passes. **All044 PS5 rows and real readiness/save/stop remain pending.**

Build044 package SHA-256: `9c617614a4f4e2627521e255181d9319574848e7bc8f9542f4701c8c75e91bd9`.


## Build044 native arena abort

The user reports044 crashed and relaunched. Current saved run
`01.000.044-1792234674-244574062` records VM ABORT. The full native trace
identifies a32752-byte allocation refusal in `arena.cpp:186`, `Chunk::new`;
the raw backend requested49152 mapped bytes and received ENOMEM. The process
then aborts and exits1, without a captured signal marker. Saved server output
ends at new-world creation, without a class-byte scratch OOM or real Done.
This does not establish scratch-pool success or its causal role; overall native
capacity remains unknown. Discovery DNS remains unresolved.

The allocator adds a32-byte ownership header. The near32KiB arena request
therefore crosses a16KiB page boundary and needs48KiB. Runtime patch0071
increases the PS5 arena sizing allowance so a default chunk plus real Chunk,
raw header and optional NMT overhead fits32KiB. Existing growth, ownership,
alignment and real OOM propagation remain. This corrects measurable page
waste without establishing sufficient total console memory.


Build045 reduces only the default arena payload by88 bytes so its allocation
fits32KiB including backend/tracking overhead. Tiny/initial/medium sizes remain
unchanged. A target static assertion checks actual layouts. Actual allocator
and os.cpp API sanitizer tests use the exact arena enum, a Chunk layout/NMT
contract model and16KiB pages: the revised request succeeds with a32KiB mapping
cap and the old32752-byte request fails. This is host evidence, not a console
pass. Heap192MiB, worker8MiB and prior scratch fixes remain unchanged.
**All045 PS5 rows and actual ready/save/stop remain pending.**

Build044 resource measurements end58s at `maxrss_raw=504784`; units and the
console memory limit are not inferred. The arena overhead correction does not
establish that overall native exhaustion is solved.

Final target rebuild and package checks pass. Initial compile was restarted after
a source-header edit invalidated its precompiled header; the final rebuild passed.
Build045 package SHA-256: `f59d9ffedfc4e1e9548b01dc18bf4c8f430997ef4be93dc0e20a38f599d6d754`.


## Build045 saved read failure and build046 bounded native reads

The human reports045 crashed and relaunched. Preserved session
`01.000.045-1792235749-802431410` instead records a returned server-row FAIL;
its full saved native trace ends at a Java fixture exception without VM ABORT,
fatal OOM or native termination markers. Saved SIGNAL records select and resume
implicit-null continuations. These reports do not explain a later app exit or
disprove the human report; that discrepancy remains unresolved.

Firefox inspection of the current server.log tail identifies datapack-loading
OOM at `RandomAccessFile.readBytes0`, through ZipFile/Inflater fill and JAR class
loading into `Commands.<init>:236`. Full server-log saving was disabled; the
local cause record is a transcription of the visible tail, not a raw download.
The short exception file cannot format its Java text. Real Done/save/stop did
not pass. Overall native capacity and discovery DNS remain unresolved.

Build046 pins PS5 readBytes to the existing8KiB stack buffer after validating
the original full caller array slice. It returns one genuine short read;
Java stream/readFully callers continue from the returned count. This removes
large bulk-read scratch allocations without changing writes, increasing stack
size, pinning Java arrays or bypassing class/ZIP checks. More native read calls
may be needed. The earlier arena sizing and class-scratch changes are retained;
heap192MiB and worker8MiB remain unchanged.

Actual JNI-body UBSan/-Xcheck:jni tests pass full-content short-read loops,
EOF/null/bounds/closed/error paths and unchanged write allocation/OOM cleanup.
Real host RandomAccessFile.readFully and ZipFile reads also pass with the actual
capped body installed in that test process and both storage backends refused.
Target rebuild passes. **All046 PS5 rows and readiness/save/stop remain pending.**

Build046 package SHA-256: `bf498ad48ca257bd9ed5550e25e3b3248cbcb39392215ac7edd44a366cb7d3b7`.


## Build046 exhausted slabs; build047 lower Java heap budget experiment

The human reports046 crashed/relaunched. Saved session
`01.000.046-1792236273-725851607` confirms VM ABORT. Its full native trace
identifies a160-byte AllocateHeap failure at `allocation.cpp:42`. At failure,
all eight fallback classes have zero free slots, with21905408 mapped bytes and
184103 live slots. Later24/16-byte refusals and a second fatal OOM precede
abort/exit1. These figures measure fallback slabs only; they do not establish
total native usage, the process limit or a memory leak. The visible server tail
ends at new-world creation; full Save was disabled. No Done/save/stop pass.

The current host flat-world harness passes real readiness/save/stop at160MiB
in interpreter mode. Build047 therefore tests a smaller Java max heap ceiling,
160MiB instead of192MiB, while retaining the same runtime pin and all prior
fixes. Initial heap16MiB, worker stack8MiB, code cache8MiB and two processors
are unchanged. The32MiB ceiling reduction is a controlled budget experiment,
not a claim of32MiB additional available native storage. It may trade native
pressure for Java heap exhaustion or more GC; actual PS5 benefit is unproven.
The historical128MiB host OOM remains recorded and is not contradicted by this
160MiB run. No additional runtime allocator change is included.

**All047 PS5 rows and real readiness/save/stop remain pending.** Discovery DNS
and overall native resource capacity remain unresolved.

Build047 package checks pass; SHA-256: `bb7193b2526bdb77b04c91af81f6f82a6750dfe2a014a061f9bbd690b229bb90`.


## Build047 external-address signal; build048 native-preparation diagnostics

The human reports047 crashed/relaunched. Preserved run
`01.000.047-1792245216-254595165` remains marked RUN server worker, while its full
native trace ends in an unresumed SIGSEGV at `pc=fault=0x100026c946` with thread
state4 (native). There is no captured native fatal OOM, VM ABORT or termination
marker. The handler anchor matches the exact retained047 ELF with load offset
`0x400000`. Raw stack words map into native-call preparation, interpreter/link
resolution and class initialization; they do not establish the active callee.
The top resident-library return/external target are not symbolized. The full
server console ends at new-world creation. Discovery DNS remains unresolved.
No ready/save/stop pass; lower heap benefit and total capacity remain unproven.

Build048 retains160MiB and adds runtime diagnostic checkpoints before native
preparation, after lookup and after signature handler installation. Bounded
stack formatting records holder/name/signature, thread identity and resolved
native address without Symbol string allocation. Native lookup/signature
behavior remains unchanged. Preparation is not a complete invocation trace:
a previously prepared native method can run again without a new event, and
nested preparation may replace the latest context. This is a diagnostic build,
not a confirmed repair for the external-address fault.

Actual formatter ASan/UBSan tests and target build pass. **All048 PS5 rows,
trace usefulness, native fault resolution and readiness/save/stop remain pending.**

Build048 package checks pass; SHA-256: `c4b44bf6871d7c8023b7cb8c8a8c09a4bced523e5b5139e616bc51619cc0a74a`.


## Build048 identifies JFR default-directory query; build049 repair

The user reports048 crashed/relaunched. Run
`01.000.048-1792246886-523251605` remains marked RUN; the full downloaded trace
captures an unresumed native signal. Its latest same-thread native preparation
is `jdk.jfr.internal.JVM.setDumpPath(String)` with target0xa2f590. Exact048 ELF
symbols confirm the0x400000 load offset and native jfr_set_dump_path address.
The null/empty setter branch calls os::get_current_directory; its dump buffer
symbol maps to the captured0x2a43860 argument and the captured0x401 length
matches1025bytes. Fault PC0x100026c946 is outside the app. There is no captured
native fatal OOM or VM ABORT. Preparation alone is incomplete call tracking;
matching target, arguments and disassembly identify this default cwd query.

Build049 pins a runtime repair that defaults PS5 JFR emergency dumps to the
real application-visible `/download0`, covering both the setter and empty-global
fallback. Explicit nonempty paths and normal file-open/write failure behavior
are retained. The helper does not create a directory or disable JFR. Other
platforms retain their cwd lookup. Native diagnostics and160MiB heap remain.

Actual JFR path helper/get/set ASan/UBSan tests pass null/empty/default fallback,
explicit/max/oversize paths, buffer bounds and desktop behavior. Target rebuild
passes; its JFR emergency-dump object has no cwd-query dependency. **All049 PS5
rows, JFR initialization/output and real readiness/save/stop remain pending.**
Overall native capacity and discovery DNS remain unresolved.

Build049 package checks pass; SHA-256: `9a4407ef9da7b47bd05f43c5767b34c101df30d103b99bf5790223e41a8e98b9`.

### Build050: generated JFR metadata in the runtime image

Build049 returned server-row FAIL without a reported crash. The full saved
server log identifies a null resource stream in `MetadataLoader.createTypes`,
through `FlightRecorder.register` and Minecraft JFR profiler initialization.
This reaches beyond the prior default dump-path query; JFR dump output itself
remains unvalidated. Target Java compilation had omitted the generated
`jdk/jfr/internal/types/metadata.bin` resource.

Build050 pins runtime `496ea846b7b960441dba6f1e77b68808db39cd07`. The image builder runs requested modules'
target data generators, including JFR and desktop data, and verifies the JFR
resource SHA-256 across target output, JMOD and linked image. No host metadata
is copied. The extracted target JFR classes/resources load the metadata and
create238 types on the host JVM; this is not PS5 registration evidence.
Signed-container integrity, package CRC/version, native/image identities and
retained symbols pass. Heap160MiB and prior native repairs remain.
**All050 PS5 rows and real readiness/save/stop remain pending.** Discovery DNS
and overall native capacity are unresolved.

Build050 package SHA-256: `a4c1bfa3dc45b5c11bff656eeaecbecd85865b3802a9aeb2ffcabe64dddfc904`.

### Build051: identify network interface startup OOM

Build050 returned FAIL at one minute without a reported crash. The full saved
console gets past JFR initialization, loads1866 advancements, starts the server
and reaches listener setup on `*:25565`. Netty's `DefaultChannelId` initialization
then fails with an `OutOfMemoryError` rooted in `NetworkInterface.getAll()`.
The later `NoClassDefFoundError` wraps this initialization failure. This is
server-thread failure before readiness, not evidence of a one-minute timeout.
The server logs stopping/saving; no real `Done` or successful saved-world check
was reached. The exception report has18874592 free Java heap bytes after failure;
this does not identify peak heap availability or rule out heap OOM.

The full native trace records fixture failure, no VM ABORT/native fatal OOM, and
three implicit-null signals that each resume. Discovery DNS still fails.
The exact allocation inside interface enumeration/conversion remains unknown.

Build051 pins runtime `e09a729f7eba8156d7d5108ac128cdd826dfe6cb` with bounded PS5 native diagnostics for
interface enumeration, counts, native checked allocation failure and Java
array/object conversion failures, including exact conversion source lines.
It preserves the real interfaces, allocation paths and exception behavior.
**This is a diagnostic build, not a confirmed OOM repair.** Actual-body writer
and getAll host tests with narrow JNI/enumeration stubs pass ASan/UBSan; target
HotSpot/java.base native build, signed containers, native/image identities,
version/heap/diagnostic labels, ZIP CRC and retained symbols pass. Heap160MiB,
worker8MiB and target JFR metadata remain. **All051 console rows and real
readiness/save/stop remain pending.**

Build051 package SHA-256: `6ae273e10141baf6f996626c4405157c0e2888bccb6a4b02fcd2de28efa0fc9d`.
