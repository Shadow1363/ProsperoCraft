# Download storage reservation — candidate080

Human reports079downloads always stop at the displayed212MB with "No space left
on device", despite382GBfree on the console. Safari reports the current run as
`client-01.000.079-1793035845-430764912`; its exceptions report records repeated
DOWNLOAD failures.079did not include the actual storage error category in that
report; the UI/user supplied ENOSPC and the repeatable progress threshold.

Source inspection identifies an inherited `downloadDataSize:256` in the startup
app metadata. The native app template documents `/download0` as title-local,
persistent storage backed by a separate image and provisioned through this field.
The main console's free space does not establish free space within that allocation.
The template also documents `/data` as outside the normal supported sandbox.
The exact mounted size/quota was not measured;212MBcompleted is not the volume's
nominal size because other data and active downloads also use it.

080requests **4096MiB(4GiB)** using the same title/content identity. Data, library,
worlds and cache remain under `/download0/ProsperoCraft`; there is no migration,
cleanup, new filesystem privilege, direct backing-image manipulation or forced
reformat. An initial idea to relocate bulk data to `/data` was discarded after
checking the supported sandbox paths. No such relocation code is shipped.

Storage errors now distinguish ENOSPC/quota/access/read-only/other I/O in the
existing launcher failure report, using fixed safe categories. ENOSPC/quota UI
messages identify app storage and suggest loader metadata refresh/relaunch.
Settings shows the actual project data root. The native startup log records the
requested reservation without pretending it is a measured available capacity.
Java filesystem capacity queries remain unavailable on this port and were not
used to reject downloads or to infer that the physical drive is empty.

## Update and test

1. Close the079app normally.
2. Copy the **whole080PPSA99874folder over the installed app**, including
   `sce_sys/param.json`. Replacing only `eboot.bin` cannot update the reservation.
   Keep the existing title; do not uninstall or clear its application data.
3. Refresh the loader's app metadata/list and launch080again.
4. Confirm the existing instance remains, then choose Repair Download or Play
   to reuse its verified files and fetch the remainder. Check progress beyond
   the previous212MBplateau and completion. Test26.3first as described in079.
5. If the same limit remains, keep the app open for build/session/startup and
   Java exception reports. Existing-volume expansion on this exact loader/
   firmware must be checked; do not delete or resize its backing image manually.

[Native template path documentation](https://github.com/blackbearreloaded/ps5-native-app-boilerplate#application-filesystem-paths).
A separate project's [storage notes](https://github.com/abhi245y/PS5LM-Plus#readme)
report non-destructive growth on next launch after increasing downloadDataSize,
tested on13.00. That is supporting evidence, not acceptance on this console.

Host tests cover the4096reservation/same title, ENOSPC/quota/access/read-only
categories, truthful app-local error text and preservation/reopening of existing
library/world files. Instance/downloader/startup regressions and actual package
metadata/CRC/signatures are checked separately. **Real080mount growth, download
completion and subsequent game launch remain pending.** Other079limits, including
GLFW26.1/26.2gameplay and Minecraft Services app review, remain unchanged.

[Build record](validation/client080-storage-build-2026-10-26.json).
