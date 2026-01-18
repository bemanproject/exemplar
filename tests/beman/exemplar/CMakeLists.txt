# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

find_package(GTest REQUIRED)

add_executable(beman.exemplar.tests.identity)
target_sources(beman.exemplar.tests.identity PRIVATE identity.test.cpp)
target_link_libraries(
    beman.exemplar.tests.identity
    PRIVATE beman::exemplar GTest::gtest GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(beman.exemplar.tests.identity)

if(BEMAN_EXEMPLAR_INSTALL_CONFIG_FILE_PACKAGE)
    # test if the targets are usable from the install directory
    add_test(
        NAME install-to-stagedir
        COMMAND
            ${CMAKE_COMMAND} --install ${CMAKE_BINARY_DIR} --prefix
            ${CMAKE_BINARY_DIR}/stagedir --config $<CONFIG>
    )
    add_test(
        NAME find-package-test
        COMMAND
            ${CMAKE_CTEST_COMMAND} # --verbose
            --output-on-failure -C $<CONFIG> --build-and-test
            "${CMAKE_SOURCE_DIR}/examples"
            "${CMAKE_CURRENT_BINARY_DIR}/find-package-test" --build-generator
            ${CMAKE_GENERATOR} --build-makeprogram ${CMAKE_MAKE_PROGRAM}
            --build-options "-DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}"
            "-DCMAKE_CXX_STANDARD=${CMAKE_CXX_STANDARD}"
            "-DCMAKE_CXX_EXTENSIONS=${CMAKE_CXX_EXTENSIONS}"
            "-DCMAKE_CXX_MODULE_STD=${CMAKE_CXX_MODULE_STD}"
            "-DCMAKE_CXX_SCAN_FOR_MODULES=${CMAKE_CXX_SCAN_FOR_MODULES}"
            "-DCMAKE_BUILD_TYPE=$<CONFIG>"
            "-DCMAKE_PREFIX_PATH=${CMAKE_BINARY_DIR}/stagedir"
    )
endif()
