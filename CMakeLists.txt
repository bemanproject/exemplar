# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.30...4.3)

include(infra/cmake/enable-experimental-import-std.cmake)

project(
    beman.exemplar
    DESCRIPTION "A Beman Library Exemplar"
    LANGUAGES CXX
    VERSION 2.4.0
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

option(BEMAN_EXEMPLAR_USE_MODULES "Provide beman.exemplar as a C++ module" OFF)

if(BEMAN_EXEMPLAR_USE_MODULES)
    set(CMAKE_CXX_SCAN_FOR_MODULES ON)
endif()

configure_file(
    "${PROJECT_SOURCE_DIR}/include/beman/exemplar/config_generated.hpp.in"
    "${PROJECT_BINARY_DIR}/include/beman/exemplar/config_generated.hpp"
    @ONLY
)

# for find of beman_install_library and configure_build_telemetry
include(infra/cmake/beman-install-library.cmake)
include(infra/cmake/BuildTelemetryConfig.cmake)

if(BEMAN_EXEMPLAR_USE_MODULES)
    add_library(beman.exemplar STATIC)
else()
    add_library(beman.exemplar INTERFACE)
endif()
add_library(beman::exemplar ALIAS beman.exemplar)

if(BEMAN_EXEMPLAR_USE_MODULES)
    target_sources(
        beman.exemplar
        PUBLIC
            FILE_SET CXX_MODULES
            FILE_SET HEADERS
                BASE_DIRS
                    "${CMAKE_CURRENT_SOURCE_DIR}/include"
                    "${CMAKE_CURRENT_BINARY_DIR}/include"
    )
    set_target_properties(beman.exemplar PROPERTIES CXX_MODULE_STD ON)
    target_compile_features(beman.exemplar PUBLIC cxx_std_23)
else()
    target_sources(
        beman.exemplar
        PUBLIC
            FILE_SET HEADERS
                BASE_DIRS
                    "${CMAKE_CURRENT_SOURCE_DIR}/include"
                    "${CMAKE_CURRENT_BINARY_DIR}/include"
    )
    set_target_properties(
        beman.exemplar
        PROPERTIES VERIFY_INTERFACE_HEADER_SETS ${PROJECT_IS_TOP_LEVEL}
    )
endif()

add_subdirectory(include/beman/exemplar)

beman_install_library(beman.exemplar TARGETS beman.exemplar)
configure_build_telemetry()

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests/beman/exemplar)
endif()

if(BEMAN_EXEMPLAR_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
