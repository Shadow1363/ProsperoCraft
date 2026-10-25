# Original Minecraft startup038 — heap-headroom candidate

037 passes native bootstrap,reaches Datafixer/render-thread initialization,and
then reports Java heap exhaustion. The saved OOM stack is in crash-report/JAR
manifest construction,so it may mask an earlier initialization exception. Native
report/session already say FAIL despite the visible black screen. No window/menu
pass or native JVM crash is established;the30minute black-screen report is not
a measured startup duration. Exact037 ZIP/symbols and current-run reports are
preserved locally;public failure JSON contains hashes and scoped evidence.

038 raises the consumer max Java heap from128MiB to256MiB,retains16MiB initial
heap/64MiB compressed class space/SerialGC/interpreter,and enables -Xlog:gc=info.
A Java checkpoint before Main reports actual max/committed/used heap. No JVM
implementation,SDK,game JAR,renderer choice or accepted native object changes.
024failed reserving512MiB before Main;256MiB reservation/commit and later game
memory adequacy remain pending on PS5. This is an intermediate headroom test,
not a guarantee of menu startup or a repair of an unknown earlier throwable.
GC info goes to the VM logging output;actual target log availability is pending.

Install dist/client-startup/PPSA99874.zip or runtime workspace dist/PPSA99874.zip.
Same PPSA99874 replaces the current app. Launch and press X once. Observe actual
notifications/window;four harness rows are not an automatic menu pass. If it
fails or stays black,report it promptly and keep the app open for logs;after
app closure,reopen without pressing X. There is no need to wait30minutes.
Relevant reports are session.txt,exception.txt,exceptions.log and startup-tail.log.

Original Main still uses offline demo/Vulkan/1280x720 arguments and existing
writable workdir/options. All54original JARs/all5147publisher assets remain
unchanged. Exact accepted036SPIRV-Cross/035VMA/033FreeType/031STB/029GL/026OpenAL
inputs are checked;combined native game API use remains unvalidated. Application
music stays absent;old existing options are preserved.

Host launch policy/bytecode and package signatures,original artifacts/runtime,
13real groups,staged constructors/heap flags/native component identity are checked.
Historical failed-build checksum checks stream the verified compact archive when
old ZIPs are not expanded,so verification does not restore gigabytes unnecessarily.
PS5 VM reservation,window/menu/gameplay,performance/global teardown and server
two-hour endurance remain unvalidated;endurance is deferred.

Host launch policy and full package checks pass. Full local ZIP SHA-256:
`9f9a871285686b43e6abe12df66552a20f6022133646ac2452eb270dfcef93f5`.
PS5 VM256MiB reservation/commit and original game startup/menu remain pending.

Follow-up:038reserved256MiB and reached backend selection without a recorded
Java OOM,but SDL/LWJGL returned different vkGetInstanceProcAddr addresses.
Vulkan was rejected;SDL OpenGL fallback/error dialog were unsupported. Main
returned and session reported FAIL.039unifies the public loader entry. See
validation/client038-startup-failure-2026-10-25.json.
