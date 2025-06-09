#!/bin/bash
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set -e
set +x
TOOL=$1
VERSION=$2

echo "Install ${TOOL} at: ${VERSION}"

shopt -s nocasematch
if [ "$TOOL" = "gcc" ]; then
    sudo apt-get remove -y gcc-"$VERSION" g++-"$VERSION" gcc g++
    sudo apt-get install -y gcc-"$VERSION" g++-"$VERSION" lcov

    sudo rm -f /usr/bin/gcc
    sudo rm -f /usr/bin/g++
    sudo rm -f /usr/bin/gcov

    sudo ln -s "$(which gcc-"$VERSION")" /usr/bin/gcc
    sudo ln -s "$(which g++-"$VERSION")" /usr/bin/g++
    sudo ln -s "$(which gcov-"$VERSION")" /usr/bin/gcov

    gcc --version
else
    sudo apt-get install -y lsb-release wget software-properties-common gnupg
    wget https://apt.llvm.org/llvm.sh

    sudo bash llvm.sh "${VERSION}"
    sudo apt-get install -y libc++-"$VERSION"-dev clang-tools-"$VERSION" lcov

    sudo rm -f /usr/bin/clang
    sudo rm -f /usr/bin/clang++

    sudo ln -s "$(which clang-"$VERSION")" /usr/bin/clang
    sudo ln -s "$(which clang++-"$VERSION")" /usr/bin/clang++

    clang --version
fi
