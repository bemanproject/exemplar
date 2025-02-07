# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25)

project(
    beman.exemplar # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman library exemplar"
    LANGUAGES CXX
    VERSION 0.1.0
)

enable_testing()

include(FetchContent)
include(GNUInstallDirs)

include(cmake/beman-configure.cmake)

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    # Fetch GoogleTest
    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG
            f8d7d77c06936315286eb55f8de22cd23c188571 # release-1.14.0
        EXCLUDE_FROM_ALL
    )
    set(INSTALL_GTEST OFF) # Disable GoogleTest installation
    FetchContent_MakeAvailable(googletest)
endif()

add_subdirectory(src/beman/exemplar)

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    add_subdirectory(tests/beman/exemplar)
endif()

if(BEMAN_EXEMPLAR_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

if(BEMAN_EXEMPLAR_CONFIG_FILE_PACKAGE)
    include(cmake/config-file-package.cmake)
endif()

find_package(beman.exemplar REQUIRED)
