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
