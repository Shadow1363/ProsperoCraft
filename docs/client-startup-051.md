# ProsperoCraft client051 — bounded original-startup thread snapshots

Client050 run `client-01.000.050-1792949111-939372034` matches its build,session
and native stderr headers. Human reports original Mojang loading screen then crash.
[Hashed reports](validation/client050-startup-failure-2026-10-25.json) retain byte
counts/checksums;raw reports remain local under runtime logs/client050-result-20261025.
Early VideoOut open0x4e100100/prepare0,three image imports and flip-thread create0
succeed. First8present enqueues have8VK_SUCCESS fences and8accepted SubmitFlip0.
390shader entries and390returns match prior046/047/049counts. Last application
output is resource reload/font loading;no recorded signal,VM abort or driver error.
Fatal report is unavailable. Cause remains unknown;neither the last shader nor last
sampled metadata allocation identifies a crash location. Accepted flips do not
establish visible frames or later success. No menu/gameplay/ALL PASS.

051 adds one optional daemon in the consumer launch harness before reflective
original Main invocation. It requests a256KiB stack,does not inherit thread locals,
and records up to90snapshots with one-second sleeps between completed snapshots.
Each includes elapsed monotonic time,used/committed/max Java heap,thread identity,
observed state and Java stacks. Invoking Main/render thread is prioritized,then
Worker-Main resource workers,then other platform threads by ID. Output excludes
the observer and is limited to32threads/24frames each,with truncation markers.
Snapshots go to existing exceptions.log with PS5 STARTUP SNAPSHOT/END markers.

Thread.getAllStackTraces allocates all platform-thread stacks before formatting;
only printed output is bounded. Sampling uses VM stack-walk/safepoint machinery,
adds allocation,I/O and thread pressure,and may alter timing. Heap/state/stacks
are observations at different instants,not atomic crash context. One-second gaps
can miss a sudden termination;native frames lack an instruction-level crash stack.
Thread creation or sampler errors are reported without stopping original Main.
The observer is interrupted/disabled before closing the stream on normal/exception
return,and automatically stops after90samples;no recovery or thread-state changes.
Actual PS5 support/capture and impact remain pending. Missing snapshots are not
proof of a game/VM cause;inspect observer-unavailable/stopped markers.

Keep046same-owner early output,047outer delegating recorder,049FILE capture and
050WSI checkpoints. No driver,heap,resolution,runtime image,official54JARs or5147
asset changes. The exact050full package,symbols,status/source reference and hashed
failure record are retained in ignored dist/failures/Client_Original_Startup-01.000.050.
All frozen passes remain intact;no release or catalog download is established.
Server two-hour endurance stays deferred.

Checks:tools/test_client_startup_host.py compiles the exact launcher and tests
real live Main/blocked resource-thread stacks,deep-stack/output bounds,finite
sampling,daemon lifecycle and interruption without later writes. It also checks
launch/workdir/allocator policy and executes original host Main to its expected
absent-native failure253. This is not a host menu or PS5 pass. Target packaging
and tools/test_client_startup_package.py verify exact observer class bytes,all
original JAR/assets,native/runtime/audit/SELF integrity,and preserved050/frozen
packages. Test results and full local ZIP checksum are recorded in startup/status.json.

Install runtime dist/PPSA99874.zip version01.000.051,launch,press X once and report
actual screen behavior. After a crash,reopen without X to preserve the failed run.
Retrieve matching build/session/native stderr,full exceptions.log (snapshots),VM
trace,startup tail,abort and fatal report. A last snapshot narrows prior activity;
it is not the crash instruction. Crash resolution/menu/gameplay remain pending.

Full local ZIP SHA-256: `a4108d61b82c8dae40f8f5babe99dce772dfb45790e21e110d57233f096cf80d`. Host observer/launch/allocation checks and
target packaging pass;full-package verification result is recorded in status.json.
PS5 observer operation,crash mechanism/resolution and menu remain pending.
