// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/{{cookiecutter.project_name}}/identity.hpp>

#include <iostream>

namespace exe = beman::{{cookiecutter.project_name}};

int main() {
    std::cout << exe::identity()(2024) << '\n';
    return 0;
}
