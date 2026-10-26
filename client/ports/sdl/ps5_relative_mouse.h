/* SPDX-License-Identifier: MIT
 * PS5's stick-driven mouse has no OS cursor to capture. SDL owns the mode,
 * focus, state and event routing; the temporary adapter supplies real deltas.
 * Returning success permits SDL to retain the requested relative-mode flag.
 */
static bool PS5_SetRelativeMouseMode(bool enabled)
{
    SDL_Log("PS5 software mouse relative mode %s",enabled?"enabled":"disabled");
    return true;
}
