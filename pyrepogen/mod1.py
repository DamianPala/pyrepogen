#!/usr/bin/env python
# -*- coding: utf-8 -*-


import jinja2
from collections import namedtuple
from dataclasses import dataclass, make_dataclass
from pprint import pprint

from pathlib import Path
from pyrepogen import settings
from pyrepogen import logger
import semver
import pbr


_logger = logger.get_logger(__name__)


def mod1_msg():
    _logger.info("Hello from mod1!")
    

if __name__ == '__main__':
    _logger.info("This is file!")
    
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
    nt = namedTupleConstructor(**d)
    pprint(nt)
    print(nt.field1)
    for item in nt:
        print(item)
#     nt.field1 = 3
    

    from types import SimpleNamespace
    
    print("---> Simple namespace")
    sn = SimpleNamespace(**d)
    print(sn)
    print(sn.field3)
    del sn.field3
    
    for field in sn.__dict__:
        print(field)
        
    if hasattr(sn, 'field1'):
        print("Field detected!")
    
    sn2 = SimpleNamespace(**{'2field1': 'val'})
    print(sn2)
    pprint(sn.__dict__)
    
    path = Path(Path().cwd() / 'test')
    pprint(path)
    pprint(path.__str__())
    
    print("----> dataclass")
    
    C = make_dataclass('C',
                   [('x', int),
                     'y',], order=True,)
    
    dc = C(10, 20)
    print(dc)
    print(dc.x)
    print(hasattr(dc, 'x'))
    print('x' in dc.__dict__)
    setattr(dc, 'x', 'new value')
    dc.x = 4
    print(dc.x)
    print(dc.__dict__)
    for k, v in dc.__dict__.items():
        print(k, v)
        
    str = ''
    if str != None:
        print(True)
    
    
    FileGenEntry = namedtuple('FileGeneratorEntry', 'src dst is_sample')
    file_entry = FileGenEntry(src='source', dst='destination', is_sample=True)
    print(file_entry)
    print(file_entry.is_sample)
    
    