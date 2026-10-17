# Prospero Store coming-soon submission

PS5 Minecraft Java was submitted as a coming-soon reservation for title ID
`PPSA99874` on 2026-10-17:

https://github.com/blackbearreloaded/ps5-homebrew-catalog/pull/353

Status: submitted; upstream maintainer review/merge is pending. This is not
confirmation that the listing is live. The catalog feeds homebrew.page and
Prospero Store. The submission changes only `apps/PPSA99874.json`.

The record describes the experimental native OpenJDK25-backed Minecraft Java
server project, with full world startup still being validated. It does not
claim a playable client or completed server startup/save/stop. All reservation
links, artifact URL, checksum, version and license are null, following the
catalog's reservation format; no game binaries or development download are
published through this reservation.

Local `python3 -m catalog check` passes (98 records; no errors, warnings or
notices). Upstream Validate submission and Scan the release checks passed.
A separate developer-release-bump check was still running when recorded.

The reservation belongs to GitHub account `mateo-cogeanu`. Only this account
can update/release it; the catalog asks for an update at least every180days.
When a distributable build is ready, a new PR must supply its complete release
metadata and satisfy the catalog's then-current requirements. Do not overwrite
previously listed release assets.

Submission rules: https://github.com/blackbearreloaded/ps5-homebrew-catalog/blob/main/docs/submitting.md#reserving-a-title-id
