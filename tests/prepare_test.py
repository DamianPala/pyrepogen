
import pytest
import inspect
from pathlib import Path

from pyrepogen.prepare import (generate_standalone_repo_dirs)
from pyrepogen.settings import STANDALONE_REPO_DIRS_TO_GEN


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/prepare_test'


def test_generate_standalone_repo_dirs():
    cwd = TESTS_SETUPS_PATH / 'test_generate_standalone_repo_dirs'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    generate_standalone_repo_dirs(cwd)
    
    generated_dirset = set()
    for dirname in Path(cwd).iterdir():
        generated_dirset.add(dirname.name)
        
    assert generated_dirset == set(STANDALONE_REPO_DIRS_TO_GEN)
    
