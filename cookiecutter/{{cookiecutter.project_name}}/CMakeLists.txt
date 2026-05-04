# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.30...4.3)

include(infra/cmake/enable-experimental-import-std.cmake)

project(
    beman.{{cookiecutter.project_name}}
    DESCRIPTION "{{cookiecutter.description}}"
    LANGUAGES CXX
{% if cookiecutter._generating_exemplar %}
    VERSION 2.4.0
{% else %}
    VERSION 0.1.0
{% endif %}
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

option(BEMAN_{{cookiecutter.project_name.upper()}}_USE_MODULES "Provide beman.{{cookiecutter.project_name}} as a C++ module" OFF)

if(BEMAN_{{cookiecutter.project_name.upper()}}_USE_MODULES)
    set(CMAKE_CXX_SCAN_FOR_MODULES ON)
endif()

configure_file(
    "${PROJECT_SOURCE_DIR}/include/beman/{{cookiecutter.project_name}}/config_generated.hpp.in"
    "${PROJECT_BINARY_DIR}/include/beman/{{cookiecutter.project_name}}/config_generated.hpp"
    @ONLY
)

# for find of beman_install_library and configure_build_telemetry
include(infra/cmake/beman-install-library.cmake)
include(infra/cmake/BuildTelemetryConfig.cmake)

if(BEMAN_{{cookiecutter.project_name.upper()}}_USE_MODULES)
    add_library(beman.{{cookiecutter.project_name}} STATIC)
else()
    add_library(beman.{{cookiecutter.project_name}} INTERFACE)
endif()
add_library(beman::{{cookiecutter.project_name}} ALIAS beman.{{cookiecutter.project_name}})

if(BEMAN_{{cookiecutter.project_name.upper()}}_USE_MODULES)
    target_sources(
        beman.{{cookiecutter.project_name}}
        PUBLIC
            FILE_SET CXX_MODULES
            FILE_SET HEADERS
                BASE_DIRS
                    "${CMAKE_CURRENT_SOURCE_DIR}/include"
                    "${CMAKE_CURRENT_BINARY_DIR}/include"
    )
    set_target_properties(beman.{{cookiecutter.project_name}} PROPERTIES CXX_MODULE_STD ON)
    target_compile_features(beman.{{cookiecutter.project_name}} PUBLIC cxx_std_23)
else()
    target_sources(
        beman.{{cookiecutter.project_name}}
        PUBLIC
            FILE_SET HEADERS
                BASE_DIRS
                    "${CMAKE_CURRENT_SOURCE_DIR}/include"
                    "${CMAKE_CURRENT_BINARY_DIR}/include"
    )
    set_target_properties(
        beman.{{cookiecutter.project_name}}
        PROPERTIES VERIFY_INTERFACE_HEADER_SETS ${PROJECT_IS_TOP_LEVEL}
    )
endif()

add_subdirectory(include/beman/{{cookiecutter.project_name}})

beman_install_library(beman.{{cookiecutter.project_name}} TARGETS beman.{{cookiecutter.project_name}})
configure_build_telemetry()

if(BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests/beman/{{cookiecutter.project_name}})
endif()

if(BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
