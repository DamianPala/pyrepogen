
import pytest
import inspect
import shutil
import os
import stat
from pathlib import Path
from pprint import pprint
from pbr import git

from pyrepogen import prepare, settings, logger, release, pygittools


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/release_test'

_logger = logger.create_logger()


class Args:
    force = True

def _error_remove_readonly(_action, name, _exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

def test_generate_file_pbr_SHOULD_generate_file_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_file_pbr_SHOULD_generate_file_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    expected_changelog_content = """CHANGES
=======

* Initial Commit
"""
    
    pygittools.init(cwd)
    with open(Path(cwd) / 'file.txt', 'w') as file:
        file.write("Some text")
    pygittools.add([str(Path(cwd) / 'file.txt')], cwd)
    pygittools.commit("Initial Commit", cwd)
    
    release._generate_file_pbr(settings.CHANGELOG_FILENAME, git.write_git_changelog, cwd)
    
    with open(Path(cwd) / settings.CHANGELOG_FILENAME, 'r') as file:
        changelog_content = file.read()
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert changelog_content == expected_changelog_content
    
    
