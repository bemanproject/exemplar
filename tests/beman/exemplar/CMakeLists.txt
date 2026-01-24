# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set(BUILD_GMOCK OFF) # not needed yet
set(INSTALL_GTEST OFF) # Disable GoogleTest installation too
find_package(GTest REQUIRED)

add_executable(beman.exemplar.tests.identity)
target_sources(beman.exemplar.tests.identity PRIVATE identity.test.cpp)
target_link_libraries(
    beman.exemplar.tests.identity
    PRIVATE beman::exemplar GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(beman.exemplar.tests.identity)
