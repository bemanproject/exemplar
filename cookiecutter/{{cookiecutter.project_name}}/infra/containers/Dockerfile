#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

ARG base_image=mcr.microsoft.com/devcontainers/cpp:1-ubuntu-24.04
FROM ${base_image}

# Create the vscode user
RUN bash <<EOF
    if ! id "vscode" &>/dev/null; then
        apt-get update && apt-get install -y sudo adduser
        useradd -ms /bin/bash -p "" vscode && usermod -aG sudo vscode
    fi
EOF

USER vscode
WORKDIR /tmp

COPY install_sys.sh .
RUN bash install_sys.sh

# Newer gcc/ clang is needed to avoid ASAN Stalling, which is turned on by default across beman projects.
# See: https://github.com/google/sanitizers/issues/1614
# Minimal version: clang-18.1.3, gcc-13.2
ARG compiler_kind=gcc
ARG compiler_version=14

COPY install_compiler.sh .
RUN bash install_compiler.sh ${compiler_kind} ${compiler_version}

# Common dependency: google-test
RUN sudo apt-get install -y libgtest-dev

# Pre-commit is beman library's standard linting tool
RUN sudo apt-get install -y pipx
RUN pipx install pre-commit
ENV PATH="/home/vscode/.local/bin:${PATH}"

ENTRYPOINT ["/usr/bin/bash"]
