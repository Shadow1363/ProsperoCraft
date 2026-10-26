# Client065 — explicit uncompressed direct-backed heap

064 crashed immediately after X. Matching run
`client-01.000.064-1793012432-698835298` never reached Minecraft: anonymous
384MiB reservations failed with ENOMEM12,andVMinitialization aborted with
"Could not reserve enough space for393216KB object heap". The native trace
records VMABORT and exit1 even though the separate abort-note placeholder says
no abort captured. [Hashed evidence](validation/client064-startup-failure-2026-10-26.json).
The earlier063world attempt instead started successfully then hit a real Java
heap OOM during chunkgeneration. Those are distinct failures.

The reusable fix lives in the Java repository as patch0118,not in game classes.
After ordinary reservation fails withENOMEM,a nonexecutable,unhinted Java heap
may use PS5 direct memory **only when compressed object pointers are disabled**.
Its512MiB heap budget is separate from the unchanged256MiB native/metadata budget.
The kernel can still refuse allocation;budgets are limits,not promises of memory.
Fixed/hinted,compressed-oop,executable and file-backed heaps retain their paths.

Direct backing is zeroed and initiallyPROT_NONE. The existing PS5mprotectcommit
path enables owned subranges. Uncommit zeroes unused owned subranges and protects
them without replacing their direct mapping. Only the exact whole reservation
may release physical backing;short/interior heap releases are refused. Failed
cleanup retains ownership/budget. NMT reservation and native trace records identify
the real path. This does not increase privileges or change the SDK.

065 requests `-Xmx512m -XX:-UseCompressedOops` with the existing16MiB initial heap,
SerialGC,compact headers and interpreter mode. Disabling compressed pointers
increases object-reference storage,so512MiB does not translate into twice the
previous effective capacity. Actual heap startup,commit/GC and world sufficiency
remain console validation items. Interpreter world generation can remain slow;
this is not a JIT or frame-rate fix.

The063temporary controls and menu-idle policy,062OpenALconfiguration and390sample
bounded observer are retained. All54originalJARs and5147assetobjects remain intact.
No world files are deleted/reset;the ordinary demo flow retries the existing data.
Exact064failed bytes/symbols/source/build/report records are preserved locally.
Accepted062/063packages and all frozen milestones/server fallbacks remain intact.

Host ASan/UBSan tests exercise actual reservation and ownership functions over
fault-controlled OS fixtures:320MiBalignment/zero/PROT_NONE/subrangeuncommit and
recommit,adjacentdata,NMT,compressed/fixed/exec/error/ordinarysuccess gates,separate
budgetexhaustion,rollbackandcleanupfailure. Existing metadata,class-space,native
allocation/concurrency and direct-thread-stack tests pass. TargetHotSpot builds.
These fixtures are not PS5memory emulation or actualconsoleacceptance.
Thehost512MiBexplicitlyuncompressed occupancy model retains224MiB of arrays plus
512MiBtransientchurn with contentsintact;the256MiBcontrol getsrealheapOOM.
That is not a Minecraftbenchmark or world-fitguarantee.

Install065,pressXonce,andcheckwhetheritnowgetsbacktothemenu.Thenretrydemo
loadingandreportactualprogress/time/worldappearance.Ifstartupfailsorloading
stops,reopenwithoutXandkeepitopenforcurrentreports. Do notreset/deleteworlds.
Worldplay,controlsincapturedmode,save/reload,speakeroutputandstabilityremainpending.
No new release or Store publication is made for this development candidate.

Reproducibility note: relinking unchanged core libraries regenerated only their
16-byte GNU build-ID descriptors. The package check parses the exact ELF note
shape and verifies every other byte against frozen023. New HotSpot bytes are
checked against the current runtime build. Core module image and game JARs stay
unchanged.

## Candidate package

TitlePPSA99874,version01.000.065. LocalZIP:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/dist/PPSA99874.zip`

SHA256 `a85c900937525c04cbae29c1a3f3018e3341e07f0ae6a85a14c733564ad3461a`.
Runtimeimplementation44fdf26ccb74cf8dd9127f1256b85416856981de.
Actualconsoleheapstartup/commit/GC/worldloadingremainpending.
