
import pytest
import inspect
import shutil
import os
import stat
import re
from pathlib import Path
from pprint import pprint
from pbr import git

from pyrepogen import (prepare, settings, logger, release, pygittools, exceptions, utils)


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/release_test'
SKIP_ALL_MARKED = False

_logger = logger.create_logger()


class Args:
    force = True
    cloud = False

def _error_remove_readonly(_action, name, _exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
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
    pygittools.add(str(Path(cwd) / 'file.txt'), cwd)
    pygittools.commit("Initial Commit", cwd)
    
    release._generate_file_pbr(settings.CHANGELOG_FILENAME, git.write_git_changelog, cwd)
    
    with open(Path(cwd) / settings.CHANGELOG_FILENAME, 'r') as file:
        changelog_content = file.read()
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert changelog_content == expected_changelog_content
    

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_prepare_release_properly():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_prepare_release_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = {
        'metadata': {
            'project_type': 'script',
            'repo_name': 'sample-repo',
            'project_name': 'sample_project',
            'author': 'Damian', 
            'author_email': 'mail@mail.com',
            'short_description': 'This is a sample project',
            'year': '2018',
        },
    }
    
    options = Args()
    options.force = True
    
    paths = prepare.generate_standalone_repo(config, cwd, options)
    expected_paths = {path.relative_to(cwd).as_posix() for path in paths}
    expected_paths.add(settings.AUTHORS_FILENAME)
    expected_paths.add(settings.CHANGELOG_FILENAME)
    expected_paths.remove('docs')
    pprint(expected_paths)
    
    pygittools.init(cwd)
    for path in paths:
        pygittools.add(path, cwd)
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag(cwd, '0.1.0', "First Release")
    
    archive_name = release.make_release(prompt=False, cwd=cwd)
    unpack_dir = Path(cwd) / Path(archive_name).stem
    
    if (unpack_dir.exists()):
        shutil.rmtree(unpack_dir)
    Path.mkdir(unpack_dir, parents=True)
    shutil.unpack_archive(archive_name, extract_dir=unpack_dir, format='gztar')
    
    unpack_paths = set()
    for path in Path(unpack_dir).glob('**/*'):
        unpack_paths.add(Path(path).relative_to(Path(cwd) / Path(archive_name).stem).as_posix())
    pprint(unpack_paths)
        
    assert unpack_paths == expected_paths
        
    shutil.rmtree(unpack_dir)

    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_rise_error_when_no_commit():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_rise_error_when_no_commit'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    pygittools.init(cwd)
    
    try:
        release.make_release(prompt=False, cwd=cwd)
    except exceptions.ReleaseMetadataError as e:
        assert "Retrieving latest commit hash error" in str(e)
            

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_rise_error_when_no_release_tag():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_rise_error_when_no_release_tag'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = {
        'metadata': {
            'project_type': 'script',
            'repo_name': 'sample-repo',
            'project_name': 'sample_project',
            'author': 'Damian', 
            'author_email': 'mail@mail.com',
            'short_description': 'This is a sample project',
            'year': '2018',
        },
    }
    
    options = Args()
    options.force = True
    
    paths = prepare.generate_standalone_repo(config, cwd, options)
    pygittools.init(cwd)
    for path in paths:
        pygittools.add(path, cwd)
    pygittools.commit("Initial Commit", cwd)
    
    try:
        release.make_release(prompt=False, cwd=cwd)
    except exceptions.ReleaseMetadataError as e:
        assert "Retrieving release tag error" in str(e)
            
            
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_version_standalone_SHOULD_update_version_properly():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_standalone_SHOULD_update_version_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = {
        'metadata': {
            'project_type': 'script',
            'repo_name': 'sample-repo',
            'project_name': 'sample_project',
            'author': 'Damian', 
            'author_email': 'mail@mail.com',
            'short_description': 'This is a sample project',
            'year': '2018',
        },
    }
    
    options = Args()
    options.force = True
    
    prepare.generate_standalone_repo(config, cwd, options)
    release._update_version_standalone('1.2.3-alpha.4', cwd)
    
    project_name = config['metadata']['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    with open(cwd / project_module_name, 'r') as file:
        content = file.read()
        m = re.search(release._VERSION_REGEX, content)
        assert m.group(0) == "__version__ = '1.2.3-alpha.4'"
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_version_standalone_SHOULD_rise_error_when_no_project_module():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_standalone_SHOULD_rise_error_when_no_project_module'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = {
        'metadata': {
            'project_type': 'script',
            'repo_name': 'sample-repo',
            'project_name': 'sample_project',
            'author': 'Damian', 
            'author_email': 'mail@mail.com',
            'short_description': 'This is a sample project',
            'year': '2018',
        },
    }
    
    options = Args()
    options.force = True
    
    project_name = config['metadata']['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    
    prepare.generate_standalone_repo(config, cwd, options)
    (cwd / project_module_name).unlink()
    
    try:
        release._update_version_standalone('1.2.3-alpha.4', cwd)
    except exceptions.FileNotFoundError as e:
        assert "Project module file sample_project.py not found" in str(e)
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_version_standalone_SHOULD_rise_error_when_no_version_in_module():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_standalone_SHOULD_rise_error_when_no_project_module'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = {
        'metadata': {
            'project_type': 'script',
            'repo_name': 'sample-repo',
            'project_name': 'sample_project',
            'author': 'Damian', 
            'author_email': 'mail@mail.com',
            'short_description': 'This is a sample project',
            'year': '2018',
        },
    }
    
    options = Args()
    options.force = True
    
    project_name = config['metadata']['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    
    prepare.generate_standalone_repo(config, cwd, options)
    with open(cwd / project_module_name, 'w'):
        pass
    
    try:
        release._update_version_standalone('1.2.3-alpha.4', cwd)
    except exceptions.VersionNotFoundError as e:
        assert "__version__ variable not found in the sample_project.py file" in str(e)
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    