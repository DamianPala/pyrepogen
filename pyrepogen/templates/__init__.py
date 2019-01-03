#!/usr/bin/env python
# -*- coding: utf-8 -*-


import inspect
from pathlib import Path


PARDIR = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent
__version__ = '{{repoassist_version}}'