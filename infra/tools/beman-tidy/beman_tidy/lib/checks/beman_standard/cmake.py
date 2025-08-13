#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from ..base.file_base_check import FileBaseCheck

# [cmake.*] checks category.
# All checks in this file extend the CMakeBaseCheck class.
#
# Note: CMakeBaseCheck is not a registered check!


class CMakeBaseCheck(FileBaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config, "CMakeLists.txt")


# TODO cmake.default


# TODO cmake.use_fetch_content


# TODO cmake.project_name


# TODO cmake.passive_projects


# TODO cmake.library_name


# TODO cmake.library_alias


# TODO cmake.target_names


# TODO cmake.passive_targets


# TODO cmake.skip_tests


# TODO cmake.skip_examples


# TODO cmake.avoid_passthroughs
