# Verified local account import — candidate 01.000.084

The user explicitly requests using their existing local Minecraft account for
PS5 offline single-player. The active local account was checked directly against
Minecraft Services: the current Minecraft access token was accepted, Java
entitlement was present and the returned profile matched the local account.
No account identifiers, tokens, private signing key or personal import record
are published in this repository or included in the app package.

This supersedes the earlier demo-only scope for this verified offline test.
It does not change the pending app registration or claim Microsoft/Mojang
approval. ProsperoCraft's device-code authentication stays unchanged.

`tools/export_offline_account.py` reads only the selected local Prism account
file. It sends the existing Minecraft access token directly to the official
HTTPS entitlement and profile endpoints, rejects redirects, expired sessions,
missing ownership and profile mismatches, then signs a small local record.
The record contains only profile name/UUID and verification/expiry timestamps.
The Microsoft refresh token and Minecraft access token are never exported.

The record is a **ProsperoCraft-issued offline lease**, not a Microsoft-signed
license or a new authenticated Minecraft session. The RSA private signing key
stays in ignored `.tools/offline-account/`, mode0600. Only its public key is
committed and packaged in `client-probe.jar`. A build with a different key does
not accept this issuer's records. Keep the local signing key for renewals; source
clones without it cannot issue records for the distributed key. A fork making its
own local test build must use its own key and corresponding packaged public key.
This is a developer-assisted import, not a public self-service account system.

The offline lease lasts seven days from a successful ownership/profile check.
Renew on the owner's Mac with the export helper and transfer the new record.
The PS5 checks the signature, schema, profile syntax, time bounds and expiry.
Missing, modified, expired or wrong-key records never enable offline launch.
The record can be loaded only from `/download0/ProsperoCraft/offline-account.json`;
no token/UUID command-line override or alternate app ID is added.

For an installed26.3SDLinstance, **Play Offline** appears as the fourth detail
button when a valid record exists. It verifies the existing original game cache
and launches with the verified name/UUID, accessToken0 and no `--demo` flag.
Multiplayer and chat remain disabled. Offline launch does not make network
requests or run downloads. **Play Demo** remains the first action and retains its
original demo arguments/profile. Locked1080p, current controls, audio settings,
world folders and the082process-replacement lifecycle are preserved. Using a
real UUID can give a different inventory/player record from the earlier demo
identity; no save/player-data migration is performed automatically.

The app package contains no official game JAR/assets, account record or private
key. The already verified/transferred26.3cache is reused. Install the complete
candidate folder into `/data/homebrew/PPSA99874`, retain existing download data,
and close/reopen the app. Root published manifest and Store083remain unchanged.

Host checks cover signature integrity, wrong keys, expiry/future/long leases,
invalid profiles, actual controller selection and offline launch arguments,
no network/token use, cache verification, demo/world preservation and1080p.
Exporter checks exercise entitlement denial, mismatched profiles, private file
permissions, output secret exclusion and actual RSA verification. Target build,
original-JAR host startup, native preview and package audits pass. Exact084PS5
signature provider, menu visibility, full offline world creation/save/reload,
audio/controls and Quit/library/relaunch remain pending. No ALL PASS is claimed.
