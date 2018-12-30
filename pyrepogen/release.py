#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import shutil
from pathlib import Path
from pbr import git
from pprint import pprint

from . import settings
from . import utils
from . import exceptions
from . import pygittools

_logger = logging.getLogger(__name__)


def make_release(cwd='.'):
    _logger.info("Preparing Release Package...")
    release_files_paths = []
    
    release_metadata = _get_release_metadata(cwd)
    release_files_paths.append(_generate_changelog(cwd))
    release_files_paths.append(_generate_authors(cwd))
    release_files_paths.extend(utils.get_git_repo_tree(cwd))
    
    unique_release_files_paths = list(set(release_files_paths))
    
    package_path = _prepare_release_archive(unique_release_files_paths, release_metadata, cwd)
    
    _logger.info("Release Package {} prepared properly.".format(Path(package_path).relative_to(cwd)))
    
    return package_path 
    

def _get_release_metadata(cwd='.'):
    release_metadata = {}
        
    ret = pygittools.get_latest_commit_hash(cwd)
    if ret['returncode'] != 0:
        raise exceptions.ReleaseMetadataError("Retrieving latest commit hash error: {}".format(ret['msg']), logger=_logger)
    else:
        release_metadata['latest_commit_hash'] = ret['msg']
    
    ret = pygittools.get_latest_tag(cwd)
    if ret['returncode'] != 0:
        raise exceptions.ReleaseMetadataError("Retrieving release tag error: {}".format(ret['msg']), logger=_logger)
    else:
        release_metadata['release_tag'] = ret['msg']
        
    return release_metadata


def _generate_changelog(cwd='.'):
    return _generate_file_pbr(settings.CHANGELOG_FILENAME, git.write_git_changelog, cwd)
    
    
def _generate_authors(cwd='.'):
    return _generate_file_pbr(settings.AUTHORS_FILENAME, git.generate_authors, cwd)
    
    
def _generate_file_pbr(filename, gen_handler, cwd='.'):
    is_error = False
    _logger.info("Generating {} file...".format(filename))
    
    file_path = Path(cwd) / filename
    git_dir = Path(cwd) / settings.GIT_DIRNAME
    if file_path.exists():
        current_mtime = file_path.stat().st_mtime
    else:
        current_mtime = 0
        
    gen_handler(git_dir=git_dir, dest_dir=cwd)
    
    if file_path.exists():
        new_mtime = file_path.stat().st_mtime
    else:
        is_error = True
        
    if new_mtime == current_mtime:
        is_error = True
        
    if is_error:
        raise exceptions.FileGenerationError("{} file generation error!".format(filename), logger=_logger)
    
    _logger.info("The {} file generated".format(filename))
    
    return file_path.resolve()
    
    
def _prepare_release_archive(release_files_paths, release_metadata, cwd='.'):
    _logger.info("Compressing package...")
    
    config = utils.read_setup_cfg(cwd)
    
    release_package_suffix = '.tar.gz'
    release_package_name = "{}_{}_{}{}".format(config['metadata']['project_name'], release_metadata['release_tag'], release_metadata['latest_commit_hash'], settings.RELEASE_PACKAGE_SUFFIX)
    release_package_temp_containter_path = Path(cwd).resolve() / settings.RELEASE_DIRNAME / release_package_name
    release_package_path = Path(cwd).resolve() / settings.RELEASE_DIRNAME / (release_package_name + release_package_suffix)
    
    if Path(release_package_temp_containter_path).exists():
        shutil.rmtree(release_package_temp_containter_path)
    if Path(release_package_path).exists():
        Path(release_package_path).unlink()
        
    Path.mkdir(release_package_temp_containter_path, parents=True)
    
    dist_path = Path(cwd) / settings.RELEASE_DIRNAME
    if not dist_path.exists():
        dist_path.mkdir()
    
    for path in release_files_paths:
        dst = release_package_temp_containter_path / path.relative_to(cwd)
        if not dst.parent.exists():
            dst.parent.mkdir()
        shutil.copy(path, dst)
        
        
    release_zip_package_name = shutil.make_archive(release_package_temp_containter_path, 'gztar', release_package_temp_containter_path)
    shutil.rmtree(release_package_temp_containter_path)
    
    _logger.info("Package compressed properly.")
    
    return release_zip_package_name
        