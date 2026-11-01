# Beman Project Infrastructure Repository

<!-- SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception -->

This repository contains the infrastructure for The Beman Project. This is NOT a library repository,
so it does not respect the usual structure of a Beman library repository nor The Beman Standard!

## Description

* `cmake/`: CMake modules and toolchain files used by Beman libraries.
* `containers/`: Containers used for CI builds and tests in the Beman org.

## Usage

This repository is intended to be used as a beman-submodule in other Beman repositories. See
[the beman-submodule documentation](https://github.com/bemanproject/beman-submodule) for details.


### CMake Modules


#### `beman_install_library`

The CMake modules in this repository are intended to be used by Beman libraries. Use the
`beman_install_library()` function to install your library, along with header
files, any metadata files, and a CMake config file for `find_package()` support.

```cmake
add_library(beman.something)
add_library(beman::something ALIAS beman.something)

# ... configure your target as needed ...

include(infra/cmake/beman-install-library.cmake)
beman_install_library(beman.something)
```

Note that the target must be created before calling `beman_install_library()`. The module
also assumes that the target is named using the `beman.something` convention, and it
uses that assumption to derive the names to match other Beman standards and conventions.
If your target does not follow that convention, raise an issue or pull request to add
more configurability to the module.

The module will configure the target to install:

* The library target itself
* Any public headers associated with the target
* CMake files for `find_package(beman.something)` support

Some options for the project and target will also be supported:

* `BEMAN_INSTALL_CONFIG_FILE_PACKAGES` - a list of package names (e.g., `beman.something`) for which to install the config file
  (default: all packages)
* `<BEMAN_NAME>_INSTALL_CONFIG_FILE_PACKAGE` - a per-project option to enable/disable config file installation (default: `ON` if the project is top-level, `OFF` otherwise). For instance for `beman.something`, the option would be `BEMAN_SOMETHING_INSTALL_CONFIG_FILE_PACKAGE`.

#### `beman_add_xfail_compile_test`

A negative compile test is a translation unit that must *fail* to compile,
and must fail with a specific diagnostic: the `static_assert` message of a
Mandates clause, the message of a `= delete("...")` overload, or the
compiler's "no matching function" when a constraint removes every
candidate. Use `beman_add_xfail_compile_test()` to register one.

```cmake
include(infra/cmake/beman-xfail-compile.cmake)

beman_add_xfail_compile_test(unexpected_array_fail
    SOURCE unexpected_array_fail.test.cpp
    LINK_LIBRARIES beman::something
)
```

with, near the top of `unexpected_array_fail.test.cpp`:

```cpp
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// NEGATIVE: unexpected<int[]> is ill-formed [expected.un.general]
// EXPECT: "E must not be an array type"
#include <beman/something/unexpected.hpp>

beman::something::unexpected<int[]> u(std::in_place); // must not compile
```

The `EXPECT` line is a CMake regular expression that the compiler output
must match. It lives in the source, next to the ill-formed code it
describes, and is read at configure time. A file may carry several `EXPECT`
lines; they are joined with `|`, so a long alternation covering several
compilers' wordings can be split one per line. Pass `EXPECT <regex>`
to the function instead for a source that cannot carry the comment.

The source becomes an OBJECT library, `<TARGET_PREFIX><name>` (default
prefix `${PROJECT_NAME}.tests.`), excluded from the default build and never
linked. The CTest test `<name>` runs `beman-xfail-compile-driver.cmake`,
which does a nested build of just that target, so the source is compiled
with exactly the toolchain, flags, launcher, and usage requirements the
rest of the project gets. The test passes only when the build fails **and**
its output matches the regex, and reports the two ways of failing
separately:

* *compiled, but was expected to fail* — the constraint or mandate is not
  firing;
* *failed to compile, but not for the expected reason* — a typo in the
  test, or a compiler whose wording the regex does not yet cover. The build
  output is echoed.

Every test carries the label `xfail-compile`, so `ctest -L xfail-compile`
runs just the negative suite and `ctest -LE xfail-compile` skips it, and a
`RESOURCE_LOCK` so `ctest -j` never runs two nested builds in one build
tree at once.

Options: `LINK_LIBRARIES <target>...`, `COMPILE_DEFINITIONS <def>...`,
`TARGET_PREFIX <prefix>`, `LABELS <label>...`. The header comment of
[beman-xfail-compile.cmake](./cmake/beman-xfail-compile.cmake) has the
full interface. `EXPECT` must not contain `;`.

# BuildTelemetry

The cmake modules in this library provide access to CMake instrumentation data in Google Trace format which is visualizable with chrome://tracing and https://ui.perfetto.dev.

Telemetry may be enabled in several ways:

## `include`

```cmake
include (infra/cmake/BuildTelemetry.cmake)
configure_build_telemetry()
```

## `find_package`

```cmake
find_package(BuildTelemetry)
configure_build_telemetry()
```

as long as [BuildTelemetryConfig.cmake](./cmake/BuildTelemetryConfig.cmake) is in your module path.

## `CMAKE_PROJECT_TOP_LEVEL_INCLUDES`
A non-invasive way to inject this telemetry into a CMake build you do not want to modify.
Add:
```sh
-DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=infra/cmake/BuildTelemetry.cmake
```
To the cmake invocation.

In any form, CMake will call `telemetry.sh` which will copy the trace data in json format into a `.trace` subdirectory within the build directory.

Multiple calls to `configure_build_telemetry` will only configure the callback hooks once, so it is safe to enable multiple times, including by TOP_LEVEL_INCLUDE.
