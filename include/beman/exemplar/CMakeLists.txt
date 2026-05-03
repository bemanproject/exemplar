# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

if(BEMAN_EXEMPLAR_USE_MODULES)
    target_sources(
        beman.exemplar
        PUBLIC
            FILE_SET CXX_MODULES FILES exemplar.cppm
            FILE_SET HEADERS
                FILES
                    config.hpp
                    exemplar.hpp
                    identity.hpp
                    "${PROJECT_BINARY_DIR}/include/beman/exemplar/config_generated.hpp"
    )
else()
    target_sources(
        beman.exemplar
        PUBLIC
            FILE_SET HEADERS
                FILES
                    config.hpp
                    exemplar.hpp
                    identity.hpp
                    "${PROJECT_BINARY_DIR}/include/beman/exemplar/config_generated.hpp"
    )
endif()
