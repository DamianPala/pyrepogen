#!/usr/bin/env python
# -*- coding: utf-8 -*-


import shutil
import logging
import jinja2
from pathlib import Path

from . import settings
from . import exceptions
from pyrepogen import PARDIR


_logger = logging.getLogger(__name__)

def generate_standalone_repo(config, cwd='.', options=None):
    paths = []
    paths.extend(generate_standalone_repo_dirs(cwd))
    paths.extend(generate_standalone_repo_files(config, cwd, options))
    paths.extend(_prepare_repoasist(cwd, options))
    
    return paths


def generate_standalone_repo_dirs(cwd='.'):
    paths = []
    for dirname in settings.STANDALONE_REPO_DIRS_TO_GEN:
        try:
            Path(Path(cwd) / dirname).mkdir()
            _logger.info("{} directory generated.".format(dirname))
            paths.append(Path(cwd) / dirname)
        except FileExistsError:
            _logger.warning("{} directory exists, not overwritten.".format(dirname))
            
    return paths


def generate_standalone_repo_files(config, cwd='.', options=None):
    _validate_config(config)
    
    paths = []
    for filename in settings.STANDALONE_REPO_FILES_TO_GEN:
        if filename == settings.REQUIREMENTS_FILENAME:
            paths.extend(_prepare_requirements(Path(cwd) / filename, settings.REQUIREMENTS, cwd, options))
        elif filename == settings.REQUIREMENTS_DEV_FILENAME:
            paths.extend(_prepare_requirements(Path(cwd) / filename, settings.REQUIREMENTS_DEV, cwd, options))
        elif filename == settings.TOX_STANDALONE_FILENAME:
            write_file_from_template(settings.TOX_STANDALONE_FILENAME, Path(cwd) / settings.TOX_FILENAME, 
                                     {'tests_dirname': settings.TESTS_DIRNAME}, cwd, options)
        elif filename == settings.LICENSE_FILENAME:
            write_file_from_template(filename, Path(cwd) / filename, config, cwd, options)
        elif filename == settings.SETUP_CFG_FILENAME:
            write_file_from_template(settings.SETUP_CFG_STANDALONE_FILENAME, Path(cwd) / filename, config, cwd, options)
        elif filename == settings.GITIGNORE_FILENAME:
            paths.extend(_copy_template_file(filename, Path(cwd) / filename, cwd, options))
        elif filename == settings.STANDALONE_SAMPLE_FILENAME:
            paths.extend(_copy_template_file(filename, Path(cwd) / filename, cwd, options))
        elif filename == settings.STANDALONE_SAMPLE_TEST_FILENAME:
            paths.extend(_copy_template_file(filename, Path(cwd) / settings.TESTS_DIRNAME / filename, cwd, options))
        elif filename == settings.PYINIT_FILENAME:
            paths.extend(_copy_template_file(settings.SAMPLE_MODULE_FILENAME, Path(cwd) / settings.TESTS_DIRNAME / filename, cwd, options))
        elif filename == settings.MAKEFILE_FILENAME:
            paths.extend(_copy_template_file(settings.MAKEFILE_STANDALONE_FILENAME, Path(cwd) / filename, cwd, options))
        elif filename == settings.LICENSE_FILENAME:
            paths.extend(_copy_template_file(settings.LICENSE_FILENAME, Path(cwd) / filename, cwd, options))
        else:
            paths.extend(_generate_empty_file(Path(cwd) / filename, cwd, options))
            
    return paths

def _generate_empty_file(path, cwd, options=None):
    try:
        if options and options.force:
            with open(Path(path), 'w'):
                pass
        else:
            with open(Path(path), 'x'):
                pass
        
        _logger.info("{} file generated.".format(path.relative_to(cwd)))
        
        return [path]
    except FileExistsError:
        _logger.warning("{} file exists, not overwritten.".format(path.relative_to(cwd)))
        
        return []
        
        
def _copy_template_file(filename, dst, cwd, options=None):
    if (options and options.force) or (not Path(dst).exists()):
        shutil.copy(PARDIR / settings.TEMPLATES_DIRNAME / filename, dst)
        _logger.info("{} file generated.".format(Path(dst).relative_to(cwd)))
        
        return [dst]
    else:
        _logger.warning("{} file exists, not overwritten.".format(Path(dst).relative_to(cwd)))
        
        return []
        
        
def _copy_file(filename, dst, cwd, options=None):
    if (options and options.force) or (not Path(dst).exists()):
        shutil.copy(PARDIR / filename, dst)
        _logger.info("{} file generated.".format(dst.relative_to(cwd)))
        
        return [dst]
    else:
        _logger.warning("{} file exists, not overwritten.".format(dst.relative_to(cwd)))
        
        return []
        
        
def _prepare_requirements(path, reqs, cwd, options=None):
    try:
        if options and options.force:
            with open(Path(path), 'w') as file:
                for req in reqs:
                    file.write("{}\n".format(req))
        else:
            with open(Path(path), 'x') as file:
                for req in reqs:
                    file.write("{}\n".format(req))
        
        _logger.info("{} file generated.".format(path.relative_to(cwd)))
        
        return [path]
    except FileExistsError:
        _logger.warning("{} file exists, not overwritten.".format(path.relative_to(cwd)))
        
        return []
    

def _prepare_repoasist(cwd, options=None):
    paths = []
    for filename in settings.REPOASSIST_FILES:
        if filename == settings.REPOASSIST_MAIN_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / settings.REPOASSIST_TARGET_MAIN_FILENAME, cwd, options))
        elif filename == settings.COLREQS_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.SETTINGS_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.LOGGER_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.PYINIT_FILENAME:
            paths.extend(_copy_template_file(settings.SAMPLE_MODULE_FILENAME, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        else:
            paths.extend(_generate_empty_file(Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
            
    return paths


def write_file_from_template(template_filename, dst, keywords, cwd='.', options=None):
    if (options and options.force) or (not Path(dst).exists()):
        templateLoader = jinja2.FileSystemLoader(searchpath=str(Path(PARDIR) / settings.TEMPLATES_DIRNAME))
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(template_filename)
        template.stream(keywords).dump(str(dst))
        
        _logger.info("{} file generated.".format(Path(dst).relative_to(cwd)))
         
        return [dst]
    else:
        _logger.warning("{} file exists, not overwritten.".format(Path(dst).relative_to(cwd)))
         
        return []
    
    
def _validate_config(config):
    for field in settings.CONFIG_MANDATORY_FIELDS:
        if field not in config:
            raise exceptions.ConfigError("The {} field not found in the config!".format(field))
