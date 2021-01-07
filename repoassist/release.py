#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import sys
from pathlib import Path
from enum import Enum

from . import settings
from . import utils
from . import exceptions
from . import pygittools
from . import wizard
from . import logger
from . import reltools


_logger = logger.get_logger(__name__)

_VERSION_REGEX = r"__version__ *= *['|\"]\S+"


class ReleaseAction(Enum):
    MAKE_RELEASE = 'rel'
    REGENERATE = 'reg'


def make_install(options=None, cwd='.'):
    _logger.info('Performing installation...')
    
    if not options or (options and options.force != 'force'):
        reltools.check_repo_tree(cwd)
        reltools.check_if_changes_to_commit(cwd)
    
    try:
        release_tag = pygittools.get_latest_tag(cwd)
    except pygittools.PygittoolsError as e:
        raise exceptions.ReleaseMetadataError(f"Retrieving release tag error: {e}", _logger)

    final_release_tag = _get_final_release_tag(release_tag, cwd)
    
    _run_setup_cmd(['install'], release_tag=final_release_tag, cwd=cwd)
    
    _logger.info('Installation completed.')
    

def make_release(action=ReleaseAction.REGENERATE, prompt=True, push=True, release_data=None, options=None, cwd='.'):
    _logger.info('Preparing Source Distribution...')
    
    if not options or (options and options.force != 'force'):
        reltools.check_repo_tree(cwd)
        reltools.check_if_changes_to_commit(cwd)
    
    release_files_paths = []
    config = utils.get_repo_config_from_setup_cfg(Path(cwd) / settings.FileName.SETUP_CFG)

    if prompt:
        action = _release_checkout(config)
        if action == ReleaseAction.MAKE_RELEASE:
            new_release_tag = reltools.prompt_release_tag(reltools.TagType.PYTHON, cwd)
            new_release_msg = reltools.prompt_release_msg(cwd)
    else:
        if action == ReleaseAction.MAKE_RELEASE:
            new_release_tag = release_data.tag
            new_release_msg = release_data.msg
            
    if action == ReleaseAction.MAKE_RELEASE:
        files_to_add = [_update_project_version(config, new_release_tag, cwd)]
        changelog_type = _get_reltools_changelog_type(config)
        changelog_generated_template_path = (Path(__file__).parent / settings.DirName.TEMPLATES 
                                             / f'{settings.FileName.CHANGELOG_GENERATED}{settings.JINJA2_TEMPLATE_EXT}')
        changelog_prepared_template_path = (Path(__file__).parent / settings.DirName.TEMPLATES 
                                            / f'{settings.FileName.CHANGELOG_PREPARED}{settings.JINJA2_TEMPLATE_EXT}')
        authors_type = _get_reltools_authors_type(config)
        authors_generated_template_path = (Path(__file__).parent / settings.DirName.TEMPLATES 
                                             / f'{settings.FileName.AUTHORS_GENERATED}{settings.JINJA2_TEMPLATE_EXT}')
        authors_prepared_template_path = (Path(__file__).parent / settings.DirName.TEMPLATES 
                                            / f'{settings.FileName.AUTHORS_PREPARED}{settings.JINJA2_TEMPLATE_EXT}')
        
        files_to_add.append(reltools.update_changelog(changelog_type, 
                                                      settings.FileName.CHANGELOG, 
                                                      config.__dict__, 
                                                      new_release_tag, 
                                                      new_release_msg, 
                                                      changelog_generated_template_path=changelog_generated_template_path, 
                                                      changelog_prepared_template_path=changelog_prepared_template_path, 
                                                      cwd=cwd))
        files_to_add.append(reltools.update_authors(authors_type, 
                                                    settings.FileName.AUTHORS, 
                                                    config.__dict__, 
                                                    authors_generated_template_path, 
                                                    authors_prepared_template_path, 
                                                    cwd))

        release_files_paths.extend(reltools.commit_and_push_release_update(new_release_tag, 
                                                                           new_release_msg, 
                                                                           files_to_add=files_to_add, 
                                                                           push=push, 
                                                                           cwd=cwd))
        release_tag = new_release_tag
        
    elif action == ReleaseAction.REGENERATE:
        try:
            release_tag = pygittools.get_latest_tag(cwd)
        except pygittools.PygittoolsError as e:
            raise exceptions.ReleaseMetadataError(f"Retrieving release tag error: {e}"
                                                  f'Repository must be tagged before regenerate.', _logger)

    final_release_tag = _get_final_release_tag(release_tag, cwd, action)
    _run_setup_cmd(['sdist', 'bdist_wheel'], release_tag=final_release_tag, cwd=cwd)
    
    package_path = utils.get_latest_tarball(Path(cwd) / settings.DirName.DISTRIBUTION)
    
    if final_release_tag and final_release_tag not in package_path.name:
        raise exceptions.RuntimeError('Source Distribution preparing error! '
                                      'Sdidt package name not valid. Please try again.', _logger) 
    
    _logger.info(f'Source Distribution {utils.get_rel_path(package_path, cwd)} prepared properly.')
    
    return package_path


