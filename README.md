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

## Current development: server start probe 01.000.025

The five rows initialize the runtime, create a 192 MiB interpreter VM, check official artifacts, start/save/stop a flat test world, and destroy the VM. Human EULA acceptance for this test is [recorded](server/eula-consent.json); the wrapper writes `eula=true` only when its explicit acceptance property is enabled.

The world and configuration live under the application-visible `/download0/mc-server-start`. The test preserves that directory across launches, writes its controlled low-distance server properties, listens on available interfaces without a preset IP, waits up to ten minutes for the real `Done` message, sends `stop`, awaits server-thread exit and reads the saved `world/level.dat`. Row 4 runs on a dedicated JNI-attached native worker with an 8 MiB stack. The menu redraws elapsed seconds while test selection and VM destruction remain disabled until the worker joins. The ten-minute readiness deadline starts after the synchronous server main method returns; it does not bound that initial call. The host readiness/save/stop test passes at 192 MiB; **PS5 server startup/save/stop remains pending**. Build 01.000.003 failed during JVM creation after a 64 MiB native reservation returned ENOMEM with its 256 MiB heap setting. A host attempt at 128 MiB exhausted Java heap during world generation. Build 01.000.004 also failed at JVM creation with an 80 MiB reservation failure. Build 01.000.005 retains the 192 MiB Java heap and includes a PS5 runtime adaptation: non-class metaspace reserves 16 MiB nodes instead of 64 MiB, growing through the existing allocator as needed. Build 01.000.005 now passes real VM creation at 192 MiB, official JAR checks and VM destruction on PS5. The server row then failed on `ServerStart25$Observer` lookup before execution. Build 01.000.006 puts all consumer probe classes in `ps5-server-probe.jar` on the system class path; the matching JNI lookup regression and real host readiness/save/stop test pass. The console memory limit and earlier signal cause remain unestablished. Build 01.000.006 executes the wrapper, but did not reach ready and exposed a partial Log4j initialization stack. Build 01.000.007 uses headless console-only logging and preserves error headings, cause chains, initial output and recent output separately. Native text capacity now holds the report instead of truncating it to 1.5 KiB. Its host readiness/save/stop and long-error diagnostic tests pass; the actual prior exception is not yet identified. This development build includes target-built `jdk.zipfs` for Minecraft datapacks, in addition to the bootstrap module set. It does not establish player-join support or sustained performance.

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
