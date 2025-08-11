#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import re

red_color = "\033[91m"
green_color = "\033[92m"
yellow_color = "\033[93m"
gray_color = "\033[90m"
no_color = "\033[0m"


def is_snake_case(name):
    return re.match("(^[a-z0-9]+$)|(^[a-z0-9][a-z0-9_.]+[a-z0-9]$)", name)


def is_beman_snake_case(name):
    """
    Has prefix "beman." and continues with snake_case.
    It must NOT end with a C++ target standard version - e.g. 17, 20, 23, 26, 32, etc.
    """

    return (
        name[:6] != "beman." and is_snake_case(name) and not re.match(".*[0-9]+$", name)
    )


def match_badges(string):
    """
    e.g., ![Library Status](https://raw.githubusercontent.com/bemanproject/beman/refs/heads/main/images/badges/beman_badge-beman_library_under_development.svg) ![Continuous Integration Tests](https://github.com/bemanproject/exemplar/actions/workflows/ci_tests.yml/badge.svg) ![Lint Check (pre-commit)](https://github.com/bemanproject/exemplar/actions/workflows/pre-commit.yml/badge.svg)
    """
    if string is None:
        return None

    badges_str = re.findall(r"!\[[^\]]+\]\([^)]+\)", string)
    return [
        re.match(r"!\[([^\]]+)\]\(([^)]+)\)", badge).groups() for badge in badges_str
    ]


def match_apache_license_v2_with_llvm_exceptions(content):
    # beman/LICENSE contains the following text (multiple lines)
    # - Apache License
    # - Version 2.0
    # - LLVM Exceptions to the Apache 2.0 License
    #
    # We also check for variations.
    #
    license_regex = [
        rf"Apache License",  # noqa: F541
        rf"Apache License 2\.0 with LLVM Exceptions",  # noqa: F541
        rf"Apache License v2\.0 with LLVM Exceptions",  # noqa: F541,
    ]
    if not any(
        re.search(regex, content, re.IGNORECASE) is not None for regex in license_regex
    ):
        return False

    version_regex = [
        rf"Version 2\.0",  # noqa: F541,
        rf"Version v2\.0",  # noqa: F541,
        rf"Version 2\.0 with LLVM Exceptions",  # noqa: F541,
        rf"Version v2\.0 with LLVM Exceptions",  # noqa: F541,
        rf"Apache License 2\.0 with LLVM Exceptions",  # noqa: F541
        rf"Apache License v2\.0 with LLVM Exceptions",  # noqa: F541,
        rf"Apache 2\.0",  # noqa: F541,
        rf"Apache v2\.0",  # noqa: F541,
    ]
    if not any(
        re.search(regex, content, re.IGNORECASE) is not None for regex in version_regex
    ):
        return False

    llvm_exceptions_regex = [
        rf"LLVM Exceptions",  # noqa: F541,
        rf"Apache License 2\.0 with LLVM Exceptions",  # noqa: F541,
        rf"Apache License v2\.0 with LLVM Exceptions",  # noqa: F541,
        rf"LLVM Exceptions to the Apache 2\.0 License",  # noqa: F541,
    ]
    if not any(
        re.search(regex, content, re.IGNORECASE) is not None
        for regex in llvm_exceptions_regex
    ):
        return False

    return True


def match_boost_software_license_v1_0(content):
    # beman/LICENSE contains the following text (multiple lines)
    # - Boost Software License
    # - Version 1.0
    #
    # We also check for variations.
    #
    license_regex = [
        rf"Boost Software License",  # noqa: F541
        rf"Boost License",  # noqa: F541
        rf"Boost Software License 1\.0",  # noqa: F541,
        rf"Boost Software License Version 1\.0",  # noqa: F541,
    ]
    if not any(
        re.search(regex, content, re.IGNORECASE) is not None for regex in license_regex
    ):
        return False

    version_regex = [
        rf"Version 1\.0",  # noqa: F541,
        rf"V1\.0",  # noqa: F541,
        rf"Boost Software License 1\.0",  # noqa: F541,
        rf"Boost Software License Version 1\.0",  # noqa: F541,
    ]
    if not any(
        re.search(regex, content, re.IGNORECASE) is not None for regex in version_regex
    ):
        return False

    return True


def match_the_mit_license(content):
    # beman/LICENSE contains the following text (multiple lines)
    # - The MIT License
    #
    # We also check for variations.
    #
    license_regex = [
        rf"The MIT License",  # noqa: F541
        rf"MIT License",  # noqa: F541
    ]
    if not any(
        re.search(regex, content, re.IGNORECASE) is not None for regex in license_regex
    ):
        return False

    return True


def skip_lines(lines, n):
    return lines[n:] if lines is not None else None


def skip_empty_lines(lines):
    if lines is None:
        return None

    while len(lines) > 0 and len(lines[0].strip()) == 0:
        lines = lines[1:]
    return lines
