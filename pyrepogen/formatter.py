#!/usr/bin/env python
# -*- coding: utf-8 -*-


import autopep8
import logging
from pathlib import Path

from . import exceptions
from . import utils
from . import settings


_logger = logging.getLogger(__name__)


def format_file(path, with_meld=True, cwd='.'):
    path = Path(cwd) / path
    formated_file_path = path.parent / (path.stem + '.tmp' + path.suffix)
    setup_file_path = (Path(cwd) / settings.SETUP_CFG_FILENAME).resolve()
    if path.is_file():
        if formated_file_path.exists():
            raise exceptions.FileExistsError("File {} already exists! Please remove it.".format(formated_file_path), logger=_logger)
        with open(formated_file_path, 'w') as file:
            options = autopep8.parse_args(['--global-config='+str(setup_file_path), str(path)], apply_config=True)
            autopep8.fix_file(str(path), output=file, options=options)
    else:
        raise exceptions.NotAFileError("Path must point to a file!", logger=_logger)
    
    if with_meld:
        utils.execute_cmd(['meld', str(path), str(path), str(formated_file_path), '-o', str(path)], str(cwd))
        formated_file_path.unlink()
    else:
        _logger.info("Formatted file has ben written to {}".format(formated_file_path))
