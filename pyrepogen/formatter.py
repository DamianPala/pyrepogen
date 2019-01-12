#!/usr/bin/env python
# -*- coding: utf-8 -*-


import autopep8
import webbrowser
from pathlib import Path

from . import exceptions
from . import utils
from . import settings
from . import logger


_logger = logger.get_logger(__name__)


def format_file(path, with_meld=True, cwd='.'):
    _logger.info(f'Format the file: {path} using {settings.Tools.FILE_FORMATTER} '
                 f'with merge mode in {settings.Tools.MERGE_TOOL}')
    
    path = Path(cwd) / path
    formated_file_path = path.parent / (path.stem + '.tmp' + path.suffix)
    setup_file_path = (Path(cwd) / settings.FileName.SETUP_CFG).resolve()
    if path.is_file():
        if formated_file_path.exists():
            raise exceptions.FileExistsError(f'File {formated_file_path} already exists! Please remove it.', _logger)
        with open(formated_file_path, 'w') as file:
            options = autopep8.parse_args(['--global-config='+str(setup_file_path), str(path)], apply_config=True)
            autopep8.fix_file(str(path), output=file, options=options)
    else:
        raise exceptions.NotAFileError('Path must point to a file!', _logger)
    
    if with_meld:
        utils.execute_cmd(['meld', str(path), str(path), str(formated_file_path), '-o', str(path)], str(cwd))
        formated_file_path.unlink()
    else:
        _logger.info(f'Formatted file has ben written to {formated_file_path}')
    
    _logger.info('Lint formatted file and show report')
    try:
        utils.execute_cmd([settings.Tools.LINTER, str(path)], str(cwd))
        _logger.info('Linter report is empty - file ok')
    except exceptions.ExecuteCmdError as e:
        print(e)
        
        
def coverage_report(cwd='.'):
    _logger.info('Open the coverage html report in the default system browser.')
    
    path_to_report = (Path(cwd).resolve() / settings.DirName.HTMLCOV / 'index.html').as_posix()
    url = f'file://{path_to_report}'
    webbrowser.open(url)
