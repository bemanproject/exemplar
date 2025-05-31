# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
cmake_minimum_required(VERSION 3.28)

project(
    beman.exemplar # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman library exemplar"
    LANGUAGES CXX
    VERSION 2.1.1
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

option(
    BEMAN_EXEMPLAR_INSTALL_CONFIG_FILE_PACKAGE
    "Enable creating and installing a CMake config-file package. Default: ${PROJECT_IS_TOP_LEVEL}. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

add_library(beman.exemplar)
add_library(beman::exemplar ALIAS beman.exemplar)

# gersemi: off
set_target_properties(
    beman.exemplar
    PROPERTIES
        VERIFY_INTERFACE_HEADER_SETS ON
        EXPORT_NAME exemplar
)


target_sources(
    beman.exemplar
    PRIVATE
        src/beman/exemplar/identity.cpp

    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS include
        FILES
            include/beman/exemplar/identity.hpp

    PUBLIC
        FILE_SET CXX_MODULES
        BASE_DIRS include
        FILES
            include/beman/exemplar/beman.exemplar.cppm
)

include(GNUInstallDirs)

install(
    TARGETS beman.exemplar
    EXPORT beman.exemplar-targets
    COMPONENT beman.exemplar

    FILE_SET CXX_MODULES
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}

    FILE_SET HEADERS
)

if(BEMAN_EXEMPLAR_INSTALL_CONFIG_FILE_PACKAGE)
    include(CMakePackageConfigHelpers)

    write_basic_package_version_file(
        ${CMAKE_CURRENT_BINARY_DIR}/beman.exemplar-config-version.cmake
        COMPATIBILITY ExactVersion
    )

    install(
        FILES
            cmake/beman.exemplar-config.cmake
            ${CMAKE_CURRENT_BINARY_DIR}/beman.exemplar-config-version.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/beman.exemplar
        COMPONENT beman.exemplar
    )

    install(
        EXPORT beman.exemplar-targets
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/beman.exemplar
        NAMESPACE beman::
        CXX_MODULES_DIRECTORY cxx-modules
        COMPONENT beman.exemplar
    )
endif()
# gersemi: on

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    include(CTestUseLaunchers)
    enable_testing()
    add_subdirectory(tests/beman/exemplar)
endif()

if(BEMAN_EXEMPLAR_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
