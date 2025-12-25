# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.28...4.2)

project(
    beman.{{cookiecutter.project_name}} # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "{{cookiecutter.description}}"
    LANGUAGES CXX
    VERSION 0.1.0
)

# [CMAKE.SKIP_TESTS]
option(
    BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS
    "Enable building tests and test infrastructure. Default: ${PROJECT_IS_TOP_LEVEL}. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

# [CMAKE.SKIP_EXAMPLES]
option(
    BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_EXAMPLES
    "Enable building examples. Default: ${PROJECT_IS_TOP_LEVEL}. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

# for find of beman-install-library
set(CMAKE_PREFIX_PATH ${CMAKE_CURRENT_SOURCE_DIR}/infra/cmake)

add_subdirectory(src/beman/{{cookiecutter.project_name}})

if(BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests/beman/{{cookiecutter.project_name}})
endif()

if(BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
