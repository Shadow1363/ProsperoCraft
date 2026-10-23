# Minecraft project scope

This repository contains Minecraft-specific PS5 homebrew work. Java runtime
fixes and acceptance probes belong in mateo-cogeanu/ps5-java25-homebrew;
reference that project instead of copying its runtime development here.

The human user authorized this public repository and publishing its README.
Keep README status accurate: Java probe passes do not establish a Minecraft
pass. Freeze a game milestone only after the user confirms its tests passed
on the actual PS5 for the exact build. Preserve passing snapshots and record
versions, dependencies, console evidence and package SHA-256 checksums.

Keep the README and its docs/readme-banner.svg consistent with project status.
Preserve the Java runtime link. Commit and push completed, authorized changes,
verify successful publication and report any failures honestly. Keep generated
builds, dependency caches, credentials, logs and unrelated files out of source
control. Passing compiled packages belong in release assets.

After every completed Minecraft source, asset, documentation, configuration
or script change, run the relevant checks, then commit and push to this
repository before ending the turn. Development can be published before
console validation; mark results pending. The user explicitly authorized
these updates. Verify each push. Runtime fixes must be published separately
to ps5-java25-homebrew using its sync script; do not mix source ownership.
Keep official downloaded JARs in ignored caches/local build packages,
with source-controlled artifact metadata and checksums for reproduction.
The initial --help bootstrap probe must not auto-accept the EULA or claim
world/server readiness from host success.

Server_Bootstrap is the frozen passing 01.000.002 snapshot. Do not modify it.
The human accepted the Minecraft EULA for the server test on 2026-10-14,
recorded in server/eula-consent.json. Development server-start code lives
in server/ and tools/. Retain passing full packages under ignored
dist/milestones before replacing the current build. Public releases omit
official game JARs and document local provisioning and separate checksums.

## Unmodified Minecraft server JAR direction

The user requires future compatibility fixes and features to live in the Java
port or the separately maintained Minecraft harness/configuration. Do not add
or expand server-JAR transformations, bytecode hooks or replacement game classes.
Keep the official downloaded server JAR intact. Existing local derivative
transformations are temporary migration debt, not the preferred architecture.

Gradually remove the existing transformations as working replacements are
implemented and validated. Move runtime compatibility into the Java port; use
vanilla configuration, ops.json and supported administration mechanisms for
Minecraft policy where possible. Do not silently remove required workarounds
or claim an unmodified server while a derivative is still executed. Record
each remaining transformation and console validation needed for its removal.
Preserve frozen passing snapshots; migrate development only.

## Work order requested on 2026-10-19

Prioritize smooth, stable server gameplay and completion of the migration to
the original unmodified server JAR. Establish actual PS5 startup, player save/
rejoin persistence and the requested two-hour baseline. Then work on server-side
mod loaders and individually validated mods for compatible pinned versions.
Client graphics, native bindings and input come after server mods work.
Track mihawk-99/PS5_Vulkan as a client graphics candidate; it is not an adopted
or validated project dependency. Keep game/mod/client plans in this repository.

## User work-order update on 2026-10-20

The user reports lag-free joined gameplay on083 and explicitly defers the
full two-hour run until later. Proceed with Fabric server/mod validation, then
Paper server/plugin validation, before client work. This overrides the earlier
requirement to finish the two-hour run before beginning server loaders. Keep
083 as a vanilla fallback and keep endurance/persistence limitations explicit.
Fabric/Paper are separate server flavors; use isolated worlds and pinned upstream
distributions. Do not add project-specific game-JAR rewrites or game replacement
classes. Standard upstream loader/Mixin behavior is part of the authorized mod
experiment and must be disclosed. Paper executes its own upstream server rather
than claiming to execute an unmodified Mojang server. No new passing milestone
is established by the083performance report alone.

## User work-order update on 2026-10-21

The user is satisfied with the Fabric experience and requests Paper next.
Validate the pinned upstream Paper distribution and a separate plugin on PS5;
once its exact candidate is confirmed passing, prepare and publish a proper
server release before client work. Do not infer a formal ALL PASS or full
two-hour completion from the satisfaction report. Preserve the Fabric094
candidate/package and vanilla083 fallback. Keep the two-hour test deferred.
Paper's upstream System.exit on shutdown is normal; report checked shutdown
evidence and distinguish a user-shortened play check from full endurance.

## User work-order update on 2026-10-22

The user reports Paper108 is much more than acceptable and by far the best yet,
after earlier satisfaction with Fabric094. The user now explicitly authorizes
client work while leaving the two-hour run pending, and requests a release
celebrating Fabric and Paper running before proceeding. Publish the accurately
qualified development prerelease and app-only artifacts; do not infer a formal
ALL PASS, completed lifecycle checklist or endurance result. Preserve exact
server packages/frozen milestones. Client work need not wait for those pending
server checks. Keep client code/artifact pins/graphics integration here and
reusable runtime fixes in the Java repository.

The user subsequently explicitly requested making Fabric-Paper-v01.000.108 a full
release, then continuing client work. Promote its GitHub release status without
inferring new console tests or ALL PASS. Keep endurance/lifecycle limitations
explicit and preserve the exact published app binaries and source tag.

The user requests reusing server title ID PPSA99874 and the same content identity
for client builds, but explicitly wants client versions to start at01.000.000
and advance independently of server versions. Do not continue the server build
counter for client packages.
Installing the client replaces the server app. Preserve tested server packages
and source snapshots for reinstalling; do not claim side-by-side installation.

Client_Foundation is the frozen passing client foundation milestone, PPSA99874
version01.000.000, user ALL PASS on2026-10-22. Preserve its source snapshot,
validation and matching compiled package. Its six foundation checks do not
establish game startup, GPU rendering, SDL/Vulkan/audio or controller gameplay.
Continue new client work in root client/, never inside Client_Foundation/.

Client_Native_Loading is the frozen passing client001 milestone, PPSA99874
version01.000.001, human ALL PASS for all seven rows on2026-10-22. Preserve
its source, validation and exact compiled package. It validates this resident
JNI loading/function-call integration, not full LWJGL/native graphics, arbitrary
ELF loading or Minecraft startup. Continue future work outside frozen folders.

Client_LWJGL_Core is the frozen passing client002 milestone, PPSA99874
version01.000.002, human ALL PASS for all eight rows on2026-10-23. Preserve
its source, validation and exact compiled package. It validates the tested
LWJGL native memory/JNI subset and PS5 resident provider; it does not establish
complete native bindings, arbitrary ELF loading, GPU/SDL/Vulkan or game startup.
Continue development outside frozen milestone folders.

Client_Native_Graphics is the frozen passing native-only client003 milestone,
PPSA99874 version01.000.003, human confirmation of all requested RGB/card checks
with no crash/corruption on2026-10-23. Preserve source, validation and exact
compiled package. It validates scoped RADV GPU clear/copy/readback and VideoOut
presentation, not Java/SDL integration, shader rendering, full Vulkan coverage
or game startup. No log retrieval was possible; evidence is the human report.
Continue development outside frozen folders.

Client_GPU_Integration is the frozen passing client004 milestone, PPSA99874
version01.000.004, user ALL PASS for all nine rows on2026-10-23. Preserve its
source, validation, exact package and symbols. It validates actual Java/LWJGL
plus resident JNI/RADV offscreen GPU copy/fill/readback, scoped provider/TLS
callback integration, three Vulkan session cycles and final JVM shutdown.
It does not establish full LWJGL Vulkan bindings, SDL/window integration,
shader/game rendering, full module cleanup or server endurance. Continue
development outside frozen folders.
