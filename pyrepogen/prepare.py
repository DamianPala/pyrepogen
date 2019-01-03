#!/usr/bin/env python
# -*- coding: utf-8 -*-


import shutil
import logging
import configparser
import datetime
from pathlib import Path
from pprint import pprint

from . import settings
from . import exceptions
from . import utils
from pyrepogen import PARDIR


_logger = logging.getLogger(__name__)


def generate_standalone_repo(config, cwd='.', options=None):
    _logger.info("Generate repository files...")
    
    paths = []
    Path(cwd).mkdir(parents=True, exist_ok=True)
    paths.extend(_generate_standalone_repo_dirs(cwd))
    paths.extend(_generate_standalone_repo_files(config, cwd, options))
    paths.extend(_prepare_repoasist(config, cwd, options))
    
    _logger.info("Repository files generated.")
    
    return paths


def _generate_standalone_repo_dirs(cwd='.'):
    paths = []
    for dirname in settings.STANDALONE_REPO_DIRS_TO_GEN:
        try:
            Path(Path(cwd) / dirname).mkdir()
            _logger.info("{} directory generated.".format(dirname))
            paths.append(Path(cwd) / dirname)
        except FileExistsError:
            _logger.warning("{} directory exists, not overwritten.".format(dirname))
            
    return paths


def _generate_standalone_repo_files(config, cwd='.', options=None):
    utils.validate_config(config['metadata'])
    
    paths = []
    for filename in settings.STANDALONE_REPO_FILES_TO_GEN:
        if filename == settings.REQUIREMENTS_FILENAME:
            paths.extend(_prepare_requirements(Path(cwd) / filename, settings.REQUIREMENTS_STANDALONE, cwd, options))
        elif filename == settings.REQUIREMENTS_DEV_FILENAME:
            paths.extend(_prepare_requirements(Path(cwd) / filename, settings.REQUIREMENTS_DEV, cwd, options))
        elif filename == settings.TOX_STANDALONE_FILENAME:
            paths.extend(utils.write_file_from_template(settings.TOX_STANDALONE_FILENAME, Path(cwd) / settings.TOX_FILENAME, 
                                     {'tests_dirname': settings.TESTS_DIRNAME}, cwd, options))
        elif filename == settings.LICENSE_FILENAME:
            paths.extend(utils.write_file_from_template(filename, Path(cwd) / filename, config['metadata'], cwd, options))
        elif filename == settings.SETUP_CFG_FILENAME:
            paths.extend(utils.write_file_from_template(settings.SETUP_CFG_STANDALONE_FILENAME, Path(cwd) / filename, config['metadata'], cwd, options))
        elif filename == settings.GITIGNORE_FILENAME:
            paths.extend(_copy_template_file(filename, Path(cwd) / filename, cwd, options))
        elif filename == settings.STANDALONE_SAMPLE_FILENAME:
            paths.extend(_copy_template_file(filename, Path(cwd) / utils.get_module_name_with_suffix(config['metadata']['project_name']), 
                                             cwd, options))
        elif filename == settings.STANDALONE_SAMPLE_TEST_FILENAME:
            paths.extend(utils.write_file_from_template(filename, Path(cwd) / settings.TESTS_DIRNAME / utils.get_module_name_with_suffix(config['metadata']['project_name'] + '_test'), 
                                                  config['metadata'], cwd, options))
        elif filename == settings.PYINIT_FILENAME:
            paths.extend(_copy_template_file(settings.SAMPLE_MODULE_FILENAME, Path(cwd) / settings.TESTS_DIRNAME / filename, cwd, options))
        elif filename == settings.MAKEFILE_FILENAME:
            paths.extend(utils.write_file_from_template(settings.MAKEFILE_STANDALONE_FILENAME, Path(cwd) / filename, config['metadata'], cwd, options))
        elif filename == settings.LICENSE_FILENAME:
            paths.extend(_copy_template_file(filename, Path(cwd) / filename, cwd, options))
        elif filename == settings.CLOUD_CREDENTIALS_FILENAME:
            if options and options.cloud:
                paths.extend(_copy_template_file(filename, Path(cwd) / filename, cwd))
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
    

def _prepare_repoasist(config, cwd, options=None):
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
        elif filename == settings.RELEASE_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.EXCEPTIONS_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.UTILS_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.PYGITTOOLS_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.CLOUD_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.WIZARD_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.FORMATTER_FILENAME:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.PYINIT_FILENAME:
            paths.extend(_copy_template_file(settings.SAMPLE_MODULE_FILENAME, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
        elif filename == settings.CHANGELOG_FILENAME:
            paths.extend(_copy_template_file(settings.CHANGELOG_GENERATED, Path(cwd) / settings.REPOASSIST_DIRNAME / settings.TEMPLATES_DIRNAME / filename, cwd, options))
        else:
            paths.extend(_generate_empty_file(Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
            
    return paths


