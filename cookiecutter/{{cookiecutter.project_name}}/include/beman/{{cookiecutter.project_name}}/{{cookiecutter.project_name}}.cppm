export module beman.{{cookiecutter.project_name}};

import std;

#define BEMAN_{{cookiecutter.project_name.upper()}}_INCLUDED_FROM_INTERFACE_UNIT
export {
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winclude-angled-in-module-purview"
#include <beman/{{cookiecutter.project_name}}/{{cookiecutter.project_name}}.hpp>
#pragma clang diagnostic pop
}
