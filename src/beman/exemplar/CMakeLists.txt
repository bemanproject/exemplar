# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

beman_add_header_only_library(beman.exemplar.headers)
beman_add_library(beman.exemplar)

target_sources(beman.exemplar PRIVATE identity.cpp)

target_sources(
    beman.exemplar
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${PROJECT_SOURCE_DIR}/include
        FILES ${PROJECT_SOURCE_DIR}/include/beman/exemplar/identity.hpp
)

target_link_libraries(beman.exemplar PUBLIC beman.exemplar.headers)

beman_install_targets(
    TARGETS beman.exemplar.headers beman.exemplar
)

beman_install_export()
