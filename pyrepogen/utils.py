#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import configparser
import datetime
import logging
from pathlib import Path

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
    
    for key in raw_config[settings.REPO_CONFIG_SECTION_NAME]:
        config[key.replace('-', '_')] = raw_config[settings.REPO_CONFIG_SECTION_NAME][key]
        
    add_auto_config_fields(config)

    validate_config_metadata(config)
    
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
           
    for key in raw_config[settings.GENERATOR_CONFIG_SECTION_NAME]:
        config[key.replace('-', '_')] = raw_config[settings.GENERATOR_CONFIG_SECTION_NAME][key] 
            
    add_auto_config_fields(config)

    validate_config_metadata(config)
    
    return config


def add_auto_config_fields(config):
    config['year'] = str(datetime.datetime.now().year)
    config[settings.REPOASSIST_VERSION] = __version__
    config['min_python'] = settings.MIN_PYTHON
    config['description_file'] = settings.README_FILENAME
    config['tests_dirname'] = settings.TESTS_DIRNAME
    config['tests_path'] = settings.TESTS_PATH
    config['metadata_section'] = settings.METADATA_CONFIG_SECTION_NAME
    config['generator_section'] = settings.GENERATOR_CONFIG_SECTION_NAME
    config['license'] = settings.LICENSE


def validate_config_metadata(config):
    _validate_metadata(config, settings.REPO_CONFIG_MANDATORY_FIELDS)
        
        
def validate_repo_config_metadata(config):
    _validate_metadata(config, settings.EXTENDED_REPO_CONFIG_MANDATORY_FIELDS)

        
def _validate_metadata(config, validator):
    for field in validator:
        if field not in config:
            raise exceptions.ConfigError("The {} field not found in the config!".format(field), _logger)
        else:
            if not config[field]:
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
                    valid_values = ['true', 'false']
                    if config[field].lower() not in valid_values:
                        raise exceptions.ConfigError("The {} field has invalid value in the config!".format(field), _logger)                    
                    

def str2bool(string):
    return string.lower() in ['yes', 'true', 't', '1']


def get_module_name_with_suffix(module_name):
    return "{}.py".format(module_name)


def get_dir_from_arg(prompt_dir):
    return (Path().cwd() / prompt_dir).resolve()

