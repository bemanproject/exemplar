# Copyright © 2024 Bret Brown
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.23)
project(example
  VERSION 1.0.0
  DESCRIPTION "An example Beman library"
  LANGUAGES CXX
)

option(
    BEMAN_EXAMPLE_BUILD_TESTING
    "Enable building tests and test infrastructure. Default: ON. Values: { ON, OFF }."
    ${PROJECT_IS_TOP_LEVEL}
)

add_subdirectory(src/example)

if (BEMAN_EXAMPLE_BUILD_TESTING)
  enable_testing()
  add_subdirectory(test/example)
endif ()
