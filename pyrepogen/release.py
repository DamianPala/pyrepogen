#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import datetime
from pathlib import Path
from pbr import git
from packaging import version as pkg_version
from enum import Enum

from . import settings
from . import utils
from . import exceptions
from . import pygittools
from . import wizard
from . import prepare
from . import logger


_logger = logger.get_logger(__name__)

_VERSION_REGEX = r"__version__ *= *['|\"]\S+"


class ReleaseAction(Enum):
    MAKE_RELEASE = 'rel'
    REGENERATE = 'reg'


def make_install(options=None, cwd='.'):
    _logger.info('Performing installation...')
    
    if not options or (options and options.force != 'force'):
        _check_repo_tree(cwd)
        _check_if_changes_to_commit(cwd)
    
    ret = pygittools.get_latest_tag(cwd)
    if ret['returncode'] != 0:
        raise exceptions.ReleaseMetadataError(f"Retrieving release tag error: {ret['msg']}", _logger)
    else:
        release_tag = ret['msg']

    final_release_tag = _get_final_release_tag(release_tag, cwd)
    
    _run_setup_cmd(['install'], release_tag=final_release_tag, cwd=cwd)
    
    _logger.info('Installation completed.')
    

def make_release(action=ReleaseAction.REGENERATE, prompt=True, push=True, release_data=None, options=None, cwd='.'):
    _logger.info('Preparing Source Distribution...')
    
    if not options or (options and options.force != 'force'):
        _check_repo_tree(cwd)
        _check_if_changes_to_commit(cwd)
    
    release_files_paths = []
    config = utils.get_repo_config_from_setup_cfg(Path(cwd) / settings.FileName.SETUP_CFG)

    if prompt:
        action = _release_checkout(config)
        if action == ReleaseAction.MAKE_RELEASE:
            new_release_tag = _prompt_release_tag(cwd)
            new_release_msg = _prompt_release_msg()
    else:
        if action == ReleaseAction.MAKE_RELEASE:
            new_release_tag = release_data.tag
            new_release_msg = release_data.msg
            
    if action == ReleaseAction.MAKE_RELEASE:
        files_to_add = []
        files_to_add.append(_update_project_version(config, new_release_tag, cwd))
        files_to_add.append(_update_changelog(config, new_release_tag, new_release_msg, cwd))
        files_to_add.append(_update_authors(config, cwd))

        release_files_paths.extend(_commit_and_push_release_update(new_release_tag, 
                                                                   new_release_msg, 
                                                                   files_to_add=files_to_add, 
                                                                   push=push, 
                                                                   cwd=cwd))
        release_tag = new_release_tag
        
    elif action == ReleaseAction.REGENERATE:
        ret = pygittools.get_latest_tag(cwd)
        if ret['returncode'] != 0:
            raise exceptions.ReleaseMetadataError(f"Retrieving release tag error: {ret['msg']}"
                                                  f'Repository must be tagged before regenerate.', _logger)
        else:
            release_tag = ret['msg']

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
    result = utils.execute_cmd([settings.Tools.PYTHON, setup_path.__str__()] + cmd, cwd)
    for line in result.splitlines():
        _logger.info(line)
        
    
def _get_final_release_tag(release_tag, cwd, action=None):
    if not action or (action == ReleaseAction.REGENERATE):
        ret = pygittools.get_tag_commit_hash(release_tag, cwd)
        if ret['returncode'] != 0:
            raise exceptions.ReleaseMetadataError(f"Retrieving tag commit hash error: {ret['msg']}", _logger)
        else:
            tag_commit_hash = ret['msg']
        
        ret = pygittools.get_latest_commit_hash(cwd)
        if ret['returncode'] != 0:
            raise exceptions.ReleaseMetadataError(f"Retrieving latest commit hash error: {ret['msg']}", _logger)
        else:
            latest_commit_hash = ret['msg']
            
        if tag_commit_hash == latest_commit_hash:
            return release_tag
        else:
            return None
    elif action == ReleaseAction.MAKE_RELEASE:
        return release_tag
        

def _check_if_changes_to_commit(cwd):
    ret = pygittools.are_uncommited_changes(cwd)
    if ret['returncode'] == 0:
        if ret['msg']:
            raise exceptions.UncommitedChangesError('There are changes to commit!', _logger)
    else:
        raise exceptions.UncommitedChangesError('Error checking if there are any changes to commit!', _logger)
    
    
