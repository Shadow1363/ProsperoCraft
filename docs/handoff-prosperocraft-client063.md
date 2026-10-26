# Current ProsperoCraft handoff — client063

Continue existing files/history. Read both AGENTS.md and the complete054 handoff
for historical/release requirements. No subagents or deferred server endurance run.
The goal remains a polished playable native Java25 PS5 Minecraft client.

062 reached the visible menu and is a full GitHub release:
https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Menu-v01.000.062
Preserve accepted062 ZIP/symbols/source and tag; no formal full-client ALL PASS.
The user then requested temporary controls and a fix for gradual menu lag, with
upstream Controlify preferred once compatible loaders/native APIs are ready.

## Current candidate

PPSA99874, client01.000.063. Full local package:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/dist/PPSA99874.zip`.
Matching consumer `dist/client-startup/PPSA99874.zip`.
SHA256 a1c62a8a6ccc8554c77ea3166633545fd08da6ca2b8e1ebffaf0c843677545f0.
Symbols `build/client-startup-probe/bootstrap-01.000.063-symbols.elf`.
[Build validation](validation/client063-build-2026-10-26.json).
Host startup/observer/logging/Main-boundary, real enum codec/options migration,
ASan/UBSan actual temporary adapter SDL/OS fixtures, shared pad initialization,
target SDL/native compile/link/SELF and full package checks pass. All54original
JARs/5147assets unchanged. Exact062 checksum verified after build;002 convenience
ZIP restored. Runtime/image/SDK/heap/interpreter unchanged. No new release/Store.

## Implementation and evidence

Read [controls063](client-controls-063.md) and
[hashed062analysis](validation/client062-menu-analysis-2026-10-26.json).
Raw062reports remain local in runtime logs/client062-menu-20261026, matching
client-01.000.062-1793009308-660533772. Human: no controls; menu starts normal then
gets laggier. Video PumpEvents was empty. Vanilla handles keyboard/mouse events,
not joystick mapping. Late main samples are parked in original frame limiter.
Original source bytecode: default AFK ->30FPS after60s/10FPS after600s without
input. Applied reason/FPS not measured; source-informed likely contributor.
Separate full SerialGC pauses286–403ms roughly16.3s,~172MiB live after full;
not proof of a leak. No heap/GC/JIT speculative tuning in063.

SDL ps5_temporary_input.h is explicitly enabled by startup SDL hint
PS5_TEMPORARY_CONTROLS, optional -Dps5.temporaryControls=0. Uses normal internal
SDL_SendKeyboardKey/MouseButton/Motion state/event functions. D-pad/left stick
menu arrows;XEnter,CircleEscape,TriangleTab,SquareBackspace. In relative captured
mode:left stickWASD,XSpace,TriangleE,right stickrelative look,R2/L2mouse buttons.
No visible menu pointer/text keyboard/rebinding/full controller UX. Buffered
short taps;launch-held button suppression;navigation repeat;release on system
interception/disconnect/focus loss;look delta cap;no idle keepalive. SDL gamepad
init disables/release bridge;futureControlify should explicitly disable it too.
Raw joystick driver retained;pad_open idempotent shares handles. Gameplay,
focus/reconnect and real event behavior need exact-console validation.

prepareWork migrates ONLY inactivityFpsLimit to JSON string minimized. Existing
options backup once options.before-menu063.txt;other bytes preserved. Original
Minecraft codec accepts value. New files get it directly. Minimization and60FPS
out-of-level menu cap stay;no FPS guarantee or GC fix. Game JARs never altered.

## Next console test and continuing work

Install063,pressXonce,release during loading. Test D-pad/left-stick menu focus,
Xselect,Circleback,TriangleTab;check held-input release when shell takes focus.
Leave idle2–3minutes and compare animation/responsiveness with fresh menu;10+
minutes can test prior long-idle cap. Note periodic pauses,crash/stuck input.
Do not infer controls/smoothness/world/play/save/audio/stability from host tests.
If failure,reopen withoutX,retrieve current build/session/reports before rerun.
Read-only Safari downloads work at known runtime-provided target;derive fresh AX
indices,Option-click links,strict completed basenames/newmtime/run identity.
Do not bake any IP/filter into inbound apps. Raw logs stay local;publish hashes
and interpretations only. Repair supported issues;new changed console candidates
advance version and preserve preceding exact artifacts before replacement.

## Storage and publication

037–061failures are losslessly archived with per-file hashes in
`dist/archives/failed-client-builds-client037-061.tar.zst` plus JSON. Earlier private
archives remain. Package tests verify named archives without expansion. See
[storage](local-storage.md);restore only needed members,not whole19.3GBbatch.
Verified release-download/extracted-kit and duplicate build-symbol copies were
removed;current dependencies/staging/logs/frozen milestones/062accepted remain.
Do not recreate excess copies or indiscriminately deleteSDK/JDK/native objects.
Current disk~28GiBfree. Source changes belong consumer Git;commit/push and verify.
Runtime edits only through runtime sync_github.py;none in063. Keep source ownership.
Current063 is development only;publication record/README must retain pending
console scope and062full release. Any future linked binary release needs a fresh
matching OpenAL source/relink kit INCLUDING current native inputs,complete pinned
JAR+asset provisioning,reconstruction/corruption checks,notices/hashes and exact
human acceptance. No Store/catalog work requested;preserve server fallbacks and
all frozen validation snapshots. Product goal extends well beyond this menu.

## Superseding063console result

Human confirms controls work and menu behavior improved;demo-world loading stalled.
Actual matching reports capture Java heap OOM during chunk generation. See
docs/validation/client063-world-failure-2026-10-26.json and client-world-064.md.
Exact063full ZIP/symbols/build/console records independently preserved in
dist/accepted/Client_Controls-01.000.063. Current development continues064;no new
formalALLPASS or release. Do not discard063because itsworld test failed.
