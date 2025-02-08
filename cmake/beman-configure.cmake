include_guard(GLOBAL)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

include(${CMAKE_CURRENT_LIST_DIR}/beman-utils.cmake)

# As required by the beman standard

# [CMAKE.SKIP_TESTS]
beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      BUILD_TESTS
  TYPE        BOOL
  DEFAULT     ${PROJECT_IS_TOP_LEVEL}
  DESCRIPTION "Enable building tests and test infrastructure"
  ENUM ON OFF
)

# [CMAKE.SKIP_EXAMPLES]
beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      BUILD_EXAMPLES
  TYPE        BOOL
  DEFAULT     ${PROJECT_IS_TOP_LEVEL}
  DESCRIPTION "Enable building examples"
  ENUM ON OFF
)

# [CMAKE.SKIP_DOCS]
beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      BUILD_DOCS
  TYPE        BOOL
  DEFAULT     ${PROJECT_IS_TOP_LEVEL}
  DESCRIPTION "Enable building documentation"
  ENUM ON OFF
)

# Project specific options

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      SHARED_LIBS
  TYPE        BOOL
  DEFAULT_FN  beman_shared_libs
  DESCRIPTION "Build shared libs for project ${PROJECT_NAME}?"
  ENUM ON OFF
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      POSITION_INDEPENDENT_CODE
  TYPE        BOOL
  DEFAULT_FN  beman_position_independent_code
  DESCRIPTION "Enable position independent code for project ${PROJECT_NAME}?"
  ENUM ON OFF
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      CONFIG_FILE_PACKAGE
  TYPE        BOOL
  DEFAULT     ${PROJECT_IS_TOP_LEVEL}
  DESCRIPTION "Configure and install a config-file package for ${PROJECT_NAME}?"
  ENUM ON OFF
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      CONFIG_FILE_PACKAGE_COMPATIBILITY
  TYPE        STRING
  DEFAULT     SameMajorVersion
  DESCRIPTION "Version compatibility for ${PROJECT_NAME} targets"
  ENUM
    AnyNewerVersion
    SameMajorVersion
    SameMinorVersion
    ExactVersion
    SameMajorVersion
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      TARGET_EXPORT_VARIANT
  TYPE        STRING
  DEFAULT_FN  beman_default_target_export_variant
  DESCRIPTION "The name of the target export variant to create for ${PROJECT_NAME}"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      DEVELOPMENT_INSTALL_COMPONENT
  TYPE        STRING
  DEFAULT     beman.development
  DESCRIPTION "The name of the install component used to selectively install headers, static libraries, etc"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      RUNTIME_INSTALL_COMPONENT
  TYPE        STRING
  DEFAULT     beman.runtime
  DESCRIPTION "The name of the install component used to selectively install binaries"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      ARCHIVE_INSTALL_COMPONENT
  TYPE        STRING
  DEFAULT     ${BEMAN_EXEMPLAR_DEVELOPMENT_INSTALL_COMPONENT}
  DESCRIPTION "The name of the install component used to selectively install ARCHIVE targets"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      RUNTIME_INSTALL_COMPONENT
  TYPE        STRING
  DEFAULT     ${BEMAN_EXEMPLAR_RUNTIME_INSTALL_COMPONENT}
  DESCRIPTION "The name of the install component used to selectively install RUNTIME targets"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      LIBRARY_INSTALL_COMPONENT
  TYPE        STRING
  DEFAULT     ${BEMAN_EXEMPLAR_RUNTIME_INSTALL_COMPONENT}
  DESCRIPTION "The name of the install component used to selectively install LIBRARY targets"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      HEADERS_INSTALL_COMPONENT
  TYPE        STRING
  DEFAULT     ${BEMAN_EXEMPLAR_DEVELOPMENT_INSTALL_COMPONENT}
  DESCRIPTION "The name of the install component used to selectively install header files targets"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      NAMELINK_INSTALL_COMPONENT
  TYPE        STRING
  DEFAULT     ${BEMAN_EXEMPLAR_DEVELOPMENT_INSTALL_COMPONENT}
  DESCRIPTION "The name of the install component used to selectively install namelinks for versioned binaries"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      CONFIG_FILE_PACKAGE_INSTALL_COMPONENT
  TYPE        STRING
  DEFAULT     ${BEMAN_EXEMPLAR_DEVELOPMENT_INSTALL_COMPONENT}
  DESCRIPTION "The installation component in which the config-file package for ${PROJECT_NAME} is included"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      INSTALL_LIBDIR
  TYPE        PATH
  DEFAULT     ${CMAKE_INSTALL_LIBDIR}
  DESCRIPTION "Locations where ${PROJECT_NAME} libraries and archives will be installed."
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      INSTALL_BINDIR
  TYPE        PATH
  DEFAULT     ${CMAKE_INSTALL_BINDIR}
  DESCRIPTION "Locations where ${PROJECT_NAME} executables will be installed."
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      INSTALL_INCLUDEDIR
  TYPE        PATH
  DEFAULT     ${CMAKE_INSTALL_BINDIR}
  DESCRIPTION "Locations where ${PROJECT_NAME} header files will be installed."
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      INSTALL_CMAKEDIR
  TYPE        PATH
  DEFAULT     "${BEMAN_EXEMPLAR_INSTALL_LIBDIR}/cmake/beman"
  DESCRIPTION "Location where the config-file package and any other CMake utilities for ${PROJECT_NAME} will be installed"
)

beman_configure_project_option(
  PROJECT     EXEMPLAR
  OPTION      LIBRARY_SUFFIX
  TYPE        STRING
  DEFAULT_FN  beman_default_library_suffix
  DESCRIPTION "The suffix to apply to output names of ${PROJECT_NAME} library targets (e.g. 'exemplar' becomes 'exemplar<suffix>')"
)
