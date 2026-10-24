# Original Minecraft startup027 — reuse passing026 native ports

026 now passes the actual PS5 callback/OpenAL five-row acceptance,with its
source/package/symbols/validation and public release frozen separately.
027 retries the original Minecraft26.3 Main with those real libffi/upcall and
OpenAL Soft providers plus the PS5 VK/ALC module dispatch overlay. All54 original
Java/game JARs and all5147publisher asset objects remain unchanged. No game
bytecode hooks,replacement game classes or SDK/JVM implementation changes.

The consumer harness configures the actual OpenAL resident library,initializes
GPU/compiler/SDL/OpenAL native providers in sequence,and invokes original Main.
The128MiB heap reservation remains the026/025 working setting. The native
acceptance fixture is bundled as a dependency resource but is not run before
Main;the original four startup rows remain,so Main can own its window/lifecycle.
Additional native dependencies remain incomplete. This build is a diagnostic
startup attempt,not an established menu/gameplay milestone.

The original native bootstrap loads OpenGL even when Vulkan is selected. Real
OpenGL,STB,FreeType,VMA,SPIRV-Cross and remaining SDL callback coverage are still
incomplete;any can stop this run. No fake GL/AL exports or ignored dependency
errors are added. Future native startup repair stays in the Java port or explicit
consumer dependency ports/harness,not original game JAR transformations.
Muting the game does not remove its OpenAL bootstrap requirement.

Launch remains supported offline demo mode,PS5Probe identity/placeholder token0,
Vulkan1280x720,disabled multiplayer/chat and no credentials/EULA acceptance.
Writable data stays under /download0/mc-client. Original assets include audio
but there is no application background music or claimed PS5 speaker backend.
System.out/err and actual game failures go to /exceptions.log;native run stages
and VM exit are in startup-tail.log. Original Main can System.exit after a
crash report;that exit is not automatically a native runtime fault.

Install current PPSA99874 version01.000.027,wait for Client027 ready and press X
once. No five-row026 or old graphics input checklist is needed. Report the last
notification/actual game window/loading/menu or error. On exit,reopen without
pressing X to preserve the new reports. Actual Main return is diagnostic only;
there is no automatic menu PASS. Leave server two-hour endurance deferred.

Host/package checks pass,including all original JAR/asset hashes,exact026
scoped FFI/OpenAL objects and frozen026 package checksum. PS5 original startup
remains pending. Package SHA-256: `e8b34ceb3532e0407e5d19802ea4f5a82dc27901b26e60daaf249e4d967b3305`.
