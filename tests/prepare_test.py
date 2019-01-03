
import pytest
import inspect
import shutil
import stat
from pathlib import Path
from pprint import pprint

from pyrepogen import prepare, settings, logger


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/prepare_test'

_logger = logger.create_logger()


_DEFAULT_CONFIG = {
    'metadata': {
        'project_type': settings.ProjectType.SCRIPT.value,
        'repo_name': 'sample-repo',
        'project_name': 'sample_project',
        'author': 'Damian', 
        'author_email': 'mail@mail.com',
        'short_description': 'This is a sample project',
        'changelog_type': settings.ChangelogType.GENERATED.value,
        'year': '2018',
    },
}


class Args:
    force = True
    cloud = False
    
    
def _error_remove_readonly(_action, name, _exc):
    Path(name).chmod(stat.S_IWRITE)
    Path(name).unlink()


def test_generate_standalone_repo_dirs():
    cwd = TESTS_SETUPS_PATH / 'test_generate_standalone_repo_dirs'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    prepare._generate_standalone_repo_dirs(cwd)
    
    generated_dirset = set()
    for dirname in Path(cwd).iterdir():
        generated_dirset.add(dirname.name)
        if dirname.name == settings.REPOASSIST_DIRNAME:
            for dirnamelvl2 in (Path(cwd) / settings.REPOASSIST_DIRNAME).iterdir():
                generated_dirset.add(str(Path(dirname.name) / dirnamelvl2.name))
        
    pprint(generated_dirset)
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert generated_dirset == set(settings.STANDALONE_REPO_DIRS_TO_GEN)
    

def test_generate_standalone_repo_SHOULD_generate_repo_tree_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_standalone_repo_SHOULD_generate_repo_tree_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    expected_paths = {
        'docs',
        'tests',
        'repoassist',
        'README.md',
        '.gitignore',
        'TODO.md',
        'conftest.py',
        '{}.py'.format(_DEFAULT_CONFIG['metadata']['project_name']),
        'tests/{}_test.py'.format(_DEFAULT_CONFIG['metadata']['project_name']),
        'tests/__init__.py',
        'requirements.txt',
        'requirements-dev.txt',
        'Makefile',
        'LICENSE',
        'tox.ini',
        'setup.cfg',
        'repoassist/templates',
        'repoassist/__init__.py',
        'repoassist/__main__.py',
        'repoassist/colreqs.py',
        'repoassist/settings.py',
        'repoassist/logger.py',
        'repoassist/release.py',
        'repoassist/pygittools.py',
        'repoassist/utils.py',
        'repoassist/formatter.py',
        'repoassist/wizard.py',
        'repoassist/cloud.py',
        'repoassist/exceptions.py',
        'repoassist/templates/CHANGELOG_generated.md',
        'cloud_credentials.txt',
    }
    
    config = _DEFAULT_CONFIG
    
    args = Args
    args.force = False
    args.cloud = True
    
    paths = prepare.generate_standalone_repo(config, cwd, options=args)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    pprint(paths)
    
    assert paths == expected_paths
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)


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
        Path(cwd) / settings.REQUIREMENTS_DEV_FILENAME,
        Path(cwd) / settings.TOX_FILENAME,
        Path(cwd) / '{}.py'.format(_DEFAULT_CONFIG['metadata']['project_name']),
        Path(cwd) / settings.TESTS_DIRNAME / '{}_test.py'.format(_DEFAULT_CONFIG['metadata']['project_name']),
        Path(cwd) / settings.TESTS_DIRNAME / settings.PYINIT_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.PYINIT_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.REPOASSIST_TARGET_MAIN_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.COLREQS_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.SETTINGS_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.LOGGER_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.RELEASE_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.EXCEPTIONS_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.UTILS_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.PYGITTOOLS_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.CLOUD_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.WIZARD_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FORMATTER_FILENAME,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.TEMPLATES_DIRNAME / settings.CHANGELOG_FILENAME,
    ]
    
    args = Args
    args.force = True
    args.cloud = True
    
    config = _DEFAULT_CONFIG
        
    prepare.generate_standalone_repo(config, cwd, options=args)
     
    for path in files_paths_to_overwrite:
        with open(path, 'r') as file:
            content = file.readlines()
            if len(content) == 0:
                assert False, "{} file not overwritten!".format(path)
                

def test_generate_standalone_repo_SHOULD_generate_makefile_without_cloud_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_standalone_repo_SHOULD_generate_makefile_without_cloud_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = _DEFAULT_CONFIG
    
    options = Args
    options.force = True
    options.cloud = False
    
    paths = prepare.generate_standalone_repo(config, cwd, options=options)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    
    with open(Path(cwd) / settings.MAKEFILE_FILENAME) as file:
        makefile_content = file.read()
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert "make upload" not in makefile_content
    
    
def test_generate_standalone_repo_SHOULD_generate_makefile_with_cloud_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_standalone_repo_SHOULD_generate_makefile_with_cloud_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = _DEFAULT_CONFIG
    
    options = Args
    options.force = True
    options.cloud = True
    
    paths = prepare.generate_standalone_repo(config, cwd, options=options)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    
    with open(Path(cwd) / settings.MAKEFILE_FILENAME) as file:
        makefile_content = file.read()
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert "make upload" in makefile_content
    
