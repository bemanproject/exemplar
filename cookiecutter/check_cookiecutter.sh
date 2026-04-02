#!/usr/bin/env bash

set -euo pipefail

declare script_dir=$(realpath $(dirname "$BASH_SOURCE"))

function stamp() {
    local cookiecutter_dir="$1" ; shift
    local output_dir="$1" ; shift
    local library_type="$1" ; shift
    local unit_test_library="$1" ; shift
    local generating_exemplar="$1" ; shift
    python3 \
        -m cookiecutter \
        --no-input \
        --output-dir "$output_dir" \
        "$cookiecutter_dir" \
        project_name="exemplar" \
        minimum_cpp_build_version="17" \
        paper="P0898R3" \
        description="A Beman Library Exemplar" \
        godbolt_link="https://godbolt.org/z/4qEPK87va" \
        library_type="$library_type" \
        unit_test_library="$unit_test_library" \
        _generating_exemplar="$generating_exemplar" \
        _ci_tests_cron="30 15 * * 6" \
        _pre_commit_update_cron="0 16 * * 0"
}

function check_consistency() {
    local out_dir_path
    out_dir_path=$(mktemp --directory --dry-run)
    cd /tmp
    stamp "$script_dir" "$out_dir_path" "interface" "gtest" "true"
    cp "$script_dir"/../.github/workflows/cookiecutter_test.yml "$out_dir_path"/exemplar/.github/workflows
    cp "$script_dir"/../.github/workflows/static_exemplar_test.yml "$out_dir_path"/exemplar/.github/workflows
    cp "$script_dir"/../.github/workflows/catch2_exemplar_test.yml "$out_dir_path"/exemplar/.github/workflows
    cp "$script_dir"/../.github/workflows/todo_exemplar_test.yml "$out_dir_path"/exemplar/.github/workflows
    local diff_path
    diff_path=$(mktemp)
    diff -r "$script_dir/.." "$out_dir_path/exemplar" \
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
    cd /tmp
    python3 \
        -m cookiecutter \
        --no-input \
        --output-dir "$out_dir_path" \
        "$script_dir" \
        project_name="RLZrmX9NfS" \
        minimum_cpp_build_version="17" \
        paper="P0898R3" \
        description="A Beman Library RLZrmX9NfS" \
        godbolt_link="https://godbolt.org/z/4qEPK87va" \
        _generating_exemplar="false" \
        _ci_tests_cron="30 15 * * 6" \
        _pre_commit_update_cron="0 16 * * 0"
    rm -rf "$out_dir_path/RLZrmX9NfS/infra"
    local grep_path
    grep_path=$(mktemp)
    grep \
        --dereference-recursive --context=5 --color=always \
        -e "exemplar" -e "identity" "$out_dir_path/RLZrmX9NfS" > "$grep_path" || true
    rm -rf "$out_dir_path"
    if [[ $(wc -l "$grep_path" | cut -d' ' -f1) -gt 0 ]] ; then
        echo "Untemplated \"exemplar\" or \"identity\" in cookiecutter:" >&2
        cat "$grep_path"
        rm "$grep_path"
        exit 1
    fi
    rm "$grep_path"
}

function setup_venv() {
    local path="$1" ; shift
    python3 -m venv "$cookiecutter_venv_path"
    source "$cookiecutter_venv_path/bin/activate"
    python3 -m pip install cookiecutter >& /dev/null
}

function main() {
    local cookiecutter_venv_path
    cookiecutter_venv_path=$(mktemp --directory --dry-run)
    setup_venv "$cookiecutter_venv_path"
    check_consistency
    check_templating
    rm -rf "$cookiecutter_venv_path"
}

[[ "${BASH_SOURCE[0]}" != "${0}" ]] || main "$@"
