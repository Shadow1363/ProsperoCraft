# Client Native Graphics — PS5 ALL PASS

Frozen milestone: **PPSA99874**, client **01.000.003**, human console acceptance on **2026-10-23**. The tester confirms the RGB sequence and legible final result card, with no crash or visual corruption. [Validation](validation.json) records the exact source/package pins and scope. Logs were unavailable for retrieval; the direct human report is the console evidence.

The pinned Mesa/RADV PS5 path now presents real GPU clears and a GPU-copied bitmap test card through VideoOut, with GPU pixel readback checks. This is a native-only diagnostic. It launches no Java, SDL, shader pipeline, audio or Minecraft code. Java002/LWJGL and earlier milestones remain separately preserved. Java/SDL integration, shader rendering, explicit teardown/recreation and game startup remain unvalidated. Server two-hour endurance stays deferred.

`client/` is the frozen source/pin/result snapshot. Reproduction tools live at this release tag's root. Preserve this folder and exact package; continue development outside it. Full local ZIP and symbols are retained under ignored `dist/milestones/Client_Native_Graphics-01.000.003/`.

## Download and run

Download the [Client_Native_Graphics-v01.000.003 release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Native_Graphics-v01.000.003) ZIP, `validation.json` and `SHA256SUMS`. The ZIP is the **exact full console-tested package**, unchanged and without exclusions. It contains no game/Java JARs and needs no provisioning helper.

1. Verify the ZIP with `SHA256SUMS` and extract it.
2. Install the complete `PPSA99874` folder. This shares the server/client app identity and replaces the installed app; prior packages remain available for reinstalling.
3. Open the app. Its initial screen may be blank; a system notification gives instructions. Release X after launching, then press **X once** to run.
4. Expect red/green/blue frames followed by **PS5 JAVA CLIENT 003**, **NATIVE GRAPHICS PASS** and **READBACK VERIFIED**. Confirm the visible output and automated-result notification.
5. Keep it open for logs at `http://<PS5-IP>:8765/`. After a crash, reopen without pressing X to preserve and share the prior reports.

The final swapchain stays resident until app close, preserving the result card. This is not a lifecycle teardown test. Embedded package metadata still says console pending because tested bytes were not rebuilt after acceptance; the attached validation records the subsequent pass.

Full/public ZIP SHA-256: `82895fc3d9381a08c61f979e9ba33a56943ea5f890830786c7dd4c1c684bf812`.

Next: combine the passing native graphics and Java/LWJGL paths, then SDL and shader/game rendering, with separate console validation.
