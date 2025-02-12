#!/bin/bash -x

cmake -S "${1}" -B "${2}" -DCMAKE_PREFIX_PATH="${3}"
cmake --build "${2}" --config Debug
