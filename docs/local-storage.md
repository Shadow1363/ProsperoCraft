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

## Space recovery after the menu release — 2026-10-26

The disk had only 1.4 GiB available after release preparation. Verified duplicate
cleanup and lossless compaction restored roughly 22 GiB of available space.
Free space varies with macOS activity; logical totals differ from APFS physical
recovery. No game/runtime implementation or release binary changed.

Removed byte-verified duplicate release downloads, extracted relink kits and
25 older build-directory symbol copies: **5,172,255,416 logical bytes**. Retained
source/relink ZIPs match every removed kit file. Every removed symbol matched an
independently preserved failed candidate. Downloaded-kit verification logs remain local.

Failed original-startup candidates 037–061 now live losslessly in:

- `dist/archives/failed-client-builds-client037-061.tar.zst`
- `dist/archives/failed-client-builds-client037-061.json`

The 117 files, originally **19,303,615,609 bytes**, compressed to **2,230,177,327
bytes**. Every decompressed file was checked against its original SHA-256 and size;
all originals were rehashed again before expanded `dist/failures` was removed.
Earlier failed-client/server archives remain unchanged. No private archive, game
JAR, raw log or credential was uploaded. Keep each archive with its manifest.

The helper supports additional named batches without replacing old ones:

```sh
python3 tools/compact_failed_client_builds.py verify --batch client037-061
# Restore the entire batch only when enough free space is available:
python3 tools/compact_failed_client_builds.py restore --batch client037-061
```

A full restore needs around 19.3 GB plus overhead. To restore just one file,
verify the archive first, then extract that exact manifest path instead:

```sh
zstd -d --long=30 -c dist/archives/failed-client-builds-client037-061.tar.zst | tar -x -C dist failures/Client_Original_Startup-01.000.061/PPSA99874-full-local.zip
```

Use an absent destination and compare the extracted file's SHA-256 with the
manifest before use. Current startup package checks discover and fully verify
all named failed-client archives, so they no longer require expanding 037–061.
The actual 062 full package check passed after this storage migration.

Still directly retained: the accepted 062 full package/symbols and current startup
package/staging; all frozen milestones; Fabric/Paper/vanilla fallbacks; source/Git
history; private crash logs; SDK/JDK/runtime/native dependency objects; public
release ZIPs, checksums and notices. The accepted 062 snapshot uses independent
copy-on-write files, so rewriting a future candidate cannot alter accepted bytes.

For future releases, remove verified downloaded/extracted kit duplicates after
publication and compact inactive failure batches before they accumulate. Preserve
needed symbols in one verified snapshot rather than every build directory. These
are explicit maintenance actions, not a background watcher. Menu confirmation
stands; world gameplay, controls, speaker audio, saving/reloading and stability
remain unvalidated. Cleanup does not change those console results.
