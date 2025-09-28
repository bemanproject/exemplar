# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

add_library(beman.{{cookiecutter.project_name}})
add_library(beman::{{cookiecutter.project_name}} ALIAS beman.{{cookiecutter.project_name}})

target_sources(beman.{{cookiecutter.project_name}} PRIVATE identity.cpp)

target_sources(
    beman.{{cookiecutter.project_name}}
    PUBLIC
        FILE_SET HEADERS
            BASE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/../../../include"
            FILES
                "${CMAKE_CURRENT_SOURCE_DIR}/../../../include/beman/{{cookiecutter.project_name}}/identity.hpp"
)

set_target_properties(beman.{{cookiecutter.project_name}} PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON)

find_package(beman-install-library REQUIRED)
beman_install_library(beman.{{cookiecutter.project_name}})
