# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#!/usr/bin/env python3
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

if "-h" in sys.argv or "--help" in sys.argv:
    print("stamp.py -- beman exemplar template library creation tool\n\n"
          "This script is intended to be run on a fork of exemplar.\n\n"
          "It sets up cookiecutter, runs it on the cookiecutter template, replaces the\n"
          "repository's current contents with the result, runs pre-commit,\n"
          "switches to a new branch 'stamp', and creates a git commit.\n\n"
          "All parameters are passed through to the cookiecutter invocation.")
    sys.exit(0)

repo_dir = Path(__file__).parent.resolve()
os.chdir(repo_dir)

with tempfile.TemporaryDirectory() as v_dir, tempfile.TemporaryDirectory() as o_dir:
    v_dir, o_dir = Path(v_dir), Path(o_dir)
    subprocess.run([sys.executable, "-m", "venv", str(v_dir)], check=True)
    bin_dir = v_dir / ("Scripts" if os.name == "nt" else "bin")
    python = bin_dir / ("python.exe" if os.name == "nt" else "python")

    subprocess.run([str(python), "-m", "pip", "install", "cookiecutter", "pre-commit"], capture_output=True, check=True)
    subprocess.run([str(python), "-m", "cookiecutter", str(repo_dir / "cookiecutter"), "-o", str(o_dir)] + sys.argv[1:], check=True)
    subprocess.run(["git", "rm", "-rf", "."], capture_output=True, check=True)
    gen_dir = next(o_dir.iterdir())
    for item in gen_dir.iterdir():
        if item.is_dir(): shutil.copytree(item, repo_dir / item.name, dirs_exist_ok=True)
        else: shutil.copy2(item, repo_dir / item.name)
    subprocess.run(["git", "add", "."], capture_output=True, check=True)
    pc = bin_dir / ("pre-commit.exe" if os.name == "nt" else "pre-commit")
    subprocess.run([str(pc), "run", "--all-files"], capture_output=True)
    subprocess.run(["git", "add", "."], capture_output=True, check=True)
    subprocess.run(["git", "checkout", "-b", "stamp"], check=True)
    subprocess.run(["git", "commit", "-q", "-m", "Stamp out exemplar template"], check=True)
    print("Successfully stamped out exemplar template to the new branch 'stamp'.")
    print("Try 'git push origin stamp' to push the branch upstream,\nthen create a pull request.")
