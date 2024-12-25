# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# This toolchain file is not meant to be used directly,
# but to be invoked by CMake preset and GitHub CI.
#
# This toolchain file configures for MSVC family of compiler.
#
# BEMAN_BUILDSYS_SANITIZER:
# This optional CMake parameter is not meant for public use and is subject to
# change.
# Possible values:
# - MaxSan: configures cl to use all available non-conflicting sanitizers.
#
# Note that in other toolchain files, TSan is also a possible value for
# BEMAN_BUILDSYS_SANITIZER, however, MSVC does not support thread sanitizer,
# thus this value is omitted.

set(CMAKE_C_COMPILER cl)
set(CMAKE_CXX_COMPILER cl)

if(BEMAN_BUILDSYS_SANITIZER STREQUAL "MaxSan")
    set(SANITIZER_FLAGS "/fsanitize=address /Zi")
endif()

set(CMAKE_CXX_FLAGS_DEBUG_INIT "/EHsc /permissive- ${SANITIZER_FLAGS}")
set(CMAKE_C_FLAGS_DEBUG_INIT "/EHsc /permissive- ${SANITIZER_FLAGS}")

set(RELEASE_FLAG "/EHsc /permissive- /O2 ${SANITIZER_FLAGS}")

set(CMAKE_C_FLAGS_RELWITHDEBINFO_INIT "${RELEASE_FLAG}")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT "${RELEASE_FLAG}")

set(CMAKE_C_FLAGS_RELEASE_INIT "${RELEASE_FLAG}")
set(CMAKE_CXX_FLAGS_RELEASE_INIT "${RELEASE_FLAG}")