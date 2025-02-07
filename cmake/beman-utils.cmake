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
    if(DEFINED BUILD_SHARED_LIBS)
        set(${outvar} ${BUILD_SHARED_LIBS})
    else()
        set(${outvar} OFF)
    endif()
endmacro()

macro(beman_position_independent_code outvar)
    if(DEFINED CMAKE_POSITION_INDEPENDENT_CODE)
        set(${outvar} ${CMAKE_POSITION_INDEPENDENT_CODE})
    else()
        set(${outvar} OFF)
    endif()
endmacro()

macro(beman_default_target_export_variant outvar)
    include(${CMAKE_CURRENT_LIST_DIR}/beman-configure.cmake)

    block(PROPAGATE ${outvar})
        if(BEMAN_EXEMPLAR_SHARED_LIBS)
            set(${outvar} shared)
        elseif(BEMAN_EXEMPLAR_POSITION_INDEPENDENT_CODE)
            set(${outvar} static-pic)
        else()
            set(${outvar} static)
        endif()
    endblock()
endmacro()
