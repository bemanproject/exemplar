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

set_target_properties(beman.exemplar PROPERTIES
    VERIFY_INTERFACE_HEADER_SETS ON
    EXPORT_NAME exemplar
)

install(
    TARGETS beman.exemplar
    EXPORT beman.exemplar-${BEMAN_EXEMPLAR_TARGET_EXPORT_VARIANT}
    DESTINATION
    $<$<CONFIG:Debug>:debug/>${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION $<$<CONFIG:Debug>:debug/>${CMAKE_INSTALL_BINDIR}
    FILE_SET HEADERS DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

if(BEMAN_EXEMPLAR_CONFIG_FILE_PACKAGE)
    install(
        EXPORT beman.exemplar-${BEMAN_EXEMPLAR_TARGET_EXPORT_VARIANT}
        DESTINATION "${BEMAN_EXEMPLAR_CONFIG_FILE_PACKAGE_INSTALLDIR}"
        NAMESPACE beman::
        COMPONENT "${BEMAN_EXEMPLAR_CONFIG_FILE_PACKAGE_INSTALL_COMPONENT}"
    )
endif()
