# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25)

project(
    beman.{{project-name}} # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman library exemplar"
    LANGUAGES CXX
)

# [CMAKE.SKIP_TESTS]
option(
    BEMAN_{{project-name | shouty_snake_case}}_BUILD_TESTS
    "Enable building tests and test infrastructure. Default: ON. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

# [CMAKE.SKIP_EXAMPLES]
option(
    BEMAN_{{project-name | shouty_snake_case}}_BUILD_EXAMPLES
    "Enable building examples. Default: ON. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

include(FetchContent)
include(GNUInstallDirs)

if(BEMAN_{{project-name | shouty_snake_case}}_BUILD_TESTS)
    enable_testing()

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
endif()

add_subdirectory(src/beman/{{project-name}})

if(BEMAN_{{project-name | shouty_snake_case}}_BUILD_TESTS)
    add_subdirectory(tests/beman/{{project-name}})
endif()

if(BEMAN_{{project-name | shouty_snake_case}}_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
