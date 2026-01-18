# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.28...4.2)

project(beman.exemplar.example LANGUAGES CXX)

if(PROJECT_IS_TOP_LEVEL)
    if(NOT DEFINED CMAKE_CXX_STANDARD)
        set(CMAKE_CXX_STANDARD 23)
        set(CMAKE_CXX_EXTENSIONS YES)
        set(CMAKE_CXX_STANDARD_REQUIRED YES)
    endif()
    if(NOT DEFINED BEMAN_HAS_MODULES)
        set(CMAKE_CXX_SCAN_FOR_MODULES OFF)
    endif()

    find_package(beman.exemplar REQUIRED)

    enable_testing()
endif()

set(ALL_EXAMPLES identity_direct_usage)

if(BEMAN_HAS_MODULES)
    list(APPEND ALL_EXAMPLES identity_module_usage)
endif()

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

message("Examples to be built: ${ALL_EXAMPLES}")

foreach(example ${ALL_EXAMPLES})
    add_executable(beman.exemplar.examples.${example})
    target_sources(beman.exemplar.examples.${example} PRIVATE ${example}.cpp)
    target_link_libraries(
        beman.exemplar.examples.${example}
        PRIVATE beman::exemplar
    )
    add_test(
        NAME beman.exemplar.examples.${example}
        COMMAND beman.exemplar.examples.${example}
    )
endforeach()
