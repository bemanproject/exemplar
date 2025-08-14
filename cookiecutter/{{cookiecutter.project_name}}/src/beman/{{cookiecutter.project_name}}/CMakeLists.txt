# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(GNUInstallDirs)

add_library(beman.{{cookiecutter.project_name}})
add_library(beman::{{cookiecutter.project_name}} ALIAS beman.{{cookiecutter.project_name}})

target_sources(beman.{{cookiecutter.project_name}} PRIVATE identity.cpp)

target_sources(
    beman.{{cookiecutter.project_name}}
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/../../../include
        FILES
            ${CMAKE_CURRENT_SOURCE_DIR}/../../../include/beman/{{cookiecutter.project_name}}/identity.hpp
)

set_target_properties(
    beman.{{cookiecutter.project_name}}
    PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON EXPORT_NAME {{cookiecutter.project_name}}
)

install(
    TARGETS beman.{{cookiecutter.project_name}} COMPONENT beman.{{cookiecutter.project_name}}
    EXPORT beman.{{cookiecutter.project_name}}
    DESTINATION
    ${CMAKE_INSTALL_LIBDIR}$<$<CONFIG:Debug>:/debug>
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}$<$<CONFIG:Debug>:/debug>
    FILE_SET HEADERS DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

if(BEMAN_{{cookiecutter.project_name.upper()}}_INSTALL_CONFIG_FILE_PACKAGE)
    include(CMakePackageConfigHelpers)

    configure_package_config_file(
        "${CMAKE_CURRENT_SOURCE_DIR}/beman.{{cookiecutter.project_name}}-config.cmake.in"
        "${CMAKE_CURRENT_BINARY_DIR}/beman.{{cookiecutter.project_name}}-config.cmake"
        INSTALL_DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/beman.{{cookiecutter.project_name}}"
        PATH_VARS PROJECT_NAME PROJECT_VERSION
    )

    write_basic_package_version_file(
        "${CMAKE_CURRENT_BINARY_DIR}/beman.{{cookiecutter.project_name}}-config-version.cmake"
        VERSION ${PROJECT_VERSION}
        COMPATIBILITY ExactVersion
    )

    install(
        FILES
            "${CMAKE_CURRENT_BINARY_DIR}/beman.{{cookiecutter.project_name}}-config.cmake"
            "${CMAKE_CURRENT_BINARY_DIR}/beman.{{cookiecutter.project_name}}-config-version.cmake"
        DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/beman.{{cookiecutter.project_name}}"
        COMPONENT beman.{{cookiecutter.project_name}}
    )

    install(
        EXPORT beman.{{cookiecutter.project_name}}
        DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/beman.{{cookiecutter.project_name}}"
        NAMESPACE beman::
        FILE beman.{{cookiecutter.project_name}}-targets.cmake
        COMPONENT beman.{{cookiecutter.project_name}}
    )
endif()
