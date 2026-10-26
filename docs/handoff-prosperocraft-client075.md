# Continue ProsperoCraft075

The human requested a native polished launcher with Microsoft login and supplied
public ID f0c7635e-8d50-4d7e-afa3-d15db4a0a3d3. Candidate075 is built locally at
dist/client-startup/PPSA99874.zip (PPSA99874). See the exact hashes, runtime commit
and checks in [build record](validation/client075-launcher-build-2026-10-26.json).
[Current guide and native previews](client-launcher-075.md).

Host auth tests use scripted credentials only. No live sign-in or console launcher
pass inferred. First test native menu navigation and Square demo handoff, then
real device-code login and Home/Play. On failure inspect current run reports and
repair within this scope. Never log or publish device secrets/tokens/responses.
Current errors are sanitized; useful future diagnostics may include fixed phase
and HTTP status only, never remote response text. Microsoft app service approval
has not been established. Public-client flow must be enabled in app registration.

UI/auth source lives in client/launcher; startup invokes it before original Main.
Returning VideoOut API is separately published in runtime de339155ba78e54be1ddc903e7df0904c866fbdb.
One installed instance and read-only settings are intentional first-version scope;
do not claim a full mod/instance manager. Tokens are memory-only. Existing074
performance/audio/settings and official game files remain unchanged. Preserve
accepted074 exact ZIP acba867efee8c503e4516a20ec4f2af69009a8ebcc647b370bd260dabed03326.
No new public release or Store publication requested. Runtime and consumer source
ownership/publication rules still apply. The002convenience ZIP was restored after
packaging; the installable075 is dist/client-startup/PPSA99874.zip and runtime/dist.
