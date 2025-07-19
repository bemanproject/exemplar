#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import sys

from ..base.base_check import BaseCheck


class DisallowFixInplaceAndUnstagedChangesCheck(BaseCheck):
    """
    --fix-inplace requires no unstaged changes.
    """

    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(
            repo_info, beman_standard_check_config, "INTERNAL.NO_UNSTAGED_CHANGES"
        )

    def check(self):
        """
        Should not allow fix if there are unstaged changes.
        """
        return len(self.repo_info["unstaged_changes"]) == 0

    def fix(self):
        """
        Stop the program if there are unstaged changes.
        """
        self.log(
            "The --fix-inplace requires no unstaged changes. Please commit or stash your changes. STOP."
        )
        sys.exit(1)
