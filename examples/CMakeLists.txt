# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25...4.1)

project(
    beman.exemplar.examples
    DESCRIPTION "Examaples for Beman implementation of exemplar"
    LANGUAGES CXX
    VERSION 2.1.1
)

if(PROJECT_IS_TOP_LEVEL)
    set(_find_package_option REQUIRED)

    # see Professional CMake Chapter 40. Making Projects Consumable
    option(CHECK_PROJECT_IS_CONSUMABLE NO)
    if(CHECK_PROJECT_IS_CONSUMABLE)
        set(_find_package_option)
    endif()

    find_package(beman.exemplar 2.1.1 EXACT ${_find_package_option})
    if(NOT TARGET beman::exemplar)
        add_subdirectory(.. exemplar_src)
    endif()

    enable_testing()
endif()

set(ALL_EXAMPLES identity_direct_usage)

# Example `identity_as_default_projection` need ranges support:
include(CheckCXXSymbolExists)
check_cxx_symbol_exists(__cpp_lib_ranges "ranges" HAS_RANGES)

if(HAS_RANGES)
    list(APPEND ALL_EXAMPLES identity_as_default_projection)
else()
    message(
        WARNING
        "Missing range support! Skip: identity_as_default_projection"
    )
endif()

message(STATUS "Examples to be built: ${ALL_EXAMPLES}")

foreach(example ${ALL_EXAMPLES})
    add_executable(beman.exemplar.examples.${example})
    target_sources(beman.exemplar.examples.${example} PRIVATE ${example}.cpp)
    target_link_libraries(
        beman.exemplar.examples.${example}
        PRIVATE beman::exemplar
    )
    add_test(
        NAME beman.exemplar.examples.${example}
        COMMAND $<TARGET_FILE:beman.exemplar.examples.${example}>
    )
endforeach()
