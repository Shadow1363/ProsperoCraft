# Launcher controller vibration — candidate01.000.089

[Build/checksum record](validation/client089-vibration-build-2026-10-27.json).

089 adds subtle compatible two-motor vibration to both launcher channels.
**Settings → Triangle** toggles it, with the current value shown on the left
panel and in the controller hint. The preference persists in the existing
library settings; older libraries default to ON. Reduced Motion remains a
separate visual preference. No gameplay vibration/audio policy is changed.

| Launcher event | Requested pulse |
| --- | --- |
| Focus movement | Light18ms tick |
| Confirm/change |45ms tap |
| Back/cancel |28ms tap |
| Rejected action/task failure |70ms pulse |
| Download/account completion |85ms pulse |

Feedback follows actual model changes, plus explicit task success/failure.
Unchanged focus at an edge, idle frames and download-progress updates do not
create vibration events. The existing80-field mailbox uses77for a sequence,
78for a fixed cue name and79for the saved preference. The renderer consumes
each sequence once; there is no delayed cue backlog or token/account data.

The native UI still owns and reads the controller. A launcher-only native
worker serializes motor writes on that handle, using compatible mode2 and the
two-byte ABI used by the pinned toolkit's PS5 pad implementation. Its requested128KiB
stack and5ms deadline polling keep motor stop requests independent of a busy
or blocked Vulkan render. Pulses are rate limited; only a fresh semantic event
can request another one. Durations are requested timing, not measured PS5 feel.

Opt-out, disconnect/interception, changed connection generation and stale input
cancel pending output. Events seen while unavailable are consumed rather than
replayed on reconnect. Stop/join occurs before scePadClose and the game's display/
controller handoff. JNI remains on its existing JVM-attached caller; the motor
worker makes no JNI calls. An API/mode or thread-start failure leaves launcher
and gameplay available. API errors disable further output until the controller
is disabled/re-enabled; cleanup still attempts zero motors.

`tools/test_launcher_haptics.py` exercises the actual worker with motor API
fixtures under ASan/UBSan: deadline stop while the UI does not poll, duplicate
sequences, opt-out/disconnect cancellation, stale replay rejection, zero/join
and nonfatal unsupported mode. Its Java fixture covers focus/confirm/back/error,
stable idle sequences, Settings Triangle persistence and old-library defaults.
The native preview fixture also requires zero motors before controller close.
Existing instance, auth, channel, download, Delete/Undo, navigation and lifecycle
regressions are retained. Both full target/package audits verify the actual
scePadSetVibration/Mode imports, source pairing and preserved older candidates.

Exact089PS5 checks remain pending: feel/strength of each cue, no idle/progress
buzz, rapid navigation, opt-out persistence, disconnect/reconnect/interception,
and no residual rumble after game launch or Quit/library/relaunch. Also retain
the088 animation/performance, controls/audio, worlds and Delete/Undo checklist.
No new console pass, frozen milestone, GitHub release or Store update is claimed.