def _run_setup_cmd(cmd, release_tag=None, cwd='.'):
    setup_path = Path(cwd).resolve() / settings.FileName.SETUP_PY
    if not setup_path.exists():
        raise exceptions.FileNotFoundError(f'{utils.get_rel_path(setup_path, cwd)} '
                                           f'file not found that is necessary to the distribution process!', _logger)

    if release_tag:
        os.environ['PBR_VERSION'] = release_tag
    else:
        _logger.info('Release tag will be set by pbr automatically.')
    result = utils.execute_cmd([sys.executable, setup_path.__str__()] + cmd, cwd)
    for line in result.splitlines():
        _logger.info(line)
        
    
def _get_final_release_tag(release_tag, cwd, action=None):
    if not action or (action == ReleaseAction.REGENERATE):
        try:
            tag_commit_hash = pygittools.get_tag_commit_hash(release_tag, cwd)
        except pygittools.PygittoolsError as e:
            raise exceptions.ReleaseMetadataError(f'Retrieving tag commit hash error: {e}', _logger)
        
        try:
            latest_commit_hash = pygittools.get_latest_commit_hash(cwd)
        except pygittools.PygittoolsError as e:
            raise exceptions.ReleaseMetadataError(f'Retrieving latest commit hash error: {e}', _logger)
            
        if tag_commit_hash == latest_commit_hash:
            return release_tag
        else:
            return None
    elif action == ReleaseAction.MAKE_RELEASE:
        return release_tag
        

def _release_checkout(config):
    action = wizard.choose_one(__name__, 
                               'Make Release or Regenerate a release package using the actual release metadata',
                               choices=[ReleaseAction.MAKE_RELEASE.value, ReleaseAction.REGENERATE.value])
    action = ReleaseAction.MAKE_RELEASE if action == ReleaseAction.MAKE_RELEASE.value else ReleaseAction.REGENERATE
    
    if action == ReleaseAction.MAKE_RELEASE:
        if not wizard.is_checkpoint_ok(__name__, 'Are you on the relevant branch?'):
            raise exceptions.ReleaseCheckoutError('Checkout to the proper branch!', _logger)
        if not wizard.is_checkpoint_ok(__name__, 'Are there any uncommited changes or files not '
                                       'added into the repo tree?', valid_value='n'):
            raise exceptions.ReleaseCheckoutError('Commit your changes!', _logger)
        if not wizard.is_checkpoint_ok(__name__, f'Is the {settings.FileName.README} file prepared correctly?'):
            raise exceptions.ReleaseCheckoutError(f'Complete {settings.FileName.README} file!', _logger)
        if not wizard.is_checkpoint_ok(__name__, 
                                       f'Is there something that should be added to {settings.FileName.TODO} file?', 
                                       valid_value='n'):
            raise exceptions.ReleaseCheckoutError(f'Complete {settings.FileName.TODO} file!', _logger)
        if config.changelog_type == settings.ChangelogType.PREPARED.value:
            if not wizard.is_checkpoint_ok(__name__, f'Is the {settings.FileName.CHANGELOG} file up to date?'):
                raise exceptions.ReleaseCheckoutError(f'Complete {settings.FileName.CHANGELOG} file!', _logger)
        
    return action


def _update_project_version(config, release_tag, cwd='.'):
    if config.project_type == settings.ProjectType.MODULE.value:
        project_module_name = utils.get_module_name_with_suffix(config.project_name)
        file_version_path = Path(cwd).resolve() / project_module_name
        _update_version(file_version_path, release_tag, cwd)
    else:
        file_version_path = Path(cwd).resolve() / config.project_name / settings.FileName.PYINIT
        _update_version(file_version_path, release_tag, cwd)
        
    return file_version_path


def _update_version(file_version_path, release_tag, cwd='.'):
    new_version_string = f"__version__ = '{release_tag}'"
    try:
        with open(file_version_path, 'r+t') as file:
            content = file.read()
            if not re.search(_VERSION_REGEX, content):
                raise exceptions.VersionNotFoundError(f'__version__ variable not found in the '
                                                      f'{utils.get_rel_path(file_version_path, cwd)} file. '
                                                      f'Please correct the file.', _logger)
            else:
                updated_content = re.sub(_VERSION_REGEX, new_version_string, content, 1)
                file.seek(0)
                file.truncate()
                file.write(updated_content)
    except FileNotFoundError:
        raise exceptions.FileNotFoundError(f'File {utils.get_rel_path(file_version_path, cwd)} with a __version__ '
                                           f'variable not foud. File with the __version__ '
                                           f'variable is searched using the project_name entry in '
                                           f'{settings.FileName.SETUP_CFG}', _logger)


def _get_reltools_changelog_type(config):
    if config.changelog_type == settings.ChangelogType.GENERATED.value:
        return reltools.ChangelogType.GENERATED
    else:
        return reltools.ChangelogType.PREPARED


def _get_reltools_authors_type(config):
    if config.authors_type == settings.AuthorsType.GENERATED.value:
        return reltools.AuthorsType.GENERATED
    else:
        return  reltools.AuthorsType.PREPARED