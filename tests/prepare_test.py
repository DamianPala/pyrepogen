
import pytest
import inspect
import shutil
from pathlib import Path
from pprint import pprint

from pyrepogen import prepare, settings, logger


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/prepare_test'

_logger = logger.create_logger()


class Args:
    force = True


def test_generate_standalone_repo_dirs():
    cwd = TESTS_SETUPS_PATH / 'test_generate_standalone_repo_dirs'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    prepare.generate_standalone_repo_dirs(cwd)
    
    generated_dirset = set()
    for dirname in Path(cwd).iterdir():
        generated_dirset.add(dirname.name)
        
    assert generated_dirset == set(settings.STANDALONE_REPO_DIRS_TO_GEN)
    

def test_generate_standalone_repo_SHOULD_generate_repo_tree_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_standalone_repo_SHOULD_generate_repo_tree_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = {
        'repo_name': 'sample-repo',
        'project_name': 'sample_project',
        'author': 'Damian', 
        'author_email': 'mail@mail.com',
        'short_description': 'This is a sample project',
        'year': '2018',
    }
    
    paths = prepare.generate_standalone_repo(config, cwd)
    pprint(paths)
    

def test_generate_standalone_repo_SHOULD_force_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_standalone_repo_SHOULD_force_properly'
#     if Path(cwd).exists():
#         shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)

    for dirname in settings.STANDALONE_REPO_DIRS_TO_GEN:
        Path(Path(cwd) / dirname).mkdir(exist_ok=True)
    
    for filename in settings.STANDALONE_REPO_FILES_TO_GEN:
        if filename == settings.STANDALONE_SAMPLE_TEST_FILENAME:
            path = cwd / settings.TESTS_DIRNAME
        elif filename == settings.PYINIT_FILENAME:
            path = cwd / settings.TESTS_DIRNAME
        elif filename == settings.TOX_STANDALONE_FILENAME:
            filename = settings.TOX_FILENAME
            path = cwd
        else:
            path = cwd
        with open(Path(path) / filename, 'w'):
            pass
        
    for filename in settings.REPOASSIST_FILES:
        if filename == settings.REPOASSIST_MAIN_FILENAME:
            filename = settings.REPOASSIST_TARGET_MAIN_FILENAME
        with open(Path(cwd) / settings.REPOASSIST_DIRNAME / filename, 'w'):
            pass
        
    files_paths_to_overwrite = [
        Path(cwd) / settings.GITIGNORE_FILENAME,
        Path(cwd) / settings.LICENSE_FILENAME,
        Path(cwd) / settings.MAKEFILE_FILENAME,
        Path(cwd) / settings.REQUIREMENTS_FILENAME,
        Path(cwd) / settings.REQUIREMENTS_DEV_FILENAME,
        Path(cwd) / settings.TOX_FILENAME,
        Path(cwd) / settings.STANDALONE_SAMPLE_FILENAME,
        Path(cwd) / settings.TESTS_DIRNAME / settings.STANDALONE_SAMPLE_TEST_FILENAME,
        Path(cwd) / settings.TESTS_DIRNAME / settings.PYINIT_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.REPOASSIST_TARGET_MAIN_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.COLREQS_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.SETTINGS_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.LOGGER_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.PYINIT_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.REPOASSIST_TARGET_MAIN_FILENAME,
    ]
    
    args = Args
    args.force = True
    
    config = {
        'repo_name': 'sample-repo',
        'project_name': 'sample_project',
        'author': 'Damian', 
        'author_email': 'mail@mail.com',
        'short_description': 'This is a sample project',
        'year': '2018',
    }
        
    prepare.generate_standalone_repo(config, cwd, options=args)
     
    for path in files_paths_to_overwrite:
        with open(path, 'r') as file:
            content = file.readlines()
            if len(content) == 0:
                assert False, "{} file not overwritten!".format(path) 
    
    
    assert 0
