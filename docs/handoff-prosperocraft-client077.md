# Continue candidate077

The user says the GUI never appears and explicitly requires separation from MC
graphics startup. Exact failing075/076 build not specified. Previously the GUI
was native C++ but invoked from Java after artifact scan/native setup/C1 warmup.
Current console reports were unreachable at the last known LAN address; do not
invent a current-run failure location. Candidate077 fixes the confirmed ordering.

[Architecture, tests and PS5 guide](client-launcher-077.md).
[Exact build/check record](validation/client077-native-first-build-2026-10-26.json).

Native UI owns VideoOut/controller on a pthread. After its first frame/WaitVblank,
the original startup thread creates Java and runs ClientStartup25. All JNI calls
remain on that startup thread; a mutex mailbox carries bounded text and input.
Java model/auth runs before inventory/native loads/C1/gameMain. gamePreflight is
a new fourth JNI binding that calls run_test(2) after menu closure. The native main
runs0, starts/waits native frontend, then1/3; it does not run2before the menu.
UI shutdown closes/unmaps/releases, publishes result, joins before game preflight.
On Java boot failure the native UI shows a failure state and stays alive for logs.
No MC GPU/SDL/OpenAL library initialization is authorized before selection.
Early raw AudioOut initialization remains on original startup thread before VM,
as on the accepted074; core constructors still precede UI thread creation.

Current native UI/threading/real MSA/handoff/audio/gameplay require PS5 tests.
Host tests are fixtures, not console acceptance. No milestone/release/Store claim.
Keep source changes in consumer; runtime API remains de339155ba78e54be1ddc903e7df0904c866fbdb.
Preserve074accepted bytes plus075/076candidates/symbols. Credentials stay memory-only;
no raw auth responses, live codes or tokens in reports/public commits. Public ID
f0c7635e-8d50-4d7e-afa3-d15db4a0a3d3 remains configured.
