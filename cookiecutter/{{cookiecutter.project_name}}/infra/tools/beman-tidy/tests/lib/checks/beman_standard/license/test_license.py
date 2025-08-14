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


def test__LICENSE_APPROVED__valid(repo_info, beman_standard_check_config):
    """
    Test that a valid LICENSE file passes the check.
    """
    valid_license_paths = [
        # Apache License v2.0 with LLVM Exceptions
        Path(f"{valid_prefix}/valid-LICENSE-v1"),
        # Boost Software License 1.0
        Path(f"{valid_prefix}/valid-LICENSE-v2"),
        # MIT License
        Path(f"{valid_prefix}/valid-LICENSE-v3"),
    ]

    run_check_for_each_path(
        True,
        valid_license_paths,
        LicenseApprovedCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__LICENSE_APPROVED__invalid(repo_info, beman_standard_check_config):
    """
    Test that an invalid LICENSE file fails the check.
    """
    invalid_license_paths = [
        # Almost valid LICENSE, but without header
        Path(f"{invalid_prefix}/invalid-LICENSE-v1"),
        # Almost valid LICENSE, but without footer
        Path(f"{invalid_prefix}/invalid-LICENSE-v2"),
        # Almost valid LICENSE, but not content between header and footer
        Path(f"{invalid_prefix}/invalid-LICENSE-v3"),
        # Almost valid LICENSE, but not exact header
        Path(f"{invalid_prefix}/invalid-LICENSE-v4"),
        # Almost valid LICENSE, but not exact footer
        Path(f"{invalid_prefix}/invalid-LICENSE-v5"),
    ]

    run_check_for_each_path(
        False,
        invalid_license_paths,
        LicenseApprovedCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__LICENSE_APPROVED__fix_inplace(repo_info, beman_standard_check_config):
    pass


def test__LICENSE_APACHE_LLVM__valid(repo_info, beman_standard_check_config):
    """
    Test that a LICENSE file with Apache LLVM passes the check.
    """
    valid_license_paths = [
        # Apache License v2.0 with LLVM Exceptions is the only one compatible with LICENSE.APACHE_LLVM.
        Path(f"{valid_prefix}/valid-LICENSE-v4"),
    ]

    run_check_for_each_path(
        True,
        valid_license_paths,
        LicenseApacheLLVMCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__LICENSE_APACHE_LLVM__invalid(repo_info, beman_standard_check_config):
    """
    Test that a LICENSE file without Apache LLVM fails the check.
    """
    invalid_license_paths = [
        # Boost Software License 1.0 is LICENSE.APPROVED compatible, but not compatible with LICENSE.APACHE_LLVM.
        Path(f"{invalid_prefix}/invalid-LICENSE-v6"),
        # MIT License  is LICENSE.APPROVED compatible, but not compatible with LICENSE.APACHE_LLVM.
        Path(f"{invalid_prefix}/invalid-LICENSE-v7"),
    ]

    run_check_for_each_path(
        False,
        invalid_license_paths,
        LicenseApacheLLVMCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__LICENSE_APACHE_LLVM__fix_inplace(repo_info, beman_standard_check_config):
    pass


def test__LICENSE_CRITERIA__valid(repo_info, beman_standard_check_config):
    valid_license_paths = [
        # LICENSE.CRITERIA is always true, e.g. for valid file with Apache License v2.0 with LLVM Exceptions.
        Path(f"{valid_prefix}/valid-LICENSE-v1"),
        # LICENSE.CRITERIA is always true, e.g. for invalid file.
        Path(f"{invalid_prefix}/invalid-LICENSE-v1"),
    ]

    run_check_for_each_path(
        True,
        valid_license_paths,
        LicenseCriteriaCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__LICENSE_CRITERIA__invalid(repo_info, beman_standard_check_config):
    # LICENSE.CRITERIA cannot be invalid. Check license.py.
    pass


@pytest.mark.skip(reason="NOT implemented")
def test__LICENSE_CRITERIA__fix_inplace(repo_info, beman_standard_check_config):
    # LICENSE.CRITERIA cannot be invalid, so no need for fix inplace. Check license.py.
    pass
