#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import logging
import shutil
import semver
from pathlib import Path
from pbr import git
from pprint import pprint
from enum import Enum

from . import settings
from . import utils
from . import exceptions
from . import pygittools
from . import wizard

_logger = logging.getLogger(__name__)

_VERSION_REGEX = r"__version__ *= *['|\"]\S+"


class ReleaseAction(Enum):
    MAKE_RELEASE = 'rel'
    REGENERATE = 'reg'
    

def make_release(prompt=True, cwd='.'):
    _logger.info("Preparing Release Package...")
    release_files_paths = []
    config_metadata = utils.read_setup_cfg(cwd)['metadata']
    
    if prompt:
        action = _release_checkout(config_metadata)
        if action == ReleaseAction.MAKE_RELEASE:
            new_release_tag = _prompt_release_metadata(cwd)
            new_release_msg = _prompt_release_msg()
            
            if config_metadata['project_type'] == settings.ProjectType.SCRIPT.value:
#                 TODO: check if updated file has not changed - git
                _update_version_standalone(new_release_tag, cwd)
            else:
                pass
            

            
            return
            commit_and_push_release_update()
            
    release_metadata = _get_release_metadata(cwd)
    if config_metadata['changelog_type'] == settings.ChangelogType.GENERATED.value:
        release_files_paths.append(_update_changelog(cwd))
    else:
        release_files_paths.append(Path(cwd).resolve() / settings.CHANGELOG_FILENAME)
    release_files_paths.append(_update_authors(cwd))
    release_files_paths.extend(utils.get_git_repo_tree(cwd))
    
    unique_release_files_paths = list(set(release_files_paths))
    
    package_path = _prepare_release_archive(unique_release_files_paths, release_metadata, cwd)
    
    _logger.info("Release Package {} prepared properly.".format(Path(package_path).relative_to(cwd)))
    
    return package_path


def _release_checkout(config_metadata):
    action = wizard.choose_one(__name__, "Make Release or Regenerate a release package using the actual release metadata",
                               choices=[ReleaseAction.MAKE_RELEASE.value, ReleaseAction.REGENERATE.value])
    action = ReleaseAction.MAKE_RELEASE if action == ReleaseAction.MAKE_RELEASE.value else ReleaseAction.REGENERATE
    
    if action == ReleaseAction.MAKE_RELEASE:
        if not wizard.is_checkpoint_ok(__name__, "Are you on the relevant branch?"):
            raise exceptions.ReleaseCheckoutError("Checkout to the proper branch!", _logger)
        if not wizard.is_checkpoint_ok(__name__, "Are there any uncommited changes or files not added into the repo tree? (y/n): ", valid_value='n'):
            raise exceptions.ReleaseCheckoutError("Commit your changes!", _logger)
        if not wizard.is_checkpoint_ok(__name__, "Is the {} file prepared correctly?".format(settings.README_FILENAME)):
            raise exceptions.ReleaseCheckoutError("Complete {} file!".format(settings.README_FILENAME), _logger)
        if not wizard.is_checkpoint_ok(__name__, "Is there something that should be added to {} file?".format(settings.TODO_FILENAME), valid_value='n'):
            raise exceptions.ReleaseCheckoutError("Complete {} file!".format(settings.TODO_FILENAME), _logger)
        if config_metadata['changelog_type'] == settings.ChangelogType.PREPARED.value:
            if not wizard.is_checkpoint_ok(__name__, "Is the {} file up to date?".format(settings.CHANGELOG_FILENAME)):
                raise exceptions.ReleaseCheckoutError("Complete {} file!".format(settings.CHANGELOG_FILENAME), _logger)
        
    return action


def _update_version_standalone(release_tag, cwd='.'):
    project_name = utils.read_setup_cfg(cwd)['metadata']['project_name']
    project_module_name = utils.get_module_name_with_suffix(project_name)
    new_version_string = "__version__ = '{}'".format(release_tag)
    try:
        with open(Path(cwd) / project_module_name, 'r+t') as file:
            content = file.read()
            if not re.search(_VERSION_REGEX, content):
                raise exceptions.VersionNotFoundError("__version__ variable not found in the {} file. Please correct the file.".format(project_module_name), _logger)
            else:
                updated_content = re.sub(_VERSION_REGEX, new_version_string, content, 1)
                file.seek(0)
                file.truncate()
                file.write(updated_content)
    except FileNotFoundError:
        raise exceptions.FileNotFoundError("Project module file {} not found. The Project Module must have the same name as the project_name entry in {}".format(
            project_module_name, settings.SETUP_CFG_FILENAME), _logger)
        

