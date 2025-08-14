# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(GNUInstallDirs)

add_library(beman.exemplar)
add_library(beman::exemplar ALIAS beman.exemplar)

target_sources(beman.exemplar PRIVATE identity.cpp)

target_sources(
    beman.exemplar
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/../../../include
        FILES
            ${CMAKE_CURRENT_SOURCE_DIR}/../../../include/beman/exemplar/identity.hpp
)

set_target_properties(
    beman.exemplar
    PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON EXPORT_NAME exemplar
)

install(
    TARGETS beman.exemplar COMPONENT beman.exemplar
    EXPORT beman.exemplar
    DESTINATION
    ${CMAKE_INSTALL_LIBDIR}$<$<CONFIG:Debug>:/debug>
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}$<$<CONFIG:Debug>:/debug>
    FILE_SET HEADERS DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

if(BEMAN_EXEMPLAR_INSTALL_CONFIG_FILE_PACKAGE)
    include(CMakePackageConfigHelpers)

    configure_package_config_file(
        "${CMAKE_CURRENT_SOURCE_DIR}/beman.exemplar-config.cmake.in"
        "${CMAKE_CURRENT_BINARY_DIR}/beman.exemplar-config.cmake"
        INSTALL_DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/beman.exemplar"
        PATH_VARS PROJECT_NAME PROJECT_VERSION
    )

    write_basic_package_version_file(
        "${CMAKE_CURRENT_BINARY_DIR}/beman.exemplar-config-version.cmake"
        VERSION ${PROJECT_VERSION}
        COMPATIBILITY ExactVersion
    )

    install(
        FILES
            "${CMAKE_CURRENT_BINARY_DIR}/beman.exemplar-config.cmake"
            "${CMAKE_CURRENT_BINARY_DIR}/beman.exemplar-config-version.cmake"
        DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/beman.exemplar"
        COMPONENT beman.exemplar
    )

    install(
        EXPORT beman.exemplar
        DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/beman.exemplar"
        NAMESPACE beman::
        FILE beman.exemplar-targets.cmake
        COMPONENT beman.exemplar
    )
endif()
