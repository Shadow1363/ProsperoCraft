# Prospero Store reservation — ProsperoCraft

The existing PPSA99874 reservation was added by mateo-cogeanu in
https://github.com/darkxex/ps5-homebrew-catalog/pull/353 and merged on2026-10-17.
The catalog repository URL now resolves under darkxex/ps5-homebrew-catalog.

On2026-10-25 the user selected ProsperoCraft and requested the supplied app icon,
name and updated Minecraft Java client/server/native-runtime description.
The reservation update is submitted at:

https://github.com/darkxex/ps5-homebrew-catalog/pull/737

Status:MERGED2026-10-25 (PR737,mergedAt12:49:50UTC). Verified during the
client044handoff:upstream apps/PPSA99874.json contains ProsperoCraft and the
description below. Live store/website propagation was not independently checked.
Only apps/PPSA99874.json changed.

Name:ProsperoCraft

Description: Minecraft Java Edition client and server on PS5, powered by native OpenJDK 25; vanilla, Fabric and Paper server playtests, with client startup under development.

The161-character description stays within the catalog's200-character limit.
It distinguishes server playtests from the still-unvalidated client startup/menu.
Reservation status remains unchanged:source_repo,artifact_url,sha256,icon_url,
version and license stay null. No full game package or development artifact is
uploaded to the catalog. Current reservation rules require icon_url null and
show the shared Coming soon art;the supplied ProsperoCraft icon is used in future
local app packages and project branding,not forced into an invalid reservation.
A later downloadable listing can supply its pinned public icon and release data.

Local python3 -m catalog check passes with138valid records and0errors/warnings/
notices. The update branch is codex/prosperocraft-branding in the user's catalog
fork. The original reservation belongs to this same account.

Consumer artwork/name live in assets/branding and tools/apply_branding.py.
Future client/server packagers apply them while preserving title/content identity
and build versions. Frozen validation/release assets and already-built038 stay
intact. Branding changes do not establish client/menu acceptance.

## Client050 continuation and eventual release

PR737MERGED and the upstream ProsperoCraft record were reverified via GitHub
on2026-10-25 during the050handoff. All six optional release/source/icon/license
fields remain null. This check does not establish live website propagation.
See [the complete050handoff](handoff-prosperocraft-client050.md) for current logs,
repair steps and release readiness. A downloadable listing must follow actual
accepted client behavior,verified public app-only release artifacts,pinned icon/
checksum,and working provisioning for omitted original JARs AND startup assets.
Existing milestone JAR-only provisioning is not yet complete startup provisioning.
Provide exact matching OpenAL source/relink materials for the accepted binary;
do not publish the full local game-containing development ZIP. Re-read current
upstream submission/artifact/versioning rules before converting this reservation.

## Downloadable launcher082 — 26 October 2026

The user explicitly requested Store publication of exact082. Release
[01.000.082](https://github.com/mateo-cogeanu/ProsperoCraft/releases/tag/01.000.082)
is public, with an installable app-folder ZIP, matching OpenAL corresponding
source/relink kit, validation records and SHA256SUMS. No game JARs/assets are
bundled: the native launcher downloads verified originals on the console.
The existing reservation conversion is
[PR811](https://github.com/darkxex/ps5-homebrew-catalog/pull/811); no new title ID
or duplicate listing. Only its apps/PPSA99874.json record changes.

Local catalog check passes for144records with0errors/warnings. Online verification
passes for the exact public ZIP digest,01.000.082 content version and pinned icon,
with0errors/warnings. All five assets were downloaded and hashes rechecked; the
downloaded relocated OpenAL kit reproduces the exact packaged ELF. See the
[publication record](validation/client082-store-publication-2026-10-26.json) and
[release guide](releases/client-launcher-082.md). Remote CI/merge/deploy is tracked
on PR811; this paragraph records submission, not a claim of live propagation.

Only26.3SDLdemo is enabled; Microsoft approval/full-account access remain pending.
Exact082PS5quit/relaunch,input,checkbox/world persistence and audio/performance
regression checks remain pending. The publication request does not establish
a formal ALL PASS or replace frozen milestones. The earlier reservation-only
paragraphs above describe historical state and are superseded by this submission.
