#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import shutil
import logging
import tempfile
import filecmp
import autopep8
import subprocess
from types import SimpleNamespace
from itertools import chain
from pathlib import Path
from enum import Enum


__author__ = 'Damian Pala'
__version__ = '0.0.1'


_logger = logging.getLogger(__name__)


class MeldFormatError(Exception):
    def __init__(self, msg, logger):
        super().__init__(msg)
        self.logger = logger


class NotAFileError(MeldFormatError):
    pass


class NotADirectoryError(MeldFormatError):
    pass


class FileNotFoundError(MeldFormatError):
    pass


class PathNotFoundError(MeldFormatError):
    pass


class FormatterNotSpecifiedError(MeldFormatError):
    pass


class ExecuteCmdError(MeldFormatError):
    pass


class MeldError(MeldFormatError):
    pass


class ClangFormatError(MeldFormatError):
    pass


class Autopep8Formatter():
    name = 'Autopep8'
    linter = SimpleNamespace(name='Flake8', cmd='flake8')
    sources_extensions = ['.py']

    def format_file(self, file_to_format_path, setup_path):
        if setup_path is None:
            options = None
        else:
            options = autopep8.parse_args(('--global-config='+setup_path.__str__(),
                                           file_to_format_path.__str__()), apply_config=True)
        temp_fd, temp_path = tempfile.mkstemp(prefix=f'{file_to_format_path.stem}_', 
                                              suffix=file_to_format_path.suffix, 
                                              text=True)
        with os.fdopen(temp_fd, 'w') as file:
            autopep8.fix_file(file_to_format_path.__str__(), output=file, options=options)
            
        return Path(temp_path)
    
    def lint_file(self, file_to_lint_path, setup_path):
        _logger.info(f'Lint {file_to_lint_path} file and show report.')
        _logger.info(f'=============== {file_to_lint_path.name} ===============')

        if not shutil.which(self.linter.cmd):
            raise MeldError(f'{self.linter.name} not found. Please install it and add to PATH', _logger)

        try:
            if setup_path is None:
                _execute_cmd((Autopep8Formatter.linter.cmd, 
                              file_to_lint_path.__str__()))
            else:
                _execute_cmd((Autopep8Formatter.linter.cmd, 
                              file_to_lint_path.__str__(), 
                              f'--config={setup_path}'))
        except ExecuteCmdError as e:
            return e.__str__()
        else:
            _logger.info('File is OK!')


class ClangFormatter():
    name = 'ClangFormat'
    sources_extensions = ['.c', '.h', '.cpp', '.cxx', '.hpp', '.hxx']
    
    def format_file(self, file_to_format_path, setup_path):
        temp_file_path = Path(tempfile.mktemp(prefix=f'{file_to_format_path.stem}_', 
                                              suffix=file_to_format_path.suffix))
        shutil.copy(file_to_format_path, temp_file_path)
        if setup_path is not None:
            temp_setup_path = temp_file_path.parent / setup_path.name
            shutil.copy(setup_path, temp_setup_path)
            
        try:
            _execute_cmd(('clang-format', '-i', temp_file_path.__str__()))
        except ExecuteCmdError as e:
            raise ClangFormatError(f'Error occured when run {self.name}: {e}', _logger)
        finally:
            if setup_path is not None:
                temp_setup_path.unlink()

        return Path(temp_file_path)
    

class Formatter(Enum):
    AUTOPEP8 = Autopep8Formatter
    CLANGFORMAT = ClangFormatter


class PathType(Enum):
    FILE = 'file'
    DIRECTORY = 'directory'


def format_file(formatter, path, setup_path=None, with_meld=True, get_logger=None):
    if get_logger:
        global _logger
        _logger = get_logger(__name__)
    formatter = _get_formatter(formatter)
    _print_greeting(formatter, path, PathType.FILE, with_meld)
    
    path = _check_path(path, PathType.FILE)
    setup_path = _check_setup_file(setup_path)
    
    formatted_file_path = formatter.format_file(path, setup_path)

    if with_meld:
        if _is_line_endings_differences_or_no_changes(path, formatted_file_path):
            _logger.info(f'No changes in {path}.')
            final_formatted_file_path = None    
        else:
            _check_meld()
            _merge_changes(path, formatted_file_path)
            final_formatted_file_path = path
    else:
        if filecmp.cmp(path, formatted_file_path):
            _logger.info(f'No changes in {path}.')
            final_formatted_file_path = None    
        else:
            path.unlink()
            shutil.copy(formatted_file_path, path)
            final_formatted_file_path = path
    
    if hasattr(formatter, 'lint_file'):
        linter_output = formatter.lint_file(path, setup_path)
        if linter_output:
            print(linter_output)
            
    return final_formatted_file_path


