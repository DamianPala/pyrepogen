#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
from pathlib import Path
from pbr import git
from pprint import pprint

from . import settings
from . import utils
from . import exceptions


_logger = logging.getLogger(__name__)


def make_release(cwd='.'):
    release_files_paths = []
    release_files_paths.append(_generate_changelog(cwd))
    release_files_paths.append(_generate_authors(cwd))
    release_files_paths.extend(utils.get_git_repo_tree(cwd))
    
    unique_release_files_paths = list(set(release_files_paths))
    
    pprint(unique_release_files_paths)


def _generate_changelog(cwd='.'):
    return _generate_file_pbr(settings.CHANGELOG_FILENAME, git.write_git_changelog, cwd)
    
    
def _generate_authors(cwd='.'):
    return _generate_file_pbr(settings.CHANGELOG_FILENAME, git.generate_authors, cwd)
    
    
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
        raise exceptions.FileGenerationError("{} file generation error!".format(filename))
    
    _logger.info("The {} file generated".format(filename))
    
    return file_path
    
    
def _prepare_release_archive(release_files_paths, cwd='.'):
    
    release_package_suffix = '.tar.gz'
    release_package_name = get_base_package_name(cwd) + RELEASE_PACKAGE_SUFFIX
    release_package_temp_containter_path = (Path(cwd).resolve() / DEPLOY_FOLDER_NAME / RELEASE_FOLDER_NAME / release_package_name)
    release_package_path = (Path(cwd).resolve() / DEPLOY_FOLDER_NAME / RELEASE_FOLDER_NAME / (release_package_name + release_package_suffix))
    
    
    dist_path = Path(cwd) / settings.DISTRIBUTION_DIRNAME
    if not dist_path.exists():
        dist_path.mkdir()
        