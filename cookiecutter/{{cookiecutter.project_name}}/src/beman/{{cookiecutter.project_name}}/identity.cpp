{% set identity = "identity" if cookiecutter._generating_exemplar else "todo" %}
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/{{cookiecutter.project_name}}/{{identity}}.hpp>

{% if cookiecutter._generating_exemplar %}
// Implementation file for static library build.
// For a simple identity function, there's nothing to implement here,
// but this file exists to demonstrate the static library structure.
{% else %}
// TODO
{% endif %}