def _update_changelog(cwd='.'):
    _logger.info("Updating {} file...".format(settings.CHANGELOG_FILENAME))
    
    changelog_path = Path(cwd).resolve() / settings.CHANGELOG_FILENAME
    changelog = pygittools.get_changelog(report_format="### Version: %(tag) | Released: %(taggerdate:short) \r\n%(contents)", cwd=cwd)
    if changelog['returncode'] != 0:
        raise exceptions.ChangelogGenerateError("Changelog generation error: {}".format(changelog['msg']), _logger)
    else:
        changelog_content = changelog['msg']
    
    shutil.copy(Path(cwd).resolve() / settings.REPOASSIST_DIRNAME / settings.TEMPLATES_DIRNAME / settings.CHANGELOG_FILENAME, Path(cwd).resolve() / settings.CHANGELOG_FILENAME)
    with open(changelog_path, 'a') as file:
        file.write(changelog_content)
    
    _logger.info("{} file updated".format(settings.CHANGELOG_FILENAME))    
    
    return changelog_path


def _prompt_release_metadata(cwd=''):
    latest_release_tag_ret = pygittools.get_latest_tag(cwd)
    
    if latest_release_tag_ret['returncode'] != 0:
        _logger.tip("Repo has not yet been tagged. Proposed initial release tag: {}".format(settings.SUGGESTED_INITIAL_RELEASE_TAG))
        is_tagged = False
    else:
        _logger.info("Last release tag: {}".format(latest_release_tag_ret['msg']))
        is_tagged = True
    
    is_release_tag_valid = False
    comparing_release_tags = True
    while not is_release_tag_valid:
        new_release_tag = input("Enter new release tag - <Major Version>.<Minor Version>.<Patch version> e.g. 1.17.3-alpha.2: ")
        try:
            semver.parse(new_release_tag)
            if is_tagged:
                try:
                    latest_release_tag_obj = semver.VersionInfo.parse(latest_release_tag_ret['msg'])
                except ValueError:
                    _logger.error("Latest release tag not valid!")
                    if wizard.is_checkpoint_ok(__name__, "Continue without comparing_release_tags the new relese tag with the latest?"):
                        comparing_release_tags = False
                    else:
                        raise exceptions.ReleaseTagError("Latest release tag not valid! Please remove it to continue.", _logger)
                        
                new_release_tag_obj = semver.VersionInfo.parse(new_release_tag)
                
                if comparing_release_tags:
                    if new_release_tag_obj > latest_release_tag_obj:
                        is_release_tag_valid = True
                    else:
                        _logger.error("Entered release tag less than the previous release tag! Correct and enter a new one.")
                else:
                    return new_release_tag
                
        except ValueError:
            _logger.error("Entered release tag not valid! Correct and enter new one.")
    
    return new_release_tag


def _get_release_metadata(cwd='.'):
    release_metadata = {}
        
    ret = pygittools.get_latest_commit_hash(cwd)
    if ret['returncode'] != 0:
        raise exceptions.ReleaseMetadataError("Retrieving latest commit hash error: {}".format(ret['msg']), _logger)
    else:
        release_metadata['latest_commit_hash'] = ret['msg']
    
    ret = pygittools.get_latest_tag(cwd)
    if ret['returncode'] != 0:
        raise exceptions.ReleaseMetadataError("Retrieving release tag error: {}".format(ret['msg']), _logger)
    else:
        release_metadata['release_tag'] = ret['msg']
        
    return release_metadata


def _prompt_release_msg():
    print("Enter release message. Type '~' and press Enter key to comfirm. Markdown syntax allowed.")
    message = []
    while True:
        line = input()
        if line and line.strip()[-1] == '~':
            message.append(line.rstrip()[:-1])
            break
        message.append(line)
        
    message = '\n'.join(message)
    
    if not message:
        raise exceptions.ValueError("Tag msg cannot be empty", _logger)
    
    return message


def _update_authors(cwd='.'):
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
        
    if not is_error and new_mtime == current_mtime:
        is_error = True
        
    if is_error:
        raise exceptions.FileGenerationError("{} file generation error!".format(filename), _logger)
    
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
        