#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import re
from beman_tidy.lib.checks.base.base_check import BaseCheck
from beman_tidy.lib.checks.beman_standard.readme import ReadmeBaseCheck
from ..system.registry import register_beman_standard_check

# [release.*] checks category.
# Note: Data is stored online - e.g. https://github.com/bemanproject/exemplar/releases
# beman-tidy is an offline tool, so it cannot check these issues,
# but for some of them it will try some heuristics.


@register_beman_standard_check("release.github")
class ReleaseGithubCheck(BaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def should_skip(self):
        # Cannot actually implement release.github, thus skip it.
        self.log(
            "beman-tidy cannot actually check release.github. "
            "See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#releasegithub."
        )
        return True


@register_beman_standard_check("release.notes")
class ReleaseNotesCheck(BaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def should_skip(self):
        # Cannot actually implement release.notes, thus skip it.
        self.log(
            "beman-tidy cannot actually check release.notes. "
            "See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#releasenotes."
        )
        return True


@register_beman_standard_check("release.godbolt_trunk_version")
class ReleaseGodboltTrunkVersionCheck(ReadmeBaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def check(self):
        """
        Check that the Godbolt badge is present in the root README.md file.
        If present, this assumes that the trunk version is available on Godbolt.

        e.g. [![Compiler Explorer Example](https://img.shields.io/badge/Try%20it%20on%20Compiler%20Explorer-grey?logo=compilerexplorer&logoColor=67c52a)](https://godbolt.org/z/Gc6Y9j6zf)
        Note: Only the suffix of the https://godbolt.org/z/* has dynamic content.
        """

        content = self.read()
        regex = re.compile(
            r"\[!\[Compiler Explorer Example\]\(https://img\.shields\.io/badge/Try%20it%20on%20Compiler%20Explorer-grey\?logo=compilerexplorer&logoColor=67c52a\)\]\(https://godbolt\.org/z/([a-zA-Z0-9]+)\)"
        )
        if not re.search(regex, content):
            self.log(
                f"The file '{self.path}' does not contain a Compiler Explorer badge - trunk version assumed to be missing."
            )
            return False

        return True

    def fix(self):
        self.log(
            "beman-tidy cannot fix this issue. See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#releasegodbolt_trunk_version."
        )