def format_dir(formatter, path, setup_path=None, with_meld=True, get_logger=None):
    if get_logger:
        global _logger
        _logger = get_logger(__name__)
    formatter = _get_formatter(formatter)
    _print_greeting(formatter, path, PathType.DIRECTORY, with_meld)

    path = _check_path(path, PathType.DIRECTORY)
    setup_path = _check_setup_file(setup_path)
    
    files_to_format = _collect_files_to_format(formatter, path)
    formatted_files = [formatter.format_file(file, setup_path) for file in files_to_format]
    
    final_formatted_files = []
    if with_meld:
        _check_meld()
        for original_file_path, formatted_file_path in zip(files_to_format, formatted_files):
            if _is_line_endings_differences_or_no_changes(original_file_path, formatted_file_path):
                _logger.info(f'No changes in {original_file_path}.')
            else:
                _merge_changes(original_file_path, formatted_file_path)
                final_formatted_files.append(original_file_path)
    else:
        for original_file_path, formatted_file_path in zip(files_to_format, formatted_files):
            if filecmp.cmp(original_file_path, formatted_file_path):
                _logger.info(f'No changes in {original_file_path}.')
            else:
                original_file_path.unlink()
                shutil.copy(formatted_file_path, original_file_path)
                final_formatted_files.append(original_file_path)
    
    if hasattr(formatter, 'lint_file'):
        for file in files_to_format:
            linter_output = formatter.lint_file(file, setup_path)
            if linter_output:
                print(linter_output)
    
    return final_formatted_files if final_formatted_files.__len__() > 0 else None


def _get_formatter(formatter):
    if not isinstance(formatter, Formatter):
        raise FormatterNotSpecifiedError('Formatter is not specified properly. Use Formatter class', _logger)

    return formatter.value()


def _print_greeting(formatter, path, path_type, with_meld):
    if with_meld:
        _logger.info(f'Format the {path_type.value}: {path} using the {formatter.name} '
                     f'with merge mode in Meld.')
    else:
        _logger.info(f'Format the {path_type.value}: {path} using the {formatter.name}.')


def _check_path(path, path_type):
    path = _get_path(path)
    if not path.exists():
        raise PathNotFoundError(f'{path_type.value.title()} to format not exists!', _logger)
    
    incorrect_path_msg = f'{path_type.value.title()} to format path must point to a {path_type.value}!'
    if path_type == PathType.FILE:
        if not path.is_file():
            raise NotAFileError(incorrect_path_msg, _logger)
    if path_type == PathType.DIRECTORY:
        if not path.is_dir():
            raise NotADirectoryError(incorrect_path_msg, _logger)
    
    return path


def _get_path(path):
    return (Path().cwd() / str(path).strip('\"')).resolve()
    

def _check_setup_file(path):
    if path is not None:
        setup_path = _get_path(path)
        if not setup_path.exists():
            raise FileNotFoundError('Formatter setup file not exists!', _logger)
        if not setup_path.is_file():
            raise NotAFileError('Formatter setup path must point to a file!', _logger)
    else:
        setup_path = None

    return setup_path


def _collect_files_to_format(formatter, path):
    return list(filter(None, list(chain.from_iterable(sorted(path.rglob(f'*{extension}')) 
                                                      for extension in formatter.sources_extensions))))


def _check_meld():
    if not shutil.which('meld'):
        raise MeldError('Meld not found. Please install it and add to PATH', _logger)


def _is_line_endings_differences_or_no_changes(path1, path2):
    with open(path1, 'r') as file1, open(path2, 'r') as file2:
        file1_lines = [line.rstrip('\n') for line in file1]
        file2_lines = [line.rstrip('\n') for line in file2] 
    
    if file1_lines.__len__() != file2_lines.__len__():
        return False
    
    for line1, line2 in zip(file1_lines, file2_lines):
        if line1 != line2:
            return False

    return True


def _merge_changes(file_to_format_path, formatted_file_path):
    try:
        _execute_cmd(('meld', 
                      file_to_format_path.__str__(), 
                      file_to_format_path.__str__(), 
                      formatted_file_path.__str__(), 
                      '-o', file_to_format_path.__str__()))
    except ExecuteCmdError as e:
        raise MeldError(f'Error occured while run Meld: {e}', _logger)
    formatted_file_path.unlink()


def _execute_cmd(args):
    try:
        p = subprocess.run(args,
                           check=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           encoding='utf-8')
    except subprocess.CalledProcessError as e:
        raise ExecuteCmdError(e.output, _logger)
    else:
        return p.stdout
