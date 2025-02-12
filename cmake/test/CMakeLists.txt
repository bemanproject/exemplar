# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25)

project(
    beman.exemplar.package-test
    DESCRIPTION "Tests for the beman.exemplar CMake config-file package"
    LANGUAGES CXX
    VERSION 0.1.0
)

find_package(beman.exemplar REQUIRED)

add_executable(beman.exemplar.package-test)
target_sources(beman.exemplar.package-test PRIVATE main.cpp)
target_link_libraries(beman.exemplar.package-test PRIVATE beman::exemplar)
