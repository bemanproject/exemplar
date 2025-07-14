#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest
from pathlib import Path

from tests.utils.path_runners import (
    run_check_for_each_path,
)

# Actual tested checks.
from beman_tidy.lib.checks.beman_standard.general import (
    RepositoryCodeownersCheck,
)

test_data_prefix = "tests/lib/checks/beman_standard/general/data"
valid_prefix = f"{test_data_prefix}/valid"
invalid_prefix = f"{test_data_prefix}/invalid"


def test__REPOSITORY_CODEOWNERS__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid CMakeLists.txt.
    """
    valid_cmake_paths = [
        Path(f"{valid_prefix}/repo-exemplar-v1/"),
    ]

    run_check_for_each_path(
        True,
        valid_cmake_paths,
        RepositoryCodeownersCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__REPOSITORY_CODEOWNERS__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid CMakeLists.txt.
    """
    invalid_cmake_paths = [
        # exemplar/ repo without CODEOWNERS file inside .github/.
        Path(f"{invalid_prefix}/repo-exemplar-v1/"),
        # exemplar/ repo with CODEOWNERS in root.
        Path(f"{invalid_prefix}/repo-exemplar-v2/"),
        # exemplar/ repo with empty .github/CODEOWNERS.
        Path(f"{invalid_prefix}/repo-exemplar-v3/"),
    ]

    run_check_for_each_path(
        False,
        invalid_cmake_paths,
        RepositoryCodeownersCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__REPOSITORY_CODEOWNERS__fix_inplace(repo_info, beman_standard_check_config):
    pass
