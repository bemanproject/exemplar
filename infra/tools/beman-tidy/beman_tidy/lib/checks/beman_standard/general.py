#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from ..base.base_check import BaseCheck
from ..system.registry import register_beman_standard_check


# General checks category.
# All checks in this file extend the BaseCheck class.
#
# Note: BaseCheck is not a registered check!


@register_beman_standard_check("library.name")
class LibraryNameCheck(BaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def should_skip(self):
        # Cannot actually implement library.name, so skip it.
        # No need to run pre_check() and check() as well, as they are not implemented.
        self.log(
            "beman-tidy cannot actually check library.name. Please ignore this message if cmake.library_name and repository.name have passed. "
            "See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#libraryname for more information."
        )
        return True
