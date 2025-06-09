# Install Basic utilities
sudo apt-get install -y ca-certificates gpg wget git curl

# Install Latest CMake
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ noble main' | sudo tee /etc/apt/sources.list.d/kitware.list >/dev/null
sudo apt-get update && sudo apt-get install -y cmake

# Install Ninja
sudo apt-get install -y ninja-build
