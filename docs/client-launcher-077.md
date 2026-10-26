# Native launcher first — candidate077

The user reports that the launcher never appears on the preceding candidate
(exact075/076version not specified). Source inspection shows both waited for VM
startup, the54JAR inventory, native library setup and the C1 warmup before drawing
the launcher. No fresh console reports could be retrieved at the previous address;
this is a confirmed ordering problem, not a diagnosed crash location.

## Separation from Minecraft

The screen is drawn in native C++. Java manages the account, authentication and
menu model. Minecraft does not draw the launcher.

Candidate077 starts the native UI on its own thread after core constructors and
early AudioOut initialization, before creating the JVM. The main startup thread
waits for the first native frame/WaitVblank before starting Java. The UI continues
to draw and poll the controller while account services prepare. Navigation edges
are queued in order, including selections made before Java is ready.

All JNI calls remain on the JVM startup thread. It exchanges bounded public UI
text and button edges with the native UI through a mutex-protected mailbox.
The UI thread never uses a JNIEnv. Account startup failures leave a native failure
screen available, while logs remain retrievable.

Only after Play/demo selection does the UI close VideoOut, unmap its buffers,
release its direct memory and finish its thread. Java then requests the original
artifact inventory, configures/loads game native libraries, performs C1 warmup
and calls the unchanged Minecraft Main. Cleanup failure prevents game startup.
Account initialization still uses the native Java25runtime; it is independent of
Minecraft graphics initialization. A post-selection loading interval is expected.

## PS5 test

Install local `dist/client-startup/PPSA99874.zip`, titlePPSA99874/version01.000.077.
The native home screen should appear before VM/account initialization and show
"Preparing" briefly. Use D-pad/X, or Square for demo. Try Microsoft sign-in and
then Play after the account name appears. Confirm that game audio, controls and
world performance remain correct. If the screen fails to appear, keep the app
open for the build/session/startup/native reports. Never share live codes/tokens.

Exact075 and076 packages/symbols remain preserved in ignored dist/accepted.
User-selected icons remain active; authentication, official game files and074
performance/audio configuration are retained. No new release or Store work.

## Verification limits

The host fixture runs the actual native UI with no JVM, checks a presented frame,
controller responsiveness while account boot is blocked, ordered input, native
failure display and cleanup. A JNI fixture table checks that the actual bridge
uses the caller thread and waits for display cleanup/join. This fixture is not a
real PS5 JVM or SDK run. Actual Java bytecode confirms menu selection precedes
game inventory, LWJGL initialization, library loads, JIT warmup and original Main.

Host success does not establish visible PS5 startup, live MSA, native thread
behavior or display-to-game handoff. These remain pending console validation.

[Build record](validation/client077-native-first-build-2026-10-26.json) ·
[Sign-in instructions](client-launcher-075.md).
