#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest
from pathlib import Path

from tests.utils.path_runners import (
    run_check_for_each_path,
)

# Actual tested checks.
from beman_tidy.lib.checks.beman_standard.license import (
    LicenseApprovedCheck,
    LicenseApacheLLVMCheck,
    LicenseCriteriaCheck,
)

test_data_prefix = "tests/lib/checks/beman_standard/license/data"
valid_prefix = f"{test_data_prefix}/valid"
invalid_prefix = f"{test_data_prefix}/invalid"


def test__license_approved__valid(repo_info, beman_standard_check_config):
    """
    Test that a valid LICENSE file passes the check.
    """
    valid_license_paths = [
        # Apache License v2.0 with LLVM Exceptions
        Path(f"{valid_prefix}/valid-LICENSE-v1"),
        # Boost Software License - Version 1.0
        Path(f"{valid_prefix}/valid-LICENSE-v2"),
        # The MIT License
        Path(f"{valid_prefix}/valid-LICENSE-v3"),
    ]

    run_check_for_each_path(
        True,
        valid_license_paths,
        LicenseApprovedCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__license_approved__invalid(repo_info, beman_standard_check_config):
    """
    Test that an invalid LICENSE file fails the check.
    """
    invalid_license_paths = [
        # TODO
    ]

    run_check_for_each_path(
        False,
        invalid_license_paths,
        LicenseApprovedCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__license_approved__fix_inplace(repo_info, beman_standard_check_config):
    """
    Test that the fix method corrects an invalid LICENSE file.
    """
    # Cannot determine what license to create. fix() is not implemented.
    pass


def test__license_apache_llvm__valid(repo_info, beman_standard_check_config):
    """
    Test that a LICENSE file with Apache LLVM passes the check.
    """
    valid_license_paths = [
        # Apache License v2.0 with LLVM Exceptions is the only one compatible with LICENSE.APACHE_LLVM.
        Path(f"{valid_prefix}/valid-LICENSE-v1"),
    ]

    run_check_for_each_path(
        True,
        valid_license_paths,
        LicenseApacheLLVMCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__license_apache_llvm__invalid(repo_info, beman_standard_check_config):
    """
    Test that a LICENSE file without Apache LLVM fails the check.
    """
    invalid_license_paths = [
        # Boost Software License 1.0 is LICENSE.APPROVED compatible, but not compatible with LICENSE.APACHE_LLVM.
        Path(f"{valid_prefix}/valid-LICENSE-v2"),
        # MIT License  is LICENSE.APPROVED compatible, but not compatible with LICENSE.APACHE_LLVM.
        Path(f"{valid_prefix}/valid-LICENSE-v3"),
    ]

    run_check_for_each_path(
        False,
        invalid_license_paths,
        LicenseApacheLLVMCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="not implemented")
def test__license_apache_llvm__fix_inplace(repo_info, beman_standard_check_config):
    """
    Test that the fix method corrects an invalid LICENSE file.
    Note: Skipping this test as it is not implemented.
    """
    pass


def test__license_criteria__is_always_skipped(repo_info, beman_standard_check_config):
    """
    Test that LICENSE.CRITERIA is always skipped, as it cannot be implemented.
    """
    assert LicenseCriteriaCheck(repo_info, beman_standard_check_config).should_skip()