def _check_repo_tree(cwd):
    if not pygittools.is_work_tree(cwd):
        raise exceptions.WorkTreeNotFoundError('Git Work Tree not found! Please check '
                                               'if the git repository is initialized.', _logger)

    if not pygittools.is_any_commit(cwd):
        raise exceptions.NoCommitFoundError('There are no commits in repository. '
                                            'Please commit before release.', _logger)
    
    if not utils.get_git_repo_tree(cwd):
        raise exceptions.EmptyRepositoryError('No files in repo tree!', _logger)
    

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
        

def _update_changelog(config, new_release_tag, new_release_msg, cwd='.'):
    if config.changelog_type == settings.ChangelogType.GENERATED.value:
        changelog_filepath = _update_generated_changelog(config, new_release_tag, new_release_msg, cwd)
    else:
        changelog_filepath = _generate_prepared_file(config, settings.FileName.CHANGELOG, 
                                                   settings.FileName.CHANGELOG_PREPARED, cwd)
        
    return changelog_filepath


def _update_generated_changelog(config, new_release_tag, new_release_msg, cwd='.'):
    _logger.info(f'Updating {settings.FileName.CHANGELOG} file...')
    
    changelog_path = Path(cwd).resolve() / settings.FileName.CHANGELOG
    ret = pygittools.get_changelog(
        report_format='### Version: %(tag) | Released: %(taggerdate:short) \r\n%(contents)', cwd=cwd)
    if ret['returncode'] != 0:
        raise exceptions.ChangelogGenerateError(f"Changelog generation error: {ret['msg']}", _logger)
    else:
        changelog_content = ret['msg']
    
    if changelog_path.exists():
        changelog_path.unlink()
    prepare.write_file_from_template(Path(settings.DirName.TEMPLATES) / settings.FileName.CHANGELOG_GENERATED, 
                                     changelog_path, config.__dict__, cwd, verbose=False)
    with open(changelog_path, 'a') as file:
        file.write('\n')
        file.write(_get_changelog_entry(new_release_tag, new_release_msg))
        file.write(changelog_content)
    
    _logger.info(f'{settings.FileName.CHANGELOG} file updated')    
    
    return changelog_path


def _get_changelog_entry(release_tag, release_msg):
    tagger_date = datetime.date.today().strftime('%Y-%m-%d')
    
    return f'### Version: {release_tag} | Released: {tagger_date} \n{release_msg}\n\n'


def _commit_and_push_release_update(new_release_tag, new_release_msg, files_to_add=None, push=True, cwd='.'):
    if push:
        _logger.info('Commit updated release files, set tag and push...')
    else:
        _logger.info('Commit updated release files, set tag...')
    
    paths = []
    for file_path in files_to_add:
        ret = pygittools.add(file_path, cwd)
        if ret['returncode'] != 0:
            raise exceptions.CommitAndPushReleaseUpdateError(f"{file_path.name} git add error: {ret['msg']}", _logger)
        paths.append(file_path)
    
    ret = pygittools.commit(settings.AUTOMATIC_RELEASE_COMMIT_MSG, cwd)
    if ret['returncode'] != 0:
        raise exceptions.CommitAndPushReleaseUpdateError(f"git commit error: {ret['msg']}", _logger)
    release_tag_ret = pygittools.set_tag(cwd, new_release_tag, new_release_msg)
    if release_tag_ret['returncode'] != 0:
        _clean_failed_release(new_release_tag, cwd)
        raise exceptions.ReleaseTagSetError(f"Error while setting release tag: {release_tag_ret['msg']}", _logger)
    
    if push and pygittools.is_origin_set(cwd):
        ret = pygittools.push_with_tags(cwd)
        if ret['returncode'] != 0:
            _clean_failed_release(new_release_tag, cwd)
            raise exceptions.CommitAndPushReleaseUpdateError(f"git push error: {ret['msg']}", _logger)
    
        _logger.info('New release data commited with tag set up and pushed properly.')
    else:
        _logger.info('New release data commited with tag set up properly.')
    
    return paths


def _clean_failed_release(new_release_tag, cwd):
    _logger.warning('Revert release process.')
    
    ret = pygittools.revert(1, cwd)
    if ret['returncode'] != 0:
        raise exceptions.CriticalError('Critical Error occured when reverting an automatic last commit. '
                                       'Please check git log, repo tree and cleanup the mess.', _logger)
    
    latest_tag_remove_error = False
    ret = pygittools.list_tags(cwd)
    if ret['returncode'] != 0:
        latest_tag_remove_error = True
    else:
        tags = ret['msg']
        if new_release_tag in tags:
            ret = pygittools.delete_tag(new_release_tag, cwd)
            if ret['returncode'] != 0:
                latest_tag_remove_error = True
        
    if latest_tag_remove_error:
        raise exceptions.CriticalError('Critical Error occured when deleting an automatic latest tag. '
                                       'Please check git log, repo tree and cleanup the mess.', _logger)


