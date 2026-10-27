# Account and launcher improvements — 01.000.091

Development on `Temp_gametest` only. No ProsperoStore or release asset update.
Preserve090, the private089login test, earlier Offline/Demo candidates and frozen
milestones. These are host/target checks; no091PS5 success is claimed.

## Icons and selection menus

32 instance choices use the actual Prism/MultiMC instance SVG artwork at Prism
revision390a240abaefe389d1ab8510cc0ba5c2692a65be, rasterized72x72RGBA into real
Vulkan textures. The Prism launcher-logo choice is replaced by the user's supplied
transparent ProsperoCraft artwork. Original SVG bytes/metadata, upstream notices,
author attribution and transformation details live in `assets/launcher-icons`
and accompany the app. No third-party launcher branding replaces ProsperoCraft.
The logo now retains its original alpha over animated backgrounds. Earlier
integer icon choices remain valid; corresponding artwork changes are visual only.

Version, instance icon, resolution, parallel-download count and background selectors
open scrollable dropdown lists. D-pad moves, left/right jumps eight entries,
X confirms and Circle cancels without changing the prior value. Rename still
uses text entry. The new96-field native mailbox remains bounded and credentials
are excluded. Existing toolkit backgrounds, glass, motion and haptics remain.

## Account, QR and player heads

While the device code is active, the account screen shows the literal
https://www.microsoft.com/link URL and a QR encoding that exact URL. Scan it and
enter the displayed code. QR generation does not include an account/device secret.
The rendered Vulkan screenshot is checked with a real QR decoder.

After the Microsoft/Xbox/Minecraft pipeline verifies ownership and profile,
the account name and an8x8skin face with hat overlay appear in the account panel
and to the right of the player's name in the account button. Downloaded skin URLs
must use textures.minecraft.net; known HTTP texture URLs are upgraded to HTTPS.
A bounded pure-Java PNG decoder checks CRC, dimensions, format and decoded length,
without AWT/native image loading. Skin/network failures retain a placeholder.
Accounts with no custom skin use the UUID-selected vanilla default texture from
the original, already-downloaded26.3JAR. No game texture is bundled in the app.

The rotated refresh credential is saved locally using AES-GCM; access tokens stay
in memory. The app refreshes the account asynchronously on future launches and
rechecks Minecraft entitlement/profile before permitting full play. Sign out
clears the session, avatar, encrypted credential and local key. A revoked refresh
requires device sign-in again. Network failures keep the saved credential for retry.
A refresh response without a rotated credential retains the existing one.
If no refresh credential is issued, sign-in succeeds for the current session only.

The encryption key is app-local with best-effort0700/0600permissions, not a
hardware-backed console keychain. Filesystem access to both key and ciphertext
can decrypt it. Credentials/keys/accounts are never source-controlled or packaged.
Symlinks, invalid lengths and tampered ciphertext are rejected. Storage failures
leave the current verified login usable and report that it could not be saved.

## All26.x downloads and snapshots

New libraries show snapshots by default; existing explicit preferences remain.
Settings → Show Snapshots enables them for an older library. The dropdown includes
all publisher26.x releases, prereleases and snapshots, with unsupported entries
marked. Publisher Java requirements are recorded rather than blocking download
of a future-runtime version. Original publisher bytes, hashes and cache repair
remain. Only26.3SDLcan launch on this build;26.2and earlier,26.4snapshots and other
untested versions warn and remain launch-blocked. No silent version substitution.

## Resolution alignment

Settings offers720p,900p,1080p,1440p and2160p. These are requested logical/window
sizes. The SDL port now reports the real Vulkan framebuffer extent independently
through GetWindowSizeInPixels, allowing vanilla Minecraft to scale logical mouse
coordinates correctly. The software cursor uses the same normalized position;
movement speed scales with window size. Resize callbacks retain the requested
logical dimensions instead of forcing1080p.

Surface creation prefers a matching actual enumerated output mode. If the driver
has no such mode, the valid physical output remains in use and its real pixel
size is reported; this does not promise arbitrary scanout modes or lower GPU
render cost on a fixed-mode display. In-game fullscreen options may also select
the physical display mode. Actual PS5 clicks, GUI scale and resolution changes
still need validation; host coordinate checks alone do not establish alignment.

## Multiplayer and LAN

The user clarified that Open to LAN returns “failed to host”; joining servers is
untested because text entry is difficult. Full authenticated play retains normal
Minecraft network/account policy; no multiplayer/chat disable flags are added.
This candidate uses IPv4 and Netty NIO instead of attempting unavailable native
transports. A short-lived socket preflight logs TCP_LISTEN/UDP_BIND results using
all-interface, ephemeral-port sockets, then closes them before original Main.
No preset device/client IP or inbound client filter is embedded.

Actual original26.3bytecode shows Open to LAN starts the TCP listener and constructs
LanServerPinger (a DatagramSocket), returning false on IOException. Host tests
exercise the real Netty NIO bind/connect/accept/close and original pinger constructor
and advertisement format. They do not prove PS5 hosting or multicast delivery.
FTP2121and the log service could not be reached at the address supplied for this
session: host error “No route to host”. No current-run LAN exception was retrieved.
Thus the transport change is a candidate repair, not a confirmed root cause/fix.
PS5 Open to LAN, discovery, external join, online authentication and server joining
remain pending. Keep the failed-host logs local and inspect them when reachable;
do not replace game classes or silently skip account/server verification.

See the [validation record](validation/client091-account-ui-build-2026-10-27.json)
for checksums and exact checks. Visual previews use fixture account/skin data,
not the user's real account, and do not establish console rendering success.
