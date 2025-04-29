# Devcontainer

<!-- SPDX-License-Identifier: 2.0 license with LLVM exceptions -->

This folder contains the infrastructure for Beman project's
generic devcontainer image. You can checkout available images in beman's
[GitHub Packages page](https://github.com/orgs/bemanproject/packages/container/package/devcontainers).

The image is build on top of GitHub's
[C++ devcontainer image](https://github.com/devcontainers/images/tree/main/src/cpp)
for Ubuntu 24.04.

The image includes:

- The latest CMake from kitware's apt repository
- Latest compiler based on build args (gnu or llvm) installed from the universe repository
- [pre-commit](https://pre-commit.com/), the standard linter manager across Beman

## Example devcontainer setup

```json
// SPDX-License-Identifier: 2.0 license with LLVM exceptions
{
    "name": "Beman Generic Devcontainer",
    "image": "ghcr.io/bemanproject/devcontainers:gnu-14",
    "postCreateCommand": "pre-commit",
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-vscode.cpptools",
                "ms-vscode.cmake-tools"
            ]
        }
    }
}
```

## Building your own image

You can build your own Beman devcontainer image with:

```bash
docker build devcontainer/
```
