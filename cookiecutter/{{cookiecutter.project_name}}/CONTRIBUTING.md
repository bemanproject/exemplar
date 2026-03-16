# Development

## Configure and Build the Project Using CMake Presets

The simplest way of configuring and building the project is to use [CMake
Presets](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html). Appropriate
presets for major compilers have been included by default.  You can use `cmake
--list-presets=workflow` to see all available presets.

Here is an example of invoking the `gcc-debug` preset:

```shell
cmake --workflow --preset gcc-debug
```

Generally, there are two kinds of presets, `debug` and `release`.

The `debug` presets are designed to aid development, so they have debuginfo and sanitizers
enabled.

> [!NOTE]
>
> The sanitizers that are enabled vary from compiler to compiler.  See the toolchain files
> under ([`infra/cmake`](infra/cmake/)) to determine the exact configuration used for each
> preset.

The `release` presets are designed for production use, and
consequently have the highest optimization turned on (e.g. `O3`).

## Configure and Build Manually

If the presets are not suitable for your use case, a traditional CMake invocation will
provide more configurability.

To configure, build and test the project manually, you can run this set of commands. Note
that this requires GoogleTest to be installed.

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
> Beman projects are [passive projects](
> https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#cmakepassive_projects),
> so you need to specify the C++ version via `CMAKE_CXX_STANDARD` when manually
> configuring the project.

## Dependency Management

### FetchContent

Instead of installing the project's dependencies via a package manager, you can optionally
configure beman.{{cookiecutter.project_name}} to fetch them automatically via CMake FetchContent.

To do so, specify
`-DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=./infra/cmake/use-fetch-content.cmake`. This will
bring in GoogleTest automatically along with any other dependency the project may require.

Example commands:

```shell
cmake \
  -B build \
  -S . \
  -DCMAKE_CXX_STANDARD={{cookiecutter.minimum_cpp_build_version}} \
  -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=./infra/cmake/use-fetch-content.cmake
cmake --build build
ctest --test-dir build
```

The file `./lockfile.json` configures the list of dependencies and versions that will be
acquired by FetchContent.

## Project-specific configure arguments

Project-specific options are prefixed with `BEMAN_{{cookiecutter.project_name.upper()}}`.
You can see the list of available options with:

```bash
cmake -LH -S . -B build | grep "BEMAN_{{cookiecutter.project_name.upper()}}" -C 2
```

<details>

<summary>Some project-specific configure arguments</summary>

### `BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_TESTS`

Enable building tests and test infrastructure. Default: `ON`.
Values: `{ ON, OFF }`.

### `BEMAN_{{cookiecutter.project_name.upper()}}_BUILD_EXAMPLES`

Enable building examples. Default: `ON`. Values: `{ ON, OFF }`.

### `BEMAN_{{cookiecutter.project_name.upper()}}_INSTALL_CONFIG_FILE_PACKAGE`

Enable installing the CMake config file package. Default: `ON`.
Values: `{ ON, OFF }`.

This is required so that users of `beman.{{cookiecutter.project_name}}` can use
`find_package(beman.{{cookiecutter.project_name}})` to locate the library.

</details>
