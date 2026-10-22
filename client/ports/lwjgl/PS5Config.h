/* LWJGL platform configuration adapted from its BSD-licensed configuration.
 * Copyright LWJGL. All rights reserved. See LICENSE.md. */
#pragma once
#include <stddef.h>
#include <stdint.h>
#define DISABLE_WARNINGS() _Pragma("GCC diagnostic push")
#define ENABLE_WARNINGS() _Pragma("GCC diagnostic pop")
#define JNIEXPORT_CRITICAL static
#define CRITICAL(function) _JavaCritical_##function
