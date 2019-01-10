
import pytest
import inspect
import shutil
import os
import stat
import re
import datetime
import time
from pathlib import Path
from pprint import pprint
from pbr import git
from types import SimpleNamespace

from pyrepogen import (prepare, settings, logger, release, pygittools, exceptions, utils)


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/release_test'
SKIP_ALL_MARKED = False

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
    'tests_path': settings.TESTS_PATH,
    'is_cloud': True,
    'is_sample_layout': True
}

_logger = logger.create_logger()


class Args:
    force = True
    cloud = False
    sample_layout = True
    
    
class ReleaseData:
    tag = ''
    msg = ''
    

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
def test_make_release_SHOULD_release_module_properly():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_release_module_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.MODULE.value
    
    options = Args()
    options.force = True
    options.cloud = True
    
    release_data = ReleaseData()
    release_data.tag = '0.2.0'
    release_data.msg = 'Next Release'
    
    paths = prepare.generate_repo(config, cwd, options)
    expected_paths = {path.relative_to(cwd).as_posix() for path in paths}
    expected_paths.remove(settings.DirName.DOCS) # TODO: think about doc in feature
    expected_paths.remove(settings.FileName.CLOUD_CREDENTIALS)
    expected_paths.remove(settings.FileName.GITIGNORE)
    expected_paths = expected_paths | {
        settings.FileName.AUTHORS,
        settings.FileName.CHANGELOG,
        'PKG-INFO',
        '{}'.format(config['project_name']),
        '{}/{}.py'.format(config['project_name'], config['project_name']),
        '{}.egg-info'.format(config['project_name']),
        '{}.egg-info/PKG-INFO'.format(config['project_name']),
        '{}.egg-info/SOURCES.txt'.format(config['project_name']),
        '{}.egg-info/dependency_links.txt'.format(config['project_name']),
        '{}.egg-info/not-zip-safe'.format(config['project_name']),
        '{}.egg-info/pbr.json'.format(config['project_name']),
        '{}.egg-info/top_level.txt'.format(config['project_name']),
        '{}.egg-info/entry_points.txt'.format(config['project_name']),
        '.'
    }
    pprint(expected_paths)
    
    pygittools.init(cwd)
    for path in paths:
        pygittools.add(path, cwd)
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag(cwd, '0.1.0', "First Release")
    
    archive_name = release.make_release(action=release.ReleaseAction.MAKE_RELEASE,
                                        prompt=False, 
                                        push=False,
                                        release_data=release_data,
                                        cwd=cwd)
    unpack_dir = Path(cwd) / Path(archive_name).stem
    
    if (unpack_dir.exists()):
        shutil.rmtree(unpack_dir)
    Path.mkdir(unpack_dir, parents=True)
    shutil.unpack_archive(archive_name, extract_dir=unpack_dir, format='gztar')
     
    unpack_paths = set()
    for path in Path(unpack_dir).glob('**/*'):
        unpack_paths.add(Path(path).relative_to(Path(cwd) / Path(archive_name).stem / Path(Path(archive_name).stem).stem).as_posix())
    pprint(unpack_paths)
         
    shutil.rmtree(unpack_dir)

    last_release_tag = pygittools.get_latest_tag(cwd)['msg']
    last_release_msg = pygittools.get_latest_tag_msg(cwd)['msg']
    
    assert unpack_paths == expected_paths
    assert release_data.tag == last_release_tag
    assert release_data.msg == last_release_msg
    assert not pygittools.are_uncommited_changes(cwd)['msg']

    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_release_package_properly():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_release_package_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.PACKAGE.value
    
    options = Args()
    options.force = True
    options.cloud = True
    
    release_data = ReleaseData()
    release_data.tag = '0.2.0'
    release_data.msg = 'Next Release'
    
    paths = prepare.generate_repo(config, cwd, options)
    expected_paths = {path.relative_to(cwd).as_posix() for path in paths}
    expected_paths.remove(settings.DirName.DOCS) # TODO: think about doc in feature
    expected_paths.remove(settings.FileName.CLOUD_CREDENTIALS)
    expected_paths.remove(settings.FileName.GITIGNORE)
    expected_paths = expected_paths | {
        settings.FileName.AUTHORS,
        settings.FileName.CHANGELOG,
        'PKG-INFO',
        '{}'.format(config['project_name']),
        '{}.egg-info'.format(config['project_name']),
        '{}.egg-info/PKG-INFO'.format(config['project_name']),
        '{}.egg-info/SOURCES.txt'.format(config['project_name']),
        '{}.egg-info/dependency_links.txt'.format(config['project_name']),
        '{}.egg-info/not-zip-safe'.format(config['project_name']),
        '{}.egg-info/pbr.json'.format(config['project_name']),
        '{}.egg-info/top_level.txt'.format(config['project_name']),
        '{}.egg-info/requires.txt'.format(config['project_name']),
        '{}.egg-info/entry_points.txt'.format(config['project_name']),
        '.'
    }
    pprint(expected_paths)
    
    pygittools.init(cwd)
    for path in paths:
        pygittools.add(path, cwd)
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag(cwd, '0.1.0', "First Release")
    
    archive_name = release.make_release(action=release.ReleaseAction.MAKE_RELEASE,
                                        prompt=False, 
                                        push=False,
                                        release_data=release_data,
                                        cwd=cwd)
    unpack_dir = Path(cwd) / Path(archive_name).stem
    
    if (unpack_dir.exists()):
        shutil.rmtree(unpack_dir)
    Path.mkdir(unpack_dir, parents=True)
    shutil.unpack_archive(archive_name, extract_dir=unpack_dir, format='gztar')
     
    unpack_paths = set()
    for path in Path(unpack_dir).glob('**/*'):
        unpack_paths.add(Path(path).relative_to(Path(cwd) / Path(archive_name).stem / Path(Path(archive_name).stem).stem).as_posix())
    pprint(unpack_paths)
         
    shutil.rmtree(unpack_dir)

    last_release_tag = pygittools.get_latest_tag(cwd)['msg']
    last_release_msg = pygittools.get_latest_tag_msg(cwd)['msg']
    
    assert unpack_paths == expected_paths
    assert release_data.tag == last_release_tag
    assert release_data.msg == last_release_msg
    assert not pygittools.are_uncommited_changes(cwd)['msg']

    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_regenerate_package_properly_on_the_same_commit():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_regenerate_package_properly_on_the_same_commit'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.PACKAGE.value
    
    options = Args()
    options.force = True
    options.cloud = True
    
    release_data = ReleaseData()
    release_data.tag = '0.2.0'
    release_data.msg = 'Next Release'
    
    paths = prepare.generate_repo(config, cwd, options)
    
    pygittools.init(cwd)
    for path in paths:
        pygittools.add(path, cwd)
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag(cwd, '0.1.0', "First Release")
    
    archive_name = release.make_release(action=release.ReleaseAction.MAKE_RELEASE,
                                        prompt=False, 
                                        push=False,
                                        release_data=release_data,
                                        cwd=cwd)
    
    assert not pygittools.are_uncommited_changes(cwd)['msg']
    
    archive_name_regenerated = release.make_release(action=release.ReleaseAction.REGENERATE,
                                        prompt=False, 
                                        push=False,
                                        release_data=None,
                                        cwd=cwd)

    assert archive_name == archive_name_regenerated 

    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_regenerate_package_properly_on_the_different_commit():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_regenerate_package_properly_on_the_different_commit'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.PACKAGE.value
    
    options = Args()
    options.force = True
    options.cloud = True
    
    release_data = ReleaseData()
    release_data.tag = '0.2.0'
    release_data.msg = 'Next Release'
    
    paths = prepare.generate_repo(config, cwd, options)
    
    pygittools.init(cwd)
    for path in paths:
        pygittools.add(path, cwd)
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag(cwd, '0.1.0', "First Release")
    
    release.make_release(action=release.ReleaseAction.MAKE_RELEASE,
                                        prompt=False, 
                                        push=False,
                                        release_data=release_data,
                                        cwd=cwd)
    
    assert not pygittools.are_uncommited_changes(cwd)['msg']
    
    file_to_modify = Path(cwd) / settings.FileName.README
    with open(file_to_modify, 'w') as file:
        file.write("test line")
        
    pygittools.add(file_to_modify, cwd)
    pygittools.commit("Next Commit", cwd)
        
    assert not pygittools.are_uncommited_changes(cwd)['msg']
    
    time.sleep(1)
    
    archive_name_regenerated = release.make_release(action=release.ReleaseAction.REGENERATE,
                                        prompt=False, 
                                        push=False,
                                        release_data=None,
                                        cwd=cwd)
    
    assert pygittools.get_latest_commit_hash(cwd)['msg'] in archive_name_regenerated.__str__()
    
