# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

add_library(beman.exemplar)
add_library(beman::exemplar ALIAS beman.exemplar)

target_sources(beman.exemplar PRIVATE identity.cpp)

target_sources(
    beman.exemplar
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${PROJECT_SOURCE_DIR}/include
        FILES ${PROJECT_SOURCE_DIR}/include/beman/exemplar/identity.hpp
)

target_include_directories(
    beman.exemplar
    PUBLIC
        $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${BEMAN_EXEMPLAR_INSTALL_INCLUDEDIR}>
)

set_target_properties(
    beman.exemplar
    PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON EXPORT_NAME exemplar
)

beman_install_targets(
    TARGETS beman.exemplar
    EXPORT beman.exemplar-${BEMAN_EXEMPLAR_TARGET_EXPORT_VARIANT}
)

if(BEMAN_EXEMPLAR_CONFIG_FILE_PACKAGE)
    install(
        EXPORT beman.exemplar-${BEMAN_EXEMPLAR_TARGET_EXPORT_VARIANT}
        DESTINATION "${BEMAN_EXEMPLAR_INSTALL_CMAKEDIR}"
        NAMESPACE beman::
        COMPONENT "${BEMAN_EXEMPLAR_CONFIG_FILE_PACKAGE_INSTALL_COMPONENT}"
    )
endif()
