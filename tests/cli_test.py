#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import stat
import sys
import shutil
import pytest
import subprocess
from pathlib import Path

from pyrepogen import cli
from pyrepogen import settings
from pyrepogen import exceptions
from pyrepogen import pygittools


TESTS_SETUPS_PATH = Path(__file__).parent / 'tests_setups/cli_test'
TESTS_CWD = Path().cwd()
RUN_ALL_TESTS = True


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


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_cli_SHOULD_print_version_properly(capsys):
    sys.argv = [sys.argv[0]]
    sys.argv.append('--version')
    cli.main()
    
    captured = capsys.readouterr()
    print(captured.out)
    
    assert re.search(r'(\d+)\.(\d+)\.(\d+)', captured.out)


@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_cli_SHOULD_generate_demo_properly():
    cwd = TESTS_SETUPS_PATH / 'test_cli_SHOULD_generate_demo_properly'
    setup_test(cwd)
    
    sys.argv = [sys.argv[0], '--demo']
    cli.main()
    
    p = subprocess.run(('make', 'test'), cwd=cwd / settings.DEMO_CONFIG.repo_name)
    
    assert p.returncode == 0
    
    teardown_test(cwd)
    

@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
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
        

@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_cli_SHOULD_generate_repo_properly_from_config_in_cwd():
    cwd = TESTS_SETUPS_PATH / 'test_cli_SHOULD_generate_repo_properly_from_config_in_cwd'
    setup_test(cwd, clean=False)
    
    repo_name = 'my_repo'
    test_project_dir = 'my_project'
    
    sys.argv = [sys.argv[0], test_project_dir]
    cli.main()
    
    p = subprocess.run(('make', 'test'), cwd=cwd / test_project_dir / repo_name)
    
    assert p.returncode == 0
    
    if (cwd / test_project_dir).exists():
        shutil.rmtree(cwd / test_project_dir, ignore_errors=False, onerror=_error_remove_readonly)
        
    teardown_test(cwd, clean=False)
   

@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_cli_SHOULD_generate_repo_properly_from_specified_config():
    cwd = TESTS_SETUPS_PATH / 'test_cli_SHOULD_generate_repo_properly_from_specified_config'
    setup_test(cwd, clean=False)
    
    repo_name = 'my_repo'
    test_project_dir = 'test_repo_dir'
    
    sys.argv = [sys.argv[0], test_project_dir, '-c', 'config/package_repo.cfg']
    cli.main()
    
    p = subprocess.run(('make', 'test'), cwd=cwd / test_project_dir / repo_name)
    
    assert p.returncode == 0
    
    if (cwd / test_project_dir).exists():
        shutil.rmtree(cwd / test_project_dir, ignore_errors=False, onerror=_error_remove_readonly)
        
    teardown_test(cwd, clean=False)
        

@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_cli_SHOULD_raise_error_WHEN_specified_config_not_exists():
    cwd = TESTS_SETUPS_PATH / 'test_cli_SHOULD_raise_error_WHEN_specified_config_not_exists'
    setup_test(cwd)
    
    test_project_dir = 'my_project'
    
    args = settings.Options()
    args.repo_path = test_project_dir
    args.config = 'config/package_repo.cfg'
    
    with pytest.raises(exceptions.FileNotFoundError):
        cli.generate(args, cwd)
        
    teardown_test(cwd)
    

@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_update_SHOULD_raise_error_WHEN_repoassist_not_found():
    cwd = TESTS_SETUPS_PATH / 'test_update_SHOULD_raise_error_WHEN_repoassist_not_found'
    setup_test(cwd)
    
    args = settings.Options()
    args.update = '.'
    
    with pytest.raises(exceptions.RepoassistNotFoundError):
        cli.update(args)
        
    teardown_test(cwd)
    
    
@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_update_SHOULD_raise_error_WHEN_config_not_found():
    cwd = TESTS_SETUPS_PATH / 'test_update_SHOULD_raise_error_WHEN_config_not_found'
    setup_test(cwd)
    
    args = settings.Options()
    args.update = '.'
    
    (cwd / 'repoassist').mkdir()
    
    with pytest.raises(exceptions.ConfigError):
        cli.update(args)
        
    teardown_test(cwd)
    
    
@pytest.mark.skipif(RUN_ALL_TESTS == False, reason='Skipped on demand')
def test_update_SHOULD_update_repoassit_properly():
    cwd = TESTS_SETUPS_PATH / 'test_update_SHOULD_update_repoassit_properly'
    setup_test(cwd, clean=False)
    
    pygittools.init(cwd)
    
    args = settings.Options()
    args.update = '.'
    
    repoassit_path = cwd / 'repoassist'
    repoassist_templates_path = cwd / 'repoassist/templates'
    
    if repoassit_path.exists():
        shutil.rmtree(repoassit_path)
    
    repoassit_path.mkdir(exist_ok=True)
    repoassist_templates_path.mkdir(exist_ok=True)
    
    main_file_path = repoassit_path / settings.FileName.MAIN
    main_file_path.touch()
    assert main_file_path.read_text() == ''
    
    cli.update(args, add_to_tree=True)
    
    assert main_file_path.read_text() != ''
    assert repoassit_path / settings.FileName.PYINIT in list(repoassit_path.iterdir())
    
    if repoassit_path.exists():
        shutil.rmtree(repoassit_path)
    
    teardown_test(cwd, clean=False)
