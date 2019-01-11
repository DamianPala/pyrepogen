#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import inspect
from pathlib import Path

from . import settings


__version__ = '{{repoassist_version}}'

PARDIR = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent
PACKAGENAME = (Path(inspect.getfile(inspect.currentframe())) / '..').resolve().name


if sys.version_info < settings.MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % settings.MIN_PYTHON)
