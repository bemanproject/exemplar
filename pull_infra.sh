#!/bin/bash
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Prerequisites
# - git subtree
# - rsync

# Configuration
VENDOR_NAME="infra"
VENDOR_REPO="https://github.com/bemanproject/${VENDOR_NAME}.git"
VENDOR_REMOTE_BRANCH="main"  # Branch in the vendor repo you're pulling from
VENDOR_PREFIX="${VENDOR_NAME}-temp"  # Vendor directory before moving selected files/folders
ITEMS_TO_KEEP=($1)  # Files/Folders to pull to the root of the repository from vendor

# Local variables
CURRENT_LOCAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)  # The current branch we are working on
VENDOR_LOCAL_BRANCH="${VENDOR_NAME}-${VENDOR_REMOTE_BRANCH}"

# Step 0: Check if lists is empty
if [ ${#ITEMS_TO_KEEP[@]} -eq 0 ]; then
    echo "⚠️  No files or folders specified to pull from ${VENDOR_NAME}. Exiting..."
    exit 1
fi

# Step 8: Clean up temp folder branch and remote
cleanup() {
    # Remove the ${VENDOR_PREFIX} directory after files/folders have been moved
    if [ -d "${VENDOR_PREFIX}" ]; then
        echo "Cleaning up ${VENDOR_PREFIX} directory..."
        rm -rf "${VENDOR_PREFIX}"
        git commit -am "Removed temporary ${VENDOR_NAME} files"
    else
        echo "✅ Vendor directory ${VENDOR_PREFIX} does not exist. Skipping"
    fi

    # Delete vendor tracking branch
    if git branch --list | grep -q "${VENDOR_LOCAL_BRANCH}"; then
        echo "Deleting vendor tracking branch ${VENDOR_LOCAL_BRANCH}..."
        git branch -D ${VENDOR_LOCAL_BRANCH}
    else
        echo "Vendor branch ${VENDOR_BRANCH} does not exist. Skipping."
    fi

    # Remove vendor remote
    if git remote get-url ${VENDOR_NAME} &>/dev/null; then
        echo "Removing vendor remote ${VENDOR_NAME}..."
        git remote remove ${VENDOR_NAME}
    else
        echo "Vendor remote ${VENDOR_NAME} does not exist. Skipping."
    fi

    echo "Cleanup complete! ✅"
}

# Ensure cleanup runs on exit, even on early exit
trap cleanup EXIT

# Step 1: Add vendor remote if not already added
if ! git remote | grep -q "${VENDOR_NAME}"; then
    echo "Adding ${VENDOR_NAME} remote..."
    git remote add ${VENDOR_NAME} ${VENDOR_REPO}
fi

# Step 2: Fetch vendor updates
echo "Fetching latest ${VENDOR_NAME} changes..."
git fetch ${VENDOR_NAME}

# Step 3: Check if vendor has new commits
LOCAL_HASH=$(git rev-parse ${VENDOR_LOCAL_BRANCH} 2>/dev/null || echo "none")
REMOTE_HASH=$(git rev-parse ${VENDOR_NAME}/${VENDOR_REMOTE_BRANCH})

if [[ "$LOCAL_HASH" == "$REMOTE_HASH" ]]; then
    echo "✅ Vendor repository is already up to date. No new changes found."
    exit 0
fi

# Step 4: Create or update vendor branch
if git branch --list | grep -q "${VENDOR_LOCAL_BRANCH}"; then
    git checkout ${VENDOR_LOCAL_BRANCH}
    git pull ${VENDOR_NAME} ${VENDOR_REMOTE_BRANCH}
else
    git checkout -b ${VENDOR_LOCAL_BRANCH} ${VENDOR_NAME}/${VENDOR_REMOTE_BRANCH}
fi

# Step 5: Add vendor code as a subtree
echo "Importing ${VENDOR_NAME} code into ${VENDOR_PREFIX}..."
git checkout "${CURRENT_LOCAL_BRANCH}"

# Check if the vendor subtree exists
if [ ! -d "${VENDOR_PREFIX}" ]; then
    echo "${VENDOR_NAME} subtree does not exist. Adding it for the first time..."
    git subtree add --prefix=${VENDOR_PREFIX} ${VENDOR_LOCAL_BRANCH} --squash
else
    echo "${VENDOR_NAME} subtree exists. Pulling latest changes..."
    git subtree pull --prefix=${VENDOR_PREFIX} ${VENDOR_LOCAL_BRANCH} --squash
fi

# Step 6: Move selected files/folders to root
echo "Moving selected ${VENDOR_NAME} files/folders to repo root..."
for item in "${ITEMS_TO_KEEP[@]}"; do
    if [ -f "${VENDOR_PREFIX}/$item" ] || [ -d "${VENDOR_PREFIX}/$item" ]; then  # don't allow symlinks with -e option
        rsync -a --no-perms --no-owner --no-group --no-times "${VENDOR_PREFIX}/$item" "./"
        git add "./$(basename "$item")"
    else
        echo "⚠️ Warning: File/Folder $item not found in ${VENDOR_NAME} repo"
    fi
done

# Step 7: Commit the changes (if there are any changes)
if ! git diff --quiet --staged; then
    git commit -m "Updated vendor files from ${VENDOR_NAME}"
    echo "✅ Vendor update committed."
else
    echo "✅ No changes to commit. Everything is already up to date."
fi

echo "Vendor pull complete! 🎉"
