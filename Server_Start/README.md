# Server Start — 01.000.058

Frozen after the human reported ALL PASS on PS5 on 2026-10-18. The five rows
cover runtime/VM lifecycle, artifact and asset preflight, real flat-world server
readiness, stop/thread exit and a nonempty saved world/level.dat. See
[validation.json](validation.json) for exact source pins, scope and checksums.
Saved-world reload, player joins, performance and endurance remain unvalidated.

Source is frozen here; use the release-tagged repository layout to reproduce
with these server/tools files and the exact separate runtime pin. Continue
changes in the active server/tools folders without altering this snapshot.

The public app-only ZIP preserves the tested app/runtime bytes and own probe
JAR. Official game/dependency JARs and the game-derived diagnostic JAR are
excluded. Run `python3 tools/prepare_server.py --runtime-workspace /path/to/PS5_Homebrew`
from the tagged repository checkout, then copy the generated
`build/assets/java25/jars/` into the extracted app's `assets/java25/jars/`.
Install the complete PPSA99874 folder with the existing app closed.
