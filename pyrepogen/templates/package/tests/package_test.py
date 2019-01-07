#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest

from spackage import modulo


def test_get_reminder():
    assert modulo.get_reminder(9, 7) == 2, "The get_reminder does not work properly"
