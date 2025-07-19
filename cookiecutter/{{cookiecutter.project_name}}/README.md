# beman.exemplar: A Beman Library Exemplar

<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

<!-- markdownlint-disable-next-line line-length -->
![Library Status](https://raw.githubusercontent.com/bemanproject/beman/refs/heads/main/images/badges/beman_badge-beman_library_under_development.svg) ![Continuous Integration Tests](https://github.com/bemanproject/exemplar/actions/workflows/ci_tests.yml/badge.svg) ![Lint Check (pre-commit)](https://github.com/bemanproject/exemplar/actions/workflows/pre-commit.yml/badge.svg) [![Coverage](https://coveralls.io/repos/github/bemanproject/exemplar/badge.svg?branch=main)](https://coveralls.io/github/bemanproject/exemplar?branch=main) ![Standard Target](https://github.com/bemanproject/beman/blob/main/images/badges/cpp29.svg)

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

## Dependencies

### Build Environment

This project requires at least the following to build:

* A C++ compiler that conforms to the C++17 standard or greater
* CMake 3.25 or later
* (Test Only) GoogleTest

You can disable building tests by setting CMake option
[`BEMAN_EXEMPLAR_BUILD_TESTS`](#beman_exemplar_build_tests) to `OFF`
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

This project officially supports:

* GCC versions 11–15
* LLVM Clang++ (with libstdc++ or libc++) versions 17–20
* AppleClang version 15.0.0 (i.e., the [latest version on GitHub-hosted MacOS runners](https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md))
* MSVC version 19.44.35211.0 (i.e., the [latest version on GitHub-hosted Windows runners](https://github.com/actions/runner-images/blob/main/images/macos/macos-14-Readme.md))

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
We recommend using GitHub codespace to explore this project as it
requires minimal setup.

Click the following badge to create a codespace:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/bemanproject/exemplar)

For more documentation on GitHub codespaces, please see
[this doc](https://docs.github.com/en/codespaces/).

> [!NOTE]
>
> The codespace container may take up to 5 minutes to build and spin-up; this is normal.

### Develop locally on your machines

<details>
<summary> For Linux </summary>

Beman libraries require [recent versions of CMake](#build-environment),
we recommend downloading CMake directly from [CMake's website](https://cmake.org/download/)
or installing it with the [Kitware apt library](https://apt.kitware.com/).

A [supported compiler](#supported-platforms) should be available from your package manager.

</details>

<details>
<summary> For MacOS </summary>

Beman libraries require [recent versions of CMake](#build-environment).
Use [`Homebrew`](https://brew.sh/) to install the latest version of CMake.

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
instrumentation enabled and many sanitizers enabled.

> [!NOTE]
>
> The sanitizers that are enabled vary from compiler to compiler.
> See the toolchain files under ([`cmake`](cmake/)) to determine the exact configuration used for each preset.

The `release` presets are designed for production use, and
consequently have the highest optimization turned on (e.g. `O3`).

### Configure and Build Manually

If the presets are not suitable for your use-case, a traditional CMake
invocation will provide more configurability.

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

Project-specific options are prefixed with `BEMAN_EXEMPLAR`.
You can see the list of available options with:

```bash
cmake -LH -S . -B build | grep "BEMAN_EXEMPLAR" -C 2
```

<details>

<summary> Details of CMake arguments. </summary>

#### `BEMAN_EXEMPLAR_BUILD_TESTS`

Enable building tests and test infrastructure. Default: ON.
Values: `{ ON, OFF }`.

You can configure the project to have this option turned off via:

```bash
cmake -B build -S . -DCMAKE_CXX_STANDARD=20 -DBEMAN_EXEMPLAR_BUILD_TESTS=OFF
```

> [!TIP]
> Because this project requires GoogleTest for running tests,
> disabling `BEMAN_EXEMPLAR_BUILD_TESTS` avoids the project from
> cloning GoogleTest from GitHub.

#### `BEMAN_EXEMPLAR_BUILD_EXAMPLES`

Enable building examples. Default: ON. Values: { ON, OFF }.

</details>

## Integrate beman.exemplar into your project

To use `beman.exemplar` in your C++ project,
include an appropriate `beman.exemplar` header from your source code.

```c++
#include <beman/exemplar/identity.hpp>
```

> [!NOTE]
>
> `beman.exemplar` headers are to be included with the `beman/exemplar/` prefix.
> Altering include search paths to spell the include target another way (e.g.
> `#include <identity.hpp>`) is unsupported.

The process for incorporating `beman.exemplar` into your project depends on the
build system being used. Instructions for CMake are provided in following sections.

### Incorporating `beman.exemplar` into your project with CMake

For CMake based projects,
you will need to use the `beman.exemplar` CMake module
to define the `beman::exemplar` CMake target:

```cmake
find_package(beman.exemplar REQUIRED)
```

You will also need to add `beman::exemplar` to the link libraries of
any libraries or executables that include `beman.exemplar` headers.

```cmake
target_link_libraries(yourlib PUBLIC beman::exemplar)
```

### Produce beman.exemplar static library

You can include exemplar's headers locally
by producing a static `libbeman.exemplar.a` library.

```bash
cmake --workflow --preset gcc-release
cmake --install build/gcc-release --prefix /opt/beman.exemplar
```

This will generate such directory structure at `/opt/beman.exemplar`.

```txt
/opt/beman.exemplar
├── include
│   └── beman
│       └── exemplar
│           └── identity.hpp
└── lib
    └── libbeman.exemplar.a
```
