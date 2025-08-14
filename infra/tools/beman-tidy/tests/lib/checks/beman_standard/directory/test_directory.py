#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest
from pathlib import Path

from tests.utils.path_runners import (
    run_check_for_each_path,
)

# Actual tested checks.
from beman_tidy.lib.checks.beman_standard.directory import (
    DirectorySourcesCheck,
)

test_data_prefix = "tests/lib/checks/beman_standard/directory/data"
valid_prefix = f"{test_data_prefix}/valid"
invalid_prefix = f"{test_data_prefix}/invalid"


def test__DIRECTORY_SOURCES__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid CMakeLists.txt.
    """
    valid_cmake_paths = [
        # exemplar/ repo with src/beman/exemplar/ - valid source tree.
        Path(f"{valid_prefix}/repo-exemplar-v1/"),
        # exemplar/ repo without src/ - no source files (header-only).
        Path(f"{valid_prefix}/repo-exemplar-v2/"),
    ]

    run_check_for_each_path(
        True,
        valid_cmake_paths,
        DirectorySourcesCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__DIRECTORY_SOURCES__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid CMakeLists.txt.
    """
    invalid_cmake_paths = [
        # Sources in src/beman/optional - wrong inner directory.
        Path(f"{invalid_prefix}/repo-exemplar-v1"),
        # Sources in src/beman/ - missing 3rd subdirectory.
        Path(f"{invalid_prefix}/repo-exemplar-v2"),
        # Sources in src/ - missing 2nd and 3rd subdirectories.
        Path(f"{invalid_prefix}/repo-exemplar-v3"),
        # Sources in sources/ - wrong prefix.
        Path(f"{invalid_prefix}/repo-exemplar-v4"),
        # Sources in source/ - wrong prefix.
        Path(f"{invalid_prefix}/repo-exemplar-v5"),
        # Sources in lib/ - wrong prefix.
        Path(f"{invalid_prefix}/repo-exemplar-v6"),
        # Sources in library/ - wrong prefix.
        Path(f"{invalid_prefix}/repo-exemplar-v7"),
    ]

    run_check_for_each_path(
        False,
        invalid_cmake_paths,
        DirectorySourcesCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__DIRECTORY_SOURCES__fix_inplace(repo_info, beman_standard_check_config):
    pass
