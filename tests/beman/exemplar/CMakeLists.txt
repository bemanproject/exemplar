# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(GoogleTest)

add_executable(beman.exemplar.tests.identity)
target_sources(beman.exemplar.tests.identity PRIVATE identity.test.cpp)
target_link_libraries(
    beman.exemplar.tests.identity
    PRIVATE beman::exemplar GTest::gtest GTest::gtest_main
)

gtest_add_tests(beman.exemplar.tests.identity "" AUTO)

if(BEMAN_EXEMPLAR_INSTALL_CONFIG_FILE_PACKAGE)
    add_test(
        NAME beman.exemplar.test.config-file-package
        COMMAND
            "${PROJECT_SOURCE_DIR}/cmake/test/test.sh" "${CMAKE_COMMAND}"
            "${PROJECT_SOURCE_DIR}/cmake/test" # source dir
            "${CMAKE_CURRENT_BINARY_DIR}/cmake/test" # build dir
            "${PROJECT_BINARY_DIR}/cmake/${PROJECT_NAME}" # prefix path
    )
endif()
