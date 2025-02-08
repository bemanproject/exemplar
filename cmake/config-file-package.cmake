# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(${CMAKE_CURRENT_LIST_DIR}/beman-configure.cmake)

if(NOT BEMAN_EXEMPLAR_CONFIG_FILE_PACKAGE)
    return()
endif()

set(${PROJECT_NAME}_DIR
    "${PROJECT_BINARY_DIR}/cmake"
    CACHE PATH
    "Build location of config file package for ${PROJECT_NAME}"
)

configure_package_config_file(
    "${CMAKE_CURRENT_LIST_DIR}/package-config-file.cmake.in"
    "${PROJECT_BINARY_DIR}/cmake/${PROJECT_NAME}-config.cmake"
    INSTALL_DESTINATION "${BEMAN_EXEMPLAR_INSTALL_CMAKEDIR}"
    PATH_VARS PROJECT_VERSION
)

write_basic_package_version_file(
    "${PROJECT_BINARY_DIR}/cmake/${PROJECT_NAME}-version.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY ${BEMAN_EXEMPLAR_CONFIG_FILE_PACKAGE_COMPATIBILITY}
)

install(
    FILES
        "${PROJECT_BINARY_DIR}/cmake/${PROJECT_NAME}-config.cmake"
        "${PROJECT_BINARY_DIR}/cmake/${PROJECT_NAME}-version.cmake"
    DESTINATION "${BEMAN_EXEMPLAR_INSTALL_CMAKEDIR}"
    COMPONENT ${BEMAN_EXEMPLAR_CONFIG_FILE_PACKAGE_INSTALL_COMPONENT}
)
