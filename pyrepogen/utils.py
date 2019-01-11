#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import configparser
import datetime
import logging
from pathlib import Path
from collections import namedtuple

from . import pygittools
from . import settings
from . import exceptions
from . import __version__


_logger = logging.getLogger(__name__)


def execute_cmd(args, cwd='.'):
    try:
        process = subprocess.run(args,
                                 check=True,
                                 cwd=str(cwd),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 encoding="utf-8")
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
                                 encoding="utf-8")
        return process.stdout.split('\n')
    except subprocess.CalledProcessError as e:
        raise exceptions.ExecuteCmdError(e.returncode, msg=e.output, logger=_logger)


def get_git_repo_tree(cwd='.'):
    return [Path(cwd).resolve() / path for path in pygittools.list_git_repo_tree(str(cwd))['msg']]


def read_config_file(path):
    def is_list_option(option):
        if option and '"' not in option[0]:
            return True if '\n' in option[0] else False

    config_dict = {}
    filepath = Path(path)

    config = configparser.ConfigParser()
    if not config.read(filepath, 'utf-8'):
        raise exceptions.FileNotFoundError("{} file not found!".format(filepath.name), _logger)

    for section in config.sections():
        config_dict[section] = {}

        for option in config.options(section):
            option_val = config.get(section, option)
            if is_list_option(option_val):
                config_dict[section][option] = list(filter(None, option_val.split('\n')))
            else:
                config_dict[section][option] = option_val


    return config_dict


def read_repo_config_file(path):
    raw_config = read_config_file(path)
    config = {}
    
    for key, value in raw_config[settings.REPO_CONFIG_SECTION_NAME].items():
        try:
            boolean = str2bool(value)
            config[key.replace('-', '_')] = boolean
        except exceptions.ValueError:
            config[key.replace('-', '_')] = value
            
    add_auto_config_fields(config)

    validate_repo_config(config)
    
    return config


def get_repo_config_from_setup_cfg(path):
    raw_config = read_config_file(path)
    config = {}
    
    for key in raw_config[settings.METADATA_CONFIG_SECTION_NAME]:
        if key == 'name':
            config['project_name'] = raw_config[settings.METADATA_CONFIG_SECTION_NAME][key]
        elif key == 'summary':
            config['short_description'] = raw_config[settings.METADATA_CONFIG_SECTION_NAME][key]
        else:
            config[key.replace('-', '_')] = raw_config[settings.METADATA_CONFIG_SECTION_NAME][key]
           
    for key, value in raw_config[settings.GENERATOR_CONFIG_SECTION_NAME].items():
        config[key.replace('-', '_')] = value
            
    add_auto_config_fields(config)

    validate_config(config)
    
    return config


def add_auto_config_fields(config):
    config['year'] = str(datetime.datetime.now().year)
    config[settings.REPOASSIST_VERSION] = __version__
    config['min_python'] = "{}.{}".format(settings.MIN_PYTHON[0], settings.MIN_PYTHON[1])
    config['description_file'] = settings.FileName.README
    config['tests_dirname'] = settings.DirName.TESTS
    config['tests_path'] = settings.TESTS_PATH
    config['metadata_section'] = settings.METADATA_CONFIG_SECTION_NAME
    config['generator_section'] = settings.GENERATOR_CONFIG_SECTION_NAME
    config['license'] = settings.LICENSE
    config['repoassist_name'] = settings.DirName.REPOASSIST


def validate_config(config):
    _validate_metadata(config, settings.REPO_CONFIG_MANDATORY_FIELDS)
        
        
def validate_repo_config(config):
    _validate_metadata(config, settings.EXTENDED_REPO_CONFIG_MANDATORY_FIELDS)

        
def _validate_metadata(config, validator):
    for field in validator:
        if field not in config:
            raise exceptions.ConfigError("The {} field not found in the config!".format(field), _logger)
        else:
            if config[field] == "":
                raise exceptions.ConfigError("The {} field is empty in the config!".format(field), _logger)
            else:
                if field == 'project_type':
                    valid_values = [item.value for item in settings.ProjectType]
                    if config[field] not in valid_values:
                        raise exceptions.ConfigError("The {} field has invalid value in the config!".format(field), _logger)
                elif field == 'changelog_type':
                    valid_values = [item.value for item in settings.ChangelogType]
                    if config[field] not in valid_values:
                        raise exceptions.ConfigError("The {} field has invalid value in the config!".format(field), _logger)
                elif (field == 'is_cloud') or (field == 'is_sample_layout'):
                    valid_values = [True, False]
                    if config[field] not in valid_values:
                        raise exceptions.ConfigError("The {} field has invalid value in the config!".format(field), _logger)                    
                    

def str2bool(string):
    if string.lower() in ['yes', 'true', 't', 'y', '1']:
        return True
    elif string.lower() in ['no', 'false', 'f', 'n', '0']:
        return False
    else:
        raise exceptions.ValueError("No boolean", _logger)


def get_module_name_with_suffix(module_name):
    return "{}.py".format(module_name)


def get_project_module_path(config, cwd='.'):
    path = Path(cwd) / '{}.py'.format(config.project_name)
    
    if not path.exists():
        raise exceptions.FileNotFoundError("File {} not found. Please check repository and a project_name field in {} file".format(
            path.relative_to(cwd.resolve()), settings.FileName.SETUP_CFG), _logger)
    
    return path


def get_dir_from_arg(prompt_dir):
    return (Path().cwd() / prompt_dir).resolve()


def get_latest_file(path):
    if path:
        path = Path(path)
        if path.exists() and path.is_dir():
            files_list = []
            FileTime = namedtuple('FileTime', ['path', 'mtime'])
            for item in path.iterdir():
                if item.is_file():
                    files_list.append(FileTime(item, Path(item).stat().st_mtime))
                    
            if files_list:
                return max(files_list, key=lambda x: x.mtime).path
            
    return None
