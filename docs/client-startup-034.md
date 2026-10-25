# Original Minecraft startup034 — failed at missing VMA

034 combines the exact native FreeType component accepted in033 with031 STB,
029 OSMesa/OpenGL,026 libffi/OpenAL and the existing SDL3/shaderc/RADV integration.
It addresses032 stopping at its first library,freetype,with missing libfreetype.so.
The official Minecraft26.3 JAR and all54 downloaded Java JARs remain unchanged.
Java runtime implementation and SDK remain unchanged. Vulkan is selected through
the supported --graphicsBackend argument;the OpenGL provider serves Minecraft's
unconditional native bootstrap. No acceptance SDL display opens before Main.

Install the local full dist/client-startup/PPSA99874.zip or the runtime workspace
dist/PPSA99874.zip. PPSA99874 replaces the existing probe/server app. Launch and
press X once. Original Main runs in offline demo mode at1280x720 with128MiB Java
heap. /download0/mc-client remains writable;existing options are preserved and
new options mute music/sound. The app has no background music.

Observe whether an actual game window/menu opens. Four diagnostic rows are not
an automatic menu pass. Main returning/exiting is diagnostic evidence. If it
fails,leave the app open for reports;after an app close,reopen without pressing X.
Reports include session.txt,exceptions.log,startup-tail.log and vm-trace.log.
There is no preset device address or inbound IP filter.

Host checks exercise launch policy/options preservation and original Main up to
expected missing host natives. Package checks verify54original JAR pins,5147
publisher asset SHA1s,exact runtime modules/native libraries,11resident groups,
staged constructors/signatures and exact033FreeType/031STB/029OpenGL inputs.
Original032/030 failure artifacts and all frozen passing milestones remain intact.
These checks do not establish a console menu pass. VMA,SPIRV-Cross and broader
SDL/native paths remain incomplete;randomized bootstrap order can expose the
next missing dependency. Game heap adequacy,menu/world/gameplay,global teardown
and server two-hour endurance remain unvalidated;endurance remains deferred.

Host/full-package checks pass. Full local package SHA-256:
`ee306f748fc37c171eec6edb1afaf5dfe59d12ef0cb57b56feb56bf8b3ba4a79`.
PS5 run failed loading vma at bootstrap index5 with missing liblwjgl_vma.so
and VM EXIT -3. The five earlier entries (shaderc,SDL,FreeType,STB,OpenAL)
loaded;no window/menu was initialized. See
[recorded failure](validation/client034-startup-failure-2026-10-25.json).
035 tests actual VMA allocations/GPU transfers before another Main retry.
