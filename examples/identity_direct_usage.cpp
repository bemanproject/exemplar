// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/exemplar/config.hpp>
#include <beman/exemplar/identity.hpp>

#if BEMAN_EXEMPLAR_USE_MODULES()
import std;
#else
    #include <iostream>
#endif

namespace exe = beman::exemplar;

int main() {
    std::cout << exe::identity()(2024) << '\n';
    return 0;
}
