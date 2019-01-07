
import inspect
import stat
import shutil
from pathlib import Path

from pyrepogen import clean, logger


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/clean_test'

_logger = logger.create_logger()


class Args:
    force = True
    cloud = False


def _error_remove_readonly(_action, name, _exc):
    Path(name).chmod(stat.S_IWRITE)
    Path(name).unlink()
    
    
def _create_file_with_path(cwd, path):
    parent_path = Path(cwd / path).parent
    Path(parent_path).mkdir(parents=True, exist_ok=True)
    with open(cwd / path, 'w'):
        pass


def test_clean_files_SHOULD_delete_files_with_wildcard_properly():
    cwd = TESTS_SETUPS_PATH / 'test_clean_files_SHOULD_delete_files_with_wildcard_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    files_to_create = {
        'file1.egg',
        'file2.egg',
        'file.txt',
        'file.egg.info',
        'test/file.egg',
    }
    
    for path in files_to_create:
        _create_file_with_path(cwd, path)

    paths_that_should_left = {
        'file.egg.info',
        'file.txt', 
        'test/file.egg'
    }
    
    paths_to_delete = {
        'file1.egg',
        'file2.egg', 
    }
    
    for path in paths_to_delete:
        if not (Path(cwd) / path).exists():
            assert False, "File {} not exists though should!".format(path)

    files_to_delete = [
        '*.egg'
    ]
    clean._clean_files(cwd, files_list=files_to_delete)
    
    for path in paths_that_should_left:
        if not (Path(cwd) / path).exists():
            assert False, "File {} not exists though should!".format(path)
            
    for path in paths_to_delete:
        if (Path(cwd) / path).exists():
            assert False, "File {} exists though should not!".format(path)
            
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))        
            
            
def test_clean_files_SHOULD_delete_specified_files_properly():
    cwd = TESTS_SETUPS_PATH / 'test_clean_files_SHOULD_delete_specified_files_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    files_to_create = {
        'file1.egg',
        'file2.egg',
        'file.txt',
        'file.egg.info',
        'to_delete.py',
        'test/file.egg',
    }
    
    for path in files_to_create:
        _create_file_with_path(cwd, path)
    
    paths_that_should_left = {
        'file.egg.info',
        'file.txt', 
        'test/file.egg'
    }
    
    paths_to_delete = {
        'file1.egg',
        'file2.egg',
        'to_delete.py'
    }
    
    for path in paths_to_delete:
        if not (Path(cwd) / path).exists():
            assert False, "File {} not exists though should!".format(path)

    files_to_delete = [
        '*.egg',
        'to_delete.py'
    ]
    clean._clean_files(cwd, files_list=files_to_delete)
    
    for path in paths_that_should_left:
        if not (Path(cwd) / path).exists():
            assert False, "File {} not exists though should!".format(path)
            
    for path in paths_to_delete:
        if (Path(cwd) / path).exists():
            assert False, "File {} exists though should not!".format(path)
            
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
            

def test_clean_dirs_SHOULD_delete_directories_properly():
    cwd = TESTS_SETUPS_PATH / 'test_clean_dirs_SHOULD_delete_directories_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    files_to_create = {
        'file1.egg',
        'file2.egg',
        'file.txt',
        'file.egg.info',
        'test/file.egg'
    }
    
    dirs_to_create = {
        'dir1.egg-info',
        '__pycache__',
        '.tox',
        'build',
        'dist', 
        'venv23',
        'test/.tox',
        'test/dir1',
        'test/__pycache__'
    }
    
    dirs_to_clean = [
        {'name': '*.egg-info', 'flag': '.'},
        {'name': '__pycache__', 'flag': 'r'},
        {'name': '.pytest_cache', 'flag': 'r'},
        {'name': '.tox', 'flag': '.'},
        {'name': 'build', 'flag': '.'},
        {'name': 'dist', 'flag': '.'},
        {'name': 'venv*', 'flag': '.'},
    ]
    
    for path in files_to_create:
        _create_file_with_path(cwd, path)
        
    for path in dirs_to_create:
        Path(cwd / path).mkdir(parents=True, exist_ok=True)
    

    paths_that_should_left = {
        'test/dir1',
        'test/.tox'
    } | files_to_create
    
    paths_to_delete = {
        'dir1.egg-info',
        '__pycache__',
        '.tox',
        'build',
        'dist', 
        'venv23',
        'test/__pycache__'
    }
    
    for path in files_to_create | dirs_to_create:
        if not (Path(cwd) / path).exists():
            assert False, "File {} not exists though should!".format(path)
    
    clean._clean_dirs(cwd, dirs_to_clean)
    
    for path in paths_that_should_left:
        if not (Path(cwd) / path).exists():
            assert False, "File {} not exists though should!".format(path)
            
    for path in paths_to_delete:
        if (Path(cwd) / path).exists():
            assert False, "File {} exists though should not!".format(path)
            
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
