# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

target_sources(beman.exemplar PUBLIC FILE_SET HEADERS FILES identity.hpp)

if(BEMAN_HAS_MODULES)
    target_sources(
        beman.exemplar
        PUBLIC FILE_SET CXX_MODULES FILES identity.cppm
    )
    # NOTE: Require C++20 for modules is needed here!
    target_compile_features(beman.exemplar PUBLIC cxx_std_20)
    if(WIN32 AND EXEMPLAR_BUILD_SHARED)
        set_target_properties(
            beman.exemplar
            PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON
        )
    endif()
else()
    set_target_properties(
        beman.exemplar
        PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON
    )
endif()
