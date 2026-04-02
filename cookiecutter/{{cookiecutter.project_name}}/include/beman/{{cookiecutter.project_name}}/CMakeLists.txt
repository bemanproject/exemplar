{% set identity = "identity" if cookiecutter._generating_exemplar else "todo" %}
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

target_sources(
    beman.{{cookiecutter.project_name}}
    PUBLIC FILE_SET HEADERS FILES {{cookiecutter.project_name}}.hpp {{identity}}.hpp
)
