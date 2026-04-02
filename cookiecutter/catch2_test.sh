#!/usr/bin/env bash

source ./check_cookiecutter.sh
cookiecutter_venv_path=$(mktemp --directory --dry-run)
setup_venv "$cookiecutter_venv_path"
rm -rf "./catch2_exemplar"
stamp "$PWD" "./catch2_exemplar" "interface" "catch2"
cd catch2_exemplar/exemplar
cmake -B build -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=./infra/cmake/use-fetch-content.cmake -DCMAKE_CXX_STANDARD=20 -DCMAKE_INSTALL_PREFIX=$PWD/dist
cmake --build build
ctest --test-dir build
cmake --install build
