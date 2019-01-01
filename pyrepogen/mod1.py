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