#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import jinja2
from pathlib import Path
from pyrepogen import PARDIR
from pyrepogen import settings

_logger = logging.getLogger(__name__)


def mod1_msg():
    _logger.info("Hello from mod1!")
    

if __name__ == '__main__':
    templateLoader = jinja2.FileSystemLoader(searchpath=str(Path(PARDIR) / settings.TEMPLATES_DIRNAME))
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template('Makefile_standalone')
    template.stream().dump(str(Path().cwd() / 'repoassist'))