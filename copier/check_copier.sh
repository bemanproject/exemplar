#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set -euo pipefail

declare script_dir=$(realpath $(dirname "$BASH_SOURCE"))

function stamp() {
    local copier_dir="$1" ; shift
    local output_dir="$1" ; shift
    local unit_test_library="$1" ; shift
    local generating_exemplar="$1" ; shift
    python3 -m copier copy \
            --vcs-ref=HEAD \
            --defaults \
            "$copier_dir" \
            "$output_dir/exemplar" \
            -d project_name="exemplar" \
            -d maintainer="test_maintainer" \
            -d minimum_cpp_build_version="17" \
            -d paper="P0898R3" \
            -d description="A Beman Library Exemplar" \
            -d unit_test_library="$unit_test_library" \
            -d generating_exemplar="$generating_exemplar" \
            -d ci_tests_cron="30 15 * * 6" \
            -d pre_commit_update_cron="0 16 * * 0"
}

function check_consistency() {
    local out_dir_path
    out_dir_path=$(mktemp --directory --dry-run)
    cd /tmp
    stamp "$script_dir/.." "$out_dir_path" "gtest" "true"
    cp "$script_dir"/../.github/workflows/copier_test.yml "$out_dir_path"/exemplar/.github/workflows
    cp "$script_dir"/../.github/workflows/catch2_exemplar_test.yml "$out_dir_path"/exemplar/.github/workflows
    cp "$script_dir"/../.github/workflows/todo_exemplar_test.yml "$out_dir_path"/exemplar/.github/workflows
    mkdir "$out_dir_path"/exemplar/images
    cp "$script_dir"/../images/use-this-template.png "$out_dir_path"/exemplar/images/use-this-template.png
    cp "$script_dir"/../stamp.sh "$out_dir_path"/exemplar/stamp.sh
    local diff_path
    diff_path=$(mktemp)
    diff -r "$script_dir/.." "$out_dir_path/exemplar" \
        | grep -v -e 'copier$' -e 'copier.yml' -e '.copier-answers.yml' -e '.git$' > "$diff_path" || true
    rm -rf "$out_dir_path"
    if [[ $(wc -l "$diff_path" | cut -d' ' -f1) -gt 0 ]] ; then
        echo "Discrepancy between exemplar and copier:" >&2
        cat "$diff_path"
        rm "$diff_path"
        exit 1
    fi
    rm "$diff_path"
}

function check_templating() {
    local unit_test_library="$1" ; shift
    local out_dir_path
    out_dir_path=$(mktemp --directory --dry-run)
    cd /tmp
    python3 -m copier copy \
            --vcs-ref=HEAD \
            --defaults \
            "$script_dir/.." \
            "$out_dir_path/rlzrmx9nfs" \
            -d project_name="rlzrmx9nfs" \
            -d maintainer="test_maintainer" \
            -d minimum_cpp_build_version="17" \
            -d paper="P0898R3" \
            -d description="A Beman Library rlzrmx9nfs" \
            -d unit_test_library="$unit_test_library" \
            -d generating_exemplar=false \
            -d ci_tests_cron="30 15 * * 6" \
            -d pre_commit_update_cron="0 16 * * 0"
    rm -rf "$out_dir_path/rlzrmx9nfs/infra"
    # The answers file intentionally points back at exemplar.
    sed -i '/^_src_path: gh:bemanproject\/exemplar$/d' "$out_dir_path/rlzrmx9nfs/.copier-answers.yml"
    local grep_path
    grep_path=$(mktemp)
    grep \
        --dereference-recursive --context=5 --color=always --ignore-case \
        -e "exemplar" -e "identity" "$out_dir_path/rlzrmx9nfs" > "$grep_path" || true
    rm -rf "$out_dir_path"
    if [[ $(wc -l "$grep_path" | cut -d' ' -f1) -gt 0 ]] ; then
        echo "Untemplated \"exemplar\" or \"identity\" in copier:" >&2
        cat "$grep_path"
        rm "$grep_path"
        exit 1
    fi
    rm "$grep_path"
}

function setup_venv() {
    local path="$1" ; shift
    python3 -m venv "$copier_venv_path"
    source "$copier_venv_path/bin/activate"
    python3 -m pip install copier >& /dev/null
}

function main() {
    local copier_venv_path
    copier_venv_path=$(mktemp --directory --dry-run)
    setup_venv "$copier_venv_path"
    check_consistency
    check_templating gtest
    check_templating catch2
    rm -rf "$copier_venv_path"
}

[[ "${BASH_SOURCE[0]}" != "${0}" ]] || main "$@"
