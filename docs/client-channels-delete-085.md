# Demo and Offline branches — candidate01.000.085

The user defines two development/release branches on2026-10-27:

| Branch | Purpose | Git branch | Default build |
| --- | --- | --- | --- |
| Demo | Public ProsperoStore build while the project appID review is pending | `codex/demo` | `demo` |
| Offline | Owner's verified offline play, future mod testing and extra features | `codex/offline` | `offline` |

`main` holds shared changes with a Demo default. Shared fixes, including instance
management, runtime stability and performance, merge from main into both channel
branches. Offline experiments stay on the Offline branch unless explicitly
selected for a shared fix. Client mods are still planned, not enabled by085.

The branch default is `client/launcher/channel.txt`. The package tool also accepts
`--launcher-channel demo|offline`; the existing `--offline` flag only means
build from cached dependencies. These flags have separate meanings. Each startup
package embeds `prosperocraft-channel.txt` into its launcher JAR and shows
**DEMO BRANCH** or **OFFLINE BRANCH** beside the version number. Missing or invalid
channel metadata defaults to Demo. No runtime account/profile toggle can turn a
Demo build into Offline. Demo ignores personal offline profiles and omits the
verification public key. Offline retains the signed, seven-day ownership/profile
import and separate Play Offline action. Both keep Play Demo and the existing
pending appID/device-code authentication behavior.

Both variants retain PPSA99874 and the existing4GiBdownload data. They replace
one another when installed; they are not side-by-side PS5 apps. Existing instance
library/cache/worlds and personal import data stay in `/download0/ProsperoCraft`.
Separate instances should be used for future mod experiments. Installing Demo
hides offline actions but does not erase the owner's import record or worlds.

## Delete and undo in both variants

Open an instance, choose **Instance Settings → Delete Instance**. Confirmation
opens with **Cancel** selected; Circle cancels. Choose Delete Instance explicitly
to remove it from the library. The complete instance UUID directory, including
worlds, options and future per-instance mod/config files, moves into
`/download0/ProsperoCraft/trash/instances/<transaction>/files/`. The adjacent
`instance.json` preserves its name, UUID, version, icon and ready state.

On the instance grid, **Triangle** restores the most recently deleted instance,
including after an app restart. Repeated undo can recover older retained entries.
An existing UUID folder is never overwritten. A full256-instance library rejects
restore until space is available. Deletion/restore are blocked while a launcher
task is busy. Deleting the last instance returns to the empty library correctly.
Shared downloaded version files/assets and account records are untouched.

Deletion is recoverable and does **not** immediately free game/world storage:
there is no automatic Trash purge or permanent-delete feature in this change.
Files stay local until explicitly managed. Failed library saves roll back the
folder and metadata; startup reconciles interrupted delete/restore moves against
the persisted library. Conflicting copies are kept and reported instead of
silently overwriting a world. Symlinked instance or Trash paths are rejected.

## Build and install

Run the existing startup package command with an explicit channel, for example:

```sh
python3 tools/package_client_vulkan.py \
  --runtime-workspace /path/to/PS5_Homebrew \
  --java-home /path/to/JDK25 \
  --offline --startup --launcher-channel demo
```

Repeat with `--launcher-channel offline` for the personal branch. Outputs are
preserved separately under `dist/client-startup-demo/` and
`dist/client-startup-offline/`, each with ZIP, symbols and channel/checksum record.
The canonical `dist/client-startup/PPSA99874.zip` and runtime ZIP mirror the most
recent build; the dual-build run finishes with Offline so the owner's default
candidate is the personal build. No personal account record/token/signing private
key is bundled or published. Exact084and published083/082remain preserved.

Host tests exercise actual delete/undo, metadata/world/options/cache/account
preservation, save failures, interrupted moves, traversal/symlink rejection,
confirmation/cancellation/busy input and selection with the final instance in
both channels. Offline checks additionally prove that Demo rejects a valid
personal proof and forced offline launch. Native previews and full target/package
audits check the new controls and resource separation. These are not a PS5 pass.

Exact085Demo/Offline controller deletion, restart undo, preserved world reload,
1080p/input/audio and quit/relaunch remain pending console validation. Root
`sce_sys/param.json` and the published Store release remain at083. This change
prepares channel candidates and publishes source; it does not replace Store
assets or claim public085availability.
