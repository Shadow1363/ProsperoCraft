# Client Runtime Shader Compilation 01.000.016 — companion-row correction

Client015 passed SDL input/display (eventMask15/stateMask15,284 graphics/sample/
guard/FIFO frames), then failed before runtime compiler initialization with:
`loader 'app' attempted duplicate class definition for ClientPresentCode25`.
Retrieved session: `client-01.000.015-1792840405-760602449`.

Adding the compiler row expanded the fixture execution range from index10 to11.
The same broad replacement accidentally expanded the companion-definition range.
That caused the compiler row to define the prior presentation companion again.
This is a bootstrap error; shaderc was not reached and this run provides no
console compiler result.

Client016 explicitly selects only indices8,9,10 for their three fixture
companions. The compiler row at11 has no companion and does not define one.
Package regression checks reject the incorrect broad range. The changed native
bootstrap is rebuilt; Java fixture bytecode/JARs and compiler/native dependency
objects remain identical to015. Failed015 package/symbols and all frozen passing
milestones stay preserved. No game/JVM/SDK or dependency-JAR changes are made.

Install **PPSA99874 01.000.016** from `dist/client-runtime_shader/PPSA99874.zip`,
also at the runtime workspace's current `dist/PPSA99874.zip`. Follow the
[015 instructions](client-runtime-shader-015.md), starting with Client016 ready:
release and press X once, complete the SDL input prompts, then wait for the
runtime shader compiler check and final PASS notification. Keep it open for
logs; after a crash reopen without pressing X.

All thirteen016 PS5 checks remain pending. Earlier host real-compiler/GPU checks
remain applicable to the unchanged Java/native dependencies. Target package
checks and exact hash are in client/runtime_shader/status.json. Runtime compiler
execution, teardown, broader graphics/game integration and server two-hour
endurance remain unvalidated. No new passing milestone is created.
