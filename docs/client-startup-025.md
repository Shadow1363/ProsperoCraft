# Original Minecraft client startup025 — bounded VM reservation

Client024 failed before original Minecraft Main. Saved reports for run
`client-01.000.024-1792849139-513138847` show repeated512MiB/520MiB native
reservation failures (`errno=12`), followed by “Could not reserve enough space
for524288 KB object heap”, VM ABORT and native exit1. The menu session remained
RUN at Create Java VM. Safari retrieved the full VM trace and startup tail;
the latter contains prior history,so only the marked024 run establishes this
failure. No game startup/native-loader failure was reached in024.

025 lowers only the consumer launch maximum heap from512MiB to128MiB,the
value used by passing023. Xms16MiB,compressed class space64MiB,interpreter,
SerialGC,original game/Java artifacts,full assets,runtime image and genuine
resident providers remain unchanged. No game-JAR transformation,allocation
success stub or JVM implementation change. The exact failed024 package and
symbols remain local under dist/failures/Client_Original_Startup-01.000.024.

This addresses the observed oversized reservation;actual PS5 VM creation and
Minecraft startup still require retesting.128MiB may be insufficient later in
Minecraft initialization. Larger heaps require separately verified runtime/
platform memory work rather than assuming512MiB is available. Full client
native coverage remains incomplete,including STB,FreeType,VMA,SPIRV-Cross,
OpenAL and SDL callbacks/libffi. A missing dependency is a real failure.

Install the current PPSA99874 version01.000.025 from the runtime workspace
`dist/PPSA99874.zip`,wait for Client025 ready,and press X once. Report the last
stage,error or actual game screen. If it crashes,reopen without pressing X to
preserve reports. No old graphics/controller checklist or automatic menu PASS.
The original four-row startup flow,offline demo arguments and writable bounded
logging are described in [the first startup attempt](client-startup-024.md).
Server two-hour endurance remains deferred;frozen023/earlier milestones intact.

Package SHA-256: `1c61c103fc96ac30a4c7acbdb985888a5cf2dfa848dadf90b74903c052097aee`.

Host128MiB original Main/native-bootstrap control and target package checks
pass,including all original JAR/assets,exact023 image/native libraries,staged
constructors,signatures and preserved frozen package hashes. No PS5 pass yet.
