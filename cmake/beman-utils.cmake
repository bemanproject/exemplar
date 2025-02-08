# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Configure a project-specific option as a cache variable according to
# the following precedence.
#
# - If the option has been explicitly set for this project, then use that value.
# - If the option has been explicitly set for all Beman projects, then use that value.
# - Otherwise, use the default value.
#
# The option value determined to the rules above is stored in the
# project-specific cache variable BEMAN_${PROJECT}_${OPTION}.
macro(beman_configure_project_option)
    block()
        cmake_parse_arguments(
            _arg
            ""
            "PROJECT;OPTION;TYPE;DEFAULT;DEFAULT_FN;DESCRIPTION"
            "ENUM"
            ${ARGN}
        )

        # Remove optional arguments from the list of missing keyword values.
        list(REMOVE_ITEM _arg_KEYWORDS_MISSING_VALUES _arg_ENUM _arg_DEFAULT_FN)

        if(DEFINED _arg_DEFAULT_FN AND NOT DEFINED _arg_DEFAULT)
            cmake_language(CALL ${_arg_DEFAULT_FN} _arg_DEFAULT)
        endif()

        if(DEFINED _arg_DEFAULT)
            list(REMOVE_ITEM _arg_KEYWORDS_MISSING_VALUES _arg_DEFAULT)
        endif()

        if(
            DEFINED _arg_UNPARSED_ARGUMENTS
            OR DEFINED _arg_KEYWORDS_MISSING_VALUES
        )
            set(error_message "Beman project option configuration failed:")

            if(DEFINED _arg_KEYWORDS_MISSING_VALUES)
                set(error_message
                    "${error_message}\n\tThe following required options are missing: ${_arg_KEYWORDS_MISSING_VALUES}"
                )
            endif()

            if(DEFINED _arg_UNPARSED_ARGUMENTS)
                set(error_message
                    "${error_message}\n\tThe following options are invalid: ${_arg_UNPARSED_ARGUMENTS}"
                )
            endif()

            message(FATAL_ERROR "${error_message}")
        endif()

        if(DEFINED BEMAN_${_arg_PROJECT}_${_arg_OPTION})
            # pass
        elseif(DEFINED BEMAN_${_arg_OPTION})
            set(BEMAN_${_arg_PROJECT}_${_arg_OPTION} ${BEMAN_${_arg_OPTION}})
        else()
            set(BEMAN_${_arg_PROJECT}_${_arg_OPTION} ${_arg_DEFAULT})
        endif()

        if(DEFINED _arg_ENUM)
            string(REPLACE ";" ", " _arg_ENUM_STR "${_arg_ENUM}")
            set(_arg_ENUM_STR " Values: { ${_arg_ENUM_STR} }.")
        endif()

        set(BEMAN_${_arg_PROJECT}_${_arg_OPTION}
            "${BEMAN_${_arg_PROJECT}_${_arg_OPTION}}"
            CACHE ${_arg_TYPE}
            "${_arg_DESCRIPTION}. Default: ${_arg_DEFAULT}.${_arg_ENUM_STR}"
        )

        if(DEFINED _arg_ENUM)
            set_property(
                CACHE BEMAN_${_arg_PROJECT}_${_arg_OPTION}
                PROPERTY STRINGS ${_arg_ENUM}
            )
        endif()
    endblock()
endmacro()

macro(beman_shared_libs outvar)
    if(DEFINED BEMAN_SHARED_LIBS)
        set(${outvar} ${BEMAN_SHARED_LIBS})
    elseif(DEFINED BUILD_SHARED_LIBS)
        set(${outvar} ${BUILD_SHARED_LIBS})
    else()
        set(${outvar} OFF)
    endif()
endmacro()

macro(beman_position_independent_code outvar)
    if(DEFINED BEMAN_POSITION_INDEPENDENT_CODE)
        set(${outvar} ${BEMAN_POSITION_INDEPENDENT_CODE})
    elseif(DEFINED CMAKE_POSITION_INDEPENDENT_CODE)
        set(${outvar} ${CMAKE_POSITION_INDEPENDENT_CODE})
    else()
        set(${outvar} OFF)
    endif()
endmacro()

macro(beman_default_target_export_variant outvar)
    include(${CMAKE_CURRENT_LIST_DIR}/beman-configure.cmake)

    if(BEMAN_EXEMPLAR_SHARED_LIBS)
        set(${outvar} shared)
    elseif(BEMAN_EXEMPLAR_POSITION_INDEPENDENT_CODE)
        set(${outvar} static-pic)
    else()
        set(${outvar} static)
    endif()
endmacro()

macro(beman_default_library_suffix outvar)
    include(${CMAKE_CURRENT_LIST_DIR}/beman-configure.cmake)

    block(PROPAGATE ${outvar})
        beman_default_target_export_variant(_variant)

        if(NOT BEMAN_EXEMPLAR_TARGET_EXPORT_VARIANT STREQUAL _variant)
            set(${outvar} .${BEMAN_EXEMPLAR_TARGET_EXPORT_VARIANT})
        endif()

        if(
            NOT BEMAN_EXEMPLAR_SHARED_LIBS
            AND BEMAN_EXEMPLAR_POSITION_INDEPENDENT_CODE
        )
            set(${outvar} ${${outvar}}-pic)
        endif()
    endblock()
endmacro()

macro(beman_add_library target)
    if(BEMAN_EXEMPLAR_SHARED_LIBS)
        add_library(${target} SHARED)
    else()
        add_library(${target} STATIC)
    endif()

    set_target_properties(
        ${target}
        PROPERTIES OUTPUT_NAME ${target}${BEMAN_EXEMPLAR_LIBRARY_SUFFIX}
    )

    if(BEMAN_EXEMPLAR_POSITION_INDEPENDENT_CODE)
        set_target_properties(${target} PROPERTIES POSITION_INDEPENDENT_CODE ON)
    endif()
endmacro()

macro(beman_install_targets)
    block()
        cmake_parse_arguments(_arg "" "EXPORT" "TARGETS" ${ARGN})

        install(
            TARGETS ${_arg_TARGETS}
            EXPORT ${_arg_EXPORT}
            ARCHIVE
                DESTINATION
                    $<$<CONFIG:Debug>:debug/>${BEMAN_EXEMPLAR_INSTALL_LIBDIR}
                COMPONENT ${BEMAN_EXEMPLAR_ARCHIVE_INSTALL_COMPONENT}
            LIBRARY
                DESTINATION
                    $<$<CONFIG:Debug>:debug/>${BEMAN_EXEMPLAR_INSTALL_LIBDIR}
                COMPONENT ${BEMAN_EXEMPLAR_LIBRARY_INSTALL_COMPONENT}
                NAMELINK_COMPONENT ${BEMAN_EXEMPLAR_NAMELINK_INSTALL_COMPONENT}
            RUNTIME
                DESTINATION
                    $<$<CONFIG:Debug>:debug/>${BEMAN_EXEMPLAR_INSTALL_BINDIR}
                COMPONENT ${BEMAN_EXEMPLAR_RUNTIME_INSTALL_COMPONENT}
            FILE_SET HEADERS
                DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
                COMPONENT ${BEMAN_EXEMPLAR_HEADERS_INSTALL_COMPONENT}
        )
    endblock()
endmacro()
