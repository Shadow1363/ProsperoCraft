# Client Vulkan Bindings 01.000.007 — sampled tracing and precise checkpoints

The saved client006 run (`client-01.000.006-1792786365-412794498`) was retrieved on2026-10-24 after reopening the app. Row8 completed its three GPU copy/fill/readback cycles and cleanup. Row9 initialized the Vulkan loader and reached its create-instance checkpoint, then remained running. No Java exception was captured. That checkpoint preceded original VK10 class initialization, the native instance call and VkInstance capability construction, so the reports do not identify which of these stopped progressing.

The VM trace contained1,240,257 lines (66.2MiB), including428,532 metadata lines and537,176 native-call lines. The probe still enabled verbose native tracing during VM startup and left runtime ENTER/DONE checkpoint sampling disabled. These diagnostics synchronously open, append and close the trace file, adding substantial avoidable IO to startup and class loading. This is a concrete source of overhead; it does not prove that logging alone caused the stall.

Client007 uses the runtime's existing `ps5_vm_set_metadata_interval(4096)` control before VM creation and quiet native-call context recording during VM startup, as already used for later fixture calls. The runtime retains last-stage and native-call context; failure/signal messages remain unsampled. Runtime code/SDK and upstream Vulkan/game JARs are unchanged. This changes only the consumer probe's diagnostic policy. Frozen000–004 and exact005/006 packages remain preserved.

The fixture now reports monotonic timestamps and separate checkpoints before/after original VK10 initialization, after vkCreateInstance, after VkInstance capability construction, after vkCreateDevice and after VkDevice capability construction. The earlier message claiming those tables were initialized before their construction is corrected. No Vulkan command is substituted, no capability table is trimmed, and no verification is disabled.

Install **PPSA99874 01.000.007** from `dist/client-vulkan/PPSA99874.zip` (also runtime workspace `dist/PPSA99874.zip`). Run all ten rows in order. Row9 still performs12 real GPU transfer/readback checks and three instance/device lifecycles; row10 destroys the JVM. If row9 does not finish after about a minute, preserve its displayed stage and reopen without running more rows so the saved reports can be collected. This is a diagnostic stopping point, not a validated completion-time guarantee.

Host Java25 Xint/XcheckJNI/verification, real LWJGL core UBSan and physical MoltenVK GPU checks pass. Target packaging and frozen-artifact checks are recorded in `client/vulkan/status.json` after packaging. All ten PS5 rows require new console validation. No new milestone or release is established. SDL, shaders, game startup and the deferred server two-hour run remain unvalidated.

## Subsequent console result

007 failed row2 before JVM entry with ENOSPC while writing its trace header. See [008 storage recovery](client-vulkan-bindings-008.md). No new Vulkan result was obtained.
