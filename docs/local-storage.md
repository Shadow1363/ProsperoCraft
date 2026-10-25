# Local storage and GitHub

Source/history live in GitHub. Passing app-only packages,validation manifests,
checksums and corresponding-source/relink kits live in GitHub Releases. Those
are the durable public archive;build staging directories are disposable copies.
Current startup sources,its package,and native dependency objects remain local
while console testing continues. Frozen source/validation records stay intact.

For verified duplicate staging cleanup:

```sh
python3 tools/clean_client_staging.py
python3 tools/clean_client_staging.py --apply
```

The default is a preview. The tool only handles named completed client probes.
It verifies the preserved full package against the frozen SHA256 and ZIP CRC,
compares every staged file byte-for-byte,and checks duplicate candidate ZIPs.
It saves small package audits before removing duplicate app/assets directories
and candidate ZIPs. It retains frozen full packages,public release assets,
symbols,source,logs,current startup staging and dependency build objects.
Tests referring to removed old staging may need that probe to be restaged;
the exact accepted full package remains under dist/milestones for restoration.
APFS clones/compression mean logical bytes removed exceed physical recovery.

On2026-10-25 the first pass removed3061877941logical duplicate bytes across
completed029/031/033/035/036probe staging and candidate ZIPs. Client037 remains
the active startup package. No runtime/game implementation changed;console
startup validation remains pending.

A future deeper GitHub-first archive can keep completed public release assets
remote and retrieve them on demand,with their published checksums verified.
That should preserve exact frozen artifacts and provenance and update any local
checks which currently expect those artifacts. It is separate from this cleanup.
Unmodified downloaded Minecraft/Java JARs are omitted from public release assets;
use the existing pinned preparation/provisioning tools to restore them locally.
Do not publish full local game packages,private raw logs,credentials or caches.
Logs and historical failed full packages have no equivalent public archive and
must not be deleted under the assumption that GitHub already stores them.

Do not indiscriminately delete .tools,build/java25 or native dependency objects:
these support current builds and expensive native/runtime compilation. Source
snapshots themselves are small compared with generated binaries and caches.

## Deeper cleanup on2026-10-25

Inactive failed client ZIPs/symbols now live losslessly in ignored
`dist/archives/failed-client-builds.tar.zst`,with a per-file SHA256 manifest
`failed-client-builds.json`. Original7652216276bytes compacted to1212395195bytes.
Every decompressed file was verified against its original hash before removing
expanded dist/failures. These are private local archives,not GitHub uploads.

```sh
python3 tools/compact_failed_client_builds.py verify
python3 tools/compact_failed_client_builds.py restore
```

Restore recreates exact dist/failures files and refuses to overwrite an existing
failures directory. Before running older checks which require dist/failures,
restore first. The compact archive remains after restoration. Pack refuses to
overwrite an existing archive. A later failed candidate can have its own active
failure folder;move that folder aside before whole-archive restoration.
Zstandard is required;compression/decompression uses a1GiB long-distance window.

Historical server full ZIPs from the runtime workspace's build/java25 directory
are similarly compacted into `dist/archives/legacy-server-packages.tar.zst` plus
`legacy-server-packages.json`. The helper is:

```sh
python3 tools/compact_legacy_server_packages.py --runtime-workspace /path/to/PS5_Homebrew
```

It archives only PPSA99874-*-full-local.zip in that historical build directory,
verifies every restored byte against its manifest,and removes only those originals.
The current consumer/server release/fallback and active client packages stay intact.
To restore one server ZIP,verify the archive SHA256 against its JSON manifest,
then use zstd decompression piped into tar extraction with that exact filename
and destination runtime build/java25. Compare the resulting file with the
manifest's SHA256 before use. Keep all private archives and manifests together.
No credentials,logs or game JARs from these archives are published to GitHub.

Frozen passing milestones,source/validation records,raw logs,active037 and native
build dependencies remain directly available. This cleanup changes storage layout,
not native/game/runtime implementations;037 console startup validation is pending.

Historical server compaction verified31ZIPs:4240004177bytes reduced to609246671bytes.
Removed 14 duplicate build-directory symbol copies (1990508984logical bytes),after matching each to a preserved milestone or verified failed-build archive.
