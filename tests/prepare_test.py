
import pytest
import inspect
import shutil
import stat
from pathlib import Path
from pprint import pprint

from pyrepogen import prepare, settings, utils, PARDIR


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/prepare_test'
SKIP_ALL_MARKED = False


_DEFAULT_CONFIG = {
    'project_type': settings.ProjectType.MODULE.value,
    'repo_name': 'sample-repo',
    'project_name': 'sample_project',
    'author': 'Damian', 
    'author_email': 'mail@mail.com',
    'maintainer': 'Mike', 
    'maintainer_email': 'mike@mail.com',
    'short_description': 'This is a sample project',
    'home_page': 'page.com',
    'changelog_type': settings.ChangelogType.GENERATED.value,
    'year': '2018',
    'repoassist_version': '0.1.0',
    'min_python': '3.7',
    'is_cloud': True,
    'is_sample_layout': True
}


class Args:
    force = True
    cloud = False
    sample_layout = True
    
    
def _error_remove_readonly(_action, name, _exc):
    Path(name).chmod(stat.S_IWRITE)
    Path(name).unlink()


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_setup_cfg():
    cwd = TESTS_SETUPS_PATH / 'test_generate_setup_cfg'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = dict(_DEFAULT_CONFIG)
    del config['is_cloud']
    del config['is_sample_layout']
    utils.add_auto_config_fields(config)
    args = Args
    args.force = True
    args.cloud = True
    
    path = prepare.write_file_from_template(Path(PARDIR) / settings.DirName.TEMPLATES / settings.FileName.SETUP_CFG, 
                                     Path(cwd) / settings.FileName.SETUP_CFG, config, cwd, args)
    
    config_from_setup = utils.get_repo_config_from_setup_cfg(path[0])
    del config_from_setup['classifier']
    keywords = config_from_setup['keywords']
    del config_from_setup['keywords']
    
    pprint(config_from_setup)
    
    assert config == config_from_setup
    assert keywords[0] == config['project_name']


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_dirs():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_dirs'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    prepare._generate_repo_dirs(_DEFAULT_CONFIG, cwd)
    
    generated_dirset = set()
    for dirname in Path(cwd).iterdir():
        generated_dirset.add(dirname.name)
        if dirname.name == settings.DirName.REPOASSIST:
            for dirnamelvl2 in (Path(cwd) / settings.DirName.REPOASSIST).iterdir():
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
    
    expected_paths = {
        'docs',
        'README.md',
        '.gitignore',
        'TODO.md',
        'conftest.py',
        'requirements.txt',
        'requirements-dev.txt',
        'Makefile',
        'LICENSE',
        'tox.ini',
        'setup.cfg',
        'setup.py',
        _DEFAULT_CONFIG['project_name'],
        '{}/{}'.format(_DEFAULT_CONFIG['project_name'], settings.FileName.CLI),
        '{}/{}'.format(_DEFAULT_CONFIG['project_name'], settings.FileName.MAIN),
        '{}/{}'.format(_DEFAULT_CONFIG['project_name'], settings.FileName.PACKAGE_SAMPLE_MODULE),
        '{}/{}'.format(_DEFAULT_CONFIG['project_name'], settings.FileName.PYINIT),
        'tests',
        'tests/{}'.format(settings.FileName.PYINIT),
        'tests/{}'.format(settings.FileName.PACKAGE_SAMPLE_TEST),
        'repoassist',
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
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.PACKAGE.value
    utils.add_auto_config_fields(config)
    
    args = Args
    args.force = False
    args.cloud = True
    
    paths = prepare.generate_repo(config, cwd, options=args)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    pprint(paths)
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)

    assert paths == expected_paths


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_SHOULD_generate_repo_tree_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_generate_repo_tree_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    expected_paths = {
        'docs',
        'tests',
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
        'setup.py',
        'repoassist',
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
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.MODULE.value
    utils.add_auto_config_fields(config)
    
    args = Args
    args.force = False
    args.cloud = True
    
    paths = prepare.generate_repo(config, cwd, options=args)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    pprint(paths)
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)

    assert paths == expected_paths


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
        if filename == settings.FileName.PYINIT:
            path = cwd / settings.DirName.TESTS
        elif filename == settings.FileName.SAMPLE_MODULE:
            path = cwd / settings.DirName.TESTS
            filename = path = cwd / settings.DirName.TESTS / '{}_test.py'.format(_DEFAULT_CONFIG['project_name'])
        elif filename == settings.FileName.MODULE_SAMPLE:
            filename = path = cwd / '{}.py'.format(_DEFAULT_CONFIG['project_name'])
        else:
            path = cwd
        with open(Path(path) / filename, 'w'):
            pass
        
    for filename in settings.REPOASSIST_FILES:
        if filename == settings.FileName.REPOASSIST_MAIN:
            filename = settings.FileName.MAIN
        with open(Path(cwd) / settings.DirName.REPOASSIST / filename, 'w'):
            pass
        
    files_paths_to_overwrite = [
        Path(cwd) / settings.FileName.GITIGNORE,
        Path(cwd) / settings.FileName.LICENSE,
        Path(cwd) / settings.FileName.MAKEFILE,
        Path(cwd) / settings.FileName.REQUIREMENTS_DEV,
        Path(cwd) / settings.FileName.TOX,
        Path(cwd) / '{}.py'.format(_DEFAULT_CONFIG['project_name']),
        Path(cwd) / settings.DirName.TESTS / '{}_test.py'.format(_DEFAULT_CONFIG['project_name']),
        Path(cwd) / settings.DirName.TESTS / settings.FileName.PYINIT,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.PYINIT,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.MAIN,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.COLREQS,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.SETTINGS,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.LOGGER,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.RELEASE,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.EXCEPTIONS,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.UTILS,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.PYGITTOOLS,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.CLOUD,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.WIZARD,
        Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.FORMATTER,
        Path(cwd) / settings.DirName.REPOASSIST / settings.DirName.TEMPLATES / settings.FileName.CHANGELOG_GENERATED,
        Path(cwd) / settings.DirName.REPOASSIST / settings.DirName.TEMPLATES / settings.FileName.CHANGELOG_PREPARED,
    ]
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.MODULE.value
    utils.add_auto_config_fields(config)
    
    args = Args
    args.force = True
    args.cloud = True
    args.sample_layout = True
    
    prepare.generate_repo(config, cwd, options=args)
     
    for path in files_paths_to_overwrite:
        with open(path, 'r') as file:
            content = file.readlines()
            if content.__len__() == 0:
                assert False, "{} file not overwritten!".format(path)
                

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_SHOULD_generate_makefile_without_cloud_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_generate_makefile_without_cloud_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.MODULE.value
    utils.add_auto_config_fields(config)
    
    options = Args
    options.force = True
    options.cloud = False
    
    paths = prepare.generate_repo(config, cwd, options=options)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    
    with open(Path(cwd) / settings.FileName.MAKEFILE) as file:
        makefile_content = file.read()
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert "make upload" not in makefile_content
    

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_SHOULD_not_generate_cloud_credentials_without_cloud():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_not_generate_cloud_credentials_without_cloud'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.MODULE.value
    utils.add_auto_config_fields(config)
    
    options = Args
    options.force = True
    options.cloud = False
    
    paths = prepare.generate_repo(config, cwd, options=options)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert settings.FileName.CLOUD_CREDENTIALS not in paths
    
    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_SHOULD_generate_makefile_with_cloud_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_generate_makefile_with_cloud_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.MODULE.value
    utils.add_auto_config_fields(config)
    
    options = Args
    options.force = True
    options.cloud = True
    
    paths = prepare.generate_repo(config, cwd, options=options)
    paths = {path.relative_to(cwd).as_posix() for path in paths}
    
    with open(Path(cwd) / settings.FileName.MAKEFILE) as file:
        makefile_content = file.read()
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert "make upload" in makefile_content
    
    
def test_generate_empty_file_SHOULD_generate_file_when_no_exists():
    cwd = TESTS_SETUPS_PATH / 'test_generate_empty_file_SHOULD_generate_file_when_no_exists'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    path = Path(cwd) / 'file.txt'
    options = Args
    options.force = True
    
    prepare._generate_empty_file(path, cwd, options)
    
    assert Path(path).exists()
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)


def test_generate_empty_file_SHOULD_overwrite_file_when_force():
    cwd = TESTS_SETUPS_PATH / 'test_generate_empty_file_SHOULD_overwrite_file_when_force'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    path = Path(cwd) / 'file.py'
    options = Args
    options.force = True
    
    with open(path, 'w') as file:
        file.write("line")
    
    prepare._generate_empty_file(path, cwd, options)
    
    with open(path, 'r') as file:
        content = file.read()
    
    assert content == ''
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    
    
    
