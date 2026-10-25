# Client_SPIRV_Cross

Frozen PPSA99874 01.000.036;human ALL5 PASS on2026-10-25.
Human ALL5 PASS corroborated by matching saved session and detailed current-run startup log.
Three real SPIRV-Cross contexts produce9GLSL450/HLSL5/MSL translations with exact
source fingerprints,SSBO set0/binding0,push8/local64 reflection,malformed input
error controls,384guards,unchanged input,allocation/context cleanup and JVM stop.

This validates the tested original C API0.68.0/LWJGL downcall workload and PS5
native localeconv/C++ error path. The reviewable locale adapter is recorded in
the audit. Translated shader GPU execution,MSL compiler validation,other shader
stages/resources/backends/options,callbacks/concurrency/large workloads,non-C/
changing locale/floating literals,global teardown and Minecraft startup/menu
remain unvalidated. Server two-hour endurance remains deferred.

Tested source:`90fcda40158ed25e1d004959ae389f966aea809b`. Full local ZIP SHA256:`e4ff7cfe2464e7f218e4b518e1dfe77cca90e67fec531f9314aeb3e1191773ac`.
See validation.json for source pins,scope,omissions and retained file hashes.
Preserve this snapshot;continue in root client/.

The app-only release omits54original game/Java JARs. Extract it and use the included
provision helper with --manifest validation.json --app-dir PPSA99874 --jars-dir
/path/to/verified/jars. All retained files and original JARs are checked.

SPIRV-Cross Apache-2.0 source/archive/license,locale patch and LWJGL BSD notice are
in app assets. The matching OpenAL LGPL source/relink kit reproduces the exact
accepted native ELF. Source edits invalidate console acceptance.
