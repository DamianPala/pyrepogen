#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import semver
import jinja2
import shutil
import datetime
import platform
import tempfile
import subprocess
from enum import Enum
from pathlib import Path
from packaging import version as pkg_version

try:
    import pygittools
except ImportError:
    try:
        from . import pygittools
    except ImportError:        
        from reltools_helpers import pygittools

try:
    from . import wizard
    from . import logger
except ImportError:
    from reltools_helpers import wizard
    from reltools_helpers import logger
    

__author__ = 'Damian Pala'
__version__ = '0.0.1'

_logger = logger.get_logger(__name__)

_TIP_MSG_MARK = '# [TIP]: '
_SUGGESTED_INITIAL_RELEASE_TAG_PYTHON = '0.1.0'
_EXAMPLE_RELEASE_TAG_PYTHON = '<Major Version>.<Minor Version>.<Patch version> e.g. 1.17.3rc2'
_SUGGESTED_INITIAL_RELEASE_TAG_C = '0.1.0'
_EXAMPLE_RELEASE_TAG_C = '1.17.3-alpha.2'
_SUGGESTED_INITIAL_RELEASE_TAG_HW = '0.1'
_EXAMPLE_RELEASE_TAG_HW = '<Major Version>.<Minor Version> e.g. 1.17-alpha.2'
_AUTOMATIC_RELEASE_COMMIT_MSG = 'Automatic update of release data files.'


class RelToolsError(Exception):
    def __init__(self, msg, logger):
        super().__init__(msg)
        self.logger = logger


class WorkTreeNotFoundError(RelToolsError):
    pass


class NoCommitFoundError(RelToolsError):
    pass


class UncommitedChangesError(RelToolsError):
    pass


class RuntimeError(RelToolsError):
    pass


class ValueError(RelToolsError):
    pass


class ReleaseTagError(RelToolsError):
    pass


class CommitAndPushReleaseUpdateError(RelToolsError):
    pass


class ReleaseTagSetError(RelToolsError):
    pass


class ReleaseTagGetError(RelToolsError):
    pass


class FileNotFoundError(RelToolsError):
    pass


class CriticalError(RelToolsError):
    pass


class ChangelogGenerationError(RelToolsError):
    pass


class FileGenerationError(RelToolsError):
    pass


class TagType(Enum):
    PYTHON = 'python'
    C = 'c'
    HW = 'hw'


class ChangelogType(Enum):
    GENERATED = 'generated'
    PREPARED = 'prepared'


class AuthorsType(Enum):
    GENERATED = 'generated'
    PREPARED = 'prepared'


def check_repo_tree(cwd):
    if not pygittools.is_work_tree(cwd):
        raise WorkTreeNotFoundError("Git Work Tree not found! Please check "
                                               "if the git repository is initialized.", _logger)

    if not pygittools.is_any_commit(cwd):
        raise NoCommitFoundError("There are no commits in repository. "
                                            "Please commit before release.", _logger)


def check_if_changes_to_commit(cwd):
    try:
        if pygittools.are_uncommited_changes(cwd):
            raise UncommitedChangesError("There are changes to commit!", _logger)
    except pygittools.PygittoolsError:
        raise UncommitedChangesError("Error occured when checking if there are any changes to commit!", _logger)


