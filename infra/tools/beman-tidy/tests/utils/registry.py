#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import importlib
import inspect
from pathlib import Path
import re


def find_pytest_test_functions_for_check(check_pattern):
    """
    Find all pytest test functions that match the given check pattern.

    Args:
        check_pattern: The check pattern (e.g., "readme_title")

    Returns:
        List of dictionaries containing module and function information
    """
    # Search in beman_standard test directories
    beman_standard_tests_dir = (
        Path(__file__).parent.parent / "lib" / "checks" / "beman_standard"
    )
    if not beman_standard_tests_dir.exists():
        return []

    test_functions = []
    # Iterate through all test modules in beman_standard
    for category_dir in beman_standard_tests_dir.iterdir():
        if category_dir.is_dir() and not category_dir.name.startswith("__"):
            test_file = category_dir / f"test_{category_dir.name}.py"

            if test_file.exists():
                # Import the test module
                try:
                    module_name = f"tests.lib.checks.beman_standard.{category_dir.name}.test_{category_dir.name}"
                    spec = importlib.util.spec_from_file_location(
                        module_name, test_file
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Find test functions that match our pattern
                    for name, obj in inspect.getmembers(module):
                        if (
                            inspect.isfunction(obj)
                            and name.startswith("test__")
                            and check_pattern in name
                        ):
                            test_functions.append(
                                {
                                    "module": module_name,
                                    "function": name,
                                    "file": str(test_file),
                                    "category": category_dir.name,
                                }
                            )

                except Exception as e:
                    print(f"Error loading module {test_file}: {e}")

    return test_functions


def find_filename_for_check(check_name):
    """
    Find the Python file that contains the check class for the given check name.

    Args:
        check_name: The check name (e.g., "readme.title")

    Returns:
        The filename of the check class
    """
    # Search in beman_standard test directories
    beman_standard_lib_dir = (
        Path(__file__).parent.parent.parent
        / "beman_tidy"
        / "lib"
        / "checks"
        / "beman_standard"
    )
    if not beman_standard_lib_dir.exists():
        assert False, (
            f"Beman Standard library directory does not exist: {beman_standard_lib_dir}"
        )
        return None

    # Find @register_beman_standard_check("{check_name}") inside the file
    for file in beman_standard_lib_dir.glob("*.py"):
        regex = r"@register_beman_standard_check\(\"{check_name}\"\)".format(
            check_name=check_name
        )
        with open(file, "r") as f:
            if re.search(regex, f.read()):
                return file.name.replace(".py", "")

    # If no file is found, return None.
    assert False, f"No file found for {check_name} in {beman_standard_lib_dir}"
    return None
