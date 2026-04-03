#!/usr/bin/env bash

{
    if [[ "$1" == "-h" || "$1" == "--help" ]] ; then
        cat <<-'EOF'
        stamp.sh -- beman exemplar template library creation tool

        This script is intended to be run on a fork of exemplar.

        It sets up cookiecutter, runs it on the cookiecutter template, replaces the
        repository's current contents with the result, runs pre-commit,
        switches to a new branch 'stamp', and creates a git commit.

        All parameters are passed through to the cookiecutter invocation.
EOF
    fi
    set -eu
    if ! type -P python3 >/dev/null ; then
        echo "Couldn't find python3 in PATH" >&2
        exit 1
    fi
    declare repo_dir=$(realpath $(dirname "$BASH_SOURCE"))
    cd "$repo_dir"
    declare cookiecutter_venv_path
    cookiecutter_venv_path=$(mktemp --directory --dry-run)
    python3 -m venv "$cookiecutter_venv_path"
    source "$cookiecutter_venv_path/bin/activate"
    python3 -m pip install cookiecutter pre-commit >& /dev/null
    declare cookiecutter_out_path
    cookiecutter_out_path=$(mktemp --directory)
    python3 -m cookiecutter "$repo_dir/cookiecutter" -o "$cookiecutter_out_path" "$@"
    git rm -rf . &>/dev/null
    cp -r "$cookiecutter_out_path"/*/. .
    git add . &>/dev/null
    pre-commit run --all-files &>/dev/null || true
    git add . &>/dev/null
    git checkout -b stamp
    git commit -q -m "Stamp out exemplar template"
    echo "Successfully stamped out exemplar template to the new branch 'stamp'."
    echo "Try 'git push origin stamp' to push the branch upstream,"
    echo "then create a pull request."
    rm -r "$cookiecutter_venv_path" "$cookiecutter_out_path"
}; exit
