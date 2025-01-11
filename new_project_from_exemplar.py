#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import argparse
import getpass
import os
import sys
try:
    from git import Repo
except:
    print("You do not have GitPython installed, but it is required.  Ubuntu users can install with 'sudo apt-get install python3-git'.  Other users, see https://gitpython.readthedocs.io/en/stable/intro.html.")
    sys.exit(1)

parser = argparse.ArgumentParser(description="Adapts the Beman exemplar project for your use as a brand new project.  Leaves 'TODO' in several places that need you attention (especially in README.md).")
parser.add_argument('project_name', type=str, help="The name of your new project.  This should be the same name as the Github repo name.  For example, 'my_proj' in 'git@github.com:me/my_proj.git'")
parser.add_argument('--owner', type=str, default=getpass.getuser(), help="The user or group in which this project's Github repo is found.  For example, 'me' in 'git@github.com:me/my_proj.git'.  Defaults to your username on this system.")
parser.add_argument('--paper', type=str, default="TODO", help="The paper that this Beman project is implementing (e.g. P1234R5).")
parser.add_argument('--cpp-version', type=int, default=26, help="The C++ version required to build this project.")
parser.add_argument('--desc', type=str, default="TODO", help="The description of this project that should appear in the title of your README.md.")
args = parser.parse_args()

subtrees = ['src/beman', 'include/beman', 'tests/beman']

# Before making any concrete changes, move 'exemplar' subtrees via 'git mv'.
repo = Repo('.')
for tree in subtrees:
    repo.index.move([f'{tree}/exemplar', f'{tree}/{args.project_name}'])

# Replace old README.md with new one.
readme = f'''<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

# beman.{args.project_name}: {args.desc}

<img src="https://github.com/bemanproject/beman/blob/main/images/logos/beman_logo-beman_library_under_development.png" style="width:5%; height:auto;"> ![Continuous Integration Tests](https://github.com/{args.owner}/{args.project_name}/actions/workflows/ci_tests.yml/badge.svg) ![Code Format](https://github.com/{args.owner}/{args.project_name}/actions/workflows/pre-commit.yml/badge.svg)

**Implements**: [`{args.project_name}` ({args.paper})](https://wg21.link/{args.paper})

**Status**: [Under development and not yet ready for production use.](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_LIBRARY_MATURITY_MODEL.md#under-development-and-not-yet-ready-for-production-use)

TODO: Describe this project.

### Usage

```c++
TODO: Copy/paste example code from examples/ here.
```

## Building beman.{args.project_name}

### Dependencies
This project has no C or C++ dependencies.

Build-time dependencies:

- `cmake`
- `ninja`, `make`, or another CMake-supported build system
  - CMake defaults to "Unix Makefiles" on POSIX systems

#### How to install dependencies

<details>
<summary>Dependencies install {args.project_name} on Ubuntu 24.04  </summary>

TODO: Update this with the appropriate versions of gcc and clang.
```shell
# Install tools:
apt-get install -y cmake make ninja-build

# Toolchains:
apt-get install                           \
  g++-14 gcc-14                           \
  clang-18 clang++-18 clang-19 clang++-19
```

</details>

<details>
<summary>Dependencies install {args.project_name} on MAC OS $VERSION </summary>

```shell
# TODO
```

</details>

<details>
<summary>Dependencies install {args.project_name} on Windows $VERSION  </summary>

```shell
# TODO
```

</details>

### How to build beman.{args.project_name}

This project strives to be as normal and simple a CMake project as possible.
This build workflow in particular will work,
producing a static `libbeman.{args.project_name}.a` library, ready to package with its headers:

```shell
cmake --workflow --preset gcc-debug
cmake --workflow --preset gcc-release
cmake --install build/gcc-release --prefix /opt/beman.{args.project_name}
```

<details>
<summary> Build beman.{args.project_name} (verbose logs) </summary>

```shell
# Configure beman.{args.project_name} via gcc-debug workflow for development.
$ cmake --workflow --preset gcc-debug
TODO: Run the command above, and copy its output here.

# Configure beman.{args.project_name} via gcc-release workflow for direct usage.
$ cmake --workflow --preset gcc-release
TODO: Run the command above, and copy its output here.

# Run examples.
$ build/gcc-release/examples/beman.{args.project_name}.examples.{args.project_name}_direct_usage
TODO: Run the command above, and copy its output here.

```

</details>

<details>
<summary> Install beman.{args.project_name} (verbose logs) </summary>

```shell
# Install build artifacts from `build` directory into `opt/beman.{args.project_name}` path.
$ cmake --install build/gcc-release --prefix /opt/beman.{args.project_name}
TODO: Run the command above, and copy its output here.

# Check tree.
$ tree /opt/beman.{args.project_name}
TODO: Run the command above, and copy its output here.
```

</details>

<details>
<summary> Disable tests build </summary>

To build this project with tests disabled (and their dependencies),
simply use `BEMAN_{args.project_name.upper()}_BUILD_TESTING=OFF` as documented in upstream [CMake documentation](https://cmake.org/cmake/help/latest/module/CTest.html):

```shell
cmake -B build -S . -DBEMAN_{args.project_name.upper()}_BUILD_TESTING=OFF
```

</details>

## Integrate beman.{args.project_name} into your project

<details>
<summary> Use beman.{args.project_name} directly from C++ </summary>

This library is header only.  If you want to use `beman.{args.project_name}` from your
project, you can include `beman/{args.project_name}/*.hpp` files from your C++ source
files

```cpp
#include <beman/{args.project_name}/TODO.hpp>
```

and directly link with `libbeman.{args.project_name}.a`

```shell
# Assume /opt/beman.{args.project_name} staging directory.
$ c++ -o {args.project_name}_usage examples/{args.project_name}_direct_usage.cpp \
    -I /opt/beman.{args.project_name}/include/ \
    -L/opt/beman.{args.project_name}/lib/ -lbeman.{args.project_name}
```

</details>

<details>
<summary> Use beman.{args.project_name} directly from CMake </summary>

For CMake based projects, you will need to use the `beman.{args.project_name}` CMake module to define the `beman::{args.project_name}` CMake target:

```cmake
find_package(beman.{args.project_name} REQUIRED)
```

You will also need to add `beman::{args.project_name}`
to the link libraries of any libraries or executables that include `beman/{args.project_name}/*.hpp` in their source or header file.

```cmake
target_link_libraries(yourlib PUBLIC beman::{args.project_name})
```

</details>

<details>
<summary> Use beman.{args.project_name} from other build systems </summary>

Build systems that support `pkg-config` by providing a `beman.{args.project_name}.pc` file.
Build systems that support interoperation via `pkg-config` should be able to detect `beman.{args.project_name}` for you automatically.

</details>

### Compiler support

GCC 14 or later; Clang 18 or later; or VS 2022 or later.

Building this repository requires **C++{args.cpp_version}** or later.

'''
with open('README.md', 'w') as f: f.write(readme)

