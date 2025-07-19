#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest
from pathlib import Path

from tests.utils.path_runners import (
    run_check_for_each_path,
)

# Actual tested checks.
from beman_tidy.lib.checks.beman_standard.toplevel import (
    ToplevelCmakeCheck,
    ToplevelLicenseCheck,
    ToplevelReadmeCheck,
)

test_data_prefix = "tests/lib/checks/beman_standard/toplevel/data"
valid_prefix = f"{test_data_prefix}/valid"
invalid_prefix = f"{test_data_prefix}/invalid"


def test__TOPLEVEL_CMAKE__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid CMakeLists.txt pass the check.
    """
    valid_cmake_paths = [
        # exemplar/ repo with valid CMakeLists.txt file.
        Path(f"{valid_prefix}/repo-exemplar-v1/"),
    ]

    run_check_for_each_path(
        True,
        valid_cmake_paths,
        ToplevelCmakeCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__TOPLEVEL_CMAKE__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid CMakeLists.txt fail the check.
    """
    invalid_cmake_paths = [
        # exemplar/ repo with empty CMakeLists.txt file.
        Path(f"{invalid_prefix}/repo-exemplar-v1/"),
        # exemplar/ repo with CMakeLists.txt in non-root location.
        Path(f"{invalid_prefix}/repo-exemplar-v2/"),
        # exemplar/ repo without CMakeLists.txt file.
        Path(f"{invalid_prefix}/repo-exemplar-v3/"),
    ]

    run_check_for_each_path(
        False,
        invalid_cmake_paths,
        ToplevelCmakeCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__TOPLEVEL_CMAKE__fix_inplace(repo_info, beman_standard_check_config):
    pass


def test__TOPLEVEL_LICENSE__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid LICENSE pass the check.
    """
    valid_license_paths = [
        # exemplar/ repo with valid LICENSE file.
        Path(f"{valid_prefix}/repo-exemplar-v1/"),
    ]

    run_check_for_each_path(
        True,
        valid_license_paths,
        ToplevelLicenseCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__TOPLEVEL_LICENSE__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid LICENSE fail the check.
    """
    invalid_license_paths = [
        # exemplar/ repo with empty LICENSE file.
        Path(f"{invalid_prefix}/repo-exemplar-v1/"),
        # exemplar/ repo with LICENSE in non-root location.
        Path(f"{invalid_prefix}/repo-exemplar-v2/"),
        # exemplar/ repo without LICENSE file.
        Path(f"{invalid_prefix}/repo-exemplar-v3/"),
    ]

    run_check_for_each_path(
        False,
        invalid_license_paths,
        ToplevelLicenseCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__TOPLEVEL_LICENSE__fix_inplace(repo_info, beman_standard_check_config):
    pass


def test__TOPLEVEL_README__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid README.md pass the check.
    """
    valid_readme_paths = [
        # exemplar/ repo with valid README.md file.
        Path(f"{valid_prefix}/repo-exemplar-v1/"),
    ]

    run_check_for_each_path(
        True,
        valid_readme_paths,
        ToplevelReadmeCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__TOPLEVEL_README__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid README.md fail the check.
    """
    invalid_readme_paths = [
        # exemplar/ repo with empty README.md file.
        Path(f"{invalid_prefix}/repo-exemplar-v1/"),
        # exemplar/ repo with README.md in non-root location.
        Path(f"{invalid_prefix}/repo-exemplar-v2/"),
        # exemplar/ repo without README.md file.
        Path(f"{invalid_prefix}/repo-exemplar-v3/"),
    ]

    run_check_for_each_path(
        False,
        invalid_readme_paths,
        ToplevelReadmeCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__TOPLEVEL_README__fix_inplace(repo_info, beman_standard_check_config):
    pass
