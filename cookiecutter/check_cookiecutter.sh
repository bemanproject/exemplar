#!/usr/bin/env bash

set -euo pipefail

declare script_dir=$(realpath $(dirname "$BASH_SOURCE"))

function check_consistency() {
    local out_dir_path
    out_dir_path=$(mktemp --directory --dry-run)
    local out_dir_name
    out_dir_name=$(basename "$out_dir_path")
    cd /tmp
    python3 \
        -m cookiecutter \
        --no-input \
        "$script_dir" \
        project_name="exemplar" \
        directory_name="$out_dir_name" \
        cpp_build_version="17" \
        paper="P0898R3" \
        owner="bemanproject" \
        description="A Beman Library Exemplar"
    cp "$script_dir"/../.github/workflows/cookiecutter_test.yml "$out_dir_path"/.github/workflows
    local diff_path
    diff_path=$(mktemp)
    diff -r "$script_dir/.." "$out_dir_path" \
        | grep -v -e 'cookiecutter$' -e '.git$' > "$diff_path" || true
    rm -rf "$out_dir_path"
    if [[ $(wc -l "$diff_path" | cut -d' ' -f1) -gt 0 ]] ; then
        echo "Discrepancy between exemplar and cookiecutter:" >&2
        cat "$diff_path"
        rm "$diff_path"
        exit 1
    fi
    rm "$diff_path"
}

function check_templating() {
    local out_dir_path
    out_dir_path=$(mktemp --directory --dry-run)
    local out_dir_name
    out_dir_name=$(basename "$out_dir_path")
    cd /tmp
    python3 \
        -m cookiecutter \
        --no-input \
        "$script_dir" \
        project_name="RLZrmX9NfS" \
        directory_name="$out_dir_name" \
        cpp_build_version="17" \
        paper="P0898R3" \
        owner="bemanproject" \
        description="A Beman Library RLZrmX9NfS"
    local grep_path
    grep_path=$(mktemp)
    grep \
        --dereference-recursive --context=5 --color=always \
        "exemplar" "$out_dir_path" > "$grep_path" || true
    rm -rf "$out_dir_path"
    if [[ $(wc -l "$grep_path" | cut -d' ' -f1) -gt 0 ]] ; then
        echo "Untemplated \"exemplar\" in cookiecutter:" >&2
        cat "$grep_path"
        rm "$grep_path"
        exit 1
    fi
    rm "$grep_path"
}

function main() {
    local cookiecutter_venv_path
    cookiecutter_venv_path=$(mktemp --directory --dry-run)
    python3 -m venv "$cookiecutter_venv_path"
    source "$cookiecutter_venv_path/bin/activate"
    python3 -m pip install cookiecutter >& /dev/null
    check_consistency
    check_templating
    rm -rf "$cookiecutter_venv_path"
}

[[ "${BASH_SOURCE[0]}" != "${0}" ]] || main "$@"
