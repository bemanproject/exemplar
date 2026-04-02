{% set identity = "identity" if cookiecutter._generating_exemplar else "todo" %}
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

{% if cookiecutter.unit_test_library == "gtest" %}
find_package(GTest REQUIRED)
{% elif cookiecutter.unit_test_library == "catch2" %}
find_package(Catch2 3 REQUIRED)
{% endif %}

add_executable(beman.{{cookiecutter.project_name}}.tests.{{identity}})
target_sources(beman.{{cookiecutter.project_name}}.tests.{{identity}} PRIVATE {{identity}}.test.cpp)
target_link_libraries(
    beman.{{cookiecutter.project_name}}.tests.{{identity}}
{% if cookiecutter.unit_test_library == "gtest" %}
    PRIVATE beman::{{cookiecutter.project_name}} GTest::gtest GTest::gtest_main
{% elif cookiecutter.unit_test_library == "catch2" %}
    PRIVATE beman::{{cookiecutter.project_name}} Catch2::Catch2WithMain
{% endif %}
)

{% if cookiecutter.unit_test_library == "gtest" %}
include(GoogleTest)
gtest_discover_tests(beman.{{cookiecutter.project_name}}.tests.{{identity}})
{% elif cookiecutter.unit_test_library == "catch2" %}
include(Catch)
catch_discover_tests(beman.{{cookiecutter.project_name}}.tests.{{identity}})
{% endif %}