def _prompt_release_tag(cwd=''):
    latest_release_tag_ret = pygittools.get_latest_tag(cwd)
    
    if latest_release_tag_ret['returncode'] != 0:
        _logger.tip(f'Repo has not been tagged yet. '
                    f'Proposed initial release tag: {settings.SUGGESTED_INITIAL_RELEASE_TAG}')
        is_tagged = False
    else:
        latest_release_tag = latest_release_tag_ret['msg']
        _logger.info(f'Last release tag: {latest_release_tag}')
        is_tagged = True
    
    is_release_tag_valid = False
    comparing_release_tags = True
    while not is_release_tag_valid:
        new_release_tag = input(f'Enter new release tag - <Major Version>.<Minor Version>.<Patch version> '
                                f'e.g. {settings.EXAMPLE_RELEASE_TAG}: ')
        if _is_release_tag_valid(new_release_tag):
            if is_tagged:
                if not _is_release_tag_valid(latest_release_tag):
                    _logger.error('Latest release tag not valid!')
                    if wizard.is_checkpoint_ok(__name__, 
                                               'Continue without comparing the '
                                               'new relese tag with the latest?'):
                        comparing_release_tags = False
                    else:
                        raise exceptions.ReleaseTagError('Latest release tag not valid! '
                                                         'Please remove it to continue.', _logger)
                        
                if comparing_release_tags:
                    if _is_higher_tag(latest_release_tag, new_release_tag):
                        is_release_tag_valid = True
                    else:
                        _logger.error('Entered release tag less than the previous release tag! '
                                      'Correct and enter a new one.')
                else:
                    return new_release_tag
            else:
                return new_release_tag
        else:
            _logger.error('Entered release tag not valid! Correct and enter new one.')
    
    return new_release_tag


def _is_release_tag_valid(release_tag):
    try:
        normalized_version = pkg_version.Version(release_tag)
        if str(normalized_version) == release_tag:
            return True
        else:
            _logger.error(f'Entered release tag not valid! Proposed release tag: {normalized_version}. '
                          f'Correct and enter new one.')
            return False
    except pkg_version.InvalidVersion:
        return False
    
    
def _is_higher_tag(latest_tag, new_tag):
    latest_tag_obj = pkg_version.Version(latest_tag)
    new_tag_obj = pkg_version.Version(new_tag)
    
    return new_tag_obj > latest_tag_obj


def _prompt_release_msg():
    _logger.info("Enter release message. Type '~' and press Enter key to comfirm. Markdown syntax allowed.")
    message = []
    while True:
        line = input()
        if line and line.strip()[-1] == '~':
            message.append(line.rstrip()[:-1])
            break
        message.append(line)
        
    message = '\n'.join(message)
    
    if not message:
        raise exceptions.ValueError('Tag msg cannot be empty', _logger)
    
    return message


def _update_authors(config, cwd='.'):
    if config.authors_type == settings.AuthorsType.GENERATED.value:
        authors_filepath = _generate_file_pbr(settings.FileName.AUTHORS, git.generate_authors, cwd)
    else:
        authors_filepath = _generate_prepared_file(config, settings.FileName.AUTHORS, 
                                                   settings.FileName.AUTHORS_PREPARED, cwd)
        
    return authors_filepath
    

def _generate_prepared_file(config, filename, template_name, cwd='.'):
    file_path = Path(cwd).resolve() / filename
    if not file_path.exists(): 
        _logger.info(f'Generating {filename} file...')
        prepare.write_file_from_template(Path(settings.DirName.TEMPLATES) / template_name, 
                                         file_path, config.__dict__, cwd, verbose=False)
        _logger.info(f'{filename} file generated')    
    
    return file_path

    
def _generate_file_pbr(filename, gen_handler, cwd='.'):
    is_error = False
    _logger.info(f'Generating {filename} file...')
    
    file_path = Path(cwd) / filename
    git_dir = Path(cwd) / settings.DirName.GIT
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
        raise exceptions.FileGenerationError(f'{filename} file generation error!', _logger)
    
    _logger.info(f'The {filename} file generated')
    
    return file_path.resolve()
