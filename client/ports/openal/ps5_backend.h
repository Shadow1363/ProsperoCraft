/* SPDX-License-Identifier: LGPL-2.0-or-later */
#pragma once
#include "alc/backends/base.h"
struct Ps5BackendFactory final : BackendFactory {
    auto init() -> bool final;
    auto querySupport(BackendType type) -> bool final;
    auto enumerate(BackendType type) -> std::vector<std::string> final;
    auto createBackend(gsl::not_null<DeviceBase*> device,BackendType type) -> BackendPtr final;
    static auto getFactory() -> BackendFactory&;
};