# Change project name in top-level CMakeLists.txt.
cmakelists_lines = None
with open('CMakeLists.txt') as f: cmakelists_lines = f.readlines()
file_contents = ''
for line in cmakelists_lines:
    if 'DESCRIPTION' in line:
        indent = line.find('DESCRIPTION')
        file_contents += (' ' * indent) + f'DESCRIPTION "{args.desc}"' + '\n'
    else:
        file_contents += line.replace('exemplar', args.project_name).replace('EXEMPLAR', args.project_name.upper())
with open('CMakeLists.txt', 'w') as f: f.write(file_contents)

# Change 'exemplar' to args.project_name in all files under subtrees[].
for tree in subtrees + ['examples', '.github/workflows']:
    for root, dirs, files in os.walk(tree):
        for f in files:
            path = os.path.join(root, f)
            contents = ''
            with open(path) as f:
                contents = f.read()
            with open(path, 'w') as f:
                f.write(contents.replace('exemplar', args.project_name).replace('EXEMPLAR', args.project_name.upper()))

# Change default C++ version in CMakePresets.json.
presets_lines = None
with open('CMakePresets.json') as f: presets_lines = f.readlines()
file_contents = ''
for line in presets_lines:
    if '"CMAKE_CXX_STANDARD":' in line:
        indent = line.find('"CMAKE_CXX_STANDARD":')
        file_contents += (' ' * indent) + f'"CMAKE_CXX_STANDARD": "{args.cpp_version}"' + '\n'
    else:
        file_contents += line
with open('CMakePresets.json', 'w') as f: f.write(file_contents)

# Change usernames in CODEOWNERS.
codeowners_lines = None
with open('.github/CODEOWNERS') as f: codeowners_lines = f.readlines()
file_contents = ''
for line in codeowners_lines:
    if '@wusatosi' in line:
        if '# Add other project owners here' in line:
            file_contents += line.replace('wusatosi', args.owner)
            continue
        elif line.startswith('*'):
            file_contents += f'*  @{args.owner}'
            continue
    file_contents += line
with open('.github/CODEOWNERS', 'w') as f: f.write(file_contents)


# 'git add' all changed files.
repo.index.add([item.a_path for item in repo.index.diff(None)])

# Remove this file; it's only need once.
repo.index.remove('new_project_from_exemplar.py')

# Commit the changes.
repo.index.commit("Ran new_project_from_exemplar.py on project.")

print(f'''Success!
All references to 'exemplar' have been replaced with '{args.project_name}'
throughout the project, and new_project_from_exemplar.py has been deleted.
The results of these changes have been committed.  Please go replace all
instances of 'TODO' with the approporate text, especially in README.md.

You'll also need to change references to the template 'identity' provided in
the exemplar project with your entity/entities.

You may also need to edit .github/workflows/ci_tests.yml to run only the
combinations of C++ version/compiler/platform that makes sense for your
project.
''')
