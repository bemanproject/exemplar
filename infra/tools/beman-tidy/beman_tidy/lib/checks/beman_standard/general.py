#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from ..base.file_base_check import FileBaseCheck
from ..system.registry import register_beman_standard_check

# [GENERAL.*] / [REPOSITORY.*] checks category.
# All checks in this file extend the GeneralBaseCheck class.
#
# Note: GeneralBaseCheck is not a registered check!


# TODO LIBRARY.NAMES
# TODO REPOSITORY.NAME


@register_beman_standard_check("REPOSITORY.CODEOWNERS")
class RepositoryCodeownersCheck(FileBaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config, ".github/CODEOWNERS")

    def check(self):
        # Since this class simply checks for the existence of a CODEOWNERS file,
        # there's nothing more to do than the default pre-check.
        return super().pre_check()

    def fix(self):
        self.log(
            "Please add a CODEOWNERS file to the repository. See https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#repositorycodeowners for more information."
        )


# TODO REPOSITORY.DISALLOW_GIT_SUBMODULES
