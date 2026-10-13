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
