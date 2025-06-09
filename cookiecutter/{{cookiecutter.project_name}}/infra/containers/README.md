# Containers

<!-- SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception -->

This folder contains the infrastructure for Beman project's
generic container images. You can checkout available images in beman's
[GitHub Packages page](https://github.com/orgs/bemanproject/packages).

These images includes:

- The latest CMake from kitware's apt repository
- Latest compiler based on build args (gcc or clang) installed from the universe repository
- [pre-commit](https://pre-commit.com/), the standard linter manager across Beman

## Devcontainer

The image is build on top of GitHub's
[C++ devcontainer image](https://github.com/devcontainers/images/tree/main/src/cpp)
for Ubuntu 24.04.

### Example devcontainer setup

```json
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
{
    "name": "Beman Generic Devcontainer",
    "image": "ghcr.io/bemanproject/devcontainers-gcc:14",
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

### Building your own image

You can build your own Beman devcontainer image with:

```bash
docker build devcontainer/
```
