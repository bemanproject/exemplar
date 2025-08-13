# beman-tidy: The Codebase Bemanification Tool

<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

## Description

`beman-tidy` is a tool used to check and apply
[The Beman Standard](https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md).

Purpose: The tool is used to `check` (`--dry-run`) and `apply` (`--fix-inplace`) the Beman Standard to a repository.
Note: `2025-06-07`: In order to make the best and quickly use of the tool in the entire organization, most of the
checks will not support the `--fix-inplace` flag in the first iteration.

## Installation

- The current recommended workflow relies on [Astral's uv](https://docs.astral.sh/uv/)
- However, we provide a [PEP 751](https://peps.python.org/pep-0751/) `pylock.toml`, so don't feel forced to use uv
- You can use beman-tidy as a pre-commit hook or install it on your system using `pipx`

```shell
uv build
pipx install path/to/wheel
```

<details>
<summary>beman-tidy: Full example - build and install</summary>

```shell
$ uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist/beman_tidy-0.1.0.tar.gz
Successfully built dist/beman_tidy-0.1.0-py3-none-any.whl

$ pipx install dist/beman_tidy-0.1.0-py3-none-any.whl
Installing to existing venv 'beman-tidy'
  installed package beman-tidy 0.1.0, installed using Python 3.13.4
  These apps are now globally available
    - beman-tidy
...
You will need to open a new terminal or re-login for the PATH changes to take effect. Alternatively, you can source your shell's config file with e.g. 'source ~/.bashrc'.

$ beman-tidy --help
usage: beman-tidy [-h] [--fix-inplace | --no-fix-inplace] [--verbose | --no-verbose] [--checks CHECKS] repo_path
...
```

</details>

## Usage

- Display help:

```shell
$ uv run beman-tidy --help
usage: beman-tidy [-h] [--fix-inplace | --no-fix-inplace] [--verbose | --no-verbose] [--require-all | --no-require-all] [--checks CHECKS] repo_path

positional arguments:
  repo_path             path to the repository to check

options:
  -h, --help            show this help message and exit
  --fix-inplace, --no-fix-inplace
                        Try to automatically fix found issues
  --verbose, --no-verbose
                        print verbose output for each check
  --require-all, --no-require-all
                        all checks are required regardless of the check type (e.g., Recommendation becomes Requirement)
  --checks CHECKS       array of checks to run
```

- Run beman-tidy on the exemplar repository **(default: dry-run mode)**

```shell
# dry-run, require-all, non-verbose
$ uv run beman-tidy /path/to/exemplar --require-all
Summary    Requirement:  18 checks passed, 1 checks failed, 5 checks skipped,  23 checks not implemented.
Summary Recommendation:  0 checks passed, 0 checks failed, 0 checks skipped,  0 checks not implemented.

Coverage    Requirement:  95.83% (23/24 checks passed).
Coverage Recommendation:   0.00% (0/0 checks passed).
Coverage          TOTAL:  95.83% (23/24 checks passed).

# dry-run, non-require-all, non-verbose
Summary    Requirement:  13 checks passed, 1 checks failed, 3 checks skipped,  9 checks not implemented.
Summary Recommendation:  5 checks passed, 0 checks failed, 2 checks skipped,  14 checks not implemented.

Coverage    Requirement:  66.67% (16/24 checks passed).
Coverage Recommendation: 100.00% (7/7 checks passed).
Coverage          TOTAL:  74.19% (23/31 checks passed).
```

or verbose mode without errors:

```shell
# dry-run, require-all, verbose mode - no errors
beman-tidy pipeline started ...

Running check [Requirement][license.approved] ...
[info           ][license.approved         ]: Valid Apache License - Version 2.0 with LLVM Exceptions found in LICENSE file.
	check [Requirement][license.approved] ... passed

Running check [Requirement][license.apache_llvm] ...
	check [Requirement][license.apache_llvm] ... passed

Running check [Requirement][license.criteria] ...
[skipped        ][license.criteria         ]: beman-tidy cannot actually check license.criteria. Please ignore this message if license.approved has passed. See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#licensecriteria for more information.
Running check [Requirement][license.criteria] ... skipped

...

Running check [Requirement][readme.title] ...
	check [Requirement][readme.title] ... passed

Running check [Requirement][readme.badges] ...
	check [Requirement][readme.badges] ... passed

Running check [Requirement][readme.implements] ...
	check [Requirement][readme.implements] ... passed

...

beman-tidy pipeline finished.

Summary    Requirement:  19 checks passed, 0 checks failed, 3 checks skipped,  23 checks not implemented.
Summary Recommendation:  0 checks passed, 0 checks failed, 2 checks skipped,  0 checks not implemented.

Coverage    Requirement: 100.00% (24/24 checks passed).
Coverage Recommendation:   0.00% (0/0 checks passed).
Coverage          TOTAL: 100.00% (24/24 checks passed).
```

or verbose mode with errors:

```shell
# dry-run, require-all, verbose mode - with errors
beman-tidy pipeline started ...

Running check [Requirement][license.approved] ...
[info           ][license.approved         ]: Valid Apache License - Version 2.0 with LLVM Exceptions found in LICENSE file.
	check [Requirement][license.approved] ... passed

Running check [Requirement][license.apache_llvm] ...
	check [Requirement][license.apache_llvm] ... passed

Running check [Requirement][license.criteria] ...
[skipped        ][license.criteria         ]: beman-tidy cannot actually check license.criteria. Please ignore this message if license.approved has passed. See https://github.com/bemanproject/beman/blob/main/docs/beman_standard.md#licensecriteria for more information.
Running check [Requirement][license.criteria] ... skipped

...

Running check [Requirement][readme.implements] ...
	check [Requirement][readme.implements] ... passed

Running check [Requirement][readme.library_status] ...
[error          ][readme.library_status    ]: The file '/Users/dariusn/dev/dn/git/Beman/exemplar/README.md' does not contain exactly one of the required statuses from ['**Status**: [Under development and not yet ready for production use.](https://github.com/bemanproject/beman/blob/main/docs/beman_library_maturity_model.md#under-development-and-not-yet-ready-for-production-use)', '**Status**: [Production ready. API may undergo changes.](https://github.com/bemanproject/beman/blob/main/docs/beman_library_maturity_model.md#production-ready-api-may-undergo-changes)', '**Status**: [Production ready. Stable API.](https://github.com/bemanproject/beman/blob/main/docs/beman_library_maturity_model.md#production-ready-stable-api)', '**Status**: [Retired. No longer maintained or actively developed.](https://github.com/bemanproject/beman/blob/main/docs/beman_library_maturity_model.md#retired-no-longer-maintained-or-actively-developed)']
	check [Requirement][readme.library_status] ... failed

...

beman-tidy pipeline finished.

Summary    Requirement:  18 checks passed, 1 checks failed, 3 checks skipped,  23 checks not implemented.
Summary Recommendation:  0 checks passed, 0 checks failed, 2 checks skipped,  0 checks not implemented.

Coverage    Requirement:  95.83% (23/24 checks passed).
Coverage Recommendation:   0.00% (0/0 checks passed).
Coverage          TOTAL:  95.83% (23/24 checks passed).
```

- Run beman-tidy on the exemplar repository (fix issues in-place):

```shell
uv run beman-tidy path/to/exemplar --fix-inplace --verbose
```

## beman-tidy Development

Please refer to the [Beman Tidy Development Guide](./docs/dev-guide.md) for more details.
