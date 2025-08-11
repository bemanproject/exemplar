#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from abc import ABC
from pathlib import Path

from ..system.registry import get_beman_standard_check_name_by_class
from ...utils.string import (
    red_color,
    yellow_color,
    gray_color,
    no_color,
)


class BaseCheck(ABC):
    """
    Base class for checks.
    This class is not meant to be used directly, it's meant to be subclassed.
    e.g., check for repository name, check for changelog, check for license, etc.


    Notes: If should_skip() is True, check()/fix() are not called,
    thus an implementation is not required in the derived class.
    """

    def __init__(self, repo_info, beman_standard_check_config, name=None):
        """
        Create a new check instance.
        """

        # check name -  e.g. "readme.title"
        self.name = (
            name
            if name is not None
            else get_beman_standard_check_name_by_class(self.__class__)
        )
        assert self.name is not None, (
            f"Check name not found for class: {self.__class__.__name__}"
        )

        # save the check config
        self.config = (
            beman_standard_check_config[self.name]
            if "internal." not in self.name
            else None
        )

        # set type - e.g. "Requirement" or "Recommendation"
        self.type = (
            beman_standard_check_config[self.name]["type"]
            if "internal." not in self.name
            else "Requirement"
        )
        assert self.type in ["Requirement", "Recommendation"], (
            f"Invalid check type: {self.type} for check = {self.name}."
        )

        # set full text body - e.g. "The README.md should begin ..."
        self.full_text_body = (
            beman_standard_check_config[self.name]["full_text_body"]
            if "internal." not in self.name
            else ""
        )
        assert self.full_text_body is not None

        # set log level - e.g. "error" or "warning" or "skipped"
        self.log_enabled = False
        self.log_level = (
            "skipped"
            if self.should_skip()
            else "error"
            if self.type == "Requirement"
            else "warning"
        )

        # set repo info
        self.repo_info = repo_info
        assert "name" in repo_info
        self.repo_name = repo_info["name"]
        assert "top_level" in repo_info
        self.repo_path = Path(repo_info["top_level"])
        assert self.repo_path is not None
        self.library_name = f"beman.{self.repo_name}"
        assert self.library_name is not None

        # set beman library maturity model
        beman_library_maturity_model = beman_standard_check_config[
            "readme.library_status"
        ]
        assert "values" in beman_library_maturity_model
        assert len(beman_library_maturity_model["values"]) == 4
        self.beman_library_maturity_model = beman_library_maturity_model["values"]

    def should_skip(self):
        """
        Returns True if the check should be skipped.
        If should_skip(), the pipeline will skip the check and not run pre_check(), check() and fix().
        """
        return False

    def pre_check(self):
        """
        Pre-checks if this rule is properly initialized.
        Usually, this is internal use only.

        Note: This method is internally called by the framework.
        """
        if self.name is None:
            self.log("The name is not set.")
            return False

        if self.repo_name is None:
            self.log(f"The repo_name is not set for check = {self.name}.")
            return False

        if not self.repo_path:
            self.log(f"The repo_path is not set for check = {self.name}.")
            return False

        return True

    def check(self):
        """
        Checks if the Beman Standard check is already applied.
        - If it's applied, this method should return True.
        - Otherwise, it returns False and self.fix() must be able to fix the issue.

        Note: This method must be implemented in the derived class only if should_skip() is False.
        """
        assert False, (
            "This method must be implemented in the derived class if should_skip() is False."
        )

    def fix(self):
        """
        Fixes the issue if the Beman Standard is not applied.
        - If check already applied, this method is a no-op and should return True.
        - Otherwise, it will try to apply the check inplace. Returns the status of the fix attempt.

        Note: This method must be implemented in the derived class only if should_skip() is False.
        The subclasses might not implement more than a stub if the fix method
        is too difficult to implement or does not make sense.
        """
        assert False, (
            "This method must be implemented in the derived class if should_skip() is False."
        )

    def convert_to_requirement(self):
        """
        Converts the check from Recommendation to Requirement.
        """
        assert self.type == "Recommendation", (
            f"Cannot convert check {self.name} to Requirement."
        )
        self.type = "Requirement"
        self.log_level = "error"

    def log(self, message, enabled=True, log_level=None):
        """
        Logs a message with the check's log level.
        e.g. [WARN][repository.name]: The name "${name}" should be snake_case.'
        e.g. [error][toplevel.cmake]: Missing top level CMakeLists.txt.'
        """

        if self.log_enabled and enabled:
            log_level = log_level if log_level else self.log_level
            color = (
                red_color
                if log_level == "error"
                else yellow_color
                if log_level == "warning"
                else gray_color
                if log_level == "skipped"
                else no_color
            )

            print(f"[{color}{log_level:<15}{no_color}][{self.name:<25}]: {message}")
