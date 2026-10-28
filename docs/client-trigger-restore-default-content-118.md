# Development118: trigger restore and non-blocking default content

A review of the115–117 client changes found two behavior gaps and one wasteful retry path. Public release117 and its Store submission are unchanged. Previous candidates and frozen passing snapshots are preserved. Java runtime source and its existing0126integration are unchanged.

## Default Controlify no longer blocks a new Fabric instance

In115–117 the default Controlify install ran inside the download task before the instance was marked ready. Any Modrinth or network failure failed the whole task, so a new Fabric instance stayed not-ready and every Play retried the download. The game and Fabric could be fully installed and still be unplayable while Modrinth was unreachable.

Default content is optional. A failure now leaves `defaultContentPending` set, logs `PS5_INSTANCE default content pending` with only the storage code, and lets the instance become ready. The launcher says Controlify could not be added and that Repair Download retries it. Cancellation still aborts the task. The offline Play/verify path stays network-free. Existing instances, user queues and later uninstall choices are unchanged.

## Adaptive triggers return after system interception

In116–117 an intercepted pad sample (PS button, system overlay) cleared the requested trigger profiles as well as the active output. Controlify sends an effect only when it changes, so resistance stayed off after returning to the game until the effect changed.

Interception now suspends output. The adapter sends OFF once and keeps the requested left/right profiles. When a connected, non-intercepted sample arrives, the requested sides are re-applied through the existing native/fallback path, including cached mode4/mode6 rejection and travel following. Close, disconnect and `PS5_JoystickClose` still clear requests completely. Sends during interception are still refused.

## One OFF attempt per state change

If the native OFF write failed (for example on a disconnected handle), the active bits stayed set and OFF was retried on every sample and poll. Reset and suspend now make one OFF attempt, log a failure once, and clear the send state, so the next real request still reaches the pad.

## Validation

- Actual SDL input adapter fixture under ASan/UBSan: interception sends OFF once, repeated intercepted polls make no further native calls, return restores the followed L2 basic effect and the R2 weapon effect without new rejections, a restored state is deduplicated, and a failed OFF is not retried per poll. Existing decode, follow, disconnect and rumble/gyro checks still pass.
- Launcher Java sources compile (host JDK21 with Gson). No end-to-end host fixture drives the live Fabric/Modrinth download task. The non-blocking failure path needs the full host suite in the build workspace and a PS5 check.
- Version tokens moved to01.000.118. No candidate package was built from this workspace, so there is no ZIP hash yet.

Pending: building candidate118, the full host/package suite, and PS5 checks of trigger restore after the PS button, a first Fabric install with Modrinth unreachable and then Repair Download, plus117regressions.
