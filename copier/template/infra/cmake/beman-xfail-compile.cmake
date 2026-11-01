# cmake/beman-xfail-compile.cmake                                   -*-CMake-*-
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include_guard(GLOBAL)

# beman_add_xfail_compile_test
# ============================
#
# Registers a negative compile test: a translation unit that must fail to
# compile, and must fail with a specific diagnostic.
#
# Usage:
# ------
#   beman_add_xfail_compile_test(<name>
#     SOURCE <file>
#     [EXPECT <regex>]
#     [LINK_LIBRARIES <target> ...]
#     [COMPILE_DEFINITIONS <definition> ...]
#     [TARGET_PREFIX <prefix>]
#     [LABELS <label> ...]
#   )
#
# Arguments:
# ----------
#
# name
#   The CTest test name.
#
# SOURCE (required)
#   The source file that must not compile.
#
# EXPECT (optional)
#   A regular expression matched against the compiler output. The test
#   passes only when the output matches, which confirms the failure is the
#   intended static_assert, deleted overload, or constraint, and not an
#   unrelated build error. Alternations such as
#   "use of deleted function|call to deleted" cover compiler phrasings.
#
#   When omitted, the regex is read from SOURCE, which must then contain
#   one or more lines of the form
#
#     // EXPECT: "<regex>"
#
#   so the expectation lives next to the ill-formed code it describes.
#   Several lines are joined with "|", so a long alternation can be split
#   one compiler's wording per line and stay inside a formatter's column
#   limit. Configuration re-runs when that file changes. Passing EXPECT
#   overrides the comment, for sources that cannot carry one.
#
# LINK_LIBRARIES (optional)
#   Targets whose usage requirements the source is compiled with, typically
#   the library under test. Nothing is ever linked.
#
# COMPILE_DEFINITIONS (optional)
#   Extra preprocessor definitions for the source.
#
# TARGET_PREFIX (optional)
#   Prefix of the per-test CMake target. Defaults to "${PROJECT_NAME}.tests."
#   so beman.<lib> gets beman.<lib>.tests.<name>.
#
# LABELS (optional)
#   CTest labels to attach to the test, in addition to "xfail-compile",
#   which every test gets so `ctest -L xfail-compile` runs just the
#   negative suite and `ctest -LE xfail-compile` skips it.
#
# Brief
# -----
#
# The source becomes an OBJECT library that is excluded from the default
# build, so an ordinary build never compiles it and nothing links it. The
# test runs beman-xfail-compile-driver.cmake, which performs a nested build
# of just that target, so the source is compiled with exactly the
# toolchain, flags, launcher, and usage requirements the rest of the
# project gets. The driver passes only when that build fails and its
# output matches EXPECT, and it reports the two ways of failing
# separately: the source compiled, or it failed for some other reason.
#
# Every test holds the RESOURCE_LOCK "beman-xfail-compile-build-tree", so
# under `ctest -j` the nested builds never run concurrently in one build
# tree. Other tests still run alongside them.
#
# EXPECT is a CMake regular expression and must not contain ";".

function(beman_add_xfail_compile_test name)
    set(oneValueArgs SOURCE EXPECT TARGET_PREFIX)
    set(multiValueArgs LINK_LIBRARIES COMPILE_DEFINITIONS LABELS)
    cmake_parse_arguments(
        BEMAN_XFAIL
        ""
        "${oneValueArgs}"
        "${multiValueArgs}"
        ${ARGN}
    )

    if(BEMAN_XFAIL_UNPARSED_ARGUMENTS)
        message(
            FATAL_ERROR
            "beman_add_xfail_compile_test(${name}): unexpected arguments '${BEMAN_XFAIL_UNPARSED_ARGUMENTS}'"
        )
    endif()
    if(NOT BEMAN_XFAIL_SOURCE)
        message(
            FATAL_ERROR
            "beman_add_xfail_compile_test(${name}): SOURCE must be specified"
        )
    endif()
    if(NOT DEFINED BEMAN_XFAIL_EXPECT)
        file(
            REAL_PATH "${BEMAN_XFAIL_SOURCE}"
            _source_path
            BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        )
        set_property(
            DIRECTORY
            APPEND
            PROPERTY CMAKE_CONFIGURE_DEPENDS "${_source_path}"
        )
        file(STRINGS "${_source_path}" _expect_lines REGEX "^// EXPECT: \"")
        if(NOT _expect_lines)
            message(
                FATAL_ERROR
                "beman_add_xfail_compile_test(${name}): no '// EXPECT: \"<regex>\"' line in ${_source_path}; add one or pass EXPECT"
            )
        endif()
        set(_alternatives)
        foreach(_line IN LISTS _expect_lines)
            string(
                REGEX REPLACE "^// EXPECT: \"(.*)\"[ \t]*$"
                "\\1"
                _alternative
                "${_line}"
            )
            list(APPEND _alternatives "${_alternative}")
        endforeach()
        list(JOIN _alternatives "|" BEMAN_XFAIL_EXPECT)
    endif()
    if("${BEMAN_XFAIL_EXPECT}" STREQUAL "")
        message(
            FATAL_ERROR
            "beman_add_xfail_compile_test(${name}): EXPECT must not be empty"
        )
    endif()
    string(FIND "${BEMAN_XFAIL_EXPECT}" ";" _semicolon)
    if(NOT _semicolon EQUAL -1)
        message(
            FATAL_ERROR
            "beman_add_xfail_compile_test(${name}): EXPECT must not contain ';'"
        )
    endif()
    if(NOT DEFINED BEMAN_XFAIL_TARGET_PREFIX)
        set(BEMAN_XFAIL_TARGET_PREFIX "${PROJECT_NAME}.tests.")
    endif()

    set(_target "${BEMAN_XFAIL_TARGET_PREFIX}${name}")

    add_library(${_target} OBJECT)
    target_sources(${_target} PRIVATE ${BEMAN_XFAIL_SOURCE})
    if(BEMAN_XFAIL_LINK_LIBRARIES)
        target_link_libraries(${_target} PRIVATE ${BEMAN_XFAIL_LINK_LIBRARIES})
    endif()
    if(BEMAN_XFAIL_COMPILE_DEFINITIONS)
        target_compile_definitions(
            ${_target}
            PRIVATE ${BEMAN_XFAIL_COMPILE_DEFINITIONS}
        )
    endif()
    set_target_properties(
        ${_target}
        PROPERTIES EXCLUDE_FROM_ALL true EXCLUDE_FROM_DEFAULT_BUILD true
    )

    add_test(
        NAME ${name}
        COMMAND
            ${CMAKE_COMMAND} -DBEMAN_XFAIL_BUILD_DIR=${CMAKE_BINARY_DIR}
            -DBEMAN_XFAIL_TARGET=${_target} -DBEMAN_XFAIL_CONFIG=$<CONFIG>
            -DBEMAN_XFAIL_EXPECT=${BEMAN_XFAIL_EXPECT} -P
            ${CMAKE_CURRENT_FUNCTION_LIST_DIR}/beman-xfail-compile-driver.cmake
    )
    set_tests_properties(
        ${name}
        PROPERTIES
            LABELS "xfail-compile;${BEMAN_XFAIL_LABELS}"
            RESOURCE_LOCK beman-xfail-compile-build-tree
    )
endfunction()
