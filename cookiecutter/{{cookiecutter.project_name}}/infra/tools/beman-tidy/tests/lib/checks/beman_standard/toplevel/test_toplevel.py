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
)

test_data_prefix = "tests/lib/checks/beman_standard/toplevel/data"
valid_prefix = f"{test_data_prefix}/valid"
invalid_prefix = f"{test_data_prefix}/invalid"


def test__TOPLEVEL_CMAKE__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid CMakeLists.txt.
    """
    valid_cmake_paths = [
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
    Test that repositories with invalid CMakeLists.txt.
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
