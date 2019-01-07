#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import jinja2
from pathlib import Path
from pyrepogen import PARDIR
from pyrepogen import settings
import semver

_logger = logging.getLogger(__name__)


def mod1_msg():
    _logger.info("Hello from mod1!")
    

if __name__ == '__main__':
    version_info1 = semver.VersionInfo.parse("1.0.1-rc2")
    version_info2 = semver.VersionInfo.parse("1.0.1-rc1")
    print(version_info1)
    print(version_info2)
    print(version_info1 > version_info2)
    
    print(str(Path('') / settings.FileName.README) == (Path('') / settings.FileName.README).name)
    print(Path().cwd())
    print(Path('<project_name>') / 'test')
    
    src = Path(settings.TEMPLATES_DIRNAME) / 'test' / 'fdafad' / settings.FileName.GITIGNORE
    
    src_parents = [item for item in src.parents]
    is_from_template = str(src_parents[-2]) == settings.TEMPLATES_DIRNAME
    
    print(src_parents[-2])
    print(is_from_template)
    print(settings.TEMPLATES_DIRNAME)
