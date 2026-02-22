// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#ifdef BEMAN_HAS_IMPORT_STD
import std;
#else
#include <iostream>
#endif

#ifdef BEMAN_HAS_MODULES
import beman.exemplar;
#else
#include <beman/exemplar/identity.hpp>
#endif

int main() {
    beman::exemplar::identity id;

    int x = 42;
    int y = id(x); // y == 42

    std::cout << y << '\n';
    return 0;
}
