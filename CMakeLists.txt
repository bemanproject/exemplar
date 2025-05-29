# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25)

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

include(cmake/feature_test.cmake)
beman_exemplar_check_cpp_17_support(COMPILER_SUPPORTS_CPP_17)

option(
    BEMAN_EXEMPLAR_OVERRIDE_CPP_17_REQUIREMENT
    "Attempt building even though the compiler doesn't advertise the requisite C++17 support"
    OFF
)

if(
    NOT BEMAN_EXEMPLAR_OVERRIDE_CPP_17_REQUIREMENT
    AND NOT COMPILER_SUPPORTS_CPP_17
)
    message(
        FATAL_ERROR
        "Your compiler isn't advertising support for C++17 with the current configuration."
        "Try adding -DCMAKE_CXX_STANDARD=17 to your CMake invocation."
        "To override this check, set BEMAN_EXEMPLAR_OVERRIDE_CPP_17_REQUIREMENT to ON."
    )
endif()

include(CTest)

add_subdirectory(src/beman/exemplar)

if(BEMAN_EXEMPLAR_BUILD_TESTS)
    add_subdirectory(tests/beman/exemplar)
endif()

if(BEMAN_EXEMPLAR_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
