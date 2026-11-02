# cmake/beman-xfail-compile-driver.cmake                            -*-CMake-*-
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# Test driver for beman_add_xfail_compile_test(). Run by CTest as
#
#   cmake -DBEMAN_XFAIL_BUILD_DIR=<build dir>
#         -DBEMAN_XFAIL_TARGET=<object library>
#         -DBEMAN_XFAIL_CONFIG=<config or empty>
#         -DBEMAN_XFAIL_EXPECT=<regex>
#         -P beman-xfail-compile-driver.cmake
#
# It builds just the target and succeeds only when the build fails and its
# output matches the regex. The three outcomes get three distinct reports:
# the source compiled when it should not have; it failed, but not with the
# expected diagnostic; or it failed with the expected diagnostic.

cmake_minimum_required(VERSION 3.30...4.3)

foreach(_var BEMAN_XFAIL_BUILD_DIR BEMAN_XFAIL_TARGET BEMAN_XFAIL_EXPECT)
    if(NOT DEFINED ${_var} OR "${${_var}}" STREQUAL "")
        message(FATAL_ERROR "beman-xfail-compile-driver: ${_var} is required")
    endif()
endforeach()

set(_build_args
    --build
    "${BEMAN_XFAIL_BUILD_DIR}"
    --target
    "${BEMAN_XFAIL_TARGET}"
)
if(BEMAN_XFAIL_CONFIG)
    list(APPEND _build_args --config "${BEMAN_XFAIL_CONFIG}")
endif()

execute_process(
    COMMAND ${CMAKE_COMMAND} ${_build_args}
    RESULT_VARIABLE _result
    OUTPUT_VARIABLE _output
    ERROR_VARIABLE _output
)

if(_result EQUAL 0)
    message(
        FATAL_ERROR
        "beman-xfail-compile-driver: ${BEMAN_XFAIL_TARGET} compiled, but was expected to fail with a diagnostic matching\n"
        "    ${BEMAN_XFAIL_EXPECT}\n"
        "Build output:\n${_output}"
    )
endif()

if(NOT _output MATCHES "${BEMAN_XFAIL_EXPECT}")
    message(
        FATAL_ERROR
        "beman-xfail-compile-driver: ${BEMAN_XFAIL_TARGET} failed to compile, but not for the expected reason. No line matches\n"
        "    ${BEMAN_XFAIL_EXPECT}\n"
        "Build output:\n${_output}"
    )
endif()

string(
    REGEX MATCH "[^\n]*(${BEMAN_XFAIL_EXPECT})[^\n]*"
    _matched_line
    "${_output}"
)
message(
    STATUS
    "beman-xfail-compile-driver: ${BEMAN_XFAIL_TARGET} failed as expected: ${_matched_line}"
)
