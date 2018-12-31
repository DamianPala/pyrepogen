#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PyRepoGenError(Exception):
    def __init__(self, msg, logger):
        super().__init__(msg)
        self.logger = logger

class ExecuteCmdError(PyRepoGenError):
    def __init__(self, returncode, msg, logger):
        super().__init__(msg)
        self.returncode = returncode
        self.logger = logger
        
class ConfigError(PyRepoGenError):
    pass

class FileGenerationError(PyRepoGenError):
    pass

class FileNotFoundError(PyRepoGenError):
    pass

class NameError(PyRepoGenError):
    pass

class ReleaseMetadataError(PyRepoGenError):
    pass

class CredentialsError(PyRepoGenError):
    pass

class BucketNotFoudError(PyRepoGenError):
    pass


