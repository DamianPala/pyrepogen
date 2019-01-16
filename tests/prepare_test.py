
import pytest
import inspect
import shutil
import stat
from pathlib import Path
from pprint import pprint

from pyrepogen import prepare
from pyrepogen import settings
from pyrepogen import utils
from pyrepogen import PARDIR
from pyrepogen import pygittools


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/prepare_test'
SKIP_ALL_MARKED = False


_DEFAULT_CONFIG = {
    'project_type': settings.ProjectType.MODULE.value,
    'project_name': 'sample_project',
    'author': 'Damian', 
    'author_email': 'mail@mail.com',
    'short_description': 'This is a sample project',
    'changelog_type': settings.ChangelogType.GENERATED.value,
    'authors_type': settings.AuthorsType.GENERATED.value,
    'pipreqs_ignore': [settings.DirName.REPOASSIST, settings.TESTS_PATH]
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
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.keywords = ['sample_project']
    
    args = Args
    args.force = True
    args.cloud = True
    
    path = prepare.write_file_from_template(Path(PARDIR) / settings.DirName.TEMPLATES / settings.FileName.SETUP_CFG, 
                                     Path(cwd) / settings.FileName.SETUP_CFG, config.__dict__, cwd, args)
    
    config_from_setup = utils.get_repo_config_from_setup_cfg(path[0])
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    
    assert config.__dict__ == config_from_setup.__dict__
    assert config_from_setup.keywords[0] == config.project_name


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_dirs():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_dirs'
    Path(cwd).mkdir(parents=True, exist_ok=True)

    config = settings.Config(**_DEFAULT_CONFIG)
    prepare._generate_repo_dirs(config, cwd)
    
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
        'repoassist/cli.py',
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
        'repoassist/templates/CHANGELOG_generated.md.j2',
        'repoassist/templates/CHANGELOG_prepared.md.j2',
        'repoassist/templates/AUTHORS_prepared.md.j2',
        'repoassist/templates/requirements-dev.txt.j2',
        'cloud_credentials.txt',
    }
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.PACKAGE.value
    config.is_sample_layout = True
    
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
def test_generate_package_repo_SHOULD_add_genereated_files_to_repo_tree_when_choosen():
    cwd = TESTS_SETUPS_PATH / 'test_generate_package_repo_SHOULD_add_genereated_files_to_repo_tree_when_choosen'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.PACKAGE.value
    config.is_sample_layout = True
    config.is_git = True
    
    args = Args
    args.force = False
    args.cloud = True
    
    paths = prepare.generate_repo(config, cwd, options=args)
    paths = {path.relative_to(cwd).as_posix() for path in paths \
             if path.is_file() and settings.FileName.CLOUD_CREDENTIALS not in path.__str__()}
    pprint(paths)
    
    pygittools.commit("Initial Commit", cwd)
    repo_paths = utils.get_git_repo_tree(cwd)
    repo_paths = {path.relative_to(cwd).as_posix() for path in repo_paths}
    pprint(repo_paths)
    
    assert paths == repo_paths
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)

    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_package_repo_SHOULD_generate_repo_tree_properly_WHEN_no_sample():
    cwd = TESTS_SETUPS_PATH / 'test_generate_package_repo_SHOULD_generate_repo_tree_properly_WHEN_no_sample'
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
        'tests',
        'repoassist',
        'repoassist/templates',
        'repoassist/__init__.py',
        'repoassist/__main__.py',
        'repoassist/cli.py',
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
        'repoassist/templates/CHANGELOG_generated.md.j2',
        'repoassist/templates/CHANGELOG_prepared.md.j2',
        'repoassist/templates/AUTHORS_prepared.md.j2',
        'repoassist/templates/requirements-dev.txt.j2',
        'cloud_credentials.txt',
    }
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.PACKAGE.value
    config.is_sample_layout = False
    
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
        'repoassist/cli.py',
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
        'repoassist/templates/CHANGELOG_generated.md.j2',
        'repoassist/templates/CHANGELOG_prepared.md.j2',
        'repoassist/templates/AUTHORS_prepared.md.j2',
        'repoassist/templates/requirements-dev.txt.j2',
        'cloud_credentials.txt',
    }
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.MODULE.value
    config.is_sample_layout = True
    
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
def test_generate_module_repo_SHOULD_generate_repo_tree_properly_WHEN_no_sample():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_generate_repo_tree_properly_WHEN_no_sample'
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
        'repoassist/cli.py',
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
        'repoassist/templates/CHANGELOG_generated.md.j2',
        'repoassist/templates/CHANGELOG_prepared.md.j2',
        'repoassist/templates/AUTHORS_prepared.md.j2',
        'repoassist/templates/requirements-dev.txt.j2',
        'cloud_credentials.txt',
    }
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.MODULE.value
    config.is_sample_layout = False
    
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
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.MODULE.value
    config.is_sample_layout = True
    
    args = Args
    args.force = True
    args.cloud = True
    args.sample_layout = True

    for dirname in settings.REPO_DIRS_TO_GEN:
        Path(Path(cwd) / dirname).mkdir(exist_ok=True)
    
    test_content = '<#test_content#>'
    
    files_paths_to_overwrite = []
    for file in settings.MODULE_REPO_FILES_TO_GEN:
        if settings.PROJECT_NAME_PATH_PLACEHOLDER in str(file.dst):
            dst = Path(str(file.dst).replace(settings.PROJECT_NAME_PATH_PLACEHOLDER, config.project_name))
        else:
            dst = file.dst
        with open(Path(cwd) / dst, 'w') as testfile:
            testfile.write(test_content)
        
        files_paths_to_overwrite.append(Path(cwd) / dst)
        
    for file in settings.REPOASSIST_FILES:
        with open(Path(cwd) / file.dst, 'w') as testfile:
            testfile.write(test_content)
        
        files_paths_to_overwrite.append(Path(cwd) / file.dst)

    prepare.generate_repo(config, cwd, options=args)
    
    pprint(files_paths_to_overwrite)
    for path in files_paths_to_overwrite:
        with open(path, 'r') as file:
            content = file.readlines()
            if content == test_content:
                assert False, "{} file not overwritten!".format(path)
                
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
                

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_generate_module_repo_SHOULD_generate_makefile_without_cloud_properly():
    cwd = TESTS_SETUPS_PATH / 'test_generate_module_repo_SHOULD_generate_makefile_without_cloud_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd))
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.MODULE.value
    
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
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.MODULE.value
    
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
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.MODULE.value
    
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
    

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
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


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
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
    
    
    
