#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import re
import textwrap

from ..base.file_base_check import FileBaseCheck
from ..base.base_check import BaseCheck
from ..system.registry import register_beman_standard_check
from ...utils.string import is_beman_snake_case

# [repository.*] checks category.
# All checks in this file extend the FileBaseCheck class.
#
# Note: FileBaseCheck is not a registered check!


@register_beman_standard_check("repository.name")
class RepositoryNameCheck(BaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def check(self):
        repo_name = self.repo_info["name"]
        if not is_beman_snake_case(repo_name):
            self.log(
                "The repository should be named after the library name excluding the 'beman.' prefix. It should not contain a target C++ version. "
                "See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#repositoryname for more information."
            )
            return False

        return True

    def fix(self):
        self.log(
            "beman-tidy can't automatically fix the repository name. "
            "Please see https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#repositoryname for more information."
        )
        pass


@register_beman_standard_check("repository.default_branch")
class RepositoryDefaultBranchCheck(BaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def check(self):
        default_branch = self.repo_info["default_branch"]
        if default_branch != "main":
            self.log(f"Invalid default branch in repo: {default_branch} vs 'main'.")
            return False

        return True

    def fix(self):
        self.log(
            "Please set `main` as default branch in the repository. See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#repositorydefault_branch for more information."
        )


@register_beman_standard_check("repository.codeowners")
class RepositoryCodeownersCheck(FileBaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config, ".github/CODEOWNERS")

    def check(self):
        # Since this class simply checks for the existence of a CODEOWNERS file,
        # there's nothing more to do than the default pre-check.
        return super().pre_check()

    def fix(self):
        self.log(
            "Please add a CODEOWNERS file to the repository. See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#repositorycodeowners for more information."
        )


@register_beman_standard_check("repository.code_review_rules")
class RepositoryCodeReviewRulesCheck(BaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def should_skip(self):
        # Cannot actually implement repository.code_review_rules, thus skip it.
        self.log(
            "beman-tidy cannot actually check repository.code_review_rules. "
            "See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#repositorycode_review_rules."
        )
        return True


@register_beman_standard_check("repository.disallow_git_submodules")
class RepositoryDisallowGitSubmodulesCheck(FileBaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config, ".gitmodules")

    def pre_check(self):
        # Need to override this, because REPOSITORY.DISALLOW_GIT_SUBMODULES is conditional
        return True

    def check(self):
        if self.path.exists():
            content = self.read()

            # Regex pattern to match "wg21" submodule
            regex = re.compile(
                textwrap.dedent(r"""
                    ^\[submodule \"(?:.+?/)?wg21\"]
                    \tpath = papers/(.+?)
                    \turl = https://github.com/mpark/wg21.git$
                """).strip()
            )

            if not regex.match(content):
                self.log(
                    "The repository should not use git submodules. Please remove them. "
                    "Known exception: wg21. "
                    "See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#repositorydisallow_git_submodules for more information."
                )
                return False

        # Check passes if .gitmodules file doesn't exist or if it only contains wg21 submodule.
        return True

    def fix(self):
        self.log(
            "beman-tidy can't automatically fix the repository submodules. "
            "See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#repositorydisallow_git_submodules for more information."
        )
