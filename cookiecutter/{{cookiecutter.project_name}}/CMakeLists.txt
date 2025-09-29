# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25)

project(
    beman.{{cookiecutter.project_name}} # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "{{cookiecutter.description}}"
    LANGUAGES CXX
    VERSION 2.2.1
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

add_library(beman.{{cookiecutter.project_name}} INTERFACE)
add_library(beman::{{cookiecutter.project_name}} ALIAS beman.{{cookiecutter.project_name}})

target_sources(
    beman.{{cookiecutter.project_name}}
    PUBLIC
        FILE_SET HEADERS
            BASE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/include"
            FILES
                "${CMAKE_CURRENT_SOURCE_DIR}/include/beman/{{cookiecutter.project_name}}/identity.hpp"
)

set_target_properties(beman.{{cookiecutter.project_name}} PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON)

find_package(beman-install-library REQUIRED)
beman_install_library(beman.{{cookiecutter.project_name}})

include(CTest)

if(BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS)
    add_subdirectory(tests/beman/{{cookiecutter.project_name}})
endif()

if(BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
