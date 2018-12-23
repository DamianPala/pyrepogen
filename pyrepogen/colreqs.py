from pathlib import Path

from . import utils
from pyrepogen import settings


def collect_reqs_min(path):
    reqs_equal = collect_reqs_specific(path)
    return _transform_to_min(reqs_equal)


def collect_reqs_latest(path):
    reqs_equal = collect_reqs_specific(path)
    return _transform_to_latest(reqs_equal)


def collect_reqs_specific(path):
    reqs = []
    raw_reqs = utils.execute_cmd_and_split_lines_to_list(['pipreqs', '--print', path])[:-1] 
    for item in raw_reqs:
        if 'INFO' not in item:
            reqs.append(item)
            
    return reqs


def write_requirements(reqs, path):
    with open(Path(path) / settings.REQUIREMENTS_FILENAME) as file:
        for reg in reqs:
            file.writeline(reg)


def write_requirements_dev(path):
    with open(Path(path) / settings.REQUIREMENTS_DEV_FILENAME) as file:
        for req in settings.DEV_REQUIREMENTS:
            file.writeline(req)


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