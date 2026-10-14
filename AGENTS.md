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
