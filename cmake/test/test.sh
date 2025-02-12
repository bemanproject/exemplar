#!/bin/bash -x

cmake -S "${1}" -B "${2}" \
      -DCMAKE_PREFIX_PATH="${3}" \
      -DCMAKE_CXX_STANDARD=17

cmake --build "${2}" --config Debug
