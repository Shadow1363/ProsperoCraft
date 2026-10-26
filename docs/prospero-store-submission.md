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

Final remote check: submission validation, static release scan and offline tests
all PASS. PR811 is OPEN and awaiting maintainer review; the live Store page still
shows Coming soon. The bot declined auto-merge because its first-release API
ordering selects older065, despite /releases/latest correctly returning082 and
082having the newest publication timestamp. Evidence is in the PR body. Upstream
push permission is unavailable; reviewers were requested by its workflow. No
older release was removed/replaced and no catalog automation was bypassed.

## Fresh submission814

At the user's explicit request, PR811 was closed and replaced by
[PR814](https://github.com/darkxex/ps5-homebrew-catalog/pull/814), from fresh branch
`codex/prosperocraft-082-resubmit` based on current upstream8566a5f. Only
apps/PPSA99874.json changes; it is byte-identical to the previous submission.
The exact082release/assets remain unchanged. Local catalog validation passes
for144records with0errors/warnings. The new PR reruns the automated checks; a
fresh PR does not itself change the catalog's release-ordering logic. This
submission supersedes earlier PR811 references as the active Store request.

PR814's fresh submission validation, release scan and offline tests all PASS.
The bot again reports “the release is not the newest of
mateo-cogeanu/ProsperoCraft” and leaves the PR for a maintainer. Recreating the
PR did not resolve the release-order issue. Current state is REVIEW_REQUIRED;
darkxex and Marice are requested reviewers. Original packages/assets unchanged.

## GPLv3 and fork credit

At the user's request, ProsperoCraft's original code/build scripts are now
explicitly GPL-3.0-or-later, consistent with the existing source headers. Root
LICENSEcontains the standard GPLv3 text;NOTICEidentifies copyright
“mateo-cogeanu — ProsperoCraft” and retained upstream credits. Distributed forks
must preserve applicable copyright/license notices and meet GPL source and
modification-notice requirements. No advertising or splash-screen condition is
added. Upstream code keeps its own license; official game files are not relicensed.

GitHub detects GPL-3.0 and activePR814now declaresGPL-3.0-or-later instead of
Unlicensed. The existing082ZIPalready includes the fullGPLv3text; its bytes,tag
and frozen validation remain unchanged. Separate license/notice/checksum release
assets accompany the explicit project grant. This follow-up supersedes earlier
Unlicensed metadata while preserving its historical validation records. See
[license publication record](validation/client082-license-2026-10-26.json).
