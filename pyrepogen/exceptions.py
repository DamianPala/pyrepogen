#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PyRepoGenError(Exception):
    pass

class ExecuteCmdError(PyRepoGenError):
    def __init__(self, returncode, msg):
        super().__init__(msg)
        self.returncode = returncode
        
class ConfigError(PyRepoGenError):
    pass

class FileGenerationError(PyRepoGenError):
    pass