#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import sys

from .checks.system.registry import get_registered_beman_standard_checks
from .checks.system.git import DisallowFixInplaceAndUnstagedChangesCheck
from .utils.string import (
    red_color,
    green_color,
    yellow_color,
    gray_color,
    no_color,
)

# import all the implemented checks.
# TODO: Consider removing F403 from ignored lint checks
from .checks.beman_standard.cmake import *  # noqa: F401, F403
from .checks.beman_standard.cpp import *  # noqa: F401, F403
from .checks.beman_standard.directory import *  # noqa: F401, F403
from .checks.beman_standard.file import *  # noqa: F401, F403
from .checks.beman_standard.general import *  # noqa: F401, F403
from .checks.beman_standard.license import *  # noqa: F401, F403
from .checks.beman_standard.readme import *  # noqa: F401, F403
from .checks.beman_standard.release import *  # noqa: F401, F403
from .checks.beman_standard.repository import *  # noqa: F401, F403
from .checks.beman_standard.toplevel import *  # noqa: F401, F403


def run_checks_pipeline(checks_to_run, args, beman_standard_check_config):
    """
    Run the checks pipeline for The Beman Standard.
    Read-only checks if args.fix_inplace is False, otherwise try to fix the issues in-place.
    Verbosity is controlled by args.verbose.

    @return: The number of failed checks.
    """

    def log(msg):
        """
        Helper function to log messages.
        """
        if args.verbose:
            print(msg)

    def run_check(check_class, log_enabled=args.verbose, require_all=args.require_all):
        """
        Helper function to run a check.
        @param check_class: The check class type to run.
        @param log_enabled: Whether to log the check result.
        @return: True if the check passed, False otherwise.
        """
        check_instance = check_class(args.repo_info, beman_standard_check_config)

        # Check if the check should be skipped, with logging disabled (by default).
        if check_instance.should_skip():
            log(f"Running check [{check_instance.type}][{check_instance.name}] ... ")
            check_instance.log_enabled = log_enabled
            check_instance.should_skip()  # Run should_skip() again, with logging enabled.
            log(
                f"Running check [{check_instance.type}][{check_instance.name}] ... {gray_color}skipped{no_color}\n"
            )
            return check_instance.type, "skipped"
        elif require_all and check_instance.type == "Recommendation":
            # Convert the check to a requirement because --require-all is set.
            check_instance.convert_to_requirement()

        # Run the check on normal mode.
        log(f"Running check [{check_instance.type}][{check_instance.name}] ... ")
        check_instance.log_enabled = log_enabled
        if (check_instance.pre_check() and check_instance.check()) or (
            args.fix_inplace and check_instance.fix()
        ):
            log(
                f"\tcheck [{check_instance.type}][{check_instance.name}] ... {green_color}passed{no_color}\n"
            )
            return check_instance.type, "passed"
        else:
            log(
                f"\tcheck [{check_instance.type}][{check_instance.name}] ... {red_color}failed{no_color}\n"
            )
            return check_instance.type, "failed"

    def run_pipeline_helper():
        """
        Helper function to run the pipeline.
        """
        # Internal checks
        if args.fix_inplace:
            run_check(DisallowFixInplaceAndUnstagedChangesCheck, log_enabled=True)

        implemented_checks = get_registered_beman_standard_checks()
        all_checks = beman_standard_check_config

        # All checks from the Beman Standard.
        cnt_all_beman_standard_checks = {
            "Requirement": 0,
            "Recommendation": 0,
        }
        # All checks from the Beman Standard that are implemented.
        cnt_implemented_checks = {
            "Requirement": 0,
            "Recommendation": 0,
        }
        # All checks from the Beman Standard that are not implemented.
        cnt_not_implemented_checks = {
            "Requirement": 0,
            "Recommendation": 0,
        }
        # All implemented checks that passed.
        cnt_passed_checks = {
            "Requirement": 0,
            "Recommendation": 0,
        }
        # All implemented checks that failed.
        cnt_failed_checks = {
            "Requirement": 0,
            "Recommendation": 0,
        }
        # All implemented checks that were skipped (e.g., dummy implementation
        # or it cannot be implemented).
        cnt_skipped_checks = {
            "Requirement": 0,
            "Recommendation": 0,
        }

        # Run the checks.
        for check_name in checks_to_run:
            if check_name not in implemented_checks:
                continue

            check_type, status = run_check(implemented_checks[check_name])
            if status == "passed":
                cnt_passed_checks[check_type] += 1
            elif status == "failed":
                cnt_failed_checks[check_type] += 1
            elif status == "skipped":
                cnt_skipped_checks[check_type] += 1
            else:
                raise ValueError(f"Invalid status: {status}")

        # Count the checks from the Beman Standard.
        for check_name in all_checks:
            check_type = (
                all_checks[check_name]["type"]
                if not args.require_all
                else "Requirement"
            )
            cnt_all_beman_standard_checks[check_type] += 1

            if check_name not in implemented_checks:
                cnt_not_implemented_checks[check_type] += 1
            else:
                cnt_implemented_checks[check_type] += 1

        return (
            cnt_passed_checks,
            cnt_failed_checks,
            cnt_skipped_checks,
            cnt_all_beman_standard_checks,
            cnt_implemented_checks,
            cnt_not_implemented_checks,
        )

    log("beman-tidy pipeline started ...\n")
    (
        cnt_passed_checks,
        cnt_failed_checks,
        cnt_skipped_checks,
        cnt_all_beman_standard_checks,
        cnt_implemented_checks,
        cnt_not_implemented_checks,
    ) = run_pipeline_helper()
    log("\nbeman-tidy pipeline finished.\n")

    # Always print the summary.
    print(
        f"Summary    Requirement: {green_color} {cnt_passed_checks['Requirement']} checks passed{no_color}, {red_color}{cnt_failed_checks['Requirement']} checks failed{no_color}, {gray_color}{cnt_skipped_checks['Requirement']} checks skipped, {no_color} {cnt_not_implemented_checks['Requirement']} checks not implemented."
    )
    print(
        f"Summary Recommendation: {green_color} {cnt_passed_checks['Recommendation']} checks passed{no_color}, {red_color}{cnt_failed_checks['Recommendation']} checks failed{no_color}, {gray_color}{cnt_skipped_checks['Recommendation']} checks skipped, {no_color} {cnt_not_implemented_checks['Recommendation']} checks not implemented."
    )

    # Always print the coverage.
    cnt_passed_requirement = (
        cnt_passed_checks["Requirement"] + cnt_skipped_checks["Requirement"]
        if not args.require_all
        else cnt_passed_checks["Requirement"]
        + cnt_skipped_checks["Requirement"]
        + cnt_passed_checks["Recommendation"]
        + cnt_skipped_checks["Recommendation"]
    )
    total_implemented_requirement = (
        cnt_implemented_checks["Requirement"] + cnt_implemented_checks["Recommendation"]
        if not args.require_all
        else cnt_implemented_checks["Requirement"]
    )
    coverage_requirement = round(
        cnt_passed_requirement / total_implemented_requirement * 100,
        2,
    )
    cnt_passed_recommendation = (
        cnt_passed_checks["Recommendation"] + cnt_skipped_checks["Recommendation"]
        if not args.require_all
        else 0
    )
    total_implemented_recommendation = (
        cnt_implemented_checks["Recommendation"] if not args.require_all else 0
    )
    coverage_recommendation = (
        round(
            cnt_passed_recommendation / total_implemented_recommendation * 100,
            2,
        )
        if total_implemented_recommendation > 0
        else 0
    )
    total_passed = (
        cnt_passed_checks["Requirement"]
        + cnt_passed_checks["Recommendation"]
        + cnt_skipped_checks["Requirement"]
        + cnt_skipped_checks["Recommendation"]
    )
    total_implemented = total_implemented_requirement + total_implemented_recommendation
    total_coverage = round((total_passed) / (total_implemented) * 100, 2)
    print(
        f"\n{calculate_coverage_color(coverage_requirement)}Coverage    Requirement: {coverage_requirement:{6}.2f}% ({cnt_passed_requirement}/{total_implemented_requirement} checks passed).{no_color}"
    )
    print(
        f"{calculate_coverage_color(coverage_recommendation, no_color=args.require_all)}Coverage Recommendation: {coverage_recommendation:{6}.2f}% ({cnt_passed_recommendation}/{total_implemented_recommendation} checks passed).{no_color}"
    )
    print(
        f"{calculate_coverage_color(total_coverage)}Coverage          TOTAL: {total_coverage:{6}.2f}% ({total_passed}/{total_implemented} checks passed).{no_color}"
    )
    # else:
    #     print("Note: RECOMMENDATIONs are not included (--require-all NOT set).")
    total_cnt_failed = cnt_failed_checks["Requirement"] + (
        cnt_failed_checks["Recommendation"] if args.require_all else 0
    )

    sys.stdout.flush()
    return total_cnt_failed


def calculate_coverage_color(coverage, no_color=False):
    """
    Returns the colour for the coverage print based on severity
    Green for 100%
    Red for 0%
    Yellow for anything else

    Exception: If no_color is True, the color will be removed.
    """
    if no_color:
        return gray_color
    elif coverage == 100:
        return green_color
    elif coverage == 0:
        return red_color
    else:
        return yellow_color
