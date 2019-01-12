#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from pathlib import Path

from . import logger


__version__ = '0.1.0'
_logger = logger.create_logger()
PARDIR = Path(__file__).parent
MIN_PYTHON = (3, 7)


if sys.version_info < MIN_PYTHON:
    sys.exit('Python %s.%s or later is required.\n' % MIN_PYTHON)
