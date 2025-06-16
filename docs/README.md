# A guide to contribute/ Develop for Beman Project

TODO: Currently only a skeleton.

## Infrastructure

### `lockfile.json`

#### Why

Some users and environments that are not currently using a package manager.
While CMake supports these scenarios in several ways, this project prefers to
provide and document a simple solution for those user who, reasonably, aren't
familiar with mechanisms available to configure CMake to configure a
`find_package(GTest)` command into steps that provide a GoogleTest
library fully built from source.

As documented in this project's README, that workflow involves injecting
some custom CMake logic into the project by using the
`CMAKE_PROJECT_TOP_LEVEL_INCLUDES` CMake variable to inject a file called
`use-fetch-content.cmake` into the build of the project. Here is an example
command:

```shell
cmake -B build -S . -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=./infra/cmake/use-fetch-content.cmake
```

The precise version of GoogleTest that will be used is maintained in
`./lockfile.json`. `use-fetch-content.cmake` locates that file and configures
the project from that data.

#### Maintenance

Typically, the only change needed to `lockfile.json` would be updating
the commit identifiers in `git_tag` fields as appropriate.

If, hypothetically, the project decided to add tests that use the
Catch2 test framework, a new dependency would need to be enumerated in
`lockfile.json`. A new dependency object would need to be added like so:

```json5
  "dependencies": [
    // ... etc ...
    {
      "name": "Catch2",
      "package_name": "Catch2",
      "git_repository": "https://github.com/catchorg/Catch2",
      "git_tag": "914aeecfe23b1e16af6ea675a4fb5dbd5a5b8d0a" // v3.8.0
    },
    // ... etc ...
  ]
```

[The upstream Catch2 documentation][catch2-docs] declare that `Catch2`
is to be include with `find_package` like so:
`find_package(Catch2)`. That means the `name` field in the `lockfile.json`
dependency object is `Catch2`. That same document describes support for
`FetchContent` APIs like so: `FetchContent_Declare(Catch2 ...)`. That means
the `name` field in the `lockfile.json` dependency object is also `Catch2`.

The `git_repository` field is the URL to the official Catch2 repository:
`https://github.com/catchorg/Catch2`. The latest release of Catch2 is
`v3.8.0`, which has the SHA `914aeecfe23b1e16af6ea675a4fb5dbd5a5b8d0a`, so
we will pin that value in `git_tag` field.

#### Design

This is a design for defining dependency providers
[discussed in CMake upstream documentation][dependency-providers]. The
`use-fetch-content.cmake` file *also* leverages CMake support for parsing
JSON to get the details of projects to provide from `lockfile.json`. This:

* Ensures that calls to FetchContent APIs within this project are consistent
  and meet Beman Standards.

* Provides a proof-of-concept for a utility that could potentially be used
  across all Beman libraries, reducing the complexity of each project.

* Avoids churn in CMake files simply because a version of a dependency
  needs updated.

* Eliminates a significant requirement for any potential automation for
  bumping the version of dependencies -- the need to parse and transform
  files written in the CMake syntax.

#### JSON Structure

The `lockfile.json` file contains an object with one field named `dependencies`.

`dependencies` should have a value that is an array of objects.

Each dependency object should contain exactly four fields with string values:

* `name` is used as the FetchContent name for the project. See
  [the API docs for FetchContent][fetch-content] for more on what a "FetchContent
  name" is.

* `package_name` *must* match the upstream-documented "package name" that would
  be provided to a `find_package` call. For GoogleTest, this is `GTest`, for instance.

* `git_repository` is a full https URL for the repository to clone.

* `git_tag` must be a valid git ref in that repository. This identifies precisely which
  version of the dependency to build. While branch and tag names will work for this value,
  the Beman Project prefers the stability provided by a full-length git commit ID, so
  please use one of those in any changes submitted to `lockfile.json`.

### Lint

[catch2-docs]: https://github.com/catchorg/Catch2/blob/devel/docs/cmake-integration.md#cmake-targets

[dependency-providers]: https://cmake.org/cmake/help/latest/guide/using-dependencies/index.html#dependency-providers]

[fetch-content]: https://cmake.org/cmake/help/latest/module/FetchContent.html
