include(CheckCXXSourceCompiles)

function(beman_exemplar_check_cpp_17_support result_var)
    check_cxx_source_compiles(
        "
    #if !(__cplusplus >= 201703L || (defined(_MSVC_LANG) && _MSVC_LANG >= 201703L))
    #error
    #endif

    int main() {}
    "
        ${result_var}
    )
endfunction()
