# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set(BUILD_GMOCK OFF) # not needed yet
set(INSTALL_GTEST OFF) # Disable GoogleTest installation too
find_package(GTest REQUIRED)

add_executable(beman.{{cookiecutter.project_name}}.tests.identity)
target_sources(beman.{{cookiecutter.project_name}}.tests.identity PRIVATE identity.test.cpp)
target_link_libraries(
    beman.{{cookiecutter.project_name}}.tests.identity
    PRIVATE beman::{{cookiecutter.project_name}} GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(beman.{{cookiecutter.project_name}}.tests.identity)
