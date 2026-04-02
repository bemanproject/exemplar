{% set identity = "identity" if cookiecutter._generating_exemplar else "todo" %}
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/{{cookiecutter.project_name}}/{{identity}}.hpp>

{% if cookiecutter._generating_exemplar %}
#include <iostream>

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
