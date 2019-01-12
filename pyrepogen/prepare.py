#!/usr/bin/env python
# -*- coding: utf-8 -*-


import shutil
import jinja2
from pathlib import Path

from . import settings
from . import PARDIR
from . import exceptions
from . import pygittools
from . import logger


_logger = logger.get_logger(__name__)


def generate_repo(config, cwd='.', options=None):
    _logger.info("Generate repository files...")

    paths = []
    
    Path(cwd).mkdir(parents=True, exist_ok=True)
    paths.extend(_generate_repo_dirs(config, cwd))
    if config.project_type == settings.ProjectType.PACKAGE.value:
        if options.sample_layout:
            config.entry_point = settings.PACKAGE_ENTRY_POINT.replace(settings.ENTRY_POINT_PLACEHOLDER, config.project_name)
        paths.extend(_generate_repo_files(settings.PACKAGE_REPO_FILES_TO_GEN, config, cwd, options))
    elif config.project_type == settings.ProjectType.MODULE.value:
        if options.sample_layout:
            config.entry_point = settings.MODULE_ENTRY_POINT.replace(settings.ENTRY_POINT_PLACEHOLDER, config.project_name)
        paths.extend(_generate_repo_files(settings.MODULE_REPO_FILES_TO_GEN, config, cwd, options))
    else:
        raise exceptions.RuntimeError("Unknown project type.", _logger)
    paths.extend(_generate_repoasist(config, cwd, options))
    
    if config.is_git:
        _init_git_repo(config, cwd)

    _logger.info("Repository files generated.")

    return paths


def _init_git_repo(config, cwd):
    ret = pygittools.init(cwd)
    if ret['returncode'] != 0:
        raise exceptions.RuntimeError("Git repository initializing error: {}".format(ret['msg']), _logger)
    
    if config.git_origin:
        ret = pygittools.add_origin(config.git_origin, cwd)
        if ret['returncode'] != 0:
            raise exceptions.RuntimeError("Git repository origin set up error: {}".format(ret['msg']), _logger)
    

def _generate_repo_dirs(config, cwd):
    paths = []

    for dirname in settings.REPO_DIRS_TO_GEN:
        paths.extend(_generate_directory(dirname, cwd))
        
    if config.project_type == settings.ProjectType.PACKAGE.value:
        paths.extend(_generate_directory(config.project_name, cwd))
        
    return paths


def _generate_directory(dirname, cwd):
    try:
        Path(Path(cwd) / dirname).mkdir()
        _logger.info("{} directory generated.".format(dirname))
        return [Path(cwd) / dirname]
    except FileExistsError:
        _logger.warning("{} directory exists, not overwritten.".format(dirname))
        return []


def generate_repo_config(cwd='.', options=None):
    _logger.info("Creating the predefined repository config file {} in your current working directory...".format(settings.FileName.REPO_CONFIG))
    path = _copy_template_file(settings.FileName.REPO_CONFIG, Path(cwd) / settings.FileName.REPO_CONFIG, cwd, options, verbose=False)
    _logger.info("Predefined repository config file created. Please fill it with relevant data and try to generate repository again!")
    
    return path
    
    
def _generate_repo_files(files_list, config, cwd, options=None):
    paths = []

    for file in files_list:
        src = file['src']
        dst = Path(cwd) / file['dst']
        
        if not options.cloud and (src.name == settings.FileName.CLOUD_CREDENTIALS):
            continue
        
        if settings.PROJECT_NAME_PATH_PLACEHOLDER in str(dst):
            dst = Path(str(dst).replace(settings.PROJECT_NAME_PATH_PLACEHOLDER, config.project_name))
            
        src_parents = [item for item in src.parents]
        if src_parents.__len__() >= 2 and (str(src_parents[-2]) == settings.DirName.TEMPLATES):
            is_from_template = True
        else:
            is_from_template = False
        
        if is_from_template:
            paths.extend(write_file_from_template(src, dst, config.__dict__, cwd, options))
        else:
            paths.extend(_generate_empty_file(dst, cwd, options))

    return paths


def _generate_repoasist(config, cwd, options=None):
    paths = []

    for filename in settings.REPOASSIST_FILES:
        if filename == settings.FileName.REPOASSIST_MAIN:
            paths.extend(_copy_file(filename,
                                    Path(cwd) / settings.DirName.REPOASSIST / settings.FileName.MAIN,
                                    cwd, options))
        elif filename == settings.FileName.PYINIT:
            paths.extend(write_file_from_template(Path(settings.DirName.TEMPLATES) / settings.FileName.PYINIT,
                                                  Path(cwd) / settings.DirName.REPOASSIST / filename, config.__dict__,
                                                  cwd, options))
        elif filename == settings.FileName.CHANGELOG:
            paths.extend(_copy_template_file(settings.FileName.CHANGELOG_GENERATED,
                                             Path(cwd) / settings.DirName.REPOASSIST / settings.DirName.TEMPLATES / settings.FileName.CHANGELOG_GENERATED,
                                             cwd, options))
            paths.extend(_copy_template_file(settings.FileName.CHANGELOG_PREPARED,
                                             Path(cwd) / settings.DirName.REPOASSIST / settings.DirName.TEMPLATES / settings.FileName.CHANGELOG_PREPARED,
                                             cwd, options))
        else:
            paths.extend(_copy_file(filename, Path(cwd) / settings.DirName.REPOASSIST / filename, cwd, options))
            
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
    filename = f'{filename}{settings.JINJA2_TEMPLATE_EXT}'
    return _copy_file_from(PARDIR / settings.DirName.TEMPLATES / filename, dst, cwd, options, verbose)


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
    src = src.parent / f'{src.name}{settings.JINJA2_TEMPLATE_EXT}'
    if (options and options.force) or (not Path(dst).exists()):
        templateLoader = jinja2.FileSystemLoader(searchpath=str(Path(PARDIR) / src.parent))
        templateEnv = jinja2.Environment(loader=templateLoader,
                                         trim_blocks=True,
                                         lstrip_blocks=True,
                                         newline_sequence='\r\n',
                                         keep_trailing_newline=True)
        template = templateEnv.get_template(src.name)
        template.stream(keywords, options=options).dump(str(dst))

        if verbose:
            _logger.info("{} file generated.".format(Path(dst).relative_to(Path(cwd).resolve())))

        return [dst]
    else:
        if verbose:
            _logger.warning("{} file exists, not overwritten.".format(Path(dst).relative_to(Path(cwd).resolve())))

        return []
