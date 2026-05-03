// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
{% set identity = "identity" if cookiecutter._generating_exemplar else "todo" %}

#include <beman/{{cookiecutter.project_name}}/config.hpp>
#include <beman/{{cookiecutter.project_name}}/{{identity}}.hpp>

{% if cookiecutter._generating_exemplar %}
#if BEMAN_{{cookiecutter.project_name.upper()}}_USE_MODULES()
import std;
#else
    #include <iostream>
#endif

namespace exe = beman::{{cookiecutter.project_name}};

int main() {
    std::cout << exe::identity()(2024) << '\n';
    return 0;
}
{% else %}
int main() {
    // TODO
}
{% endif %}
