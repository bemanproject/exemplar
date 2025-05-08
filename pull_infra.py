#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd, cwd=None, check=True):
    print(f"🔧 Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, check=check, text=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command: {e.cmd} failed with error code {e.returncode}")
        sys.exit(e.returncode)
    return result.stdout.strip()


def branch_exists_locally(branch_name):
    return branch_name in run(["git", "branch", "--list"], check=False)


def remote_exists_locally(remote_name):
    return remote_name in run(["git", "remote"], check=False)


def cleanup_directory(prefix, remote_name):
    if Path(prefix).exists():
        print(f"🧹 Cleaning up {prefix} directory...")
        shutil.rmtree(prefix)
        run(["git", "commit", "-am", f"Removed temporary {remote_name} files"], check=False)
    else:
        print(f"✅ Vendor directory {prefix} does not exist. Skipping.")


def cleanup_branch(local_branch):
    if branch_exists_locally(local_branch):
        print(f"🧹 Deleting vendor tracking branch {local_branch}...")
        run(["git", "branch", "-D", local_branch])
    else:
        print(f"Vendor branch {local_branch} does not exist. Skipping.")


def cleanup_remote(remote_name):
    if remote_exists_locally(remote_name):
        print(f"🧹 Removing vendor remote {remote_name}...")
        run(["git", "remote", "remove", remote_name])
    else:
        print(f"Vendor remote {remote_name} does not exist. Skipping.")


def cleanup(prefix, local_branch, remote_name):
    cleanup_directory(prefix, remote_name)
    cleanup_branch(local_branch)
    cleanup_remote(remote_name)
    print("✅ Cleanup complete!")


def main():
    parser = argparse.ArgumentParser(description="Pull and merge selected files/folders from a vendor git repo")
    parser.add_argument("-f", "--files", nargs="*", default=[], help="Files to pull")
    parser.add_argument("-d", "--dirs", nargs="*", default=[], help="Folders to pull")
    args = parser.parse_args()

    if not args.files and not args.dirs:
        print("⚠️  No files or folders specified to pull. Use -f and/or -d options. Exiting...")
        parser.print_help()
        sys.exit(1)

    # Configuration
    vendor_name = "infra"
    vendor_repo = f"https://github.com/bemanproject/{vendor_name}.git"
    vendor_remote_branch = "main"
    vendor_prefix = f"{vendor_name}-temp"
    vendor_local_branch = f"{vendor_name}-{vendor_remote_branch}"
    current_branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])

    try:
        # Add remote if missing
        if not remote_exists_locally(vendor_name):
            print(f"🌐 Adding remote {vendor_name}...")
            run(["git", "remote", "add", vendor_name, vendor_repo])

        # Fetch updates
        print(f"⬇️  Fetching from {vendor_name}...")
        run(["git", "fetch", vendor_name])

        # Checkout or create vendor tracking branch
        if branch_exists_locally(vendor_local_branch):
            run(["git", "switch", vendor_local_branch])

            # Check for changes
            print("🔍 Checking for changes...")
            local_hash = run(["git", "rev-parse", vendor_local_branch], check=False) or "none"
            remote_hash = run(["git", "rev-parse", f"{vendor_name}/{vendor_remote_branch}"])

            if local_hash == remote_hash:
                print("✅ Vendor repository is already up to date. No new changes found.")
                run(["git", "switch", current_branch])
                cleanup(vendor_prefix, vendor_local_branch, vendor_name)
                return

            run(["git", "pull", vendor_name, vendor_remote_branch])
        else:
            run(["git", "checkout", "-b", vendor_local_branch, f"{vendor_name}/{vendor_remote_branch}"])

        # Return to working branch
        run(["git", "switch", current_branch])

        # Add or pull subtree
        if not Path(vendor_prefix).exists():
            print(f"🌱 Adding subtree {vendor_prefix}...")
            run(["git", "subtree", "add", f"--prefix={vendor_prefix}", vendor_local_branch, "--squash"])
        else:
            print(f"🔄 Pulling subtree into {vendor_prefix}...")
            run(["git", "subtree", "pull", f"--prefix={vendor_prefix}", vendor_local_branch, "--squash"])

        # Move files and folders
        all_items = args.files + args.dirs
        print("📁 Moving selected files and folders to root...")
        for item in all_items:
            src = Path(vendor_prefix) / item
            dest = Path(item)

            if not src.exists():
                print(f"⚠️  Skipping {item}: Not found in vendor repo.")
                continue

            if src.is_dir():
                shutil.copytree(src, dest, dirs_exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)

            run(["git", "add", str(dest)])

        # Commit changes
        if run(["git", "diff", "--cached", "--name-only"], check=False) == "":
            print("✅ No changes to commit.")
        else:
            run(["git", "commit", "-m", f"Updated vendor files from {vendor_name}"])
            print("✅ Vendor update committed.")

    finally:
        cleanup(vendor_prefix, vendor_local_branch, vendor_name)


if __name__ == "__main__":
    main()