def prompt_release_tag(tag_type, cwd='.'):
    if tag_type == TagType.PYTHON:
        suggested_initial_release_tag = _SUGGESTED_INITIAL_RELEASE_TAG_PYTHON
        example_release_tag = _EXAMPLE_RELEASE_TAG_PYTHON
        is_release_tag_valid = _is_release_tag_valid_python
        is_higher_tag = _is_higher_tag_python
    elif tag_type == TagType.C:
        suggested_initial_release_tag = _SUGGESTED_INITIAL_RELEASE_TAG_C
        example_release_tag = _EXAMPLE_RELEASE_TAG_C
        is_release_tag_valid = _is_release_tag_valid_c
        is_higher_tag = _is_higher_tag_c
    elif tag_type == TagType.HW:
        suggested_initial_release_tag = _SUGGESTED_INITIAL_RELEASE_TAG_HW
        example_release_tag = _EXAMPLE_RELEASE_TAG_HW
        is_release_tag_valid = _is_release_tag_valid_hw
        is_higher_tag = _is_higher_tag_hw
    else:
        raise ValueError('Invalid tag_type', _logger)
    
    latest_release_tag = _get_latest_tag(suggested_initial_release_tag, cwd)

    is_tag_valid = False
    comparing_release_tags = True
    while not is_tag_valid:
        new_release_tag = input(f'Enter new release tag - {example_release_tag}: ')
        if is_release_tag_valid(new_release_tag):
            if latest_release_tag:
                if not is_release_tag_valid(latest_release_tag):
                    _logger.error('Latest release tag not valid!')
                    if wizard.is_checkpoint_ok(__name__, 
                                               'Continue without comparing the '
                                               'new relese tag with the latest?'):
                        comparing_release_tags = False
                    else:
                        raise ReleaseTagError('Latest release tag not valid! '
                                                         'Please remove it to continue.', _logger)
                        
                if comparing_release_tags:
                    if is_higher_tag(latest_release_tag, new_release_tag):
                        is_tag_valid = True
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


def prompt_release_msg(cwd='.'):
    tip_msg = f"""{_TIP_MSG_MARK}Below are commit messages generated from the last tag.
{_TIP_MSG_MARK}If the last tag not exists, messages are from the first commit.
{_TIP_MSG_MARK}Use these messages to prepare a relevant release message.
{_TIP_MSG_MARK}All lines with the '{_TIP_MSG_MARK}' will be automatically removed.
{_TIP_MSG_MARK}You can leave these lines or remove them manually.

"""

    try:
        current_log = pygittools.get_commit_msgs_from_last_tag(cwd)
    except pygittools.PygittoolsError:
        info_msg = tip_msg
    else:
        info_msg = tip_msg + current_log
     
    try:
        message = _input_with_editor(info_msg)
    except RuntimeError as e:
        _logger.error(e)
        _logger.info('Input your release message in command line instead.')
        message = _prompt_release_msg_cli()
        
    message = '\n'.join([line for line in message.splitlines() if not line.startswith(_TIP_MSG_MARK)])
     
    return message.strip()


def _prompt_release_msg_cli():
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
        raise ValueError('Tag msg cannot be empty', _logger)
    
    return message


def _input_with_editor(msg=''):
    platform_name = platform.system()
    if platform_name == 'Windows':
        cmd = 'start'
        options = ['/WAIT']
    elif platform_name == 'Linux':
        cmd = 'xdg-open'
        options = []
    elif platform_name == 'Darwin':
        cmd = 'open' 
        options = []
    else:
        cmd = 'open'
        options = []
        
    fd, filepath = tempfile.mkstemp(prefix='Release_Message_Tempfile_', suffix='.txt', text=True)
    filepath = Path(filepath)
    
    with open(fd, 'wt', encoding='utf-8') as file:
        file.write(msg)
    
    cmd_list = [cmd] + options + [filepath.name]
        
    try:
        subprocess.run(cmd_list, 
                       cwd=filepath.parent, 
                       shell=True, 
                       check=True, 
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, 
                       encoding='utf-8')
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'Editor opening error occured: {e.output}', _logger)
    else:
        return filepath.read_text(encoding='utf-8')
    finally:
        filepath.unlink()


def _is_release_tag_valid_python(release_tag):
    try:
        normalized_version = pkg_version.Version(release_tag)
    except pkg_version.InvalidVersion:
        return False
    else:
        if str(normalized_version) == release_tag:
            return True
        else:
            _logger.error(f'Entered release tag not valid! Proposed release tag: {normalized_version}. '
                          f'Correct and enter new one.')
            return False


def _is_release_tag_valid_c(release_tag):
    try:
        semver.parse(release_tag)
    except Exception:
        return False
    else:
        return True


def _is_release_tag_valid_hw(release_tag):
    try:
        release_tag_sem = _convert_tag_to_semantic_tag(release_tag)
    except ReleaseTagError:
        return False
    else:
        return _is_release_tag_valid_c(release_tag_sem)


