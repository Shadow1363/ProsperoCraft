# Development112: native input, audio reload and mod downloads

Candidate112 is for PS5 testing. Public release/ProsperoStore remain108. No new passing milestone or console compatibility claim is made.

## Audio and world saves

The preserved111 reports show a working native OpenAL output closed during resource reload. Subsequent native opens fail0x8026000d, before the later descriptor-exhaustion errors.112 retains at most one drained healthy native main output across logical OpenAL closes, joins the mixer before returning it and discards failed outputs. The port is reserved before JVM/graphics allocation. Actual OpenAL mixing tests cover reload, pause/resume, errors and a permanent reopen-allocation failure; audible PS5 playback after reload is pending.

Chunk saves and other real file operations fail with `Too many open files`.112 requests a soft descriptor limit of8192 before starting Java, bounded by the existing hard limit, and logs the query/change/result and descriptor snapshot. The log server adds `/resource-status.txt` and reports actual file-open errno under pressure instead of claiming all reports are missing. This is mitigation and instrumentation: the descriptor accumulation owner, actual permitted console limit and sustained save/reload remain unresolved. See [bounded observations and report hashes](validation/client112-observations.json); raw reports remain local.

## Controlify

SDL's real DualSense joystick now offers a gyro only after the native motion-state call succeeds and forwards finite sampled angular velocity with controller timestamps. Enable/disable requests reach the native pad service. PS5 axis orientation, reconnect and physical motion remain pending.

A separate four-channel48kHz floating-point SDL audio endpoint exposes DualSense haptics after the real type10 actuator output and advanced vibration mode probe succeed. Controlify's actuator channels2/3 become native stereo signed16-bit samples; speaker channels0/1 are discarded. OpenAL game speakers stay separate. One actuator port is reserved early and retained across healthy reloads. Failed output/mode changes clean up; unsupported probes do not advertise a usable device. Primary-user only; hotplug, physical haptic effects and simultaneous game audio require PS5 testing. No new rumble/LED/adaptive-trigger capability is claimed.

## Download queue

Each root's required dependency graph is resolved before grouping overlapping plans. An artifact download failure blocks that artifact's dependent roots, while unrelated roots, shader packs and resource packs continue. Shared dependency failures skip only their consumers. Successful roots leave the queue immediately; failed roots remain. Metadata/plan conflicts can fail their connected group when no narrower failed artifact is identifiable, while independent groups still proceed. The final error summarizes failures, and local `content-download-errors.json` retains details. Cancellation still stops the operation. Existing per-plan rollback and verified dependency-upgrade behavior are preserved.

## Distant Horizons Fabric26.3 test variant

The original3.3.4 launch hits unsupported `PS5` platform detection and missing shaded Zstd native code.112 embeds genuine pinned Zstd JNI and SQLite JDBC implementations for the mod's existing shaded Java namespaces, using the reusable Java runtime's optional build tools. The official mod JAR is preserved. A separately identified variant built from complete pinned upstream source adds an explicit PS5 Unix platform enum, without pretending to be Linux or editing installed bytecode. No new incompatibility block was added.

Use `tools/build_distant_horizons_ps5.py` to reproduce `DistantHorizons-fabric-3.3.4+ps5.112-26.3.jar`. Upstream commit eb1007cb6cc3e0419effe2b40ab485cf24e55b43; core64410621767ee697e8bc175c2a3ebe4c5e2ce520. Exact patch and build hashes are recorded beside the candidate. Replace the original Distant Horizons JAR in the test instance's `mods` folder with this variant; keep only one Distant Horizons JAR. It requires app112. Source patch and licenses are retained; existing worlds are not migrated.

The full Fabric source build passes. Host tests exercise the actual enum under `os.name=PS5`, actual original upstream Java compression arrays/streams/contexts and SQLite WAL/prepared statements/commit/rollback/persistent reopen with explicitly built natives. Missing-native controls fail. PS5 launch, Vulkan interoperability, LOD rendering, database locking, save/reload and performance remain pending. No claim that source compilation establishes game compatibility.

Candidate package SHA-256: `ff2ef87a5f7980016385d7f50da34b42be212eb75ae88165583f59d8c9051ade`.
Distant Horizons variant SHA-256: `2ad04d4b68f8d0c4956486b81cae2b694863751d884b6b1c2310689775e61f16`.

[Validation](validation/client112.json). Frozen passing snapshots and public packages are preserved.
