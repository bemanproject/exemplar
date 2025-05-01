# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import beman_module
import os
import pathlib
import pytest
import shutil
import stat
import subprocess
import tempfile

def create_test_git_repository():
    tmpdir = tempfile.TemporaryDirectory()
    subprocess.run(['git', 'init'], check=True, cwd=tmpdir.name, capture_output=True)
    def make_commit(a_txt_contents):
        with open(os.path.join(tmpdir.name, 'a.txt'), 'w') as f:
            f.write(a_txt_contents)
        subprocess.run(
            ['git', 'add', 'a.txt'], check=True, cwd=tmpdir.name, capture_output=True)
        subprocess.run(
            ['git', '-c', 'user.name=test', '-c', 'user.email=test@example.com', 'commit',
             '--author="test <test@example.com>"', '-m', 'test'],
            check=True, cwd=tmpdir.name, capture_output=True)
    make_commit('A')
    make_commit('a')
    return tmpdir

def test_directory_compare():
    def create_dir_structure(dir_path):
        bar_path = os.path.join(dir_path, 'bar')
        os.makedirs(bar_path)

        with open(os.path.join(dir_path, 'foo.txt'), 'w') as f:
            f.write('foo')
        with open(os.path.join(bar_path, 'baz.txt'), 'w') as f:
            f.write('baz')

    with tempfile.TemporaryDirectory() as dir_a, \
         tempfile.TemporaryDirectory() as dir_b:

        create_dir_structure(dir_a)
        create_dir_structure(dir_b)

        assert beman_module.directory_compare(dir_a, dir_b, [])

        with open(os.path.join(os.path.join(dir_a, 'bar'), 'quux.txt'), 'w') as f:
            f.write('quux')

        assert not beman_module.directory_compare(dir_a, dir_b, [])
        assert beman_module.directory_compare(dir_a, dir_b, ['quux.txt'])

def test_parse_beman_module_file():
    def valid_file():
        tmpfile = tempfile.NamedTemporaryFile()
        tmpfile.write('[beman_module]\n'.encode('utf-8'))
        tmpfile.write(
            'remote=git@github.com:bemanproject/infra.git\n'.encode('utf-8'))
        tmpfile.write(
            'commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77\n'.encode('utf-8'))
        tmpfile.flush()
        module = beman_module.parse_beman_module_file(tmpfile.name)
        assert module.dirpath == str(pathlib.Path(tmpfile.name).resolve().parent)
        assert module.remote == 'git@github.com:bemanproject/infra.git'
        assert module.commit_hash == '9b88395a86c4290794e503e94d8213b6c442ae77'
    valid_file()
    def invalid_file_missing_remote():
        threw = False
        try:
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write('[beman_module]\n'.encode('utf-8'))
            tmpfile.write(
                'commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77\n'.encode('utf-8'))
            tmpfile.flush()
            beman_module.parse_beman_module_file(tmpfile.name)
        except:
            threw = True
        assert threw
    invalid_file_missing_remote()
    def invalid_file_missing_commit_hash():
        threw = False
        try:
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write('[beman_module]\n'.encode('utf-8'))
            tmpfile.write(
                'remote=git@github.com:bemanproject/infra.git\n'.encode('utf-8'))
            tmpfile.flush()
            beman_module.parse_beman_module_file(tmpfile.name)
        except:
            threw = True
        assert threw
    invalid_file_missing_commit_hash()
    def invalid_file_wrong_section():
        threw = False
        try:
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write('[invalid]\n'.encode('utf-8'))
            tmpfile.write(
                'remote=git@github.com:bemanproject/infra.git\n'.encode('utf-8'))
            tmpfile.write(
                'commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77\n'.encode('utf-8'))
            tmpfile.flush()
            beman_module.parse_beman_module_file(tmpfile.name)
        except:
            threw = True
        assert threw
    invalid_file_wrong_section()

def test_get_beman_module():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = os.getcwd()
    os.chdir(tmpdir2.name)
    beman_module.add_command(tmpdir.name, 'foo')
    assert beman_module.get_beman_module('foo')
    os.remove('foo/.beman_module')
    assert not beman_module.get_beman_module('foo')
    os.chdir(original_cwd)

