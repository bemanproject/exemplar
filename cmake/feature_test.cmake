include(CheckCXXSourceCompiles)

function(BEMAN_FEATURE_TEST FEATURE_TEST_EXP RESULT_VAR)
    check_cxx_source_compiles(
        "
    #if (${FEATURE_TEST_EXP})
    int main() {}
    #else
    #error
    #endif
    "
        ${RESULT_VAR}
    )
endfunction()

function(BEMAN_MIN_CXX_VERSION CXX_VERSION)
    set(VERSION_MAP
        11
        201103L
        14
        201402L
        17
        201703L
        20
        202002L
        23
        202302L
    )

    list(FIND VERSION_MAP "${CXX_VERSION}" INDEX)
    if(INDEX EQUAL -1)
        message(FATAL_ERROR "Unknown required C++ version: ${CXX_VERSION}")
    else()
        math(EXPR INDEX "${INDEX} + 1")
        list(GET VERSION_MAP ${INDEX} VERSION_DATE)
    endif()

    beman_feature_test("__cplusplus >= ${VERSION_DATE}" CXX_VERSION_MET)
    if(NOT CXX_VERSION_MET)
        if(MSVC)
            message(
                WARNING
                "Note: C++ version support detection requires a well-formed __cplusplus feature flag, \
            MSVC does not set this flag correctly unless /Zc:__cplusplus flag is passed through.\
            If you believe minimum C++ version detection is function incorrectly,\
            please double check your compiler flags or use the provided presets if available."
            )
        endif()
        message(
            FATAL_ERROR
            "This project requires a minimum C++ version of ${CXX_VERSION}"
        )
    endif()
endfunction()
