#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import inspect
from pathlib import Path

from . import settings
from . import logger


__version__ = '{{repoassist_version}}'
_logger = logger.create_logger()
PARDIR = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent


if sys.version_info < settings.MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % settings.MIN_PYTHON)
