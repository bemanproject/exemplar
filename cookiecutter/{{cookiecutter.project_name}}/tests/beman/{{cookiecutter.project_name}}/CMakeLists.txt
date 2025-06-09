# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

find_package(GTest REQUIRED)

add_executable(beman.{{cookiecutter.project_name}}.tests.identity)
target_sources(beman.{{cookiecutter.project_name}}.tests.identity PRIVATE identity.test.cpp)
target_link_libraries(
    beman.{{cookiecutter.project_name}}.tests.identity
    PRIVATE beman::{{cookiecutter.project_name}} GTest::gtest GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(beman.{{cookiecutter.project_name}}.tests.identity)