#     if Path(cwd).exists():
#         shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)

    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_rise_error_when_no_commit():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_rise_error_when_no_commit'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    prepare.generate_repo(_DEFAULT_CONFIG, cwd, options)
    
    pygittools.init(cwd)
    
    try:
        release.make_release(prompt=False, cwd=cwd)
        assert False, "Expected error did not occured."
    except exceptions.NoCommitFoundError as e:
        if Path(cwd).exists():
            shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        assert "There are no commits in repository" in str(e)
        
            
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_rise_error_when_no_release_tag():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_rise_error_when_no_release_tag'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    paths = prepare.generate_repo(_DEFAULT_CONFIG, cwd, options)
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
def test_update_version_module_SHOULD_update_version_properly():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_module_SHOULD_update_version_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    _DEFAULT_CONFIG['project_type'] = settings.ProjectType.MODULE.value
    
    options = Args()
    options.force = True
    
    prepare.generate_repo(_DEFAULT_CONFIG, cwd, options)
    config = SimpleNamespace(**_DEFAULT_CONFIG)
    release._update_project_version(config, '1.2.3-alpha.4', cwd)
    
    project_name = _DEFAULT_CONFIG['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    file_version_path = Path(cwd) / project_module_name
    with open(file_version_path, 'r') as file:
        content = file.read()
        m = re.search(release._VERSION_REGEX, content)
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert m.group(0) == "__version__ = '1.2.3-alpha.4'"
    
    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_version_package_SHOULD_update_version_properly():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_package_SHOULD_update_version_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = dict(_DEFAULT_CONFIG)
    config['project_type'] = settings.ProjectType.PACKAGE.value
    
    options = Args()
    options.force = True
    
    prepare.generate_repo(config, cwd, options)
    
    config_namespace = SimpleNamespace(**config)
    release._update_project_version(config_namespace, '1.2.3-alpha.4', cwd)
    
    project_name = config['project_name']
    file_version_path = Path(cwd) / project_name / settings.FileName.PYINIT
    with open(file_version_path, 'r') as file:
        content = file.read()
        m = re.search(release._VERSION_REGEX, content)
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
    assert m.group(0) == "__version__ = '1.2.3-alpha.4'"

        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_version_module_SHOULD_rise_error_when_no_project_module():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_module_SHOULD_rise_error_when_no_project_module'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    project_name = _DEFAULT_CONFIG['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    file_version_path = Path(cwd) / project_module_name
    
    prepare.generate_repo(_DEFAULT_CONFIG, cwd, options)
    (cwd / project_module_name).unlink()
    
    try:
        release._update_version(file_version_path, '1.2.3-alpha.4', cwd)
        assert False, "Expected error did not occured."
    except exceptions.FileNotFoundError as e:
        if Path(cwd).exists():
            shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        assert "with a __version__ variable not foud" in str(e)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_update_version_module_SHOULD_rise_error_when_no_version_in_module():
    cwd = TESTS_SETUPS_PATH / 'test_update_version_module_SHOULD_rise_error_when_no_project_module'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    project_name = _DEFAULT_CONFIG['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    file_version_path = Path(cwd) / project_module_name
    
    prepare.generate_repo(_DEFAULT_CONFIG, cwd, options)
    with open(cwd / project_module_name, 'w'):
        pass
    
    try:
        release._update_version(file_version_path, '1.2.3-alpha.4', cwd)
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
    
    paths = prepare.generate_repo(_DEFAULT_CONFIG, cwd, options)
    
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
    
    config = SimpleNamespace(**_DEFAULT_CONFIG)
    release._update_generated_changelog(config, new_release_tag, new_release_msg, cwd)
    
    with open(Path(cwd) / settings.FileName.CHANGELOG, 'r') as file:
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
    
    paths = prepare.generate_repo(_DEFAULT_CONFIG, cwd, options)
    
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
    
    utils.execute_cmd(['git', 'config', '--local', 'remote.origin.url', 'some url'], cwd)
    
    last_commit_hash = pygittools.get_latest_commit_hash(cwd)
    last_tag = pygittools.get_latest_tag(cwd)

    files_to_add = []
    
    new_release_tag = '0.3.0'
    new_release_msg = "next release"
    
    config = SimpleNamespace(**_DEFAULT_CONFIG)
    files_to_add.append(release._update_changelog(config, new_release_tag, new_release_msg, cwd))
    files_to_add.append(release._update_authors(cwd))
    
    try:
        release._commit_and_push_release_update(new_release_tag, new_release_msg, files_to_add=files_to_add, cwd=cwd)
        assert False, "Expected error not occured!"
    except exceptions.CommitAndPushReleaseUpdateError:
        assert last_commit_hash == pygittools.get_latest_commit_hash(cwd)
        assert last_tag == pygittools.get_latest_tag(cwd)
        
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    
