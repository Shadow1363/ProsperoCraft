# ProsperoCraft client052 — later and deeper startup observations

The user now confirms client051 crashed and was restarted: “i restarted it, it
crashed”. Its last visible screen and elapsed crash time remain unknown. Do not
assign050's Mojang-loading report to051. Safari retrieval after refreshing the
index returned the same051run and byte-identical versions of all eight reports;
there is no additional fatal context. See the [follow-up evidence](validation/client051-crash-followup-2026-10-25.json).
Exact051full package,matching symbols,status,source references and report hashes
are preserved in ignored dist/failures/Client_Original_Startup-01.000.051.

## Read-only dependency investigation

Inspected original pinned client-26.3.jar with JDK25 javap -p -c;no JAR was changed.
The JAR SHA-256 remains the client/26.3.lock.json pin. Local disassembly is under
build/client051-investigation and is excluded from publication.

- PipelineCache.get checks its cache,then calls device.compilePipeline with
  Util.backgroundExecutor,joins that CompletableFuture,and only then invokes the
  returned Pending.finishCompile. The051stack is at join,not finishCompile.
- FrontendGpuDevice delegates to PipelineBuilder.compilePipeline. Its ordinary
  supported path calls CompletableFuture.supplyAsync with the supplied executor.
  The supplier generates backend create information (GLSL/SPIR-V/reflection),
  invokes backendDevice.compilePipeline and returns the Pending completion.
  VulkanDevice delegates that backend compilation to VulkanRenderPipeline.compile.
- Util.backgroundExecutor returns BACKGROUND_EXECUTOR,created with makeExecutor
  (Main). TracingExecutor.execute delegates to its ExecutorService after optional
  tracing. The ordinary service is a ForkJoinPool with asyncMode=true;parallelism
  is availableProcessors minus one,clamped to1..getMaxThreads. max.bg.threads is
  supported with a minimum of1. This inspection does not measure the PS5 pool's
  queue,parallelism or pending future's identity.

This proves the waited compilation is submitted to the original shared background
executor. Samples show Worker-Main-1 executing resource work while render waits;
queue delay is a possibility. They do not prove starvation,deadlock or a broken
future. No executor/property/processor override is justified by these observations.

## Allocation retry context

Inspected the existing patched OpenJDK source read-only. The64MiB ordinary class
reservation failures and68MiB aligned attempt occur before a successful
PS5 class space direct reservation of64MiB at0x1000000000 (trace line142).
The existing compact-class-space fallback follows ordinary attempts,requires
ENOMEM and compact headers,and retains normal compressed-pointer validation.
Later4MiB ordinary reservation failures can fall back through MemoryReserver's
non-executable mtMetaspace direct path;successful markers are captured,including
trace line3088. These early attempts did not stop initialization in this run.
This is not proof of adequate total console memory or future allocations.

The four FAIL Metadata arena allocation records are emitted by the nonthrowing
Metaspace::allocate overload immediately after the initial arena attempt. Its
Java-thread overload calls satisfy_failed_metadata_allocation on null after VM
initialization. That retries the arena,then a VM operation retries,collects,
retries,expands/allocates,and finally collects soft references/retries. Only a
remaining null reaches report_metadata_oome in that caller. Non-Java callers
must handle null themselves. The trace lacks thread/request correlation and
complete retry results;interleaved later successes cannot be assigned to each
of these four failed requests. No Java OOM/VM abort was captured. No allocator
repair or suppression follows from these records.

## Candidate change and checks

052 changes only the consumer launcher observer and version labels. It keeps the
first90snapshots with1second sleeps,then takes60more with5second sleeps. The last
sample is nominally389seconds after the first,plus stack collection/I/O/scheduling
time. This is a finite later window,not a timeout or a deadline for Minecraft.
Output remains bounded to32threads but now allows64frames per thread to expose
resource-task roots previously truncated at24. One optional daemon still requests
256KiB stack and does not inherit thread locals. Capture adds safepoints,
allocations,I/O and thread pressure;it may alter timing and cannot capture a fatal
native instruction or guarantee observation before a sudden crash. Normal final
completion is not a crash marker. Main return closes/interrupts the observer.

Original54JARs/5147assets,runtime,heap,graphics,input and native dependency behavior
are unchanged. Crash cause remains unknown. No menu/gameplay/ALL PASS or release.
The server two-hour run stays deferred. Full release and Store conversion still
require console acceptance and all provisioning/license/relink requirements in
the [prior complete handoff](handoff-prosperocraft-client051.md#full-release-readiness--do-after-actual-successnot-from-host-checks).

The host check exercises live blocked/deep resource stacks,64frame/32thread bounds,
finite lifecycle,late-cadence boundaries and interrupted close without later writes.
It also checks launch/workdir/native allocation policy and expected original host
Main exit253 at absent native bootstrap. Target package checks verify exact nested
and outer observer bytecode,original JARs/assets,native audits,runtime/SELF identity
and exact preserved051package. Console validation remains pending.

Install the052package,press X once,and note visible screen changes and elapsed time
until menu,crash or continued loading. If still open,leave it running through the
later window (roughly6.5minutes) and save reports. After a crash,reopen without X
for retrieval. Keep timing and run identity explicit. Do not infer failure from
normal observer completion or success from saved RUN.

Host and target/package checks passed;[build validation](validation/client052-build-2026-10-25.json).
Full local ZIP SHA-256: `096b371c3927f0125922c591eb8c3033a206068ee6c2c3e39376736cd84f5a2e`.
