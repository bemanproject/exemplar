#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import os
from pathlib import Path

def file_testcase_run(file_path, check_class, repo_info, beman_standard_check_config, expected_result):
    check_instance = check_class(repo_info, beman_standard_check_config)
    check_instance.path = Path(file_path)
    check_instance.log_level = True

    assert check_instance.pre_check(
    ) is True, f"[{check_instance.__class__.__name__}] pre_check() failed for {file_path}"
    assert check_instance.check(
    ) is expected_result, f"[{check_instance.__class__.__name__}] check() failed for {file_path}"


def file_testcase_run_valid(file_path, check_class, repo_info, beman_standard_check_config):
    file_testcase_run(file_path, check_class, repo_info,
                      beman_standard_check_config, True)


def file_testcase_run_invalid(file_path, check_class, repo_info, beman_standard_check_config):
    file_testcase_run(file_path, check_class, repo_info,
                      beman_standard_check_config, False)


def file_testcase_run_fix_invalid(invalid_file_path, check_class, repo_info, beman_standard_check_config):
    check_instance = check_class(repo_info, beman_standard_check_config)
    check_instance.path = Path(f"{invalid_file_path}.delete_me")
    check_instance.write(invalid_file_path.read_text())

    assert check_instance.pre_check() is True
    assert check_instance.check() is False

    assert check_instance.fix() is True

    assert check_instance.pre_check() is True
    assert check_instance.check() is True

    # Delete the temporary file
    os.remove(f"{invalid_file_path}.delete_me")


def file_testcases_run(file_paths, check_class, repo_info, beman_standard_check_config, expected_result):
    for file_path in file_paths:
        file_testcase_run(file_path, check_class, repo_info,
                          beman_standard_check_config, expected_result)


def file_testcases_run_valid(file_paths, check_class, repo_info, beman_standard_check_config):
    file_testcases_run(file_paths, check_class, repo_info,
                       beman_standard_check_config, True)


def file_testcases_run_invalid(file_paths, check_class, repo_info, beman_standard_check_config):
    file_testcases_run(file_paths, check_class, repo_info,
                       beman_standard_check_config, False)


def file_testcases_run_fix_invalid(invalid_file_paths, check_class, repo_info, beman_standard_check_config):
    for invalid_file_path in invalid_file_paths:
        file_testcase_run_fix_invalid(
            invalid_file_path, check_class, repo_info, beman_standard_check_config)
