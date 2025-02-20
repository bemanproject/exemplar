# beman.exemplar: A Beman Library Exemplar

<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

<!-- markdownlint-disable-next-line line-length -->
![Library Status](https://raw.githubusercontent.com/bemanproject/beman/refs/heads/main/images/badges/beman_badge-beman_library_under_development.svg) ![Continuous Integration Tests](https://github.com/bemanproject/exemplar/actions/workflows/ci_tests.yml/badge.svg) ![Lint Check (pre-commit)](https://github.com/bemanproject/exemplar/actions/workflows/pre-commit.yml/badge.svg)

`beman.exemplar` is a minimal C++ library conforming to [The Beman Standard](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md).
This can be used as a template for those intending to write Beman libraries.
It may also find use as a minimal and modern  C++ project structure.

**Implements**: `std::identity` proposed in [Standard Library Concepts (P0898R3)](https://wg21.link/P0898R3).

**Status**: [Under development and not yet ready for production use.](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_LIBRARY_MATURITY_MODEL.md#under-development-and-not-yet-ready-for-production-use)

## Usage

`std::identity` is a function object type whose `operator()` returns its argument unchanged.
`std::identity` serves as the default projection in constrained algorithms.
Its direct usage is usually not needed.

### Usage: default projection in constrained algorithms

The following code snippet illustrates how we can achieve a default projection using `beman::exemplar::identity`:

```cpp
#include <beman/exemplar/identity.hpp>

namespace exe = beman::exemplar;

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

## Dependency

### Build Environment

This project requires minimal **C++17** and **CMake 3.25** to build.

This project pulls [Google Test](https://github.com/google/googletest)
from GitHub as a development dependency for its testing framework,
thus requiring an active internet connection to configure.
You can disable this behavior by setting cmake option
[`BEMAN_EXEMPLAR_BUILD_TESTS`](#beman_exemplar_build_tests) to `OFF`
when configuring the project.

However,
some examples and tests will not be compiled
unless provided compiler support **C++20** or ranges capabilities enabled.

> [!TIP]
>
> You will be able to see if there's any examples that isn't enabled due to
> compiler capabilities or minimum C++ version it is configured to in the logs.
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

- GNU GCC Compiler \[version 12-14\]
- LLVM Clang++ Compiler \[version 17-20\]
- AppleClang compiler on Mac OS
- MSVC compiler on Windows

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

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/bemanproject/exemplar)

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

Beman libraries requires [recent versions of CMake](#build-environment),
we advice you download CMake directly from [CMake's website](https://cmake.org/download/)
or install via the [Kitware apt library](https://apt.kitware.com/).

A [supported compiler](#supported-platforms) should be available from your package manager.
Alternatively you could use an install script from official compiler vendors.

Here is an example of how to install the latest stable version of clang
as per [the official LLVM install guide](https://apt.llvm.org/).

```bash
bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"
```

</details>

<details>
<summary> For MacOS based systems </summary>

Beman libraries requires [recent versions of CMake](#build-environment),
you can use `Homebrew` to install the latest major version of CMake.

```bash
brew install cmake
```

A [supported compiler](#supported-platforms) is also available from brew.

For example, you can install latest major release of Clang++ compiler as:

```bash
brew install llvm
```

</details>

### Configure and Build the project using CMake Preset

This project recommends using [CMake Preset](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)
to configure, build and test the project.
Appropriate presets for major compilers has been included by default.
You can use `cmake --list-presets` to see all available presets.

Here is an example to invoke the `gcc-debug` preset.

```shell
cmake --workflow --preset gcc-debug
```

Generally, there's two kinds of presets, `debug` and `release`.

The `debug` presets are designed to aid development,
thus it has as much sanitizers turned on as possible.

> [!NOTE]
>
> The set of sanitizer supports are different across compilers,
> you can checkout the exact set compiler arguments by looking at the toolchain
> files under the [`cmake`](cmake/) directory.

The `release` presets are designed for use in production environments,
thus it has the highest optimization turned on (e.g. `O3`).

### Configure and Build the project manually

While [CMake Preset](#configure-and-build-the-project-using-cmake-preset) is
convenient,
you might want to pass extra config/ compiler arguments for configuration.

To configure, build and test the project with extra arguments,
you can run this sets of command.

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
> you will need to specify C++ version via `CMAKE_CXX_STANDARD`
> when manually configuring the project.

### Project specific configure arguments

When configuring the project manually,
you can pass an array of project specific CMake configs to customize your build.

Project specific options are prefixed with `BEMAN_EXEMPLAR`.
You can see the list of available options with:

```bash
cmake -LH | grep "BEMAN_EXEMPLAR" -C 2
```

<details>

<summary> Details of CMake arguments. </summary>

#### `BEMAN_EXEMPLAR_BUILD_TESTS`

Enable building tests and test infrastructure. Default: ON.
Values: { ON, OFF }.

You can configure the project to have this option turned off via:

```bash
cmake -B build -S . -DCMAKE_CXX_STANDARD=20 -DBEMAN_EXEMPLAR_BUILD_TESTS=OFF
```

> [!TIP]
> Because this project requires Google Tests as part of its development
> dependency,
> disable building tests avoids the project from pulling Google Tests from
> GitHub.

#### `BEMAN_EXEMPLAR_BUILD_EXAMPLES`

Enable building examples. Default: ON. Values: { ON, OFF }.

</details>

## Integrate beman.exemplar into your project

To use `beman.exemplar` in your C++ project,
you should include relevant headers from `beman.exemplar` in your source files.

```c++
#include <beman/exemplar/identity.hpp>
```

You will then link your project to `beman.exemplar`.

### Produce beman.exemplar static library locally

You can include exemplar's headers locally
by producing a static `libbeman.exemplar.a` library.

```bash
cmake --workflow --preset gcc-release
cmake --install build/gcc-release --prefix /opt/beman.exemplar
```

This will generate such project structure at `/opt/beman.exemplar`.

```txt
/opt/beman.exemplar
├── include
│   └── beman
│       └── exemplar
│           └── identity.hpp
└── lib
    └── libbeman.exemplar.a
```

### Linking your project to beman.exemplar with CMake

For CMake based projects,
you will need to use the `beman.exemplar` CMake module
to define the `beman::exemplar` CMake target:

```cmake
find_package(beman.exemplar REQUIRED)
```

You will also need to add `beman::exemplar` to the link libraries of
any libraries or executables that include beman.exemplar's header file.

```cmake
target_link_libraries(yourlib PUBLIC beman::exemplar)
```

### Linking your project to beman.exemplar with compiler options

Compile your project so that it links to the header and library correctly.

```bash
c++ -I/opt/beman.exemplar/include \
    -L/opt/beman.exemplar/lib -lbeman.exemplar \
    your_project.cpp -o your_project
```

## Contributing

Please do!
You encourage you to checkout our [contributor's guide](docs/README.md).
Issues and pull requests are appreciated.
