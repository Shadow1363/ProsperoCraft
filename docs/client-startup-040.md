# ProsperoCraft client040 — layerless Vulkan discovery

The saved039 exceptions.log identifies check4's concrete blocker:
VulkanInstance.getSupportedValidationLayers receives VK_ERROR_LAYER_NOT_PRESENT
when enumerating layers. The previous loader pointer mismatch is no longer
reported. Main cannot create a graphics backend and returns;the harness correctly
reports failure. Full exceptions.log was saved;session/startup reports became
unreachable before retrieval. No successful menu is inferred.

The resident native wrapper implements loader-owned discovery for its actual
configuration:no installed instance layers. Both count and fill queries return
VK_SUCCESS/count0 without writing properties. Named-layer extension queries and
instance creation requesting layers return VK_ERROR_LAYER_NOT_PRESENT;layers
are never silently enabled or ignored. Queries for driver extensions,layerless
instance creation and other GPU commands still use the real resident ICD.
Self lookup returns the same public loader entry used by SDL and LWJGL.

Original Minecraft/LWJGL JARs,256MiB heap and all previously accepted native
components stay unchanged. Frozen milestones and exact failed039 package/symbols
are preserved. No validation layer implementation is claimed.

Checks:

```sh
python3 tools/test_sdl_loader_identity_host.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

The UBSan host test compiles the actual loader wrapper and PS5 SDL loader hook
with host symbol adaptation,using real MoltenVK underneath. It checks empty
count/fill discovery with untouched property guards,missing-layer rejection,
self/unknown lookups,SDL pointer identity,real extension discovery and physical
GPU enumeration/instance destruction. A raw-loader pointer negative control
reproduces038. Host graphics success does not validate PS5 RADV integration.
Package checks cover original54JARs/5147assets,exact runtime,accepted native
inputs,resident groups/constructors,branding,signatures and preserved packages.

Install dist/client-startup/PPSA99874.zip or runtime dist/PPSA99874.zip,launch
and press X once. Observe actual screen/menu;report failure promptly and keep
open for logs. If it crashes,reopen without pressing X. Main returning does not
count as menu success. PS5 instance creation,window/rendering/menu,broader GPU
API coverage,game memory/performance/network services and teardown remain pending.
Server two-hour endurance remains deferred.

Host loader/launch-policy and full-package checks pass. Full local ZIP SHA-256:
`3950044b662911773ad5d262174b873d7bd48ab44e3e532086880430f94265b5`.
PS5 console integration remains pending.
