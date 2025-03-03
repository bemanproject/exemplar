FROM mcr.microsoft.com/devcontainers/cpp:1-ubuntu-24.04

USER vscode

# Add extra apt repositories
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null
RUN echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ noble main' | sudo tee /etc/apt/sources.list.d/kitware.list >/dev/null
RUN sudo apt-get update

# Newer gcc/ llvm is needed to avoid ASAN Stalling
# See: https://github.com/google/sanitizers/issues/1614
# Minimal version: clang-18.1.3, gcc-13.2

# Install apt dependencies
RUN sudo apt-get install -y \
    cmake \
    gcc-14 \
    libgtest-dev \
    pipx

# Install pip dependencies
RUN pipx install \
    pre-commit
