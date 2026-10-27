# Temporary authenticated game test — 01.000.090

The user requested `Temp_gametest` to replace `codex/offline` on2026-10-27.
This branch contains the temporary legacy Mojang-client-ID login experiment for
personal testing while ProsperoCraft's own app approval remains pending. This
is a source development branch, not a ProsperoStore or GitHub release. `main`
and `codex/demo` retain their own app ID and Demo behavior. The old Offline commit
2691bed1cd3b43762d4882213124134a45850e1d is an ancestor of this branch; saved
Offline084–089 packages and frozen milestones remain available locally.

The user reported “LOG in works!!” on the preceding personal089package, SHA256
ccf692aac72ed4eeb3d91d67bce7c2fad33e0de0ae0a634ff976d08c0c91949c.
That establishes the reported sign-in result on that package. It does not establish
ProsperoCraft app approval, this090package, authenticated gameplay or downloads.

## Authentication and the full game

The branch uses legacy Live device authorization at oauth20_connect.srf, the
Xbox MBI_SSL service scope, oauth20_token.srf polling and an unprefixed legacy
RPS token. All Microsoft/Xbox/XSTS/Minecraft exchanges remain HTTPS. Minecraft
entitlement and Java profile validation remain mandatory before creating a
Session. Codes/tokens are not printed; access tokens remain memory-only and
sign-out clears the active session. No client secret or credential capture is
introduced. No refresh-token persistence or automatic account restoration.

The downloader already fetches the complete original publisher game JAR,
libraries and assets with their hashes. Demo is a launch option, not a separate
smaller game download. Existing verified26.3downloads can be reused. A missing
or corrupt file is downloaded/repaired by the existing installer. No game JAR or
asset payload is redistributed in the app package.

`PLAY FULL GAME` on the temporary channel requires an unexpired verified Session
both before preparing the launch and immediately before returning arguments.
Original Minecraft Main receives that Session's profile name, UUID and token;
`--demo`, `--disableMultiplayer` and `--disableChat` are omitted for this path.
The Java client applies its normal account/server checks. Multiplayer, chat,
account services and full-game gameplay are not claimed PS5-passing yet.
Only the supported26.3 SDL version can launch; other versions remain guarded.
The temporary build contains no offline-proof verification key or Offline action.
Preserved Offline builds retain their previous policy.

## Instance deletion

Runtime patch0122 fixes Files.move failing with “Is a directory” before rename.
The PS5 write-access preflight opened a directory with O_WRONLY; this rejects
directories with EISDIR. The PS5-only change lets real rename enforce permissions.
The existing library Trash archive, Undo, metadata rollback and interrupted-move
reconciliation remain. No world copying, recursive deletion or destructive
fallback is added. Shared caches and account data stay outside the archive.
The runtime fix is maintained in ps5-java25-homebrew, not in a game-class patch.

## Validation and console checklist

Host checks cover actual legacy auth polling/failures, entitlement rejection,
profile validation, cancellation/redaction; complete publisher install/cache
repair, existing world retention, authenticated arguments, missing/expired/
signed-out sessions, Demo isolation; Delete/Undo and restart recovery in all
three historical/current channel fixtures; and the actual runtime UnixFileSystem
move implementation with the failing directory access preflight injected.
The target java.base build and the090target app/package audits are recorded in
[the validation record](validation/client090-temp-gametest-build-2026-10-27.json).
Host fixtures do not establish PS5 success.

On PS5: sign in again, download or verify a26.3instance, launch the full game,
check your account identity and an existing world, return to the launcher and
sign in again after its fresh-process restart. Check Delete Instance → Cancel,
confirm another disposable instance deletion, Triangle Undo, and restart Undo.
Do not use your only world as the first deletion test. Check existing UI motion,
vibration, graphics/audio and quit/relaunch. Full gameplay, multiplayer/chat,
actual download completion, deletion/Undo and lifecycle remain pending for090.
Same PPSA99874 identity and4GiBdownload storage; installation replaces the existing
app. Existing data paths and game JAR bytes remain unchanged. No new ALL PASS
milestone, Store update or release asset is created.
