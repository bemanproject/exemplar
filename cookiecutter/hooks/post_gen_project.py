#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

"""Post-generation hook to clean up template files based on library_type."""

import shutil
from pathlib import Path
import os

# Get the library type from cookiecutter context
library_type = "{{ cookiecutter.library_type }}"

# If interface library, remove the src/ directory (not needed for header-only)
if library_type == "interface":
    src_dir = Path("src")
    if src_dir.exists():
        shutil.rmtree(src_dir)
