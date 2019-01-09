#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import jinja2
from collections import namedtuple
from pprint import pprint

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
    
    src = Path(settings.DirName.TEMPLATES) / 'test' / 'fdafad' / settings.FileName.GITIGNORE
    
    src_parents = [item for item in src.parents]
    is_from_template = str(src_parents[-2]) == settings.DirName.TEMPLATES
    
    print(src_parents[-2])
    print(is_from_template)
    print(settings.DirName.TEMPLATES)
    
    d = {'field1': 'val1', 'field2': 'val2', 'field3': 3}
    namedTupleConstructor = namedtuple('myNamedTuple', ' '.join(sorted(d.keys())))
    nt= namedTupleConstructor(**d)
    pprint(nt)
    print(nt.field1)

    from types import SimpleNamespace
    
    sn = SimpleNamespace(**d)
    print(sn)
    print(sn.field3)
    del sn.field3
    
    sn2 = SimpleNamespace(**{'2field1': 'val'})
    print(sn2)
    pprint(sn.__dict__)
    
    path = Path(Path().cwd() / 'test')
    pprint(path)
    pprint(path.__str__())