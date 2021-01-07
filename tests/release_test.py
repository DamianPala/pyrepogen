#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

from pyrepogen import logger, reltools
_logger = logger.create_logger(name=None)
from pyrepogen import prepare 
from pyrepogen import settings 
from pyrepogen import release
from pyrepogen import pygittools 
from pyrepogen import exceptions 
from pyrepogen import utils


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/release_test'
SKIP_ALL_MARKED = False

_DEFAULT_CONFIG = {
    'project_type': settings.ProjectType.MODULE.value,
    'project_name': 'sample_project',
    'author': 'Damian', 
    'author_email': 'mail@mail.com',
    'short_description': 'This is a sample project',
    'changelog_type': settings.ChangelogType.GENERATED.value,
    'authors_type': settings.AuthorsType.GENERATED.value,
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
def test_make_release_SHOULD_release_module_properly():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_release_module_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.MODULE.value
    config.is_sample_layout = True
    
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
        '{}.egg-info'.format(config.project_name),
        '{}.egg-info/PKG-INFO'.format(config.project_name),
        '{}.egg-info/SOURCES.txt'.format(config.project_name),
        '{}.egg-info/dependency_links.txt'.format(config.project_name),
        '{}.egg-info/not-zip-safe'.format(config.project_name),
        '{}.egg-info/pbr.json'.format(config.project_name),
        '{}.egg-info/top_level.txt'.format(config.project_name),
        '{}.egg-info/entry_points.txt'.format(config.project_name),
        '.'
    }
    pprint(expected_paths)
    
    pygittools.init(cwd)
    for path in paths:
        try:
            pygittools.add(path, cwd)
        except pygittools.PygittoolsError:
            pass
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag('0.1.0', "First Release", cwd)
    
    time.sleep(1) # Sleep for different release time than previous
    
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

    last_release_tag = pygittools.get_latest_tag(cwd)
    last_release_msg = pygittools.get_latest_tag_msg(cwd)
    
    assert unpack_paths == expected_paths
    assert release_data.tag == last_release_tag
    assert release_data.msg == last_release_msg
    assert not pygittools.are_uncommited_changes(cwd)

    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_release_package_properly():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_release_package_properly'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.PACKAGE.value
    config.is_sample_layout = True
    
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
        '{}'.format(config.project_name),
        '{}.egg-info'.format(config.project_name),
        '{}.egg-info/PKG-INFO'.format(config.project_name),
        '{}.egg-info/SOURCES.txt'.format(config.project_name),
        '{}.egg-info/dependency_links.txt'.format(config.project_name),
        '{}.egg-info/not-zip-safe'.format(config.project_name),
        '{}.egg-info/pbr.json'.format(config.project_name),
        '{}.egg-info/top_level.txt'.format(config.project_name),
        '{}.egg-info/requires.txt'.format(config.project_name),
        '{}.egg-info/entry_points.txt'.format(config.project_name),
        '.'
    }
    pprint(expected_paths)
    
    pygittools.init(cwd)
    for path in paths:
        try:
            pygittools.add(path, cwd)
        except pygittools.PygittoolsError:
            pass
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag('0.1.0', "First Release", cwd)
    
    time.sleep(1) # Sleep for different release time than previous
    
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

    last_release_tag = pygittools.get_latest_tag(cwd)
    last_release_msg = pygittools.get_latest_tag_msg(cwd)
    
    assert unpack_paths == expected_paths
    assert release_data.tag == last_release_tag
    assert release_data.msg == last_release_msg
    assert not pygittools.are_uncommited_changes(cwd)

    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_release_package_properly_WHEN_origin_not_reached():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_release_package_properly_WHEN_origin_not_reached'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.PACKAGE.value
    config.is_sample_layout = True
    
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
        '{}'.format(config.project_name),
        '{}.egg-info'.format(config.project_name),
        '{}.egg-info/PKG-INFO'.format(config.project_name),
        '{}.egg-info/SOURCES.txt'.format(config.project_name),
        '{}.egg-info/dependency_links.txt'.format(config.project_name),
        '{}.egg-info/not-zip-safe'.format(config.project_name),
        '{}.egg-info/pbr.json'.format(config.project_name),
        '{}.egg-info/top_level.txt'.format(config.project_name),
        '{}.egg-info/requires.txt'.format(config.project_name),
        '{}.egg-info/entry_points.txt'.format(config.project_name),
        '.'
    }
    pprint(expected_paths)
    
    pygittools.init(cwd)
    pygittools.set_origin('http://origin', cwd)
    for path in paths:
        try:
            pygittools.add(path, cwd)
        except pygittools.PygittoolsError:
            pass
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag('0.1.0', "First Release", cwd)
    
    time.sleep(1) # Sleep for different release time than previous
    
    archive_name = release.make_release(action=release.ReleaseAction.MAKE_RELEASE,
                                        prompt=False,
                                        push=True,
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

    last_release_tag = pygittools.get_latest_tag(cwd)
    last_release_msg = pygittools.get_latest_tag_msg(cwd)
    
    assert unpack_paths == expected_paths
    assert release_data.tag == last_release_tag
    assert release_data.msg == last_release_msg
    assert not pygittools.are_uncommited_changes(cwd)

    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_regenerate_package_properly_on_the_same_commit():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_regenerate_package_properly_on_the_same_commit'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.PACKAGE.value
    config.is_sample_layout = True
    
    options = Args()
    options.force = True
    options.cloud = True
    
    release_data = ReleaseData()
    release_data.tag = '0.2.0'
    release_data.msg = 'Next Release'
    
    paths = prepare.generate_repo(config, cwd, options)
    
    pygittools.init(cwd)
    for path in paths:
        try:
            pygittools.add(path, cwd)
        except pygittools.PygittoolsError:
            pass
    pygittools.commit("Initial Commit", cwd)
    pygittools.set_tag('0.1.0', "First Release", cwd)
    
    time.sleep(1) # Sleep for different release time than previous
    
    archive_name = release.make_release(action=release.ReleaseAction.MAKE_RELEASE,
                                        prompt=False, 
                                        push=False,
                                        release_data=release_data,
                                        cwd=cwd)
    
    assert not pygittools.are_uncommited_changes(cwd)
    
    archive_name_regenerated = release.make_release(action=release.ReleaseAction.REGENERATE,
                                        prompt=False, 
                                        push=False,
                                        release_data=None,
                                        cwd=cwd)

    assert archive_name == archive_name_regenerated 

    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
@pytest.mark.skip(reason='Skipped due to problem with testing on one instance of pytest run. Behaviour checked and passed manually')
def test_make_release_SHOULD_regenerate_package_properly_on_the_different_commit():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_regenerate_package_properly_on_the_different_commit'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.PACKAGE.value
    config.is_sample_layout = True
    
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
    pygittools.set_tag('0.1.0', "First Release", cwd)
    
    time.sleep(1) # Sleep for different release time than previous
    
    release.make_release(action=release.ReleaseAction.MAKE_RELEASE,
                                        prompt=False, 
                                        push=False,
                                        release_data=release_data,
                                        cwd=cwd)
    
    assert not pygittools.are_uncommited_changes(cwd)
    
    file_to_modify = Path(cwd) / settings.FileName.README
    with open(file_to_modify, 'w') as file:
        file.write("test line")
        
    pygittools.add(file_to_modify, cwd)
    pygittools.commit("Next Commit", cwd)
        
    assert not pygittools.are_uncommited_changes(cwd)
    
    time.sleep(1)
    
    archive_name_regenerated = release.make_release(action=release.ReleaseAction.REGENERATE,
                                        prompt=False, 
                                        push=False,
                                        release_data=None,
                                        cwd=cwd)
    
    assert pygittools.get_latest_commit_hash(cwd) in archive_name_regenerated.__str__()
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)

    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_make_release_SHOULD_rise_error_when_no_commit():
    cwd = TESTS_SETUPS_PATH / 'test_make_release_SHOULD_rise_error_when_no_commit'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    options = Args()
    options.force = True
    
    config = settings.Config(**_DEFAULT_CONFIG)
    prepare.generate_repo(config, cwd, options)
    
    pygittools.init(cwd)
    
    try:
        release.make_release(prompt=False, cwd=cwd)
        assert False, "Expected error did not occured."
    except reltools.NoCommitFoundError as e:
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
    
    config = settings.Config(**_DEFAULT_CONFIG)
    paths = prepare.generate_repo(config, cwd, options)
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
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.MODULE.value
    config.is_sample_layout = True
    
    options = Args()
    options.force = True
    
    prepare.generate_repo(config, cwd, options)
    release._update_project_version(config, '1.2.3-alpha.4', cwd)
    
    project_name = config.project_name
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
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.project_type = settings.ProjectType.PACKAGE.value
    config.is_sample_layout = True
    
    options = Args()
    options.force = True
    
    prepare.generate_repo(config, cwd, options)
    
    release._update_project_version(config, '1.2.3-alpha.4', cwd)
    
    project_name = config.project_name
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
    
    config = settings.Config(**_DEFAULT_CONFIG)
    
    options = Args()
    options.force = True
    config.is_sample_layout = True
    
    project_name = config.project_name
    project_module_name = utils.get_module_name_with_suffix(project_name)
    file_version_path = Path(cwd) / project_module_name
    
    prepare.generate_repo(config, cwd, options)
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
    
    config = settings.Config(**_DEFAULT_CONFIG)
    config.is_sample_layout = True
    
    options = Args()
    options.force = True
    
    project_name = config.project_name
    project_module_name = utils.get_module_name_with_suffix(project_name)
    file_version_path = Path(cwd) / project_module_name
    
    prepare.generate_repo(config, cwd, options)
    with open(cwd / project_module_name, 'w'):
        pass
    
    try:
        release._update_version(file_version_path, '1.2.3-alpha.4', cwd)
    except exceptions.VersionNotFoundError as e:
        if Path(cwd).exists():
            shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        assert "__version__ variable not found in the sample_project.py file" in str(e)
    
