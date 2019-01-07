
import pytest
import inspect
import shutil
import stat
from pathlib import Path
from pprint import pprint

from pyrepogen import prepare, settings, logger, utils


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/prepare_test'
SKIP_ALL_MARKED = False

_logger = logger.create_logger()


_DEFAULT_CONFIG = {
    'project_type': settings.ProjectType.MODULE.value,
    'repo_name': 'sample-repo',
    'project_name': 'sample_project',
    'author': 'Damian', 
    'author_email': 'mail@mail.com',
    'short_description': 'This is a sample project',
    'changelog_type': settings.ChangelogType.GENERATED.value,
    'year': '2018',
    'repoassist_version': '0.1.0',
    'min_python': '3.7',
}


class Args:
    force = True
    cloud = False
    
    
def _error_remove_readonly(_action, name, _exc):
    Path(name).chmod(stat.S_IWRITE)
    Path(name).unlink()


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_dirs():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_dirs'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    prepare._generate_repo_dirs(cwd)
    
    generated_dirset = set()
    for dirname in Path(cwd).iterdir():
        generated_dirset.add(dirname.name)
        if dirname.name == settings.REPOASSIST_DIRNAME:
            for dirnamelvl2 in (Path(cwd) / settings.REPOASSIST_DIRNAME).iterdir():
                generated_dirset.add(str(Path(dirname.name) / dirnamelvl2.name))
        
    pprint(generated_dirset)
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert generated_dirset == set(settings.REPO_DIRS_TO_GEN)


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_package_repo_SHOULD_generate_repo_tree_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_package_repo_SHOULD_generate_repo_tree_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    args = Args
    args.force = False
    args.cloud = True
    
    utils.add_auto_config_fields(_DEFAULT_CONFIG)
    paths = prepare.generate_package_repo(_DEFAULT_CONFIG, cwd, options=args)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    pprint(paths)
    
    assert 0
    
#     if Path(cwd).exists():
#         shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_SHOULD_generate_repo_tree_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_generate_repo_tree_properly'
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
        '{}.py'.format(_DEFAULT_CONFIG['project_name']),
        'tests/{}_test.py'.format(_DEFAULT_CONFIG['project_name']),
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
        'repoassist/prepare.py',
        'repoassist/clean.py',
        'repoassist/templates/CHANGELOG_generated.md',
        'repoassist/templates/CHANGELOG_prepared.md',
        'cloud_credentials.txt',
    }
    
    args = Args
    args.force = False
    args.cloud = True
    
    paths = prepare.generate_module_repo(_DEFAULT_CONFIG, cwd, options=args)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    pprint(paths)
    
    assert paths == expected_paths
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_SHOULD_force_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_force_properly'
#     if Path(cwd).exists():
#         shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)

    for dirname in settings.REPO_DIRS_TO_GEN:
        Path(Path(cwd) / dirname).mkdir(exist_ok=True)
    
    for file in settings.MODULE_REPO_FILES_TO_GEN:
        filename = file['src'].name
        if filename == settings.FileName.MODULE_SAMPLE_TEST_FILENAME:
            path = cwd / settings.TESTS_DIRNAME
        elif filename == settings.FileName.PYINIT:
            path = cwd / settings.TESTS_DIRNAME
        elif filename == settings.FileName.SAMPLE_MODULE:
            path = cwd / settings.TESTS_DIRNAME
        else:
            path = cwd
        with open(Path(path) / filename, 'w'):
            pass
        
    for filename in settings.REPOASSIST_FILES:
        if filename == settings.FileName.REPOASSIST_MAIN:
            filename = settings.FileName.MAIN
        with open(Path(cwd) / settings.REPOASSIST_DIRNAME / filename, 'w'):
            pass
        
    files_paths_to_overwrite = [
        Path(cwd) / settings.FileName.GITIGNORE,
        Path(cwd) / settings.FileName.LICENSE,
        Path(cwd) / settings.FileName.MAKEFILE,
        Path(cwd) / settings.FileName.REQUIREMENTS_DEV,
        Path(cwd) / settings.FileName.TOX,
        Path(cwd) / '{}.py'.format(_DEFAULT_CONFIG['project_name']),
        Path(cwd) / settings.TESTS_DIRNAME / '{}_test.py'.format(_DEFAULT_CONFIG['project_name']),
        Path(cwd) / settings.TESTS_DIRNAME / settings.FileName.PYINIT,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.PYINIT,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.MAIN,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.COLREQS,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.SETTINGS,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.LOGGER,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.RELEASE,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.EXCEPTIONS,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.UTILS,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.PYGITTOOLS,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.CLOUD,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.WIZARD,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.FORMATTER,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.TEMPLATES_DIRNAME / settings.FileName.CHANGELOG_GENERATED,
        Path(cwd) / settings.REPOASSIST_DIRNAME / settings.TEMPLATES_DIRNAME / settings.FileName.CHANGELOG_PREPARED,
    ]
    
    args = Args
    args.force = True
    args.cloud = True
    
    prepare.generate_module_repo(_DEFAULT_CONFIG, cwd, options=args)
     
    for path in files_paths_to_overwrite:
        with open(path, 'r') as file:
            content = file.readlines()
            if len(content) == 0:
                assert False, "{} file not overwritten!".format(path)
                

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_SHOULD_generate_makefile_without_cloud_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_generate_makefile_without_cloud_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args
    options.force = True
    options.cloud = False
    
    paths = prepare.generate_module_repo(_DEFAULT_CONFIG, cwd, options=options)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    
    with open(Path(cwd) / settings.FileName.MAKEFILE) as file:
        makefile_content = file.read()
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert "make upload" not in makefile_content
    
    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_SHOULD_generate_makefile_with_cloud_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_generate_makefile_with_cloud_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args
    options.force = True
    options.cloud = True
    
    paths = prepare.generate_module_repo(_DEFAULT_CONFIG, cwd, options=options)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    
    with open(Path(cwd) / settings.FileName.MAKEFILE) as file:
        makefile_content = file.read()
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert "make upload" in makefile_content
    
