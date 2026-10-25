# ProsperoCraft client053 — native observations around startup snapshots

The user reports052crashed at the original Mojang loading screen,approaching
completion but before the menu fade,around1½minutes after X. Matching run
client-01.000.052-1792952033-557961309 has91complete snapshots,the last at94195ms.
There is no normal observer-completion marker,error marker or later snapshot.
This is the last recorded activity,not proof of an exact crash deadline.
[Hashed reports and human result](validation/client052-startup-failure-2026-10-25.json).
Raw files remain local in runtime logs/client052-result-20261025.

The final render stack still joins PipelineCache's future. The deeper worker stack
shows FaceBakery/ItemModelGenerator/ModelBakery -> ParallelMapTransform ->
SimpleReloadInstance preparation task -> ForkJoinPool. This confirms resource
preparation activity,not execution of the pending pipeline supplier. Shared-pool
queue delay remains possible;no deadlock or crash instruction is identified.
390shader entries/390returns and first8successful fences/accepted flips remain.
No fatal signal,VM abort,driver error or Java OOM is captured. Heap used ranges
60917304..230307112bytes,last201468440/max259522560. Last native direct allocator
accounting held0xc8ac000bytes with failure/policy-rejection counts0;these are
scoped counters,not total native/console usage. Four initial metadata-null records
are88/88/40/24bytes;the existing retry-path limits still apply. The current native
resource report was unavailable. Exact052package,symbols,status,implementation
commit,build validation and failure evidence are preserved under ignored
dist/failures/Client_Original_Startup-01.000.052.

053 adds observations to fill two gaps:there are no native resource samples near
termination,and startup's earlier four-handler install does not establish that
the recorder still owns those handlers later. No resource or handler defect is
claimed from the missing evidence.

The existing Java observer invokes a new consumer JNI callback before stack
collection (phase0) and after publishing a complete snapshot (phase1). Each record
includes monotonic elapsed milliseconds,raw getrusage result/errno/RSS/fault/CPU
counters,sceKernelAvailableFlexibleMemorySize result/bytes,and read-only fault
recorder ownership/query-error masks. The report is /process-usage.log with its
own build/run header,initialized only when X starts a new run and archived by the
existing report mechanism. Merely reopening preserves the failed run. Phase
pairs help distinguish last native-query progress from Java collection/publication;
a missing record alone is not a crash location or proof of process death.

RSS units remain unspecified;do not convert them to bytes without target evidence.
A failed query invalidates its associated values. Flexible availability is one
pool query,not total system memory. Fault bits0..3 map SIGSEGV,SIGBUS,SIGILL,SIGABRT;
0xf with error mask0means these four queried handlers currently match the recorder.
A query-error bit makes the corresponding ownership observation unavailable.
A displaced handler is observed only;it is never reinstalled or overridden.
The ownership query holds the recorder's existing mutex and uses sigaction reads.
Recorder install/delegation/restoration/context handling is unchanged. Resource
queries use fixed stack storage and direct append IO,preserve errno and close
the descriptor. They do not change limits,allocate memory pools or alter game
threads. Open/append failure throws a harness IOException caught by the observer;
the native portion disables itself and Java snapshots continue. Close serializes
against native/Java output to prevent writes after closure.

Sampling now keeps1second sleeps through120samples,then60more with5second sleeps:
180total,nominal last sample419seconds plus query/stack/I/O/scheduling overhead.
Output retains32thread/64frame bounds and the optional256KiB-requested daemon.
This covers the observed ~95s period more densely and retains a later window.
Safepoints,allocations,queries,mutex contention and IO can alter timing. This
remains bounded diagnostic instrumentation,not atomic crash-context capture,
crash recovery or a proposed Minecraft performance repair.

Original54JARs/5147assets,runtime image,heap/executor properties and graphics
behavior remain intact. Consumer launcher and native recorder query/helper are
changed;exact native corresponding-source/relink materials for a future release
must match that accepted candidate. No frozen pass changed. Crash cause/menu/
gameplay/stability remain unvalidated;server2H stays deferred. Full release and
existing Store reservation conversion remain subject to all [051handoff release
requirements](handoff-prosperocraft-client051.md).

Host tests compile the actual native helper under ASan/UBSan with controlled
query values/failures and real file IO;verify raw results,formatting,append errors
and errno preservation. Fault tests exercise actual signal delegation/restoration
and ownership displacement without reinstallation. Java tests cover real blocked/
deep stacks,bounds,cadence,absent-native fallback and finite/closed lifecycle.
Target/full-package checks verify callback symbols/strings,exact Java bytecode,
original artifact hashes,native audits/runtime/SELF integrity and preserved052.
These checks do not establish a PS5 resource-query or menu pass.

On PS5 install053,press X once and note actual screen/timing. After crash,reopen
without X and retrieve /process-usage.log alongside build/session/exceptions/VM/
native-stderr/startup-tail/abort/fatal reports. Never infer successful menu or a
new milestone from diagnostic output or saved RUN.

Host/native helper/fault tests,target compilation and full-package verification pass.
[Build validation](validation/client053-build-2026-10-25.json). Full local ZIP
SHA-256: `cea95dcd5ef98f851a1f66e023a6e3323914d589df29cff6452f3f858cb1e65d`. PS5 validation remains pending.
