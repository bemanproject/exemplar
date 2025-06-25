#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from ..base.base_check import BaseCheck
from ..system.registry import register_beman_standard_check

# [TOPLEVEL.*] checks category.
# All checks in this file extend the ToplevelBaseCheck class.
#
# Note: ToplevelBaseCheck is not a registered check!


class ToplevelBaseCheck(BaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

@register_beman_standard_check("TOPLEVEL.CMAKE")
class ToplevelCmakeCheck(ToplevelBaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def check(self):
        """
        self.config["value"] contains the CMake file name.
        """
        self.path = self.repo_path / self.config["value"]
        assert self.config["value"].endswith(".txt")

        if not self.path.exists():
            self.log("The top-level CMake file does not exist.")
            return False

        try:
            with open(self.path, 'r') as file:
                if len(file.read()) == 0:
                    self.log("The top-level CMake file is empty.")
                    return False
        except Exception:
            self.log("Failed to read the top-level CMake file.")
            return False

        return True

    def fix(self):
        # TODO: Implement the fix.
        pass

# TODO TOPLEVEL.LICENSE - use FileBaseCheck


# TODO TOPLEVEL.README - use ReadmeBaseCheck
