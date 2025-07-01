# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

find_package(GTest REQUIRED)

add_executable(beman.{{cookiecutter.project_name}}.tests.identity)
target_sources(beman.{{cookiecutter.project_name}}.tests.identity PRIVATE identity.test.cpp)
target_link_libraries(
    beman.{{cookiecutter.project_name}}.tests.identity
    PRIVATE beman::{{cookiecutter.project_name}} GTest::gtest GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(beman.exemplar.tests.identity)

# test if the targets are usable from the install directory
add_test(
    NAME install-to-stagedir
    COMMAND
        ${CMAKE_COMMAND} --install ${CMAKE_BINARY_DIR} --prefix
        ${CMAKE_BINARY_DIR}/stagedir
)
add_test(
    NAME find-package-test
    COMMAND
        ${CMAKE_CTEST_COMMAND}
        # --verbose
        --output-on-failure -C $<CONFIG> --build-and-test
        "${CMAKE_SOURCE_DIR}/examples"
        "${CMAKE_CURRENT_BINARY_DIR}/find-package-test" --build-generator
        ${CMAKE_GENERATOR} --build-makeprogram ${CMAKE_MAKE_PROGRAM}
        --build-options "-DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}"
        "-DCMAKE_CXX_STANDARD=${CMAKE_CXX_STANDARD}"
        "-DCMAKE_BUILD_TYPE=$<CONFIG>"
        "-DCMAKE_PREFIX_PATH=${CMAKE_BINARY_DIR}/stagedir"
)
