# Client SDL Window/Input 01.000.013 — fixture companion loading

Client012 failed automatic check9, before SDL initialization, with
`ClientVulkan25: java.lang.NoClassDefFoundError: ClientVulkan25$Allocation`.
The retrieved session is `client-01.000.012-1792838530-795865272`.
The earlier GPU row completed three cycles. SDL check11 was not reached.

The exact012 ZIP contains the Allocation bytecode both as a standalone fixture
class and inside client-probe.jar. The failure therefore is not explained by
an omitted class in the packaged source artifact; target deployment or Java
classpath discovery remains unresolved. This run does not establish an SDL bug.

The probe already defines each main fixture using native packaged-file IO and
JNI DefineClass in the actual system class loader. Client013 extends that same
explicit fixture-loading path to its companions: ClientVulkan25$Allocation,
ClientShaderCode25 and ClientPresentCode25, before their corresponding checks.
Native reads/format failures and DefineClass exceptions stop the row with
separate diagnostics. Java bytecode/JARs, SDL native code, JVM and SDK are
unchanged. No fallback fabricates GPU or input success. This is a consumer
harness workaround; it does not claim to repair the unresolved classpath cause.
Failed012's exact ZIP/symbols and frozen passing milestones remain preserved.

Install **PPSA99874 01.000.013** from `dist/client-sdl/PPSA99874.zip`, also copied
to the runtime workspace's current `dist/PPSA99874.zip`. Use the [012 run
instructions](client-sdl-window-input-012.md): wait for Client013 ready, release
and press X once, then after Input ready supply X/Circle/D-pad Left/left-stick
input. Confirm automatic PASS and the visible final pattern. The input limit
is two minutes. Keep it open for logs; after a crash reopen without pressing X.

All twelve PS5 checks, real SDL input and visual acceptance require a new013
result. Previous host real-SDL virtual-input checks remain applicable because
those fixtures/native sources are unchanged. Package checks verify compiled
bootstrap companion-loading diagnostics, matching packaged helper bytecode,
SDL exports/scoping/licenses, original JARs and earlier frozen package hashes.
The original server two-hour test remains deferred. No new milestone is frozen.
