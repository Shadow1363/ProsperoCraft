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
