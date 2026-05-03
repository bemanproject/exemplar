// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
{% set identity = "identity" if cookiecutter._generating_exemplar else "todo" %}

#ifndef BEMAN_{{cookiecutter.project_name.upper()}}_{{cookiecutter.project_name.upper()}}_HPP
#define BEMAN_{{cookiecutter.project_name.upper()}}_{{cookiecutter.project_name.upper()}}_HPP

#include <beman/{{cookiecutter.project_name}}/config.hpp>

#if BEMAN_{{cookiecutter.project_name.upper()}}_USE_MODULES() && !defined(BEMAN_{{cookiecutter.project_name.upper()}}_INCLUDED_FROM_INTERFACE_UNIT)

import beman.{{cookiecutter.project_name}};

#else

    #include <beman/{{cookiecutter.project_name}}/{{identity}}.hpp>

#endif // BEMAN_{{cookiecutter.project_name.upper()}}_USE_MODULES() &&
       // !defined(BEMAN_{{cookiecutter.project_name.upper()}}_INCLUDED_FROM_INTERFACE_UNIT)

#endif // BEMAN_{{cookiecutter.project_name.upper()}}_{{cookiecutter.project_name.upper()}}_HPP
