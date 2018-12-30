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
from .exceptions import (ExecuteCmdError)


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
        raise ExecuteCmdError(e.returncode, msg=e.output, logger=_logger)
    
    
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
        raise ExecuteCmdError(e.returncode, msg=e.output, logger=_logger)
    
    
def get_git_repo_tree(cwd='.'):
    return [Path(cwd).resolve() / path for path in pygittools.list_git_repo_tree(str(cwd))['msg']]


def read_setup_cfg(cwd='.'):
    def is_list_option(option):
        if option and '"' not in option[0]:
            return True if '\n' in option[0] else False
        
    filepath = Path(cwd) / settings.SETUP_CFG_FILENAME
        
    config_dict = {}
    
    config = configparser.ConfigParser()
    if not config.read(filepath, 'utf-8'):
        raise exceptions.FileNotFoundError("{} file not found!".format(filepath.name), logger=_logger)
    
    for section in config.sections():
        config_dict[section] = {}
        for option in config.options(section):
            option_val = config.get(section, option)
            config_dict[section][option] = option_val if not is_list_option(option_val) else list(filter(None, option_val.split('\n')))

    now = datetime.datetime.now()
    config_dict['metadata']['year'] = str(now.year)
    validate_config(config_dict['metadata'])

    return config_dict


def validate_config(config):
    for field in settings.CONFIG_MANDATORY_FIELDS:
        if field not in config:
            raise exceptions.ConfigError("The {} field not found in the config!".format(field), logger=_logger)
        