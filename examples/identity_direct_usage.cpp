// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/{{project-name}}/identity.hpp>

#include <iostream>

namespace exe = beman::{{project-name}};

int main() {
    std::cout << exe::identity()(2024) << '\n';
    return 0;
}
