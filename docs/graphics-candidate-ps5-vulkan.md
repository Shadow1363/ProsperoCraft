# PS5_Vulkan client graphics candidate

The user supplied [mihawk-99/PS5_Vulkan](https://github.com/mihawk-99/PS5_Vulkan)
on2026-10-19. Reviewed main revision:
`f410e67a0241b3e8edcdbcd2a9b285dfc4a412ed`.

The [upstream README](https://github.com/mihawk-99/PS5_Vulkan/blob/f410e67a0241b3e8edcdbcd2a9b285dfc4a412ed/README.md)
describes a Mesa/RADV-based PS5 driver and VideoOut presentation, Vulkan1.4
reporting with conformance qualifications, and use by other native PS5 titles.
It also documents the earlier ps5vk backend and links its SDK/platform dependencies.
These are upstream claims, not validation by this project.

This is a promising platform candidate. It does not establish Minecraft-client
compatibility: Java/native bindings, library loading, GPU-memory/swapchain and
window/input integration, plus a renderer compatible with the selected client,
still need work. This assessment is an inference from the interfaces involved.
No driver build, SDK change or graphics dependency is adopted by this task.

The requested order is stable unmodified server, validated server mods, then
client work. Revisit and pin the driver/SDK when that client stage begins.

On2026-10-22 the user authorizes client work while deferring server endurance.
The revision above remains current at review. See [client bring-up](client-bringup.md)
and `client/graphics-candidates.json` for artifact/preflight results, dependency
pins and native integration work. No driver/SDK adoption or PS5 graphics pass
has occurred yet. The earlier server-first work order is superseded.
