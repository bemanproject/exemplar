#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import inspect
from pathlib import Path

from beman_tidy.lib.checks.system.registry import (
    get_registered_beman_standard_checks,
)
from tests.utils.registry import (
    find_pytest_test_functions_for_check,
    find_filename_for_check,
)


def test__get_registered_beman_standard_checks__valid(
    repo_info, beman_standard_check_config
):
    """
    Test that the get_registered_beman_standard_checks() function returns the correct checks
    and verify that each registered check has corresponding pytest test functions.
    """
    all_registered_checks = get_registered_beman_standard_checks()
    for check_name, check_class in all_registered_checks.items():
        # Convert check name to test function pattern.
        # e.g., "readme.title" -> "readme_title"
        check_pattern = check_name.replace(".", "_")

        # Find the filename for the check class.
        filename = find_filename_for_check(check_name)
        expected_function_path = (
            Path(__file__).parent.parent.parent.parent
            / "lib"
            / "checks"
            / "beman_standard"
            / filename
            / f"test_{filename}.py"
        )
        assert filename is not None and expected_function_path.exists(), (
            f"[{check_name}] Missing file {expected_function_path}"
        )

        # Find all test functions that match the check name.
        test_functions = find_pytest_test_functions_for_check(check_pattern)

        # Decide if the check is runnable or skipped.
        check_instance = check_class(repo_info, beman_standard_check_config)
        if check_instance.should_skip():
            # Skipped checks have exactly one test function.
            expected_function_name = f"test__{check_pattern}__is_always_skipped"
            assert len(test_functions) == 1, (
                f"[{check_name}] Expected exactly one test function for {check_name}: {expected_function_name} at {expected_function_path}"
            )

            actual_function_path = Path(test_functions[0]["file"])
            actual_function_name = test_functions[0]["function"]

            assert expected_function_path == actual_function_path, (
                f"[{check_name}] Test function path should match the expected pattern: {actual_function_path} != {expected_function_path}"
            )
            assert expected_function_name == actual_function_name, (
                f"[{check_name}] Test function name should match the expected pattern: {actual_function_name} != {expected_function_name}"
            )
        else:
            # Runnable checks have exactly three test functions.
            expected_function_names = [
                f"test__{check_pattern}__valid",
                f"test__{check_pattern}__invalid",
                f"test__{check_pattern}__fix_inplace",
            ]
            assert len(test_functions) == len(expected_function_names), (
                f"[{check_name}] Expected exactly three test functions for runnable check {check_name}: {expected_function_names} at {expected_function_path}"
            )

            for test_function in test_functions:
                actual_function_path = Path(test_function["file"])
                actual_function_name = test_function["function"]
                assert expected_function_path == actual_function_path, (
                    f"[{check_name}] Test function path should match the expected pattern: {actual_function_path} != {expected_function_path}"
                )
                assert any(
                    expected_function_name == actual_function_name
                    for expected_function_name in expected_function_names
                ), (
                    f"[{check_name}] Test function name should match the expected pattern: {actual_function_name} != {expected_function_name}"
                )


def test__registry_completeness__check():
    """
    Test that verifies the completeness of the registry system.
    This is a comprehensive test of all registry functionality.
    """
    from beman_tidy.lib.checks.system.registry import (
        get_all_beman_standard_check_names,
        get_beman_standard_check_by_name,
        get_beman_standard_check_name_by_class,
    )

    registered_checks = get_registered_beman_standard_checks()
    registered_names = get_all_beman_standard_check_names()

    # Basic registry validation
    assert len(registered_checks) > 0, "Registry should not be empty"
    assert len(registered_names) == len(registered_checks), (
        "Names list and checks dict should have same length"
    )

    # Test each registry function
    for check_name in registered_names:
        # Test get_beman_standard_check_by_name.
        check_class = get_beman_standard_check_by_name(check_name)
        assert check_class is not None, (
            f"Should be able to retrieve check class for '{check_name}'"
        )
        assert check_class == registered_checks[check_name], (
            "Retrieved class should match registry entry"
        )

        # Test get_beman_standard_check_name_by_class
        reverse_name = get_beman_standard_check_name_by_class(check_class)
        assert reverse_name == check_name, (
            f"Reverse lookup should work for '{check_name}'"
        )

        # Verify class structure.
        assert inspect.isclass(check_class), (
            f"'{check_name}' should be registered to a class"
        )
        assert hasattr(check_class, "check"), (
            f"'{check_name}' class should have 'check' method"
        )
        assert hasattr(check_class, "fix"), (
            f"'{check_name}' class should have 'fix' method"
        )


def test__registry_no_duplicates__check():
    """
    Test that no check class is registered multiple times.
    """
    registered_checks = get_registered_beman_standard_checks()

    # Create reverse mapping: class -> list of names.
    class_to_names = {}
    for check_name, check_class in registered_checks.items():
        if check_class not in class_to_names:
            class_to_names[check_class] = []
        class_to_names[check_class].append(check_name)

    # Verify each class is only registered once
    duplicates = []
    for check_class, check_names in class_to_names.items():
        if len(check_names) > 1:
            duplicates.append((check_class.__name__, check_names))

    assert len(duplicates) == 0, f"Found duplicate registrations: {duplicates}"
