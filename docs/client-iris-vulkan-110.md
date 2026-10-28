# Iris Vulkan launch protection, development110

Safari-retrieved reports identify109 run
`client-01.000.109-1793174236-428176634` as the failed launch. Fabric successfully
loaded Iris1.11.7, Sodium0.9.2 and Fabric API0.165.0 on Minecraft26.3. Dependency
download planning had succeeded. Minecraft selected Vulkan and created the PS5
SDL Vulkan surface. Iris then initialized its OpenGL sampler limits through
`GL11C.glGetInteger`;LWJGL aborted the VM because no OpenGL context was current.
The startup tail records the fatal native-method stack and `STAGE: VM ABORT`.
The missing hs-error and placeholder abort report alone would not identify it.
Earlier OSHI/storage-report warnings were caught and execution continued.

Development110 reads the selected instance's original Fabric manifests, including
bundled modules, before launch. An installed mod with ID `iris` stops launch in
the launcher with a message explaining OpenGL versus Vulkan, directing the user
to Installed/Uninstall and Vitrail as the Vulkan shader-loader alternative. Renamed
and bundled Iris are detected by manifest ID rather than filename or receipt.
The shared online/offline/install-and-play path checks before any dependency
repair network requests. Download browsing and queues remain available. Existing
mods, configuration, shader packs and worlds are not edited or removed.

The guard covers current Iris as unsupported for this launcher;it must be revisited
if an upstream Iris Vulkan backend becomes supported. This does not implement a
usable game OpenGL context, make Iris render, or establish Distant Horizons
compatibility. Earlier scoped OSMesa/OpenGL milestone checks do not establish full
game OpenGL support. Use Vitrail with the Vulkan backend for the existing shader
path;shader-pack compatibility and performance still depend on the pack.

Host tests cover original Iris detection, renamed/nested Iris, clear explanation,
byte preservation and successful non-Iris/Vitrail checks. The actual launcher
repair entry is exercised in both online and offline modes with no installed
Fabric loader cache: it reports the compatibility reason before any repair or
launch handoff. Real Modrinth download
checks retain109's queue-order fix. Exact110 PS5 launcher-message, uninstall and
Vitrail launch checks remain pending. Public Store108 and prior packages remain
unchanged. This is consumer launch policy;no Java runtime source fix is needed.

Candidate ZIP SHA-256:
`67cc61e7d5528a6ddaea42978ceddc16e7d13205b25e4630f355eb71b32175ca`.
