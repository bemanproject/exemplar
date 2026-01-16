#include <iostream>

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