def _is_higher_tag_python(latest_tag, new_tag):
    latest_tag_obj = pkg_version.Version(latest_tag)
    new_tag_obj = pkg_version.Version(new_tag)

    return new_tag_obj > latest_tag_obj


def _is_higher_tag_c(latest_tag, new_tag):
    latest_tag_obj = semver.VersionInfo.parse(latest_tag)
    new_tag_obj = semver.VersionInfo.parse(new_tag)

    return new_tag_obj > latest_tag_obj


def _is_higher_tag_hw(latest_tag, new_tag):
    latest_tag_sem = _convert_tag_to_semantic_tag(latest_tag)
    new_tag_sem = _convert_tag_to_semantic_tag(new_tag)

    return _is_higher_tag_c(latest_tag_sem, new_tag_sem)


def _convert_tag_to_semantic_tag(tag):
    m = re.match(r'[0-9]+\.[0-9]+\.[0-9]+', tag)
    if m:
        return tag
    else:
        m = re.match(r'([0-9]+\.[0-9]+)((.)*)', tag)
        if m:
            tag = '{}.0{}'.format(m.group(1), m.group(2))
            return tag
        else:
            raise ReleaseTagError("Release tag is not valid", _logger)


def _get_latest_tag(suggested_initial_release_tag, cwd):
    try:
        latest_release_tag = pygittools.get_latest_tag(cwd)
    except pygittools.PygittoolsError:
        _logger.tip(f'Repo has not been tagged yet. '
                    f'Proposed initial release tag: {suggested_initial_release_tag}')
        latest_release_tag = None
    else:
        _logger.info(f'Last release tag: {latest_release_tag}')

    return latest_release_tag


def commit_and_push_release_update(new_release_tag, new_release_msg, ssh_key=None, 
                                   files_to_add=None, push=True, cwd='.', debug=None):
    if push:
        _logger.info('Commit updated release files, set tag and push...')
    else:
        _logger.info('Commit updated release files, set tag...')
    
    paths = []
    for file_path in files_to_add:
        try:
            pygittools.add(file_path, cwd)
        except pygittools.PygittoolsError as e:
            raise CommitAndPushReleaseUpdateError(f'{file_path.name} git add error: {e}', _logger)
        paths.append(file_path)
    
    try:
        pygittools.commit(_AUTOMATIC_RELEASE_COMMIT_MSG, cwd)
    except pygittools.PygittoolsError as e:
        raise CommitAndPushReleaseUpdateError(f"git commit error: {e}", _logger)
    _logger.info('New commit with updated release files was created.')
    
    try:
        pygittools.set_tag(new_release_tag, new_release_msg, cwd)
        if debug:
            raise pygittools.PygittoolsError('Error for debug', returncode=1)
    except pygittools.PygittoolsError as e:
        _clean_failed_release(new_release_tag, cwd)
        raise ReleaseTagSetError(f"Error while setting release tag: {e}", _logger)
    
    try:
        new_latest_tag = pygittools.get_latest_tag(cwd)
    except pygittools.PygittoolsError as e:
        _clean_failed_release(new_release_tag, cwd)
        raise ReleaseTagSetError(f"Error while check if the new release tag was set properly: {e}", _logger)
    else:
        if new_latest_tag != new_release_tag:
            _clean_failed_release(new_release_tag, cwd)
            raise ReleaseTagSetError('New release tag was set incorrectly.', _logger)
    
    _logger.info('New tag established.')
    
    if push and pygittools.is_origin_set(cwd):
        if ssh_key and not ssh_key.exists():
            _logger.error(f'SSH key file not found. Please check {ssh_key.name} file.')
            wizard.get_data(__name__, 'Please push with tags later manually and press Enter to continue')
        else:
            try:
                pygittools.push_with_tags(ssh_key=ssh_key, cwd=cwd)
            except pygittools.PygittoolsError as e:
                _logger.error(f'git push error: {e}')
                ssh_key = Path(wizard.get_data(__name__, 'Enter a path to the SSH key or leave empty to continue '
                                               'and push with tags later manually'))
                if ssh_key:
                    if not ssh_key.exists():
                        _logger.error(f'SSH key file not found. Please check {ssh_key.name} file.')
                        wizard.get_data(__name__, 'Please push with tags later manually '
                                        'and press Enter to continue')
                    else:
                        try:
                            pygittools.push_with_tags(ssh_key=ssh_key, cwd=cwd)
                        except pygittools.PygittoolsError as e:
                            _logger.error(f'git push error: {e}')
                            wizard.get_data(__name__, 'Please push with tags later manually '
                                            'and press Enter to continue')
                            _logger.info('New release data commited with tag set properly.')
                        else:
                            _logger.info('New release data commited with tag set and pushed properly.')
                else:
                    _logger.info('New release data commited with tag set properly.')
            else:
                _logger.info('New release data commited with tag set and pushed properly.')
    else:
        _logger.info('New release data commited with tag set properly.')
    
    return paths


