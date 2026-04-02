{% set identity = "identity" if cookiecutter._generating_exemplar else "todo" %}
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/{{cookiecutter.project_name}}/{{identity}}.hpp>

{% if cookiecutter.unit_test_library == "gtest" %}
#include <gtest/gtest.h>
{% elif cookiecutter.unit_test_library == "catch2" %}
#include <catch2/catch_all.hpp>
{% endif %}

{% if cookiecutter._generating_exemplar %}
#include <algorithm>
#include <functional>

namespace exe = beman::{{cookiecutter.project_name}};

{% if cookiecutter.unit_test_library == "gtest" %}
TEST(IdentityTest, call_identity_with_int) {
{% elif cookiecutter.unit_test_library == "catch2" %}
TEST_CASE("can call identity with int", "[{{cookiecutter.project_name}}::call_identity_with_int]") {
{% endif %}
    for (int i = -100; i < 100; ++i) {
{% if cookiecutter.unit_test_library == "gtest" %}
        EXPECT_EQ(i, exe::identity()(i));
{% elif cookiecutter.unit_test_library == "catch2" %}
        CHECK(i == exe::identity()(i));
{% endif %}
    }
}

{% if cookiecutter.unit_test_library == "gtest" %}
TEST(IdentityTest, call_identity_with_custom_type) {
{% elif cookiecutter.unit_test_library == "catch2" %}
TEST_CASE("can call identity with custom type", "[{{cookiecutter.project_name}}::call_identity_with_custom_type]") {
{% endif %}
    struct S {
        int i;
    };

    for (int i = -100; i < 100; ++i) {
        const S s{i};
        const S s_id = exe::identity()(s);
{% if cookiecutter.unit_test_library == "gtest" %}
        EXPECT_EQ(s.i, s_id.i);
{% elif cookiecutter.unit_test_library == "catch2" %}
        CHECK(s.i == s_id.i);
{% endif %}
    }
}

{% if cookiecutter.unit_test_library == "gtest" %}
TEST(IdentityTest, compare_std_vs_beman) {
{% elif cookiecutter.unit_test_library == "catch2" %}
TEST_CASE("compare std vs beman", "[{{cookiecutter.project_name}}::compare_std_vs_beman]") {
{% endif %}
// Requires: std::identity support.
#if defined(__cpp_lib_type_identity)
    std::identity std_id;
    exe::identity beman_id;
    for (int i = -100; i < 100; ++i) {
{% if cookiecutter.unit_test_library == "gtest" %}
        EXPECT_EQ(std_id(i), beman_id(i));
{% elif cookiecutter.unit_test_library == "catch2" %}
        CHECK(std_id(i) == beman_id(i));
{% endif %}
    }
#endif
}

{% if cookiecutter.unit_test_library == "gtest" %}
TEST(IdentityTest, check_is_transparent) {
{% elif cookiecutter.unit_test_library == "catch2" %}
TEST_CASE("check is transparent", "[{{cookiecutter.project_name}}::check_is_transparent]") {
{% endif %}
// Requires: transparent operators support.
#if defined(__cpp_lib_transparent_operators)

    exe::identity id;

    const auto container = {1, 2, 3, 4, 5};
    auto       it        = std::find(std::begin(container), std::end(container), 3);
{% if cookiecutter.unit_test_library == "gtest" %}
    EXPECT_EQ(3, *it);
{% elif cookiecutter.unit_test_library == "catch2" %}
    CHECK(3 == *it);
{% endif %}
    auto it_with_id = std::find(std::begin(container), std::end(container), id(3));
{% if cookiecutter.unit_test_library == "gtest" %}
    EXPECT_EQ(3, *it_with_id);

    EXPECT_EQ(it, it_with_id);
{% elif cookiecutter.unit_test_library == "catch2" %}
    CHECK(3 == *it_with_id);

    CHECK(it == it_with_id);
{% endif %}
#endif
}
{% else %}
{% if cookiecutter.unit_test_library == "gtest" %}
TEST(TodoTest, todo) {
{% elif cookiecutter.unit_test_library == "catch2" %}
TEST_CASE("todo", "[{{cookiecutter.project_name}}::todo]") {
{% endif %}
    const bool todo = true;
{% if cookiecutter.unit_test_library == "gtest" %}
    EXPECT_TRUE(todo);
{% elif cookiecutter.unit_test_library == "catch2" %}
    CHECK(todo);
{% endif %}
}
{% endif %}
