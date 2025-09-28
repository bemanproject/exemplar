# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

add_library(beman.exemplar)
add_library(beman::exemplar ALIAS beman.exemplar)

target_sources(beman.exemplar PRIVATE identity.cpp)

target_sources(
    beman.exemplar
    PUBLIC
        FILE_SET HEADERS
            BASE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/../../../include"
            FILES
                "${CMAKE_CURRENT_SOURCE_DIR}/../../../include/beman/exemplar/identity.hpp"
)

set_target_properties(beman.exemplar PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON)

find_package(beman-install-library REQUIRED)
beman_install_library(beman.exemplar)
