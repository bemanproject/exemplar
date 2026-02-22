# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.30...4.3)

include(./cmake/prelude.cmake)

project(
    beman.exemplar # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman Library Exemplar"
    LANGUAGES CXX
    VERSION 0.1.0
)

# Modules opt in only on compilers that support it: msvc, g++-15 and clang-20+
include(./cmake/cxx-modules-rules.cmake)

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

option(BEMAN_EXEMPLAR_BUILD_SHARED "Build exemplar as shared library" OFF)
if(BEMAN_EXEMPLAR_BUILD_SHARED)
    set(BUILD_SHARED_LIBS ON)
endif()

#===============================================================================
if(BEMAN_USE_MODULES)
    # Require C++20 or newer with extensions for modules!
    set(CMAKE_CXX_EXTENSIONS ON)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    set(CMAKE_CXX_VISIBILITY_PRESET hidden)
    set(CMAKE_VISIBILITY_INLINES_HIDDEN TRUE)
    # XXX add_library(beman.exemplar src/identity.cpp)
    add_library(beman.exemplar)
    target_compile_definitions(beman.exemplar PUBLIC BEMAN_HAS_MODULES)
    set_target_properties(
        beman.exemplar
        PROPERTIES
            VERSION ${PROJECT_VERSION}
            SOVERSION ${PROJECT_VERSION_MAJOR}
            DLL_NAME_WITH_SOVERSION TRUE
    )
    add_library(beman::exemplar ALIAS beman.exemplar)
endif()

if(BEMAN_USE_MODULES AND BEMAN_HAS_IMPORT_STD)
    target_compile_definitions(beman.exemplar PUBLIC BEMAN_HAS_IMPORT_STD)
    set_target_properties(beman.exemplar PROPERTIES CXX_MODULE_STD ON)
elseif(BEMAN_USE_MODULES)
    message(WARNING "Missing or disabled support for CMAKE_CXX_MODULE_STD!")
endif()
#===============================================================================

add_library(beman.exemplar_headers INTERFACE)
add_library(beman::exemplar_headers ALIAS beman.exemplar_headers)
target_sources(
    beman.exemplar_headers
    PUBLIC FILE_SET HEADERS BASE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

add_subdirectory(include/beman/exemplar)

#===============================================================================
# NOTE: this must be done before tests! CK
include(./cmake/beman-install-library.cmake)
beman_install_library(${PROJECT_NAME} TARGETS ${PROJECT_NAME} beman.exemplar_headers #
    # MAYBE: VERSION_SUFFIX
    # TODO(CK): DEPENDENCIES [===[beman.inplace_vector 1.0.0]===] [===[beman.scope 0.0.1 EXACT]===] fmt
)
#===============================================================================

enable_testing()

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    add_subdirectory(tests/beman/exemplar)
endif()

if(BEMAN_EXEMPLAR_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
