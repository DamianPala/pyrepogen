#!/usr/bin/env python
# -*- coding: utf-8 -*-


import shutil
import logging
import jinja2
from pathlib import Path

from . import settings
from . import utils
from . import PARDIR


_logger = logging.getLogger(__name__)


def generate_package_repo(config, cwd='.', options=None):
    _logger.info("Generate repository files...")

    paths = []

    Path(cwd).mkdir(parents=True, exist_ok=True)
    paths.extend(_generate_repo_dirs(cwd))
    paths.extend(_generate_package_dir(config, cwd))
    paths.extend(_generate_package_repo_files(config, cwd, options))
    paths.extend(_generate_repoasist(config, cwd, options))

    _logger.info("Repository files generated.")

    return paths


def generate_repo_config(cwd='.', options=None):
    _logger.info("Creating the predefined repository config file {} in your current working directory...".format(settings.REPO_CONFIG_FILENAME))
    path = _copy_template_file(settings.REPO_CONFIG_FILENAME, Path(cwd) / settings.REPO_CONFIG_FILENAME, cwd, options, verbose=False)
    _logger.info("Predefined repository config file created. Please fill it with relevant data and try to generate repository again!")
    
    return path


def generate_module_repo(config, cwd='.', options=None):
    _logger.info("Generate repository files...")

    paths = []

    Path(cwd).mkdir(parents=True, exist_ok=True)
    paths.extend(_generate_repo_dirs(cwd))
    paths.extend(_generate_module_repo_files(config, cwd, options))
    paths.extend(_generate_repoasist(config, cwd, options))

    _logger.info("Repository files generated.")

    return paths


def _generate_repo_dirs(cwd):
    paths = []

    for dirname in settings.REPO_DIRS_TO_GEN:
        paths.extend(_generate_directory(dirname, cwd))

    return paths


def _generate_package_dir(config, cwd):
    return _generate_directory(config['project_name'], cwd)
    

def _generate_directory(dirname, cwd):
    try:
        Path(Path(cwd) / dirname).mkdir()
        _logger.info("{} directory generated.".format(dirname))
        return [Path(cwd) / dirname]
    except FileExistsError:
        _logger.warning("{} directory exists, not overwritten.".format(dirname))
        return []


def _generate_package_repo_files(config, cwd, options=None):
    return _generate_repo_files(settings.PACKAGE_REPO_FILES_TO_GEN, config, cwd, options)


def _generate_module_repo_files(config, cwd, options=None):
    return _generate_repo_files(settings.MODULE_REPO_FILES_TO_GEN, config, cwd, options)
    
    
def _generate_repo_files(files_list, config, cwd, options=None):
    paths = []

    utils.validate_config_metadata(config)

    for file in files_list:
        src = file['src']
        dst = Path(cwd) / file['dst']
        if settings.PROJECT_NAME_PATH_PLACEHOLDER in str(dst):
            dst = Path(str(dst).replace(settings.PROJECT_NAME_PATH_PLACEHOLDER, config['project_name']))
            
        src_parents = [item for item in src.parents]
        if len(src_parents) >= 2 and (str(src_parents[-2]) == settings.TEMPLATES_DIRNAME):
            is_from_template = True
        else:
            is_from_template = False
            
        if is_from_template:
            paths.extend(write_file_from_template(src, dst, config, cwd, options))
        else:
            paths.extend(_generate_empty_file(dst, cwd, options))

    return paths


def _generate_repoasist(config, cwd, options=None):
    paths = []

    utils.validate_config_metadata(config)

    for filename in settings.REPOASSIST_FILES:
        if filename == settings.FileName.REPOASSIST_MAIN:
            paths.extend(_copy_file(filename,
                                    Path(cwd) / settings.REPOASSIST_DIRNAME / settings.FileName.MAIN,
                                    cwd, options))
        elif filename == settings.FileName.PYINIT:
            paths.extend(write_file_from_template(Path(settings.TEMPLATES_DIRNAME) / settings.FileName.PYINIT,
                                                  Path(cwd) / settings.REPOASSIST_DIRNAME / filename, config,
                                                  cwd, options))
        elif filename == settings.FileName.CHANGELOG:
            paths.extend(_copy_template_file(settings.FileName.CHANGELOG_GENERATED,
                                             Path(cwd) / settings.REPOASSIST_DIRNAME / settings.TEMPLATES_DIRNAME / settings.FileName.CHANGELOG_GENERATED,
                                             cwd, options))
            paths.extend(_copy_template_file(settings.FileName.CHANGELOG_PREPARED,
                                             Path(cwd) / settings.REPOASSIST_DIRNAME / settings.TEMPLATES_DIRNAME / settings.FileName.CHANGELOG_PREPARED,
                                             cwd, options))
        else:
            paths.extend(_copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options))
            
    return paths


def _generate_empty_file(path, cwd, options=None):
    try:
        if options and options.force:
            with open(Path(path), 'w'):
                pass
        else:
            with open(Path(path), 'x'):
                pass

        _logger.info("{} file generated.".format(path.relative_to(Path(cwd).resolve())))

        return [path]
    except FileExistsError:
        _logger.warning("{} file exists, not overwritten.".format(path.relative_to(Path(cwd).resolve())))

        return []


def _copy_file(filename, dst, cwd, options=None, verbose=True):
    return _copy_file_from(PARDIR / filename, dst, cwd, options, verbose)


def _copy_template_file(filename, dst, cwd, options=None, verbose=True):
    return _copy_file_from(PARDIR / settings.TEMPLATES_DIRNAME / filename, dst, cwd, options, verbose)


def _copy_file_from(src, dst, cwd, options=None, verbose=True):
    if (options and options.force) or (not Path(dst).exists()):
        shutil.copy(src, dst)
        
        if verbose:
            _logger.info("{} file generated.".format(Path(dst).relative_to(Path(cwd).resolve())))

        return [dst]
    else:
        if verbose:
            _logger.warning("{} file exists, not overwritten.".format(Path(dst).relative_to(Path(cwd).resolve())))

        return []


def write_file_from_template(src, dst, keywords, cwd, options=None, verbose=True):
    if (options and options.force) or (not Path(dst).exists()):
        templateLoader = jinja2.FileSystemLoader(searchpath=str(Path(PARDIR) / src.parent))
        templateEnv = jinja2.Environment(loader=templateLoader,
                                         trim_blocks=True,
                                         lstrip_blocks=True,
                                         newline_sequence='\r\n')
        template = templateEnv.get_template(src.name)
        template.stream(keywords, options=options).dump(str(dst))

        if verbose:
            _logger.info("{} file generated.".format(Path(dst).relative_to(Path(cwd).resolve())))

        return [dst]
    else:
        if verbose:
            _logger.warning("{} file exists, not overwritten.".format(Path(dst).relative_to(Path(cwd).resolve())))

        return []
