# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25)

project(
    beman.exemplar # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman library exemplar"
    LANGUAGES CXX
)

enable_testing()

option(
    BEMAN_EXEMPLAR_BUILD_TESTS
    "Enable building tests and test infrastructure."
    ${PROJECT_IS_TOP_LEVEL}
)

option(
    BEMAN_EXEMPLAR_BUILD_EXAMPLES
    "Enable building examples."
    ${PROJECT_IS_TOP_LEVEL}
)

option(
    BEMAN_EXEMPLAR_FETCH_GOOGLETEST
    "Enable downloading and building googletest from source."
    ${PROJECT_IS_TOP_LEVEL}
)

include(FetchContent)
include(GNUInstallDirs)

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    if(BEMAN_EXEMPLAR_FETCH_GOOGLETEST)
        # Fetch GoogleTest
        FetchContent_Declare(
            googletest
            GIT_REPOSITORY https://github.com/google/googletest.git
            GIT_TAG
                f8d7d77c06936315286eb55f8de22cd23c188571 # release-1.14.0
            EXCLUDE_FROM_ALL
        )
        block()
            set(INSTALL_GTEST OFF) # Disable GoogleTest installation
            FetchContent_MakeAvailable(googletest)
        endblock()
    else()
        find_package(GTest REQUIRED)
    endif()
endif()

add_subdirectory(src/beman/exemplar)

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    add_subdirectory(tests/beman/exemplar)
endif()

if(BEMAN_EXEMPLAR_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
