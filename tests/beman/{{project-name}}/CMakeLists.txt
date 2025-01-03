# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(GoogleTest)

add_executable(beman.{{project-name}}.tests.identity)
target_sources(beman.{{project-name}}.tests.identity PRIVATE identity.test.cpp)
target_link_libraries(
    beman.{{project-name}}.tests.identity
    PRIVATE beman::{{project-name}} GTest::gtest GTest::gtest_main
)

gtest_add_tests(beman.{{project-name}}.tests.identity "" AUTO)
