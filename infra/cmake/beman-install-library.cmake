# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include_guard(GLOBAL)

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

# beman_install_library
# =====================
#
# Installs a library (or set of targets) along with headers, C++ modules,
# and optional CMake package configuration files.
#
# Usage:
# ------
#   beman_install_library(<name>
#     TARGETS <target1> [<target2> ...]
#     [DEPENDENCY <package> [<version>] [EXACT]]
#     [DEPENDENCY <package> ...]
#     [NAMESPACE <namespace>]
#     [EXPORT_NAME <export-name>]
#     [DESTINATION <install-prefix>]
#   )
#
# Arguments:
# ----------
#
# name
#   Logical package name (e.g. "beman.utility").
#   Used to derive config file names and cache variable prefixes.
#
# TARGETS (required)
#   List of CMake targets to install.
#
# DEPENDENCY (optional, repeatable)
#   A dependency to add as a find_dependency() call in the generated config
#   file. Each DEPENDENCY keyword starts a new entry; all tokens up to the
#   next keyword are passed as arguments to find_dependency(). May be
#   specified multiple times.
#
#   Example:
#     DEPENDENCY beman.inplace_vector 1.0.0
#     DEPENDENCY beman.scope 0.0.1 EXACT
#     DEPENDENCY fmt
#
# NAMESPACE (optional)
#   Namespace for exported targets.
#   Defaults to "beman::".
#
# EXPORT_NAME (optional)
#   Name of the CMake export set.
#   Defaults to "<name>-targets".
#
# DESTINATION (optional)
#   The install destination for CXX_MODULES.
#   Defaults to ${CMAKE_INSTALL_LIBDIR}/cmake/${name}/modules.
#
# Brief
# -----
#
# This function installs the specified project TARGETS and its FILE_SET
# HEADERS to the default CMAKE install destination.
#
# It also handles the installation of the CMake config package files if
# needed.  If the given targets has FILE_SET CXX_MODULE, it will also
# installed to the given DESTINATION
#
# Cache variables:
# ----------------
#
# BEMAN_INSTALL_CONFIG_FILE_PACKAGES
#   List of package names for which config files should be installed.
#
# <PREFIX>_INSTALL_CONFIG_FILE_PACKAGE
#   Per-package override to enable/disable config file installation.
#   <PREFIX> is the uppercased package name with dots replaced by underscores.
#
# Caveats
# -------
#
# **Only one `FILE_SET CXX_MODULES` is yet supported to install with this
# function!**
#
# **Only header files contained in a `PUBLIC FILE_SET TYPE HEADERS` will be
# install with this function!**

