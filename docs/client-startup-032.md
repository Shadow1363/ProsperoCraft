# Original Minecraft startup032 — failed at missing FreeType

Client01.000.032 combines the exact native STB object accepted in031 with the
OSMesa/OpenGL provider and dependency dispatch accepted in029. This addresses
030 failing at its first native bootstrap entry, STB. Existing026 libffi/OpenAL,
SDL3, shaderc and RADV remain included. Original Minecraft26.3 and all54 upstream
Java JARs remain byte-identical; the Java runtime implementation is unchanged.
Vulkan remains selected through the supported --graphicsBackend argument.

Install the local full `dist/client-startup/PPSA99874.zip` (also copied into the
runtime workspace's `dist/PPSA99874.zip`). Title ID remains PPSA99874; this
replaces the currently installed probe/server app. Launch and press X once.
The harness invokes original Main directly without first opening an SDL fixture.
It uses offline demo arguments,1280x720,128MiB Java heap and a writable
/download0/mc-client directory. Existing options are preserved; newly created
options mute sound/music. There is no application music.

Observe whether an actual Minecraft window/menu appears. Four diagnostic rows
are not an automatic menu pass, and Main returning or exiting is diagnostic
failure evidence. After failure, keep the app open for logs; if the app closes,
reopen without pressing X. Collect session.txt,exceptions.log,startup-tail.log
and vm-trace.log from its log page. No preset device address is embedded.

Host checks cover launch arguments/options preservation and original Main
reaching native bootstrap with its expected missing host natives. Package checks
verify all5147 original asset SHA1s,all54 JAR hashes,exact runtime modules/libs,
real STB and GL objects against passing packages,10resident groups,staged native
constructors and signed-container integrity. These checks do not establish PS5
startup. FreeType,VMA,SPIRV-Cross and broader SDL/callback coverage remain
incomplete; native bootstrap order may expose a different missing dependency.
Game heap adequacy,menu/world/gameplay and global teardown remain unvalidated.
Server two-hour endurance remains deferred. Frozen031/029/026/023 and failed030
packages are preserved. No passing milestone or release is inferred for032.

Host and full package checks pass. Full local package SHA-256:
`5d6fb33084876e0d0b08e5b020c6de196b98508d31b983a6f33cd9028635e434`.
Actual PS5 run failed at first native bootstrap entry,freetype,with missing
libfreetype.so and VM EXIT -3. Window/menu were not reached. See
[recorded failure](validation/client032-startup-failure-2026-10-25.json).
Development033 tests real FreeType before the next original Main retry.