def test_find_beman_modules_in():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = os.getcwd()
    os.chdir(tmpdir2.name)
    beman_module.add_command(tmpdir.name, 'foo')
    beman_module.add_command(tmpdir.name, 'bar')
    beman_modules = beman_module.find_beman_modules_in(tmpdir2.name)
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    assert beman_modules[0].dirpath == os.path.join(tmpdir2.name, 'bar')
    assert beman_modules[0].remote == tmpdir.name
    assert beman_modules[0].commit_hash == sha
    assert beman_modules[1].dirpath == os.path.join(tmpdir2.name, 'foo')
    assert beman_modules[1].remote == tmpdir.name
    assert beman_modules[1].commit_hash == sha
    os.chdir(original_cwd)

def test_cwd_git_repository_path():
    original_cwd = os.getcwd()
    tmpdir = tempfile.TemporaryDirectory()
    os.chdir(tmpdir.name)
    assert not beman_module.cwd_git_repository_path()
    subprocess.run(['git', 'init'])
    assert beman_module.cwd_git_repository_path() == tmpdir.name
    os.chdir(original_cwd)

def test_clone_beman_module_into_tmpdir():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = os.getcwd()
    os.chdir(tmpdir2.name)
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD^'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    beman_module.add_command(tmpdir.name, 'foo')
    module = beman_module.get_beman_module(os.path.join(tmpdir2.name, 'foo'))
    module.commit_hash = sha
    tmpdir3 = beman_module.clone_beman_module_into_tmpdir(module, False)
    assert not beman_module.directory_compare(tmpdir.name, tmpdir3.name, ['.git'])
    tmpdir4 = beman_module.clone_beman_module_into_tmpdir(module, True)
    assert beman_module.directory_compare(tmpdir.name, tmpdir4.name, ['.git'])
    subprocess.run(
        ['git', 'reset', '--hard', sha], capture_output=True, check=True,
        cwd=tmpdir.name)
    assert beman_module.directory_compare(tmpdir.name, tmpdir3.name, ['.git'])
    os.chdir(original_cwd)

def test_beman_module_status():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = os.getcwd()
    os.chdir(tmpdir2.name)
    beman_module.add_command(tmpdir.name, 'foo')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    assert '  ' + sha + ' foo' == beman_module.beman_module_status(
        beman_module.get_beman_module(os.path.join(tmpdir2.name, 'foo')))
    with open(os.path.join(os.path.join(tmpdir2.name, 'foo'), 'a.txt'), 'w') as f:
        f.write('b')
    assert '+ ' + sha + ' foo' == beman_module.beman_module_status(
        beman_module.get_beman_module(os.path.join(tmpdir2.name, 'foo')))
    os.chdir(original_cwd)

def test_update_command_no_paths():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = os.getcwd()
    os.chdir(tmpdir2.name)
    beman_module.add_command(tmpdir.name, 'foo')
    beman_module.add_command(tmpdir.name, 'bar')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD^'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    subprocess.run(
        ['git', 'reset', '--hard', sha], capture_output=True, check=True,
        cwd=tmpdir.name)
    with open(os.path.join(os.path.join(tmpdir2.name, 'foo'), '.beman_module'), 'w') as f:
        f.write(f'[beman_module]\nremote={tmpdir.name}\ncommit_hash={sha}\n')
    with open(os.path.join(os.path.join(tmpdir2.name, 'bar'), '.beman_module'), 'w') as f:
        f.write(f'[beman_module]\nremote={tmpdir.name}\ncommit_hash={sha}\n')
    beman_module.update_command(tmpdir.name, None)
    assert beman_module.directory_compare(
        tmpdir.name, os.path.join(tmpdir2.name, 'foo'), ['.git', '.beman_module'])
    assert beman_module.directory_compare(
        tmpdir.name, os.path.join(tmpdir2.name, 'bar'), ['.git', '.beman_module'])
    os.chdir(original_cwd)

def test_update_command_with_path():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    tmpdir_copy1 = tempfile.TemporaryDirectory()
    shutil.copytree(tmpdir.name, tmpdir_copy1.name, dirs_exist_ok=True)
    original_cwd = os.getcwd()
    os.chdir(tmpdir2.name)
    beman_module.add_command(tmpdir.name, 'foo')
    beman_module.add_command(tmpdir.name, 'bar')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD^'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    subprocess.run(
        ['git', 'reset', '--hard', sha], capture_output=True, check=True,
        cwd=tmpdir.name)
    with open(os.path.join(os.path.join(tmpdir2.name, 'foo'), '.beman_module'), 'w') as f:
        f.write(f'[beman_module]\nremote={tmpdir.name}\ncommit_hash={sha}\n')
    with open(os.path.join(os.path.join(tmpdir2.name, 'bar'), '.beman_module'), 'w') as f:
        f.write(f'[beman_module]\nremote={tmpdir.name}\ncommit_hash={sha}\n')
    beman_module.update_command(tmpdir.name, 'foo')
    assert beman_module.directory_compare(
        tmpdir.name, os.path.join(tmpdir2.name, 'foo'), ['.git', '.beman_module'])
    assert beman_module.directory_compare(
        tmpdir_copy1.name, os.path.join(tmpdir2.name, 'bar'), ['.git', '.beman_module'])
    os.chdir(original_cwd)

