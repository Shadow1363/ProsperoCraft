# Home, Instances and readable controls — 01.000.094

Temp_gametest source development only, PPSA99874. The user explicitly defers LAN
hosting work. Existing runtime0123 and network settings are retained. No Store,
release or frozen milestone is created. Preserve093 and every older candidate.

## Navigation and Home

Top-level pages are Home, Instances, Settings and Sign in/player name. L1/R1 opens
each page and focuses its actual content. Up from the first item can focus the
header; while the header is focused the model exports row -1, so content controls
cannot compete with its focus outline. The previous Settings jitter was caused
by header and row selection updating the same animated focus rectangle in one
frame. Header buttons now also share the same glass sizing treatment.

Instances always ends with a plus-only add card, including after a page boundary.
An empty library has one large card containing only a normally sized plus. Home
uses the same empty state. Its plus opens the instance picker (or instance creation
if the library is empty). Choose an instance to browse saved worlds and servers;
X pins/unpins the selected destination. Instance details also offer Worlds &
Servers. Home retains pinned cards in insertion order across launches, followed
by its plus card. Favorites are associated with the UUID instance, so identical
world folder names in different instances do not conflict.

Home cards open a detail page with PLAY and Remove from Home. Authenticated PLAY
uses the original Main's supported `--quickPlaySingleplayer` world-folder or
`--quickPlayMultiplayer` server-address argument. These flags were verified in the
original26.3Main bytecode; the JAR stays intact. Arguments retain spaces as one
array item. Normal authentication/ownership/version and preparation checks apply.
Actual PS5 quick-play behavior still needs console validation. Removing a pin
keeps the world/server; deleting the instance removes its pins.

Discovery reads ordinary saves/*/level.dat and servers.dat without modifying them.
The bounded NBT reader handles gzip/plain compounds, standard tag payloads and
lists; it caps file size, decompressed bytes, nesting, entry counts and display
labels. Invalid server targets are skipped and duplicates coalesced. Symlinked
storage is not followed. A malformed server list reports a read error and keeps
the original file. World display-name read failure falls back to the folder name.
The inventory refreshes whenever the instance's browser is opened. Renamed/deleted
worlds or externally edited servers can leave an older pin until it is unpinned;
no game files are renamed or repaired by this UI.

## Permanent deletion

There is no Undo action or Triangle restore binding. Delete asks **No / Yes,
Delete**, defaults to No and explicitly warns that the instance, all worlds and
settings will be permanently removed. Shared publisher cache, account storage and
other instances remain. Removal first uses a private journal to roll back an
interruption before metadata commits, then recursively purges the UUID folder.
If final cleanup fails, the instance remains removed and cleanup retries on the
next launcher startup. A post-commit journal is never exposed as user undo.

Legacy093and earlier Trash archives are not silently purged by this migration.
Their old interrupted-move recovery is retained to protect previously live data;
new deletions do not create recoverable archives and the launcher exposes no
restore UI. Source-only host fixtures check precommit rollback, postcommit purge,
symlinks and unrelated-data preservation. Actual PS5 deletion/purge needs testing
with a disposable instance, not an important world.

## Controls

The PLAY tutorial presents six large essentials: move, look, jump, mine/attack,
use/place and pause. It keeps the existing persisted Don't show again checkbox
and OK preparation gate. OPTIONS also opens the full guide from this tutorial;
background preparation cannot bypass the tutorial's OK gate while reading it.

The full OPTIONS guide has five pages: Movement & Actions, Inventory & Menus,
Text Keyboard, World Shortcuts and Touchpad Shortcuts. Each page shows six spaced
entries in two columns. Left/right changes section; Circle/OPTIONS returns to the
exact prior screen, including the prelaunch tutorial. Controller glyphs remain.
There is no longer a dense ten-line-per-column sheet.

Exact candidate hashes and test results are in the [094 validation record](validation/client094-home-library-build-2026-10-27.json).
Host tests and Vulkan previews do not establish controller feel, focus stability,
world discovery, quick-play, storage purge or lifecycle correctness on the PS5.
