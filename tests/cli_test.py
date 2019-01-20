#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import stat
import sys
import shutil
import subprocess
from pathlib import Path

from pyrepogen import cli
from pyrepogen import settings


TESTS_SETUPS_PATH = Path(__file__).parent / 'tests_setups/cli_test'
TESTS_CWD = Path().cwd()
SKIP_ALL_MARKED = False


def _error_remove_readonly(_action, name, _exc):
    Path(name).chmod(stat.S_IWRITE)
    Path(name).unlink()


def setup_test(cwd, clean=True):
    if Path(cwd).exists() and clean:
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    os.chdir(cwd)


def teardown_test(cwd, clean=True):
    os.chdir(TESTS_CWD)
    if Path(cwd).exists() and clean:
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)


def test_cli_SHOULD_print_version_properly(capsys):
    sys.argv = [sys.argv[0]]
    sys.argv.append('--version')
    cli.main()
    
    captured = capsys.readouterr()
    print(captured.out)
    
    assert re.search(r'(\d+)\.(\d+)\.(\d+)', captured.out)


def test_cli_SHOULD_generate_demo_properly():
    cwd = TESTS_SETUPS_PATH / 'test_cli_SHOULD_generate_demo_properly'
    setup_test(cwd)
    
    sys.argv = [sys.argv[0], '--demo']
    cli.main()
    
    p = subprocess.run(('make', 'test'), shell=True, cwd=cwd / settings.DEMO_PROJECT_NAME)
    
    assert p.returncode == 0
    
    teardown_test(cwd)
    

def test_cli_SHOULD_generate_config_file_in_cwd_when_no_exists():
    cwd = TESTS_SETUPS_PATH / 'test_cli_SHOULD_generate_config_file_in_cwd_when_no_exists'
    setup_test(cwd)
    
    test_project_dir = 'my_project'
    
    sys.argv = [sys.argv[0], test_project_dir]
    try:
        cli.main()
        assert False, 'Expected error not occured'
    except SystemExit:
        config_content = (cwd / settings.FileName.REPO_CONFIG).read_text()
        print(config_content)
        
        assert 'project-type' in config_content
        
    teardown_test(cwd)
        

def test_cli_SHOULD_generate_repo_properly_from_config_in_cwd():
    cwd = TESTS_SETUPS_PATH / 'test_cli_SHOULD_generate_repo_properly_from_config_in_cwd'
    setup_test(cwd, clean=False)
    
    test_project_dir = 'my_project'
    
    sys.argv = [sys.argv[0], test_project_dir]
    cli.main()
    
    p = subprocess.run(('make', 'test'), shell=True, cwd=cwd / test_project_dir)
    
    assert p.returncode == 0
    
    if (cwd / test_project_dir).exists():
        shutil.rmtree(cwd / test_project_dir, ignore_errors=False, onerror=_error_remove_readonly)
        
    teardown_test(cwd, clean=False)
    
    
def test_cli_SHOULD_generate_repo_properly_from_specified_config():
    cwd = TESTS_SETUPS_PATH / 'test_cli_SHOULD_generate_repo_properly_from_specified_config'
    setup_test(cwd, clean=False)
    
    test_project_dir = 'my_project'
    
    sys.argv = [sys.argv[0], test_project_dir, '-c', 'config/package_repo.cfg']
    cli.main()
    
    p = subprocess.run(('make', 'test'), shell=True, cwd=cwd / test_project_dir)
    
    assert p.returncode == 0
    
    if (cwd / test_project_dir).exists():
        shutil.rmtree(cwd / test_project_dir, ignore_errors=False, onerror=_error_remove_readonly)
        
    teardown_test(cwd, clean=False)
        

def test_cli_SHOULD_raise_error_WHEN_specified_config_not_exists():
    cwd = TESTS_SETUPS_PATH / 'test_cli_SHOULD_raise_error_WHEN_specified_config_not_exists'
    setup_test(cwd)
    
    test_project_dir = 'my_project'
    
    sys.argv = [sys.argv[0], test_project_dir, '-c', 'config/package_repo.cfg']
    try:
        cli.main()
        assert False, 'Expected error not occured'
    except SystemExit as e:
        assert 'generation error' in e.__str__()

    teardown_test(cwd)
