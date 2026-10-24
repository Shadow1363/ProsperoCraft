# Original Minecraft Client Startup 01.000.024 — first attempt

024 invokes the original26.3 `net.minecraft.client.main.Main.main` through a
consumer harness. The downloaded client JAR and all54 original Java artifacts
remain hash-identical. No game classes/bytecode are replaced or instrumented.
The existing explicit LWJGL PS5 dependency port and genuine resident graphics/
SDL/shaderc providers are configured for game execution for the first time.
Other native dependencies are incomplete;this build may fail before a window.
This is a startup attempt,not a demonstrated menu or gameplay milestone.

All5,147original asset objects (484,894,038bytes) are staged with the pinned
publisher index34;every object matches its size and SHA1. The asset index hash
and all Java artifact SHA256pins are checked. Audio assets remain present as
original data;PS5 OpenAL/audio support is not implemented or claimed. The app
has no background music;new demo options default music/master volume to zero
and existing options are preserved.

Four rows initialize the embedded runtime,create a real interpreter VM,verify
client artifacts and call original Main. Prior graphics probes are not run or
used to claim client startup success;their exact passing packages stay frozen.
The maximum Java heap is512MiB and compressed class space64MiB for client
bootstrap. Shared runtime image/native libraries,JVM/SDK implementation and
the paired consumer C++ allocation providers remain unchanged.

Launch arguments use supported offline demo settings:PS5Probe identity,a
consistent offline UUID,placeholder access token0,version26.3,graphics backend
vulkan,1280x720,and disabled multiplayer/chat. No account credentials are used
and no EULA is automatically accepted. These are demo startup parameters,not
an authenticated game session or promise that the client makes no network calls.
Game data is isolated under `/download0/mc-client`;assets are read from the
packaged hashed tree. Desktop native libraries are not substituted for PS5.

System.out/err are redirected to `/download0/java25-exceptions.log`,available
through the existing `/exceptions.log` endpoint. Log4j also writes bounded
`/download0/mc-client/logs/latest.log` and console output. Original Main may
catch its own failures and invoke System.exit;the native exit callback records
VM EXIT,and current session may remain RUN after a process exit. Reopen without
pressing X to retrieve the failure. An original Main return is not an automatic
menu PASS;the harness reports it for manual/log review.

Host validation checks writable folder creation,preservation of existing options,
demo/credential-free launch policy,and the original JAR hash. A separate host
process invokes the actual original Main with real assets/arguments and reaches
native-library bootstrap,then exits at expected missing host natives. No host
menu or PS5 startup pass is inferred. Existing native limitations include full
SDL callbacks/libffi,STB,FreeType,VMA,SPIRV-Cross,OpenAL and other client paths;
which one blocks actual PS5 startup must be observed in the run's logs.

Install PPSA99874 **01.000.024** from the runtime workspace's current
`dist/PPSA99874.zip` (consumer path `dist/client-startup/PPSA99874.zip`). This
full local package includes original assets/JARs and replaces the shared-ID
server/client app. Wait for Client024 ready,release X and press X once.
The screen may remain blank during startup. This build does not ask for the
old graphics/controller checklist. Report whether an actual Minecraft window/
loading screen/menu appears,or the error notification. If it fails,leave it
open;if it exits/crashes,reopen without pressing X. The existing read-only log
server listens on available interfaces with no preset IP/client filter. Safari
native UI can retrieve reports when shell access is blocked on this Mac.

Actual menu/rendering,input mapping,authenticated play,world startup,full native
coverage/global teardown and endurance remain unvalidated. Camera work is
superseded for this step by the user's explicit startup request. Server two-hour
endurance stays deferred. Public source excludes downloaded assets/JARs,caches,
logs and compiled packages;no release/milestone is frozen before console acceptance.

Target package verification passes:CRC/signatures,all54 original JAR SHA256s,
all5147original asset hashes/sizes,pinned index,exact023 runtime image/native
libraries,359+4+5 staged constructors/5real resident groups,paired C++ allocator,
actual Main invocation/four-row/log config and preserved022/023 packages.
PS5 startup/menu validation remains pending. Package SHA-256: `95a48cfddca9cadc10c7121959b52db71daff93b68ec0da4d5189b03b4a9ca3d`.

Console follow-up2026-10-24:024 aborted while creating the VM,with512MiB
heap reservation refused (`errno=12`);original Main was never reached.
See [025 correction](client-startup-025.md). The original package/symbols are
preserved as failed evidence,not a passing milestone.
