#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest
from pathlib import Path

from tests.utils.path_runners import (
    run_check_for_each_path,
    run_fix_inplace_for_each_file_path,
)

# Actual tested checks.
from beman_tidy.lib.checks.beman_standard.readme import (
    ReadmePurposeCheck,
    ReadmeTitleCheck,
    ReadmeBadgesCheck,
    ReadmeImplementsCheck,
    ReadmeLibraryStatusCheck,
    ReadmeLicenseCheck,
)

test_data_prefix = "tests/lib/checks/beman_standard/readme/data"
valid_prefix = f"{test_data_prefix}/valid"
invalid_prefix = f"{test_data_prefix}/invalid"


def test__readme_purpose__is_always_skipped(repo_info, beman_standard_check_config):
    """
    Test that readme.purpose is always skipped, as it cannot be implemented.
    """
    assert ReadmePurposeCheck(repo_info, beman_standard_check_config).should_skip()


def test__readme_title__valid(repo_info, beman_standard_check_config):
    """
    Test that a valid README.md title passes the check.
    """
    valid_readme_paths = [
        # Title: # beman.exemplar: A Beman Library Exemplar
        Path(f"{valid_prefix}/README-v1.md"),
        # Title: # beman.exemplar: Another Beman Library
        Path(f"{valid_prefix}/README-v2.md"),
        # Title: # beman.exemplar: Awesome Beman Library
        Path(f"{valid_prefix}/README-v3.md"),
        # Title: # beman.exemplar: The Most Awesome Beman Library
        Path(f"{valid_prefix}/README-v4.md"),
    ]

    run_check_for_each_path(
        True,
        valid_readme_paths,
        ReadmeTitleCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__readme_title__invalid(repo_info, beman_standard_check_config):
    """
    Test that an invalid README.md title fails the check.
    """
    invalid_readme_paths = [
        # Title: Wrong Title Format
        Path(f"{invalid_prefix}/invalid.md"),
        # Title: Missing . in beman.exemplar
        Path(f"{invalid_prefix}/invalid-title-v1.md"),
        # Title: Missing : after beman.exemplar
        Path(f"{invalid_prefix}/invalid-title-v2.md"),
        # Title: Wromg name beman.exemaplar vs beman.optional
        Path(f"{invalid_prefix}/invalid-title-v3.md"),
    ]

    run_check_for_each_path(
        False,
        invalid_readme_paths,
        ReadmeTitleCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__readme_title__fix_inplace(repo_info, beman_standard_check_config):
    """
    Test that the fix method corrects an invalid README.md title.
    """
    invalid_readme_paths = [
        Path(f"{invalid_prefix}/invalid-title-v1.md"),
        Path(f"{invalid_prefix}/invalid-title-v2.md"),
        Path(f"{invalid_prefix}/invalid-title-v3.md"),
    ]

    run_fix_inplace_for_each_file_path(
        invalid_readme_paths, ReadmeTitleCheck, repo_info, beman_standard_check_config
    )


def test__readme_badges__valid(repo_info, beman_standard_check_config):
    """
    Test that a valid README.md badges passes the check.
    """
    valid_readme_paths = [
        # Badges: under development status and cpp26 target
        Path(f"{valid_prefix}/README-v1.md"),
        # Badges: production ready (api may undergo changes) status and cpp26 target
        Path(f"{valid_prefix}/README-v2.md"),
        # Badges: production ready (stable api) status and cpp29 target
        Path(f"{valid_prefix}/README-v3.md"),
        # Badges: retired status and cpp26 target
        Path(f"{valid_prefix}/README-v4.md"),
    ]

    run_check_for_each_path(
        True,
        valid_readme_paths,
        ReadmeBadgesCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__readme_badges__invalid(repo_info, beman_standard_check_config):
    """
    Test that an invalid README.md badges fails the check.
    """
    invalid_readme_paths = [
        Path(f"{invalid_prefix}/invalid.md"),
        # Badges: typos in badge for library status
        Path(f"{invalid_prefix}/invalid-badge-v1.md"),
        # Badges: typos in badge for standard target
        Path(f"{invalid_prefix}/invalid-badge-v2.md"),
        # Badges: other description in badge for library status
        Path(f"{invalid_prefix}/invalid-badge-v3.md"),
        # Badges: other description in badge for standard target
        Path(f"{invalid_prefix}/invalid-badge-v4.md"),
        # Badges: non-sense badge for library status (broken badge URL)
        Path(f"{invalid_prefix}/invalid-badge-v5.md"),
        # Badges: non-sense badge for standard target (broken badge URL)
        Path(f"{invalid_prefix}/invalid-badge-v6.md"),
        # Badges: 1/2 badges are missing (standard target)
        Path(f"{invalid_prefix}/invalid-badge-v7.md"),
        # Badges: 1/2 badges are missing (library status)
        Path(f"{invalid_prefix}/invalid-badge-v8.md"),
    ]

    run_check_for_each_path(
        False,
        invalid_readme_paths,
        ReadmeBadgesCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="not implemented")
def test__readme_badges__fix_inplace(repo_info, beman_standard_check_config):
    """
    Test that the fix method corrects an invalid README.md badges.
    Note: Skipping this test as it is not implemented.
    """
    pass


def test__readme_implements__valid(repo_info, beman_standard_check_config):
    """
    Test that a valid README.md "Implements" passes the check
    """
    valid_readme_paths = [
        Path(f"{valid_prefix}/README-v1.md"),
        Path(f"{valid_prefix}/README-v2.md"),
        Path(f"{valid_prefix}/README-v3.md"),
        Path(f"{valid_prefix}/README-v4.md"),
    ]

    run_check_for_each_path(
        True,
        valid_readme_paths,
        ReadmeImplementsCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__readme_implements__invalid(repo_info, beman_standard_check_config):
    """
    Test that an invalid README.md "Implements" fails the check
    """
    invalid_readme_paths = [
        Path(f"{invalid_prefix}/invalid.md"),
        Path(f"{invalid_prefix}/invalid-implements-v1.md"),
        Path(f"{invalid_prefix}/invalid-implements-v2.md"),
        Path(f"{invalid_prefix}/invalid-implements-v3.md"),
        Path(f"{invalid_prefix}/invalid-implements-v4.md"),
    ]

    run_check_for_each_path(
        False,
        invalid_readme_paths,
        ReadmeImplementsCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="not implemented")
def test__readme_implements__fix_inplace(repo_info, beman_standard_check_config):
    """
    Test that the fix method corrects an invalid README.md "Implements".
    Note: Skipping this test as it is not implemented.
    """
    pass


def test__readme_library_status__valid(repo_info, beman_standard_check_config):
    """
    Test that a valid README.md library status passes the check.
    """
    valid_readme_paths = [
        Path(f"{valid_prefix}/README-v1.md"),
        Path(f"{valid_prefix}/README-v2.md"),
        Path(f"{valid_prefix}/README-v3.md"),
        Path(f"{valid_prefix}/README-v4.md"),
    ]

    run_check_for_each_path(
        True,
        valid_readme_paths,
        ReadmeLibraryStatusCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__readme_library_status__invalid(repo_info, beman_standard_check_config):
    """
    Test that an invalid README.md library status fails the check.
    """
    invalid_readme_paths = [
        Path(f"{invalid_prefix}/invalid.md"),
        Path(f"{invalid_prefix}/invalid-status-line-v1.md"),
        Path(f"{invalid_prefix}/invalid-status-line-v2.md"),
        Path(f"{invalid_prefix}/invalid-status-line-v3.md"),
    ]

    run_check_for_each_path(
        False,
        invalid_readme_paths,
        ReadmeLibraryStatusCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="not implemented")
def test__readme_library_status__fix_inplace(repo_info, beman_standard_check_config):
    """
    Test that the fix method corrects an invalid README.md library status.
    Note: Skipping this test as it is not implemented.
    """
    pass


def test__readme_license__valid(repo_info, beman_standard_check_config):
    """
    Test that a valid README.md license passes the check.
    """
    valid_readme_paths = [
        # License: Apache License 2.0 with LLVM Exceptions
        Path(f"{valid_prefix}/README-v1.md"),
        # License: Boost Software License 1.0
        Path(f"{valid_prefix}/README-v2.md"),
        # License: MIT License
        Path(f"{valid_prefix}/README-v3.md"),
        # License: Apache License 2.0 with LLVM Exceptions and MIT License
        Path(f"{valid_prefix}/README-v4.md"),
    ]

    run_check_for_each_path(
        True,
        valid_readme_paths,
        ReadmeLicenseCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__readme_license__invalid(repo_info, beman_standard_check_config):
    """
    Test that an invalid README.md license fails the check.
    """
    invalid_readme_paths = [
        # License: Missing license section
        Path(f"{invalid_prefix}/invalid-license-section-v1.md"),
        # License: Empty license section
        Path(f"{invalid_prefix}/invalid-license-section-v2.md"),
        # License: Invalid license
        Path(f"{invalid_prefix}/invalid-license-section-v3.md"),
    ]

    run_check_for_each_path(
        False,
        invalid_readme_paths,
        ReadmeLicenseCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="not implemented")
def test__readme_license__fix_inplace(repo_info, beman_standard_check_config):
    """
    Test that the fix method corrects an invalid README.md license.
    Note: Skipping this test as it is not implemented.
    """
    pass
