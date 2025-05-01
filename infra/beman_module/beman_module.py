#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import argparse
import configparser
import filecmp
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

def directory_compare(dir1, dir2, ignore):
    compared = filecmp.dircmp(dir1, dir2, ignore=ignore)
    if compared.left_only or compared.right_only or compared.diff_files:
        return False
    for common_dir in compared.common_dirs:
        path1 = os.path.join(dir1, common_dir)
        path2 = os.path.join(dir2, common_dir)
        if not directory_compare(path1, path2, ignore):
            return False
    return True

class BemanModule:
    def __init__(self, dirpath, remote, commit_hash):
        self.dirpath = dirpath
        self.remote = remote
        self.commit_hash = commit_hash

def parse_beman_module_file(path):
    config = configparser.ConfigParser()
    read_result = config.read(path)
    def fail():
        raise Exception(f'Failed to parse {path} as a .beman_module file')
    if not read_result:
        fail()
    if not 'beman_module' in config:
        fail()
    if not 'remote' in config['beman_module']:
        fail()
    if not 'commit_hash' in config['beman_module']:
        fail()
    return BemanModule(
        str(pathlib.Path(path).resolve().parent),
        config['beman_module']['remote'], config['beman_module']['commit_hash'])

def get_beman_module(dir):
    beman_module_filepath = os.path.join(dir, '.beman_module')
    if os.path.isfile(beman_module_filepath):
        return parse_beman_module_file(beman_module_filepath)
    else:
        return None

def find_beman_modules_in(dir):
    assert os.path.isdir(dir)
    result = []
    for dirpath, _, filenames in os.walk(dir):
        if '.beman_module' in filenames:
            result.append(parse_beman_module_file(os.path.join(dirpath, '.beman_module')))
    return sorted(result, key=lambda module: module.dirpath)

def cwd_git_repository_path():
    process = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True,
        check=False)
    if process.returncode == 0:
        return process.stdout.strip()
    elif "fatal: not a git repository" in process.stderr:
        return None
    else:
        raise Exception("git rev-parse --show-toplevel failed")

def clone_beman_module_into_tmpdir(beman_module, remote):
    tmpdir = tempfile.TemporaryDirectory()
    subprocess.run(
        ['git', 'clone', beman_module.remote, tmpdir.name], capture_output=True,
        check=True)
    if not remote:
        subprocess.run(
            ['git', '-C', tmpdir.name, 'reset', '--hard', beman_module.commit_hash],
            capture_output=True, check=True)
    return tmpdir

def beman_module_status(beman_module):
    tmpdir = clone_beman_module_into_tmpdir(beman_module, False)
    if directory_compare(tmpdir.name, beman_module.dirpath, ['.beman_module', '.git']):
        status_character=' '
    else:
        status_character='+'
    parent_repo_path = cwd_git_repository_path()
    if not parent_repo_path:
        raise Exception('this is not a git repository')
    relpath = pathlib.Path(
        beman_module.dirpath).relative_to(pathlib.Path(parent_repo_path))
    return status_character + ' ' + beman_module.commit_hash + ' ' + str(relpath)

def beman_module_update(beman_module, remote):
    tmpdir = clone_beman_module_into_tmpdir(beman_module, remote)
    shutil.rmtree(beman_module.dirpath)
    with open(os.path.join(tmpdir.name, '.beman_module'), 'w') as f:
        f.write('[beman_module]\n')
        f.write(f'remote={beman_module.remote}\n')
        f.write(f'commit_hash={beman_module.commit_hash}\n')
    shutil.rmtree(os.path.join(tmpdir.name, '.git'))
    shutil.copytree(tmpdir.name, beman_module.dirpath)

def update_command(remote, path):
    if not path:
        parent_repo_path = cwd_git_repository_path()
        if not parent_repo_path:
            raise Exception('this is not a git repository')
        beman_modules = find_beman_modules_in(parent_repo_path)
    else:
        beman_module = get_beman_module(path)
        if not beman_module:
            raise Exception(f'{path} is not a beman_module')
        beman_modules = [beman_module]
    for beman_module in beman_modules:
        beman_module_update(beman_module, remote)

def add_command(repository, path):
    tmpdir = tempfile.TemporaryDirectory()
    subprocess.run(
        ['git', 'clone', repository], capture_output=True, check=True, cwd=tmpdir.name)
    repository_name = os.listdir(tmpdir.name)[0]
    if not path:
        path = repository_name
    if os.path.exists(path):
        raise Exception(f'{path} exists')
    os.makedirs(path)
    tmpdir_repo = os.path.join(tmpdir.name, repository_name)
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir_repo)
    with open(os.path.join(tmpdir_repo, '.beman_module'), 'w') as f:
        f.write('[beman_module]\n')
        f.write(f'remote={repository}\n')
        f.write(f'commit_hash={sha_process.stdout.strip()}\n')
    shutil.rmtree(os.path.join(tmpdir_repo, '.git'))
    shutil.copytree(tmpdir_repo, path, dirs_exist_ok=True)

def status_command(paths):
    if not paths:
        parent_repo_path = cwd_git_repository_path()
        if not parent_repo_path:
            raise Exception('this is not a git repository')
        beman_modules = find_beman_modules_in(parent_repo_path)
    else:
        beman_modules = []
        for path in paths:
            beman_module = get_beman_module(path)
            if not beman_module:
                raise Exception(f'{path} is not a beman_module')
            beman_modules.append(beman_module)
    for beman_module in beman_modules:
        print(beman_module_status(beman_module))

def get_parser():
    parser = argparse.ArgumentParser(description='Beman pseudo-submodule tool')
    subparsers = parser.add_subparsers(dest='command', help='available commands')
    parser_update = subparsers.add_parser('update', help='update beman_modules')
    parser_update.add_argument(
        '--remote', action='store_true',
        help='update a beman_module to its latest from upstream')
    parser_update.add_argument(
        'beman_module_path', nargs='?',
        help='relative path to the beman_module to update')
    parser_add = subparsers.add_parser('add', help='add a new beman_module')
    parser_add.add_argument('repository', help='git repository to add')
    parser_add.add_argument(
        'path', nargs='?', help='path where the repository will be added')
    parser_status = subparsers.add_parser(
        'status', help='show the status of beman_modules')
    parser_status.add_argument('paths', nargs='*')
    return parser

def parse_args(args):
    return get_parser().parse_args(args);

def usage():
    return get_parser().format_help()

def run_command(args):
    if args.command == 'update':
        update_command(args.remote, args.beman_module_path)
    elif args.command == 'add':
        add_command(args.repository, args.path)
    elif args.command == 'status':
        status_command(args.paths)
    else:
        raise Exception(usage())

def check_for_git(path):
    env = os.environ.copy()
    if path is not None:
        env["PATH"] = path
    return shutil.which("git", path=env.get("PATH")) is not None

def main():
    try:
        if not check_for_git(None):
            raise Exception('git not found in PATH')
        args = parse_args(sys.argv[1:])
        run_command(args)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