function(beman_install_library name)
    # ----------------------------
    # Argument parsing
    # ----------------------------

    # Pre-process ARGN to extract repeated DEPENDENCY entries, since
    # cmake_parse_arguments does not support repeated keywords.
    set(_known_keywords
        TARGETS DEPENDENCY NAMESPACE EXPORT_NAME DESTINATION
    )
    set(_dependencies "")
    set(_filtered_args "")
    set(_in_dep FALSE)
    set(_current_dep "")

    foreach(_token ${ARGN})
        if(_token STREQUAL "DEPENDENCY")
            # Flush previous dependency if any
            if(_in_dep AND NOT "${_current_dep}" STREQUAL "")
                list(APPEND _dependencies "${_current_dep}")
            endif()
            set(_in_dep TRUE)
            set(_current_dep "")
        elseif(_in_dep AND "${_token}" IN_LIST _known_keywords)
            # Hit another keyword; flush current dep and pass token through
            if(NOT "${_current_dep}" STREQUAL "")
                list(APPEND _dependencies "${_current_dep}")
            endif()
            set(_in_dep FALSE)
            set(_current_dep "")
            list(APPEND _filtered_args "${_token}")
        elseif(_in_dep)
            # Accumulate tokens as space-separated find_dependency() args
            if("${_current_dep}" STREQUAL "")
                set(_current_dep "${_token}")
            else()
                string(APPEND _current_dep " ${_token}")
            endif()
        else()
            list(APPEND _filtered_args "${_token}")
        endif()
    endforeach()
    # Flush final dependency
    if(_in_dep AND NOT "${_current_dep}" STREQUAL "")
        list(APPEND _dependencies "${_current_dep}")
    endif()

    set(options "")
    set(oneValueArgs NAMESPACE EXPORT_NAME DESTINATION)
    set(multiValueArgs TARGETS)

    cmake_parse_arguments(
        BEMAN
        "${options}"
        "${oneValueArgs}"
        "${multiValueArgs}"
        ${_filtered_args}
    )

    if(NOT BEMAN_TARGETS)
        message(
            FATAL_ERROR
            "beman_install_library(${name}): TARGETS must be specified"
        )
    endif()

    if(CMAKE_SKIP_INSTALL_RULES)
        message(
            WARNING
            "beman_install_library(${name}): not installing targets '${BEMAN_TARGETS}' due to CMAKE_SKIP_INSTALL_RULES"
        )
        return()
    endif()

    set(_config_install_dir "${CMAKE_INSTALL_LIBDIR}/cmake/${name}")

    # ----------------------------
    # Defaults
    # ----------------------------
    if(NOT BEMAN_NAMESPACE)
        set(BEMAN_NAMESPACE "beman::")
    endif()

    if(NOT BEMAN_EXPORT_NAME)
        set(BEMAN_EXPORT_NAME "${name}-targets")
    endif()

    if(NOT BEMAN_DESTINATION)
        set(BEMAN_DESTINATION "${_config_install_dir}/modules")
    endif()

    string(REPLACE "beman." "" install_component_name "${name}")
    message(
        VERBOSE
        "beman-install-library(${name}): COMPONENT '${install_component_name}'"
    )

    # --------------------------------------------------
    # Install each target with all of its file sets
    # --------------------------------------------------
    foreach(_tgt IN LISTS BEMAN_TARGETS)
        if(NOT TARGET "${_tgt}")
            message(
                WARNING
                "beman_install_library(${name}): '${_tgt}' is not a target"
            )
            continue()
        endif()

        # Given foo.bar, the component name is bar
        string(REPLACE "." ";" name_parts "${_tgt}")
        # fail if the name doesn't look like foo.bar
        list(LENGTH name_parts name_parts_length)
        if(NOT name_parts_length EQUAL 2)
            message(
                FATAL_ERROR
                "beman_install_library(${name}): expects a name of the form 'beman.<name>', got '${_tgt}'"
            )
        endif()
        list(GET name_parts -1 component_name)
        set_target_properties(
            "${_tgt}"
            PROPERTIES EXPORT_NAME "${component_name}"
        )
        message(
            VERBOSE
            "beman_install_library(${name}): EXPORT_NAME ${component_name} for TARGET '${_tgt}'"
        )

        # Get the list of interface header sets, exact one expected!
        set(_install_header_set_args)
        get_target_property(
            _available_header_sets
            ${_tgt}
            INTERFACE_HEADER_SETS
        )
        if(_available_header_sets)
            message(
                VERBOSE
                "beman-install-library(${name}): '${_tgt}' has INTERFACE_HEADER_SETS=${_available_header_sets}"
            )
            foreach(_install_header_set IN LISTS _available_header_sets)
                list(
                    APPEND
                    _install_header_set_args
                    FILE_SET
                    "${_install_header_set}"
                    COMPONENT
                    "${install_component_name}_Development"
                )
            endforeach()
        else()
            set(_install_header_set_args FILE_SET HEADERS) # Note: empty FILE_SET in this case! CK
        endif()

        # Detect presence of C++ module file sets, exact one expected!
        get_target_property(_module_sets "${_tgt}" CXX_MODULE_SETS)
        if(_module_sets)
            message(
                VERBOSE
                "beman-install-library(${name}): '${_tgt}' has CXX_MODULE_SETS=${_module_sets}"
            )
            install(
                TARGETS "${_tgt}"
                EXPORT ${BEMAN_EXPORT_NAME}
                ARCHIVE
                    COMPONENT "${install_component_name}_Development"
                LIBRARY
                    COMPONENT "${install_component_name}_Runtime"
                    NAMELINK_COMPONENT "${install_component_name}_Development"
                RUNTIME
                    COMPONENT "${install_component_name}_Runtime"
                ${_install_header_set_args}
                FILE_SET ${_module_sets}
                    DESTINATION "${BEMAN_DESTINATION}"
                    COMPONENT "${install_component_name}_Development"
                CXX_MODULES_BMI
                    COMPONENT "${install_component_name}_Development"
            )
        else()
            install(
                TARGETS "${_tgt}"
                EXPORT ${BEMAN_EXPORT_NAME}
                ARCHIVE
                    COMPONENT "${install_component_name}_Development"
                LIBRARY
                    COMPONENT "${install_component_name}_Runtime"
                    NAMELINK_COMPONENT "${install_component_name}_Development"
                RUNTIME
                    COMPONENT "${install_component_name}_Runtime"
                ${_install_header_set_args}
            )
        endif()
    endforeach()

    # --------------------------------------------------
    # Export targets
    # --------------------------------------------------
    # gersemi: off
    install(
        EXPORT ${BEMAN_EXPORT_NAME}
        NAMESPACE ${BEMAN_NAMESPACE}
        CXX_MODULES_DIRECTORY cxx-modules
        DESTINATION ${_config_install_dir}
        COMPONENT "${install_component_name}_Development"
    )
    # gersemi: on

    # ----------------------------------------
    # Config file installation logic
    #
    # Precedence (highest to lowest):
    #   1. Per-package variable <PREFIX>_INSTALL_CONFIG_FILE_PACKAGE
    #   2. Allow-list BEMAN_INSTALL_CONFIG_FILE_PACKAGES (if defined)
    #   3. Default: ON
    # ----------------------------------------
    string(TOUPPER "${name}" _pkg_upper)
    string(REPLACE "." "_" _pkg_prefix "${_pkg_upper}")

    set(_pkg_var "${_pkg_prefix}_INSTALL_CONFIG_FILE_PACKAGE")

    # Default: install config files
    set(_install_config ON)

    # If the allow-list is defined, only install for packages in the list
    if(DEFINED BEMAN_INSTALL_CONFIG_FILE_PACKAGES)
        if(NOT "${name}" IN_LIST BEMAN_INSTALL_CONFIG_FILE_PACKAGES)
            set(_install_config OFF)
        endif()
    endif()

    # Per-package override takes highest precedence
    if(DEFINED ${_pkg_var})
        set(_install_config ${${_pkg_var}})
    endif()

    # ----------------------------------------
    # expand dependencies
    # ----------------------------------------
    set(_beman_find_deps "")
    foreach(_dep IN LISTS _dependencies)
        message(
            VERBOSE
            "beman-install-library(${name}): Add find_dependency(${_dep})"
        )
        string(APPEND _beman_find_deps "find_dependency(${_dep})\n")
    endforeach()
    set(BEMAN_FIND_DEPENDENCIES "${_beman_find_deps}")

    # ----------------------------------------
    # Generate + install config files
    # ----------------------------------------
    if(_install_config)
        configure_package_config_file(
            "${CMAKE_CURRENT_FUNCTION_LIST_DIR}/Config.cmake.in"
            "${CMAKE_CURRENT_BINARY_DIR}/${name}-config.cmake"
            INSTALL_DESTINATION ${_config_install_dir}
        )

        write_basic_package_version_file(
            "${CMAKE_CURRENT_BINARY_DIR}/${name}-config-version.cmake"
            VERSION ${PROJECT_VERSION}
            COMPATIBILITY SameMajorVersion
        )

        install(
            FILES
                "${CMAKE_CURRENT_BINARY_DIR}/${name}-config.cmake"
                "${CMAKE_CURRENT_BINARY_DIR}/${name}-config-version.cmake"
            DESTINATION ${_config_install_dir}
            COMPONENT "${install_component_name}_Development"
        )
    else()
        message(
            WARNING
            "beman-install-library(${name}): Not installing a config package for '${name}'"
        )
    endif()
endfunction()

set(CPACK_GENERATOR TGZ)
include(CPack)
