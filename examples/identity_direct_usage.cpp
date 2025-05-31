// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <iostream>

// Alternatively: #include <beman/exemplar/identity.hpp>
import beman.exemplar;

namespace exe = beman::exemplar;

int main() {
    std::cout << exe::identity()(2024) << '\n';
    return 0;
}
