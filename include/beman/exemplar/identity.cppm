// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// identity.cppm
module;

#ifdef BEMAN_HAS_IMPORT_STD
import std;
#else
#include <utility>
#endif

export module beman.exemplar;

export namespace beman::exemplar {

struct __is_transparent;

struct identity {
    template <class T>
    constexpr T&& operator()(T&& t) const noexcept {
        return std::forward<T>(t);
    }

    using is_transparent = __is_transparent;
};

} // namespace beman::exemplar