def test_add_command():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = os.getcwd()
    os.chdir(tmpdir2.name)
    beman_module.add_command(tmpdir.name, 'foo')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    assert beman_module.directory_compare(
        tmpdir.name, os.path.join(tmpdir2.name, 'foo'), ['.git', '.beman_module'])
    with open(os.path.join(os.path.join(tmpdir2.name, 'foo'), '.beman_module'), 'r') as f:
        assert f.read() == f'[beman_module]\nremote={tmpdir.name}\ncommit_hash={sha}\n'
    os.chdir(original_cwd)

def test_status_command_no_paths(capsys):
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = os.getcwd()
    os.chdir(tmpdir2.name)
    beman_module.add_command(tmpdir.name, 'foo')
    beman_module.add_command(tmpdir.name, 'bar')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    with open(os.path.join(os.path.join(tmpdir2.name, 'bar'), 'a.txt'), 'w') as f:
        f.write('b')
    beman_module.status_command([])
    sha = sha_process.stdout.strip()
    assert capsys.readouterr().out == '+ ' + sha + ' bar\n' + '  ' + sha + ' foo\n'
    os.chdir(original_cwd)

def test_status_command_with_path(capsys):
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = os.getcwd()
    os.chdir(tmpdir2.name)
    beman_module.add_command(tmpdir.name, 'foo')
    beman_module.add_command(tmpdir.name, 'bar')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    with open(os.path.join(os.path.join(tmpdir2.name, 'bar'), 'a.txt'), 'w') as f:
        f.write('b')
    beman_module.status_command(['bar'])
    sha = sha_process.stdout.strip()
    assert capsys.readouterr().out == '+ ' + sha + ' bar\n'
    os.chdir(original_cwd)

def test_check_for_git():
    tmpdir = tempfile.TemporaryDirectory()
    assert not beman_module.check_for_git(tmpdir.name)
    fake_git_path = os.path.join(tmpdir.name, 'git')
    with open(fake_git_path, 'w'):
        pass
    os.chmod(fake_git_path, stat.S_IRWXU)
    assert beman_module.check_for_git(tmpdir.name)

def test_parse_args():
    def plain_update():
        args = beman_module.parse_args(['update'])
        assert args.command == 'update'
        assert not args.remote
        assert not args.beman_module_path
    plain_update()
    def update_remote():
        args = beman_module.parse_args(['update', '--remote'])
        assert args.command == 'update'
        assert args.remote
        assert not args.beman_module_path
    update_remote()
    def update_path():
        args = beman_module.parse_args(['update', 'infra/'])
        assert args.command == 'update'
        assert not args.remote
        assert args.beman_module_path == 'infra/'
    update_path()
    def update_path_remote():
        args = beman_module.parse_args(['update', '--remote', 'infra/'])
        assert args.command == 'update'
        assert args.remote
        assert args.beman_module_path == 'infra/'
    update_path_remote()
    def plain_add():
        args = beman_module.parse_args(['add', 'git@github.com:bemanproject/infra.git'])
        assert args.command == 'add'
        assert args.repository == 'git@github.com:bemanproject/infra.git'
        assert not args.path
    plain_add()
    def add_path():
        args = beman_module.parse_args(
            ['add', 'git@github.com:bemanproject/infra.git', 'infra/'])
        assert args.command == 'add'
        assert args.repository == 'git@github.com:bemanproject/infra.git'
        assert args.path == 'infra/'
    add_path()
    def plain_status():
        args = beman_module.parse_args(['status'])
        assert args.command == 'status'
        assert args.paths == []
    plain_status()
    def status_one_module():
        args = beman_module.parse_args(['status', 'infra/'])
        assert args.command == 'status'
        assert args.paths == ['infra/']
    status_one_module()
    def status_multiple_modules():
        args = beman_module.parse_args(['status', 'infra/', 'foobar/'])
        assert args.command == 'status'
        assert args.paths == ['infra/', 'foobar/']
    status_multiple_modules()
