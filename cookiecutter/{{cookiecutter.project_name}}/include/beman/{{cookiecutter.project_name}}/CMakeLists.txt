# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
{% set identity = "identity" if cookiecutter._generating_exemplar else "todo" %}

if(BEMAN_{{cookiecutter.project_name.upper()}}_USE_MODULES)
    target_sources(
        beman.{{cookiecutter.project_name}}
        PUBLIC
            FILE_SET CXX_MODULES FILES {{cookiecutter.project_name}}.cppm
            FILE_SET HEADERS
                FILES
                    config.hpp
                    {{cookiecutter.project_name}}.hpp
                    {{identity}}.hpp
                    "${PROJECT_BINARY_DIR}/include/beman/{{cookiecutter.project_name}}/config_generated.hpp"
    )
else()
    target_sources(
        beman.{{cookiecutter.project_name}}
        PUBLIC
            FILE_SET HEADERS
                FILES
                    config.hpp
                    {{cookiecutter.project_name}}.hpp
                    {{identity}}.hpp
                    "${PROJECT_BINARY_DIR}/include/beman/{{cookiecutter.project_name}}/config_generated.hpp"
    )
endif()
