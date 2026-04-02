#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import shutil
from pathlib import Path
import os

project_name = "{{ cookiecutter.project_name }}"
library_type = "{{ cookiecutter.library_type }}"
generating_exemplar = "{{ cookiecutter._generating_exemplar }}" == "True"

# If interface library, remove the src/ directory (not needed for header-only)
if library_type == "interface":
    src_dir = Path("src")
    if src_dir.exists():
        shutil.rmtree(src_dir)

if not generating_exemplar:
    os.rename("include/beman/" + project_name + "/identity.hpp", "include/beman/" + project_name + "/todo.hpp")
    os.rename("examples/identity_direct_usage.cpp", "examples/todo.cpp")
    os.remove("examples/identity_as_default_projection.cpp")
    os.rename("tests/beman/" + project_name + "/identity.test.cpp", "tests/beman/" + project_name + "/todo.test.cpp")
    if library_type == "static":
        os.rename("src/beman/" + project_name + "/identity.cpp", "src/beman/" + project_name + "/todo.cpp")
