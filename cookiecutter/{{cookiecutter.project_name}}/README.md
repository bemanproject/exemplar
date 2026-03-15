# beman.{{cookiecutter.project_name}}: {{cookiecutter.description}}

<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

<!-- markdownlint-disable-next-line line-length -->
![Library Status](https://raw.githubusercontent.com/bemanproject/beman/refs/heads/main/images/badges/beman_badge-beman_library_under_development.svg) ![Continuous Integration Tests](https://github.com/{{cookiecutter.owner}}/{{cookiecutter.project_name}}/actions/workflows/ci_tests.yml/badge.svg) ![Lint Check (pre-commit)](https://github.com/{{cookiecutter.owner}}/{{cookiecutter.project_name}}/actions/workflows/pre-commit-check.yml/badge.svg) [![Coverage](https://coveralls.io/repos/github/{{cookiecutter.owner}}/{{cookiecutter.project_name}}/badge.svg?branch=main)](https://coveralls.io/github/{{cookiecutter.owner}}/{{cookiecutter.project_name}}?branch=main) ![Standard Target](https://github.com/bemanproject/beman/blob/main/images/badges/cpp29.svg) [![Compiler Explorer Example](https://img.shields.io/badge/Try%20it%20on%20Compiler%20Explorer-grey?logo=compilerexplorer&logoColor=67c52a)]({{cookiecutter.godbolt_link}})

`beman.{{cookiecutter.project_name}}` is a minimal C++ library conforming to [The Beman Standard](https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md).
This can be used as a template for those intending to write Beman libraries.
It may also find use as a minimal and modern  C++ project structure.

**Implements**: `std::identity` proposed in [Standard Library Concepts ({{cookiecutter.paper}})](https://wg21.link/{{cookiecutter.paper}}).

**Status**: [Under development and not yet ready for production use.](https://github.com/bemanproject/beman/blob/main/docs/beman_library_maturity_model.md#under-development-and-not-yet-ready-for-production-use)

## License

`beman.{{cookiecutter.project_name}}` is licensed under the Apache License v2.0 with LLVM Exceptions.

## Usage

`std::identity` is a function object type whose `operator()` returns its argument unchanged.
`std::identity` serves as the default projection in constrained algorithms.
Its direct usage is usually not needed.

### Usage: default projection in constrained algorithms

The following code snippet illustrates how we can achieve a default projection using `beman::{{cookiecutter.project_name}}::identity`:

```cpp
#include <beman/{{cookiecutter.project_name}}/identity.hpp>

namespace exe = beman::{{cookiecutter.project_name}};

// Class with a pair of values.
struct Pair
{
    int n;
    std::string s;

    // Output the pair in the form {n, s}.
    // Used by the range-printer if no custom projection is provided (default: identity projection).
    friend std::ostream &operator<<(std::ostream &os, const Pair &p)
    {
        return os << "Pair" << '{' << p.n << ", " << p.s << '}';
    }
};

// A range-printer that can print projected (modified) elements of a range.
// All the elements of the range are printed in the form {element1, element2, ...}.
// e.g., pairs with identity: Pair{1, one}, Pair{2, two}, Pair{3, three}
// e.g., pairs with custom projection: {1:one, 2:two, 3:three}
template <std::ranges::input_range R,
          typename Projection>
void print(const std::string_view rem, R &&range, Projection projection = exe::identity>)
{
    std::cout << rem << '{';
    std::ranges::for_each(
        range,
        [O = 0](const auto &o) mutable
        { std::cout << (O++ ? ", " : "") << o; },
        projection);
    std::cout << "}\n";
};

int main()
{
    // A vector of pairs to print.
    const std::vector<Pair> pairs = {
        {1, "one"},
        {2, "two"},
        {3, "three"},
    };

    // Print the pairs using the default projection.
    print("\tpairs with beman: ", pairs);

    return 0;
}

```

Full runnable examples can be found in [`examples/`](examples/).

## Dependencies

### Build Environment

This project requires at least the following to build:

* A C++ compiler that conforms to the C++17 standard or greater
* CMake 3.28 or later
* (Test Only) GoogleTest

You can disable building tests by setting CMake option
[`BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS`](#beman_{{cookiecutter.project_name}}_build_tests) to `OFF`
when configuring the project.

Even when tests are being built and run, some of them will not be compiled
unless the provided compiler supports **C++20** ranges.

> [!TIP]
>
> The logs indicate examples disabled due to lack of compiler support.
>
> For example:
>
> ```txt
> -- Looking for __cpp_lib_ranges
> -- Looking for __cpp_lib_ranges - not found
> CMake Warning at examples/CMakeLists.txt:12 (message):
>   Missing range support! Skip: identity_as_default_projection
>
>
> Examples to be built: identity_direct_usage
> ```

### Supported Platforms

| Compiler   | Version | C++ Standards | Standard Library  |
|------------|---------|---------------|-------------------|
| GCC        | 15-13   | C++26-C++17   | libstdc++         |
| GCC        | 12-11   | C++23-C++17   | libstdc++         |
| Clang      | 22-19   | C++26-C++17   | libstdc++, libc++ |
| Clang      | 18-17   | C++26-C++17   | libc++            |
| Clang      | 18-17   | C++20, C++17  | libstdc++         |
| AppleClang | latest  | C++26-C++17   | libc++            |
| MSVC       | latest  | C++23         | MSVC STL          |

## Development

See the [Contributing Guidelines](CONTRIBUTING.md).

## Integrate beman.{{cookiecutter.project_name}} into your project

To use `beman.{{cookiecutter.project_name}}` in your C++ project,
include an appropriate `beman.{{cookiecutter.project_name}}` header from your source code.

```c++
#include <beman/{{cookiecutter.project_name}}/identity.hpp>
```

> [!NOTE]
>
> `beman.{{cookiecutter.project_name}}` headers are to be included with the `beman/{{cookiecutter.project_name}}/` prefix.
> Altering include search paths to spell the include target another way (e.g.
> `#include <identity.hpp>`) is unsupported.

The process for incorporating `beman.{{cookiecutter.project_name}}` into your project depends on the
build system being used. Instructions for CMake are provided in following sections.

### Incorporating `beman.{{cookiecutter.project_name}}` into your project with CMake

For CMake based projects,
you will need to use the `beman.{{cookiecutter.project_name}}` CMake module
to define the `beman::{{cookiecutter.project_name}}` CMake target:

```cmake
find_package(beman.{{cookiecutter.project_name}} REQUIRED)
```

You will also need to add `beman::{{cookiecutter.project_name}}` to the link libraries of
any libraries or executables that include `beman.{{cookiecutter.project_name}}` headers.

```cmake
target_link_libraries(yourlib PUBLIC beman::{{cookiecutter.project_name}})
```

### Produce beman.{{cookiecutter.project_name}} {{ cookiecutter.library_type }} library

{% if cookiecutter.library_type == "interface" %}
You can produce {{cookiecutter.project_name}}'s interface library locally by:
{% else %}
You can produce {{cookiecutter.project_name}}'s static library `libbeman.{{cookiecutter.project_name}}.a` by:
{% endif %}

```bash
cmake --workflow --preset gcc-release
cmake --install build/gcc-release --prefix /opt/beman
```

This will generate the following directory structure at `/opt/beman`.

{% if cookiecutter.library_type == "interface" %}
```txt
/opt/beman
├── include
│   └── beman
│       └── {{cookiecutter.project_name}}
│           └── identity.hpp
└── lib
    └── cmake
        └── beman.{{cookiecutter.project_name}}
            ├── beman.{{cookiecutter.project_name}}-config-version.cmake
            ├── beman.{{cookiecutter.project_name}}-config.cmake
            └── beman.{{cookiecutter.project_name}}-targets.cmake
```
{% else %}
```txt
/opt/beman
├── include
│   └── beman
│       └── {{cookiecutter.project_name}}
│           └── identity.hpp
└── lib
    ├── cmake
    │   └── beman.{{cookiecutter.project_name}}
    │       ├── beman.{{cookiecutter.project_name}}-config-version.cmake
    │       ├── beman.{{cookiecutter.project_name}}-config.cmake
    │       ├── beman.{{cookiecutter.project_name}}-targets-debug.cmake
    │       └── beman.{{cookiecutter.project_name}}-targets.cmake
    └── libbeman.{{cookiecutter.project_name}}.a
```
{% endif %}
