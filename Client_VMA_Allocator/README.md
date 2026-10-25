# Client_VMA_Allocator

Frozen PPSA99874 01.000.035;human ALL5 PASS on2026-10-25.
Human ALL5 PASS corroborated by matching saved session and detailed current-run startup log.
Three real VMA3.4.0 allocator/instance/device lifecycles use two mapped65536-byte
buffer suballocations each for12copy/fill GPU transfers,exact output/source/guards,
NEVER_ALLOCATE error controls,map/flush/invalidate/unmap/free and JVM shutdown.

This does not establish images,pools,defragmentation,budgets,virtual allocations,
allocation callbacks,concurrent/large workloads,global teardown or Minecraft
startup/menu. Server two-hour endurance remains deferred.

Tested source:`951ec1c8411d4a0bc141712db6dc262c2afbc94e`. Full local ZIP SHA256:`7e62bc9b982a48f0ffbb9fe384b40f100d132fcd6be271fdc1df13c1738d46fd`.
See validation.json for source pins,scope,omissions and retained file hashes.
Preserve this snapshot;continue in root client/.

The app-only release omits54original game/Java JARs. Extract it and use the included
provision helper with --manifest validation.json --app-dir PPSA99874 --jars-dir
/path/to/verified/jars. All retained files and original JARs are checked.

Original VMA AMD MIT and LWJGL BSD/Vulkan-header notices are in the app assets.
The matching OpenAL LGPL source/relink kit reproduces the exact accepted native
ELF. Source edits invalidate console acceptance.
