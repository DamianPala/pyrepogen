#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import configparser
from pathlib import Path
from collections import namedtuple

from . import pygittools
from . import settings
from . import exceptions
from . import logger


_logger = logger.get_logger(__name__)


def execute_cmd(args, cwd='.'):
    try:
        process = subprocess.run(args,
                                 check=True,
                                 cwd=str(cwd),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 encoding='utf-8')
        return process.stdout
    except subprocess.CalledProcessError as e:
        raise exceptions.ExecuteCmdError(e.returncode, msg=e.output, logger=_logger)


def execute_cmd_and_split_lines_to_list(args, cwd='.'):
    try:
        process = subprocess.run(args,
                                 check=True,
                                 cwd=str(cwd),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 encoding='utf-8')
        return process.stdout.split('\n')
    except subprocess.CalledProcessError as e:
        raise exceptions.ExecuteCmdError(e.returncode, msg=e.output, logger=_logger)


def get_git_repo_tree(cwd='.'):
    return [Path(cwd).resolve() / path for path in pygittools.list_git_repo_tree(str(cwd))['msg']]


def read_repo_config_file(path):
    return _prepare_config(path, [settings.REPO_CONFIG_SECTION_NAME])


def get_repo_config_from_setup_cfg(path):
    return _prepare_config(path, [settings.METADATA_CONFIG_SECTION_NAME, settings.GENERATOR_CONFIG_SECTION_NAME])


def _prepare_config(path, sections):
    raw_config = _read_config_file(path)
    config_dict = {}

    for section in sections:
        for field, value in raw_config[section].items():
            config_dict.update(_parse_config_field(field, value))

    _remove_junk_fields(config_dict)

    try:
        config = settings.Config(**config_dict)
    except TypeError as e:
        raise exceptions.ConfigError(f'Invalid config file structure: {str(e)}', _logger)
    _validate_config(config)

    return config


def _read_config_file(path):
    def is_list_option(option):
        if option and '"' not in option[0]:
            return True if '\n' in option[0] else False

    config_dict = {}
    filepath = Path(path)

    config = configparser.ConfigParser()
    if not config.read(filepath, 'utf-8'):
        raise exceptions.FileNotFoundError(f'{filepath.name} file not found!', _logger)

    for section in config.sections():
        config_dict[section] = {}

        for option in config.options(section):
            option_val = config.get(section, option)
            if is_list_option(option_val):
                config_dict[section][option] = list(filter(None, option_val.split('\n')))
            else:
                config_dict[section][option] = option_val

    return config_dict


def _parse_config_field(field, value):
    if not isinstance(value, list):
        try:
            new_value = str2bool(value)
        except exceptions.ValueError:
            new_value = value
    else:
        new_value = value

    if field == 'name':
        new_field = 'project_name'
    elif field == 'summary':
        new_field = 'short_description'
    else:
        new_field = field.replace('-', '_')

    return {new_field: new_value}


def _remove_junk_fields(config_dict):
    fields_to_remove = [field for field in config_dict if field not in settings.Config.get_fields()]

    for field in fields_to_remove:
        _logger.warning(f'Detected unknown field: {field} in {settings.FileName.SETUP_CFG} file.')
        config_dict.pop(field)


def _validate_config(config, extra_fields=[]):
    for field in extra_fields:
        if getattr(config, field) is None:
            raise exceptions.ConfigError(f'The {field} field is empty in the config!', _logger)

    for field, value in config.__dict__.items():
        if field not in config.get_default_fields() and value == '':
            raise exceptions.ConfigError(f'The {field} field is empty in the config!', _logger)
        
        invalid_value_msg = f'The {field} field has invalid value: {value} in the config!'
        if field == 'project_type':
            valid_values = [item.value for item in settings.ProjectType]
            if value not in valid_values:
                raise exceptions.ConfigError(invalid_value_msg, _logger)
        elif field == 'changelog_type' or field == 'authors_type':
            if field == 'changelog_type':
                valid_values = [item.value for item in settings.ChangelogType]
            if field == 'authors_type':
                valid_values = [item.value for item in settings.AuthorsType]
            if value not in valid_values:
                raise exceptions.ConfigError(invalid_value_msg, _logger)
        elif extra_fields and ((field == 'is_cloud') or (field == 'is_sample_layout')):
            valid_values = [True, False]
            if value not in valid_values:
                raise exceptions.ConfigError(invalid_value_msg, _logger)


def str2bool(string):
    if string.lower() in ['yes', 'true', 't', 'y', '1']:
        return True
    elif string.lower() in ['no', 'false', 'f', 'n', '0']:
        return False
    else:
        raise exceptions.ValueError('No boolean', _logger)


def get_module_name_with_suffix(module_name):
    return f'{module_name}.py'


def get_project_module_path(config, cwd='.'):
    path = Path(cwd) / f'{config.project_name}.py'

    if not path.exists():
        raise exceptions.FileNotFoundError(f'File {path.relative_to(cwd.resolve())} not found. '
                                           f'Please check repository and a project_name field in '
                                           f'{settings.FileName.SETUP_CFG} file', _logger)

    return path


def get_dir_from_arg(prompt_dir):
    return (Path().cwd() / prompt_dir).resolve()


def get_latest_file(path):
    if path:
        path = Path(path)
        if path.exists() and path.is_dir():
            FileTime = namedtuple('FileTime', ['path', 'mtime'])
            files_list = [FileTime(item, Path(item).stat().st_mtime) for item in path.iterdir() if item.is_file()]

            if files_list:
                return max(files_list, key=lambda x: x.mtime).path

    return None


def get_latest_tarball(path):
    if path:
        path = Path(path)
        if path.exists() and path.is_dir():
            FileTime = namedtuple('FileTime', ['path', 'mtime'])
            files_list = [FileTime(item, Path(item).stat().st_mtime) for item in path.iterdir() \
                          if item.is_file() \
                          and (item.suffixes.__len__() >= 2) \
                          and (item.suffixes[-2] == settings.TARBALL_SUFFIX)]

            if files_list:
                return max(files_list, key=lambda x: x.mtime).path

    return None
