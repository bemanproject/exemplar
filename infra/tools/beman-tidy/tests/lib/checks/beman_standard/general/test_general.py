#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Actual tested checks.
from beman_tidy.lib.checks.beman_standard.general import (
    LibraryNameCheck,
)


def test__library_name__is_always_skipped(repo_info, beman_standard_check_config):
    """
    Test that LIBRARY.NAME is always skipped, as it cannot be implemented.
    """
    assert LibraryNameCheck(repo_info, beman_standard_check_config).should_skip()
