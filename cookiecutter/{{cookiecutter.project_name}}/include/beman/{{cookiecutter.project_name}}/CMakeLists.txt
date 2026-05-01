# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
{% set identity = "identity" if cookiecutter._generating_exemplar else "todo" %}

target_sources(
    beman.{{cookiecutter.project_name}}
    PUBLIC FILE_SET HEADERS FILES {{cookiecutter.project_name}}.hpp {{identity}}.hpp
)
