# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set(ALL_EXAMPLES identity_direct_usage)

# Example `identity_as_default_projection` need ranges support:
include(CheckCXXSymbolExists)
check_cxx_symbol_exists(__cpp_lib_ranges "ranges" HAS_RANGES)

if(HAS_RANGES)
    list(APPEND ALL_EXAMPLES identity_as_default_projection)
else()
    message(
        WARNING
        "Missing range support! Skip: identity_as_default_projection"
    )
endif()

message("Examples to be built: ${ALL_EXAMPLES}")

foreach(example ${ALL_EXAMPLES})
    add_executable(beman.{{cookiecutter.project_name}}.examples.${example})
    target_sources(beman.{{cookiecutter.project_name}}.examples.${example} PRIVATE ${example}.cpp)
    target_link_libraries(
        beman.{{cookiecutter.project_name}}.examples.${example}
        PRIVATE beman::{{cookiecutter.project_name}}
    )
endforeach()
