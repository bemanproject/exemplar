# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25...4.0)

project(
    beman.exemplar # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman library exemplar"
    LANGUAGES CXX
)

enable_testing()

# [CMAKE.SKIP_TESTS]
option(
    BEMAN_EXEMPLAR_BUILD_TESTS
    "Enable building tests and test infrastructure. Default: ON. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

# [CMAKE.SKIP_EXAMPLES]
option(
    BEMAN_EXEMPLAR_BUILD_EXAMPLES
    "Enable building examples. Default: ON. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

include(FetchContent)
include(GNUInstallDirs)

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    # Fetch GoogleTest
    FetchContent_Declare(
        googletest
        FETCHCONTENT_TRY_FIND_PACKAGE_MODE ALWAYS
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG v1.16.0
        FIND_PACKAGE_ARGS 1.16.0 NAMES GTest COMPONENTS gmain_main
        EXCLUDE_FROM_ALL
        SYSTEM
    )
    block()
        set(CMAKE_UNITY_BUILD ON)
        set(BUILD_GMOCK OFF)
        set(INSTALL_GTEST OFF) # Disable GoogleTest installation
        FetchContent_MakeAvailable(googletest)
    endblock()
endif()

add_subdirectory(src/beman/exemplar)

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    add_subdirectory(tests/beman/exemplar)
endif()

if(BEMAN_EXEMPLAR_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