def _clean_failed_release(new_release_tag, cwd):
    _logger.warning('Revert release process.')
    
    try:
        pygittools.revert(1, cwd)
    except pygittools.PygittoolsError:
        raise CriticalError('Critical Error occured when reverting an automatic last commit. '
                            'Please check git log, repo tree and cleanup the mess.', _logger)
    
    latest_tag_remove_error = False
    try:
        tags = pygittools.list_tags(cwd)
    except pygittools.PygittoolsError:
        latest_tag_remove_error = True
    else:
        if new_release_tag in tags:
            try:
                pygittools.delete_tag(new_release_tag, cwd)
            except pygittools.PygittoolsError:
                latest_tag_remove_error = True
        
    if latest_tag_remove_error:
        raise CriticalError('Critical Error occured when deleting an automatic latest tag. '
                            'Please check git log, repo tree and cleanup the mess.', _logger)


def get_latest_tag_on_regenerate(cwd):
    try:
        return pygittools.get_latest_tag(cwd)
    except pygittools.PygittoolsError as e:
        raise ReleaseTagGetError(f'Retrieving release tag error: {e}'
                                 f'Repository must be tagged before regenerate.', _logger)


def update_changelog(changelog_type, changelog_filename, 
                     keywords, new_release_tag, new_release_msg, 
                     changelog_generated_template_path=None, 
                     changelog_prepared_template_path=None, 
                     cwd='.'):
    if changelog_type == ChangelogType.PREPARED:
        if changelog_prepared_template_path is None:
            raise ValueError('changelog_prepared_template_path cannot be None', _logger);
        path = _generate_prepared_file(changelog_filename, changelog_prepared_template_path, keywords, cwd=cwd)
    elif changelog_type == ChangelogType.GENERATED:
        if changelog_generated_template_path is None:
            raise ValueError('changelog_generated_template_path cannot be None', _logger);
        path = _update_generated_changelog(changelog_filename, changelog_generated_template_path, 
                                           keywords, new_release_tag, new_release_msg, cwd=cwd)

    return path


def _update_generated_changelog(changelog_filename, changelog_generated_template_path, 
                                keywords, new_release_tag, new_release_msg, cwd='.'):
    _logger.info(f'Updating {changelog_filename} file...')
    
    changelog_path = Path(cwd).resolve() / changelog_filename
    try:
        changelog_content = pygittools.get_changelog(
            report_format='### Version: %(tag) | Released: %(taggerdate:short) \r\n%(contents)', cwd=cwd)
    except pygittools.PygittoolsError as e:
        raise ChangelogGenerationError(f'{changelog_filename} generation error: {e}', _logger)
    
    if changelog_path.exists():
        log_msg = f'{changelog_filename} file updated.'
        changelog_path.unlink()
    else:
        log_msg = f'{changelog_filename} file generated.'
    write_file_from_template(changelog_generated_template_path, changelog_path, keywords)
    with open(changelog_path, 'a') as file:
        file.write('\n')
        file.write(_get_changelog_entry(new_release_tag, new_release_msg))
        file.write(changelog_content)
    
    _logger.info(log_msg)    
    
    return changelog_path


def _get_changelog_entry(release_tag, release_msg):
    tagger_date = datetime.date.today().strftime('%Y-%m-%d')
    return f'### Version: {release_tag} | Released: {tagger_date} \n{release_msg}\n\n'


