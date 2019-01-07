
import pytest
import inspect
import shutil
import os
import stat
import re
import datetime
from pathlib import Path
from pprint import pprint
from pbr import git

from pyrepogen import (prepare, settings, logger, release, pygittools, exceptions, utils)


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/release_test'
SKIP_ALL_MARKED = False

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
        'repoassist_version': '0.1.0',
        'min_python': '3.7',
        'tests_path': settings.TESTS_PATH
    },
}

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
    
    release._generate_file_pbr('ChangeLog', git.write_git_changelog, cwd)
    
    with open(Path(cwd) / 'ChangeLog', 'r') as file:
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
    
    options = Args()
    options.force = True
    
    paths = prepare.generate_standalone_repo(_DEFAULT_CONFIG, cwd, options)
    expected_paths = {path.relative_to(cwd).as_posix() for path in paths}
    expected_paths.remove(settings.DOCS_DIRNAME) # TODO: think about doc in feature
    expected_paths.remove(settings.CLOUD_CREDENTIALS_FILENAME)
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
        
    shutil.rmtree(unpack_dir)
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)

    assert unpack_paths == expected_paths
    
    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_rise_error_when_no_commit():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_rise_error_when_no_commit'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    prepare.generate_standalone_repo(_DEFAULT_CONFIG, cwd, options)
    
    pygittools.init(cwd)
    
    try:
        release.make_release(prompt=False, cwd=cwd)
        assert False, "Expected error did not occured."
    except exceptions.ReleaseMetadataError as e:
        if Path(cwd).exists():
            shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        assert "Retrieving latest commit hash error" in str(e)
        
            
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_rise_error_when_no_release_tag():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_rise_error_when_no_release_tag'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    paths = prepare.generate_standalone_repo(_DEFAULT_CONFIG, cwd, options)
    pygittools.init(cwd)
    for path in paths:
        pygittools.add(path, cwd)
    pygittools.commit("Initial Commit", cwd)
    
    try:
        release.make_release(prompt=False, cwd=cwd)
        assert False, "Expected error did not occured."
    except exceptions.ReleaseMetadataError as e:
        if Path(cwd).exists():
            shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        assert "Retrieving release tag error" in str(e)

            
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_version_standalone_SHOULD_update_version_properly():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_standalone_SHOULD_update_version_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    prepare.generate_standalone_repo(_DEFAULT_CONFIG, cwd, options)
    release._update_version_standalone('1.2.3-alpha.4', cwd)
    
    project_name = _DEFAULT_CONFIG['metadata']['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    with open(cwd / project_module_name, 'r') as file:
        content = file.read()
        m = re.search(release._VERSION_REGEX, content)
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert m.group(0) == "__version__ = '1.2.3-alpha.4'"

        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_version_standalone_SHOULD_rise_error_when_no_project_module():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_standalone_SHOULD_rise_error_when_no_project_module'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    project_name = _DEFAULT_CONFIG['metadata']['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    
    prepare.generate_standalone_repo(_DEFAULT_CONFIG, cwd, options)
    (cwd / project_module_name).unlink()
    
    try:
        release._update_version_standalone('1.2.3-alpha.4', cwd)
        assert False, "Expected error did not occured."
    except exceptions.FileNotFoundError as e:
        if Path(cwd).exists():
            shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        assert "Project module file sample_project.py not found" in str(e)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_version_standalone_SHOULD_rise_error_when_no_version_in_module():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_standalone_SHOULD_rise_error_when_no_project_module'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    project_name = _DEFAULT_CONFIG['metadata']['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    
    prepare.generate_standalone_repo(_DEFAULT_CONFIG, cwd, options)
    with open(cwd / project_module_name, 'w'):
        pass
    
    try:
        release._update_version_standalone('1.2.3-alpha.4', cwd)
    except exceptions.VersionNotFoundError as e:
        if Path(cwd).exists():
            shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        assert "__version__ variable not found in the sample_project.py file" in str(e)
    

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_changelog():
    cwd = TESTS_SETUPS_PATH / 'test_update_changelog'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    paths = prepare.generate_standalone_repo(_DEFAULT_CONFIG, cwd, options)
    
    pygittools.init(cwd)
    for path in paths:
        pygittools.add(path, cwd)
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag(cwd, '0.1.0', "First Release")
    
    with open(Path(cwd) / 'test.txt', 'w'):
        pass
    pygittools.add(str(Path(cwd) / 'test.txt'), cwd)
    pygittools.commit("Next Commit", cwd)
    
    new_release_tag = '0.2.0'
    new_release_msg = """- Next Release
- another line

- last line."""
    
    tagger_date = datetime.date.today().strftime('%Y-%m-%d')
    expected_changelog = '# sample_project - Change Log\nThis is a sample project\n\n### Version: 0.2.0 | Released: {} \n- Next Release\n- another line\n\n- last line.\n\n### Version: 0.1.0 | Released: {} \nFirst Release'.format(tagger_date, tagger_date)
    
    release._update_generated_changelog(_DEFAULT_CONFIG['metadata'], new_release_tag, new_release_msg, cwd)
    
    with open(Path(cwd) / settings.CHANGELOG_FILENAME, 'r') as file:
        content = file.read()
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)

    assert content == expected_changelog
    
    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_clean_filed_release():
    cwd = TESTS_SETUPS_PATH / 'test_clean_filed_release'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    paths = prepare.generate_standalone_repo(_DEFAULT_CONFIG, cwd, options)
    
    pygittools.init(cwd)
    for path in paths:
        pygittools.add(path, cwd)
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag(cwd, '0.1.0', "First Release")
    
    with open(Path(cwd) / 'test.txt', 'w'):
        pass
    pygittools.add(str(Path(cwd) / 'test.txt'), cwd)
    pygittools.commit("Next Commit", cwd)
    pygittools.set_tag(cwd, '0.2.0', """- Next Release
- another line

- last line.""")
    
    last_commit_hash = pygittools.get_latest_commit_hash(cwd)
    last_tag = pygittools.get_latest_tag(cwd)

    files_to_add = []
    
    new_release_tag = '0.3.0'
    new_release_msg = "next release"
    
    files_to_add.append(release._update_changelog(_DEFAULT_CONFIG['metadata'], new_release_tag, new_release_msg, cwd))
    files_to_add.append(release._update_authors(cwd))
    
    
    try:
        release._commit_and_push_release_update(new_release_tag, new_release_msg, files_to_add, cwd)
        assert False, "Expected error not occured!"
    except exceptions.CommitAndPushReleaseUpdateError:
        assert last_commit_hash == pygittools.get_latest_commit_hash(cwd)
        assert last_tag == pygittools.get_latest_tag(cwd)
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    