#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest
from pathlib import Path

from tests.utils.path_runners import (
    run_check_for_each_path,
    run_check_for_each_repo_info,
)

# Actual tested checks.
from beman_tidy.lib.checks.beman_standard.repository import (
    RepositoryCodeownersCheck,
    RepositoryDefaultBranchCheck,
)

test_data_prefix = "tests/lib/checks/beman_standard/repository/data"
valid_prefix = f"{test_data_prefix}/valid"
invalid_prefix = f"{test_data_prefix}/invalid"


def test__REPOSITORY_CODEOWNERS__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid CODEOWNERS pass the check.
    """
    valid_codeowners_paths = [
        # exemplar/ repo with valid .github/CODEOWNERS file.
        Path(f"{valid_prefix}/repo-exemplar-v1/"),
    ]

    run_check_for_each_path(
        True,
        valid_codeowners_paths,
        RepositoryCodeownersCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__REPOSITORY_CODEOWNERS__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid CODEOWNERS fail the check.
    """
    invalid_codeowners_paths = [
        # exemplar/ repo without CODEOWNERS file inside .github/.
        Path(f"{invalid_prefix}/repo-exemplar-v1/"),
        # exemplar/ repo with CODEOWNERS in root.
        Path(f"{invalid_prefix}/repo-exemplar-v2/"),
        # exemplar/ repo with empty .github/CODEOWNERS.
        Path(f"{invalid_prefix}/repo-exemplar-v3/"),
    ]

    run_check_for_each_path(
        False,
        invalid_codeowners_paths,
        RepositoryCodeownersCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__REPOSITORY_CODEOWNERS__fix_inplace(repo_info, beman_standard_check_config):
    pass


def test__REPOSITORY_DEFAULT_BRANCH__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid default branch pass the check.
    """
    # Create mock repo info with valid default branch
    valid_repo_infos = [
        repo_info.copy() | {"default_branch": "main"},
    ]

    run_check_for_each_repo_info(
        True,
        RepositoryDefaultBranchCheck,
        valid_repo_infos,
        beman_standard_check_config,
    )


def test__REPOSITORY_DEFAULT_BRANCH__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid default branch fail the check.
    """
    # Test various invalid branch names
    invalid_repo_infos = [
        repo_info.copy() | {"default_branch": "master"},
        repo_info.copy() | {"default_branch": "develop"},
        repo_info.copy() | {"default_branch": "dev"},
        repo_info.copy() | {"default_branch": "trunk"},
        repo_info.copy() | {"default_branch": "default"},
        repo_info.copy() | {"default_branch": "production"},
        repo_info.copy() | {"default_branch": "release"},
        repo_info.copy() | {"default_branch": "stable"},
        repo_info.copy() | {"default_branch": "testing"},
        repo_info.copy() | {"default_branch": "alpha"},
        repo_info.copy() | {"default_branch": "beta"},
        repo_info.copy() | {"default_branch": "experimental"},
    ]

    run_check_for_each_repo_info(
        False,
        RepositoryDefaultBranchCheck,
        invalid_repo_infos,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__REPOSITORY_DEFAULT_BRANCH__fix_inplace(
    repo_info, beman_standard_check_config
):
    pass