def write_file_from_template(src, dst, keywords):
    templateLoader = jinja2.FileSystemLoader(searchpath=str(src.parent))
    templateEnv = jinja2.Environment(loader=templateLoader,
                                     trim_blocks=True,
                                     lstrip_blocks=True,
                                     newline_sequence='\r\n',
                                     keep_trailing_newline=True)
    template = templateEnv.get_template(src.name)
    template.stream(keywords).dump(str(dst))

    return dst


def _generate_prepared_file(filename, template_path, keywords, cwd='.'):
    file_path = Path(cwd).resolve() / filename
    if not file_path.exists(): 
        _logger.info(f'Generating {filename} file...')
        write_file_from_template(template_path, file_path, keywords)
        _logger.info(f'{filename} file generated.')    
    
    return file_path


def update_authors(authors_type, authors_filename, keywords, 
                   authors_generated_template_path=None,
                   authors_prepared_template_path=None, 
                   cwd='.'):
    if authors_type == AuthorsType.PREPARED:
        if authors_prepared_template_path is None:
            raise ValueError('authors_prepared_template_path cannot be None', _logger);
        path = _generate_prepared_file(authors_filename, authors_prepared_template_path, keywords, cwd=cwd)
    elif authors_type == AuthorsType.GENERATED:
        if authors_generated_template_path is None:
            raise ValueError('authors_generated_template_path cannot be None', _logger);
        path = _update_generated_authors(authors_filename, authors_generated_template_path, keywords, cwd=cwd)

    return path


def _update_generated_authors(authors_filename, authors_generated_template_path, keywords, cwd='.'):
    _logger.info(f'Updating {authors_filename} file...')
    
    authors_path = Path(cwd).resolve() / authors_filename
    try:
        authors_content = '\n'.join(pygittools.get_authors(cwd=cwd))
    except pygittools.NoAuthorsError:
        authors_content = ''
    except pygittools.PygittoolsError as e:
        raise ChangelogGenerationError(f'{authors_filename} generation error: {e}', _logger)
    
    if authors_path.exists():
        log_msg = f'{authors_filename} file updated.'
        authors_path.unlink()
    else:
        log_msg = f'{authors_filename} file generated.'
    write_file_from_template(authors_generated_template_path, authors_path, keywords)
    with open(authors_path, 'a') as file:
        file.write('\n')
        file.write(authors_content)
    
    _logger.info(log_msg)    
    
    return authors_path


def prepare_archive(archive_name, dst_dir, files, files_root='.', add_extra_files=None, extension='zip', cwd='.'):
    archive_path = Path(cwd).resolve() / dst_dir / (archive_name + f'.{extension}')
    temp_dir = archive_path.parent / archive_name
    
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    if archive_path.exists():
        archive_path.unlink()
    
    Path(dst_dir).mkdir(parents=True, exist_ok=True)
    
    copy_list = _prepare_copy_list(files)
    for path in copy_list:
        dst = temp_dir / path.relative_to(files_root)
        if path.is_dir():
            if not dst.exists():
                shutil.copytree(path, dst)
        else:
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(path, dst)
    
    if add_extra_files:
        add_extra_files(temp_dir)
    
    zip_archive_name = shutil.make_archive(temp_dir, extension, temp_dir)
    shutil.rmtree(temp_dir)
    
    assert archive_path.name == Path(zip_archive_name).name
            
    return archive_path


def _prepare_copy_list(paths):
    copy_list = []
    dirs = _list_dirs(paths)
    for directory in dirs:
        if not _is_path_in_dirs(directory, dirs):
            copy_list.append(directory)
    
    copy_list.extend(_list_files_not_in_dirs(paths))
    
    return copy_list
    

def _list_dirs(paths):
    dirs = [Path(path) for path in paths if Path(path).is_dir()]
    return dirs


def _list_files_not_in_dirs(paths):
    dirs = _list_dirs(paths)
    files_paths = [Path(path) for path in paths if not Path(path).is_dir() and not _is_path_in_dirs(Path(path), dirs)]
    return files_paths


def _is_path_in_dirs(path, dirs):
    for directory in dirs:
        try:
            rel = Path(path).relative_to(directory)
        except Exception:
            pass
        else:
            return False if rel.__str__() == '.' else True
    
    return False
