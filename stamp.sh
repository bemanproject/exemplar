#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

{
    if [[ "$1" == "-h" || "$1" == "--help" ]] ; then
        cat <<-'EOF'
        stamp.sh -- beman exemplar template library creation tool

        This script is intended to be run on a fork of exemplar.

        It sets up copier, runs it on the copier template at the head of
        upstream exemplar's default branch, replaces the repository's
        current contents with the result, runs pre-commit, switches to a new
        branch 'stamp', and creates a git commit.

        All parameters are passed through to the copier invocation.
EOF
    fi
    set -eu
    if ! type -P python3 >/dev/null ; then
        echo "Couldn't find python3 in PATH" >&2
        exit 1
    fi
    declare repo_dir=$(realpath $(dirname "$BASH_SOURCE"))
    cd "$repo_dir"
    declare copier_venv_path
    copier_venv_path=$(mktemp --directory --dry-run)
    python3 -m venv "$copier_venv_path"
    source "$copier_venv_path/bin/activate"
    python3 -m pip install copier pre-commit >& /dev/null
    declare copier_out_path
    copier_out_path=$(mktemp --directory)
    # Copy from upstream rather than this repository: repositories created
    # from the exemplar template don't share its history, so their commits
    # can't serve as the _commit that 'copier update' starts from.
    python3 -m copier copy --vcs-ref=HEAD --quiet gh:bemanproject/exemplar "$copier_out_path" "$@"
    git rm -rf . &>/dev/null
    cp -r "$copier_out_path"/. .
    git add . &>/dev/null
    pre-commit run --all-files &>/dev/null || true
    git add . &>/dev/null
    git checkout -b stamp
    git commit -q -m "Stamp out exemplar template"
    echo "Successfully stamped out exemplar template to the new branch 'stamp'."
    echo "Try 'git push origin stamp' to push the branch upstream,"
    echo "then create a pull request."
    rm -r "$copier_venv_path" "$copier_out_path"
}; exit
