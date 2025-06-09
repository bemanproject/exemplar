# beman.{{cookiecutter.project_name}}: {{cookiecutter.description}}

<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

<!-- markdownlint-disable-next-line line-length -->
![Library Status](https://raw.githubusercontent.com/bemanproject/beman/refs/heads/main/images/badges/beman_badge-beman_library_under_development.svg) ![Continuous Integration Tests](https://github.com/{{cookiecutter.owner}}/{{cookiecutter.project_name}}/actions/workflows/ci_tests.yml/badge.svg) ![Lint Check (pre-commit)](https://github.com/{{cookiecutter.owner}}/{{cookiecutter.project_name}}/actions/workflows/pre-commit.yml/badge.svg)

`beman.{{cookiecutter.project_name}}` is a minimal C++ library conforming to [The Beman Standard](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md).
This can be used as a template for those intending to write Beman libraries.
It may also find use as a minimal and modern  C++ project structure.

**Implements**: `std::identity` proposed in [Standard Library Concepts ({{cookiecutter.paper}})](https://wg21.link/{{cookiecutter.paper}}).

**Status**: [Under development and not yet ready for production use.](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_LIBRARY_MATURITY_MODEL.md#under-development-and-not-yet-ready-for-production-use)

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

* C++17
* CMake 3.25
* (Test Only) GoogleTest

You can disable building tests by setting cmake option
[`BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS`](#beman_{{cookiecutter.project_name}}_build_tests) to `OFF`
when configuring the project.

Even when tests are being built and run, some will not be compiled
unless provided compiler support **C++20** or ranges capabilities enabled.

> [!TIP]
>
> In the logs you will be able to see if there are any examples that aren't enabled
> due to compiler capabilities or the configured C++ version.
>
> Below is an example:
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

This project officially supports:

* GNU GCC Compiler \[version 12-14\]
* LLVM Clang++ Compiler \[version 17-20\]
* AppleClang compiler on Mac OS
* MSVC compiler on Windows

> [!NOTE]
>
> Versions outside of this range would likely work as well,
> especially if you're using a version above the given range
> (e.g. HEAD/ nightly).
> These development environments are verified using our CI configuration.

## Development

### Develop using GitHub Codespace

This project supports [GitHub Codespace](https://github.com/features/codespaces)
via [Development Containers](https://containers.dev/),
which allows rapid development and instant hacking in your browser.
We recommend you using GitHub codespace to explore this project as this
requires minimal setup.

You can create a codespace for this project by clicking this badge:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/bemanproject/{{cookiecutter.project_name}})

For more detailed documentation regarding creating and developing inside of
GitHub codespaces, please reference [this doc](https://docs.github.com/en/codespaces/).

> [!NOTE]
>
> The codespace container may take up to 5 minutes to build and spin-up,
> this is normal as we need to build a custom docker container to setup
> an environment appropriate for beman projects.

### Develop locally on your machines

<details>
<summary> For Linux based systems </summary>

Beman libraries require [recent versions of CMake](#build-environment),
we advise you to download CMake directly from [CMake's website](https://cmake.org/download/)
or install it via the [Kitware apt library](https://apt.kitware.com/).

A [supported compiler](#supported-platforms) should be available from your package manager.
Alternatively you could use an install script from official compiler vendors.

Here is an example of how to install the latest stable version of clang
as per [the official LLVM install guide](https://apt.llvm.org/).

```bash
bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"
```

If the included test suite is being built and run, a GoogleTest library will be
required. Here is an example of installing GoogleTest on a Debian-based Linux
environment:

```bash
apt install libgtest-dev
```

The precise command and package name will vary depending on the Linux OS you are
using. Be sure to consult documentation and the package repository for the system
you are using.

</details>

<details>
<summary> For MacOS based systems </summary>

Beman libraries require [recent versions of CMake](#build-environment).
You can use [`Homebrew`](https://brew.sh/) to install the latest major version of CMake.

```bash
brew install cmake
```

A [supported compiler](#supported-platforms) is also available from brew.

For example, you can install the latest major release of Clang as:

```bash
brew install llvm
```

</details>

<details>
<summary> For Windows </summary>

To build Beman libraries, you will need the MSVC compiler. MSVC can be obtained
by installing Visual Studio; the free Visual Studio 2022 Community Edition can
be downloaded from
[Microsoft](https://visualstudio.microsoft.com/vs/community/).

After Visual Studio has been installed, you can launch "Developer PowerShell for
VS 2022" by typing it into Windows search bar. This shell environment will
provide CMake, Ninja, and MSVC, allowing you to build the library and run the
tests.

Note that you will need to use FetchContent to build GoogleTest. To do so,
please see the instructions in the "Build GoogleTest dependency from github.com"
dropdown in the [Project specific configure
arguments](#project-specific-configure-arguments) section.

</details>

### Configure and Build the Project Using CMake Presets

This project recommends using [CMake Presets](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)
to configure, build and test the project.
Appropriate presets for major compilers have been included by default.
You can use `cmake --list-presets` to see all available presets.

Here is an example to invoke the `gcc-debug` preset.

```shell
cmake --workflow --preset gcc-debug
```

Generally, there are two kinds of presets, `debug` and `release`.

The `debug` presets are designed to aid development, so it has debugging
instrumentation enabled and as many sanitizers turned on as possible.

> [!NOTE]
>
> The set of sanitizer supports are different across compilers.
> You can checkout the exact set of compiler arguments by looking at the toolchain
> files under the [`cmake`](cmake/) directory.

The `release` presets are designed for use in production environments,
thus they have the highest optimization turned on (e.g. `O3`).

### Configure and Build Manually

While [CMake Presets](#configure-and-build-the-project-using-cmake-presets) are
convenient, you might want to set different configuration or compiler arguments
than any provided preset supports.

To configure, build and test the project with extra arguments,
you can run this set of commands.

```bash
cmake -B build -S . -DCMAKE_CXX_STANDARD=20 # Your extra arguments here.
cmake --build build
ctest --test-dir build
```

> [!IMPORTANT]
>
> Beman projects are
> [passive projects](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#cmake),
> therefore,
> you will need to specify the C++ version via `CMAKE_CXX_STANDARD`
> when manually configuring the project.

### Finding and Fetching GTest from GitHub

If you do not have GoogleTest installed on your development system, you may
optionally configure this project to download a known-compatible release of
GoogleTest from source and build it as well.

Example commands:

```shell
cmake -B build -S . \
    -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=./infra/cmake/use-fetch-content.cmake \
    -DCMAKE_CXX_STANDARD=20
cmake --build build --target all
cmake --build build --target test
```

The precise version of GoogleTest that will be used is maintained in
`./lockfile.json`.

### Project specific configure arguments

When configuring the project manually,
you can pass an array of project specific CMake configs to customize your build.

Project specific options are prefixed with `BEMAN_{{cookiecutter.project_name.upper()}}`.
You can see the list of available options with:

```bash
cmake -LH | grep "BEMAN_{{cookiecutter.project_name.upper()}}" -C 2
```

<details>

<summary> Details of CMake arguments. </summary>

#### `BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS`

Enable building tests and test infrastructure. Default: ON.
Values: { ON, OFF }.

You can configure the project to have this option turned off via:

```bash
cmake -B build -S . -DCMAKE_CXX_STANDARD=20 -DBEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS=OFF
```

> [!TIP]
> Because this project requires Google Tests as part of its development
> dependency,
> disable building tests avoids the project from pulling Google Tests from
> GitHub.

#### `BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_EXAMPLES`

Enable building examples. Default: ON. Values: { ON, OFF }.

</details>

## Integrate beman.{{cookiecutter.project_name}} into your project

To use `beman.{{cookiecutter.project_name}}` in your C++ project,
include an appropriate `beman.{{cookiecutter.project_name}}` header from your source code.

```c++
#include <beman/{{cookiecutter.project_name}}/identity.hpp>
```

> [!NOTE]
>
> `beman.{{cookiecutter.project_name}}` headers are to be included with the `beman/{{cookiecutter.project_name}}/` directories prefixed.
> It is not supported to alter include search paths to spell the include target another way. For instance,
> `#include <identity.hpp>` is not a supported interface.

How you will link your project against `beman.{{cookiecutter.project_name}}` will depend on your build system.
CMake instructions are provided in following sections.

### Linking your project to beman.{{cookiecutter.project_name}} with CMake

For CMake based projects,
you will need to use the `beman.{{cookiecutter.project_name}}` CMake module
to define the `beman::{{cookiecutter.project_name}}` CMake target:

```cmake
find_package(beman.{{cookiecutter.project_name}} REQUIRED)
```

You will also need to add `beman::{{cookiecutter.project_name}}` to the link libraries of
any libraries or executables that include beman.{{cookiecutter.project_name}}'s header file.

```cmake
target_link_libraries(yourlib PUBLIC beman::{{cookiecutter.project_name}})
```

### Produce beman.{{cookiecutter.project_name}} static library locally

You can include {{cookiecutter.project_name}}'s headers locally
by producing a static `libbeman.{{cookiecutter.project_name}}.a` library.

```bash
cmake --workflow --preset gcc-release
cmake --install build/gcc-release --prefix /opt/beman.{{cookiecutter.project_name}}
```

This will generate such directory structure at `/opt/beman.{{cookiecutter.project_name}}`.

```txt
/opt/beman.{{cookiecutter.project_name}}
├── include
│   └── beman
│       └── {{cookiecutter.project_name}}
│           └── identity.hpp
└── lib
    └── libbeman.{{cookiecutter.project_name}}.a
```

## Contributing

Please do!
You encourage you to checkout our [contributor's guide](docs/README.md).
Issues and pull requests are appreciated.
