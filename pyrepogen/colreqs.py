#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
from pathlib import Path
from pipreqs import pipreqs

from . import settings


_logger = logging.getLogger(__name__)


def collect_reqs_min(cwd='.'):
    reqs_equal = collect_reqs_specific(cwd)
    return _transform_to_min(reqs_equal)


def collect_reqs_latest(cwd='.'):
    reqs_equal = collect_reqs_specific(cwd)
    return _transform_to_latest(reqs_equal)


def collect_reqs_specific(cwd='.'):
    reqs = []
    ignore_dirs = [str(Path(cwd).resolve() / settings.REPOASSIST_DIRNAME)]
    raw_reqs = pipreqs.get_all_imports(str(cwd), extra_ignore_dirs=ignore_dirs)
    for item in raw_reqs:
        if 'INFO' not in item:
            reqs.append(item)
            
    return reqs


def write_requirements(reqs, cwd='.'):
    file_path = Path(cwd) / settings.FileName.REQUIREMENTS
    file_exists = True if file_path.exists() else False
    
    with open(file_path, 'w') as file:
        for reg in reqs:
            file.write("{}\n".format(reg))
            
        if file_exists:
            _logger.info("{} file updated.".format(settings.FileName.REQUIREMENTS))
        else:
            _logger.info("{} file prepared.".format(settings.FileName.REQUIREMENTS))
            
    return file_path


def write_requirements_dev(cwd='.'):
    file_path = Path(cwd) / settings.FileName.REQUIREMENTS_DEV
    
    try:
        with open(file_path, 'x') as file:
            for reg in settings.REQUIREMENTS_DEV:
                file.write("{}\n".format(reg))
                _logger.info("{} file prepared.".format(settings.FileName.REQUIREMENTS_DEV))
    except FileExistsError:
        _logger.warning("{} file already exists, not overwritten.".format(settings.FileName.REQUIREMENTS_DEV))
            
    return file_path
            
            
def _transform_to_min(reqs):
    final_reqs = []
    for req in reqs:
        splitted = req.split('==')
        try:
            final_reqs.append("{}>={}".format(splitted[0], splitted[1]))
        except IndexError:
            final_reqs.append(req) 
        
    return final_reqs


def _transform_to_latest(reqs):
    final_reqs = []
    for req in reqs:
        splitted = req.split('==')
        if len(splitted) == 1:
            splitted = req.split('>=')
        final_reqs.append(splitted[0]) 
        
    return final_reqs

