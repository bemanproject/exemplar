## Development

### Develop using GitHub Codespace

This project supports [GitHub Codespace](https://github.com/features/codespaces)
via [Development Containers](https://containers.dev/),
which allows rapid development and instant hacking in your browser.
We recommend using GitHub Codespace to explore this project as it
requires minimal setup.

Click the following badge to create a Codespace:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/bemanproject/{{cookiecutter.project_name}})

For more documentation on GitHub Codespaces, please see
[this doc](https://docs.github.com/en/codespaces/).

> [!NOTE]
>
> The Codespace container may take up to 5 minutes to build and spin-up; this is normal.

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
cmake \
  -B build \
  -S . \
  -DCMAKE_CXX_STANDARD={{cookiecutter.minimum_cpp_build_version}} \
  # Your extra arguments here.
cmake --build build
ctest --test-dir build
```

> [!IMPORTANT]
>
> Beman projects are
> [passive projects](https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#cmake),
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
    -DCMAKE_CXX_STANDARD={{cookiecutter.minimum_cpp_build_version}}
cmake --build build --target all
cmake --build build --target test
```

The precise version of GoogleTest that will be used is maintained in
`./lockfile.json`.

### Project specific configure arguments

Project-specific options are prefixed with `BEMAN_{{cookiecutter.project_name.upper()}}`.
You can see the list of available options with:

```bash
cmake -LH -S . -B build | grep "BEMAN_{{cookiecutter.project_name.upper()}}" -C 2
```

<details>

<summary> Details of CMake arguments. </summary>

#### `BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS`

Enable building tests and test infrastructure. Default: ON.
Values: `{ ON, OFF }`.

You can configure the project to have this option turned off via:

```bash
cmake -B build -S . -DCMAKE_CXX_STANDARD={{cookiecutter.minimum_cpp_build_version}} -DBEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS=OFF
```

> [!TIP]
> Because this project requires GoogleTest for running tests,
> disabling `BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS` avoids the project from
> cloning GoogleTest from GitHub.

#### `BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_EXAMPLES`

Enable building examples. Default: ON. Values: { ON, OFF }.

#### `BEMAN_{{cookiecutter.project_name.upper()}}_INSTALL_CONFIG_FILE_PACKAGE`

Enable installing the CMake config file package. Default: ON.
Values: { ON, OFF }.

This is required so that users of `beman.{{cookiecutter.project_name}}` can use
`find_package(beman.{{cookiecutter.project_name}})` to locate the library.

</details>
