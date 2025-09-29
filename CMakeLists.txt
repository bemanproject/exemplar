# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.28...4.2)

project(
    beman.exemplar # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman Library Exemplar"
    LANGUAGES CXX
    VERSION 0.1.0
)

# [CMAKE.SKIP_TESTS]
option(
    BEMAN_EXEMPLAR_BUILD_TESTS
    "Enable building tests and test infrastructure. Default: ${PROJECT_IS_TOP_LEVEL}. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

# [CMAKE.SKIP_EXAMPLES]
option(
    BEMAN_EXEMPLAR_BUILD_EXAMPLES
    "Enable building examples. Default: ${PROJECT_IS_TOP_LEVEL}. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

# for find of beman-install-library
include(infra/cmake/beman-install-library-config.cmake)

add_library(beman.exemplar INTERFACE)
add_library(beman::exemplar ALIAS beman.exemplar)

target_sources(
    beman.exemplar
    PUBLIC FILE_SET HEADERS BASE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

set_target_properties(beman.exemplar PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON)

add_subdirectory(include/beman/exemplar)

beman_install_library(beman.exemplar)

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests/beman/exemplar)
endif()

if(BEMAN_EXEMPLAR_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
