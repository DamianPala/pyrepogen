#!/usr/bin/env python
# -*- coding: utf-8 -*-


from enum import Enum
from pathlib import Path


SUGGESTED_INITIAL_RELEASE_TAG = '0.1.0'

REQUIREMENTS_FILENAME = 'requirements.txt'
REQUIREMENTS_DEV_FILENAME = 'requirements-dev.txt'


REQUIREMENTS_STANDALONE = []

REQUIREMENTS_PACKAGE = [
    'setuptools',
]

REQUIREMENTS_DEV = [
    'Sphinx',
    'pytest',
    'flake8>=3.6.0',
    'pycodestyle>=2.4.0'
    'coverage',
    'tox',
    'hacking'
]


TEMPLATES_DIRNAME = 'templates'

DOCS_DIRNAME = 'docs'
TESTS_DIRNAME = 'tests'
DISTRIBUTION_DIRNAME = 'dist'
REPOASSIST_DIRNAME = 'repoassist'
GIT_DIRNAME = '.git'
RELEASE_DIRNAME = "release"

RELEASE_PACKAGE_SUFFIX = "_release"

SETUP_CFG_FILENAME = 'setup.cfg'
SETUP_CFG_STANDALONE_FILENAME = 'setup_standalone.cfg'
SETUP_CFG_PACKAGE_FILENAME = 'setup_package.cfg'
CHANGELOG_FILENAME = 'CHANGELOG.md'
CHANGELOG_GENERATED = 'CHANGELOG_generated.md'
CHANGELOG_PREPARED = 'CHANGELOG_prepared.md'
AUTHORS_FILENAME = 'AUTHORS'
GITIGNORE_FILENAME = '.gitignore'
README_FILENAME = 'README.md'
TODO_FILENAME = 'TODO.md'
LICENSE_FILENAME = 'LICENSE'
MAKEFILE_FILENAME = 'Makefile'
MAKEFILE_STANDALONE_FILENAME = 'Makefile_standalone'
MAKEFILE_PACKAGE_FILENAME = 'Makefile_package'
CONFTEST_FILENAME = 'conftest.py'
STANDALONE_SAMPLE_FILENAME = 'sample_standalone.py'
STANDALONE_SAMPLE_TEST_FILENAME = 'sample_standalone_test.py'
TOX_STANDALONE_FILENAME = 'tox_standalone.ini'
TOX_FILENAME = 'tox.ini'
PYINIT_FILENAME = '__init__.py'
SAMPLE_MODULE_FILENAME = 'module.py'
REPOASSIST_MAIN_FILENAME = 'repoassist_main.py'
REPOASSIST_TARGET_MAIN_FILENAME = '__main__.py'
COLREQS_FILENAME = 'colreqs.py'
SETTINGS_FILENAME = 'settings.py'
LOGGER_FILENAME = 'logger.py'
RELEASE_FILENAME = 'release.py'
EXCEPTIONS_FILENAME = 'exceptions.py'
UTILS_FILENAME = 'utils.py'
PYGITTOOLS_FILENAME = 'pygittools.py'
CLOUD_FILENAME = 'cloud.py'
WIZARD_FILENAME = 'wizard.py'
FORMATTER_FILENAME = 'formatter.py'
CLOUD_CREDENTIALS_FILENAME = "cloud_credentials.txt"

STANDALONE_REPO_FILES_TO_GEN = [
    README_FILENAME,
    GITIGNORE_FILENAME,
    TODO_FILENAME,
    CONFTEST_FILENAME,
    STANDALONE_SAMPLE_FILENAME,
    STANDALONE_SAMPLE_TEST_FILENAME,
    TOX_STANDALONE_FILENAME,
    PYINIT_FILENAME,
    REQUIREMENTS_FILENAME,
    REQUIREMENTS_DEV_FILENAME,
    MAKEFILE_FILENAME,
    LICENSE_FILENAME,
    SETUP_CFG_FILENAME,
    CLOUD_CREDENTIALS_FILENAME,
]

STANDALONE_REPO_DIRS_TO_GEN = [
    DOCS_DIRNAME,
    TESTS_DIRNAME,
    REPOASSIST_DIRNAME,
    str(Path(REPOASSIST_DIRNAME) / TEMPLATES_DIRNAME)
]

REPOASSIST_FILES = [
    PYINIT_FILENAME,
    REPOASSIST_MAIN_FILENAME,
    COLREQS_FILENAME,
    SETTINGS_FILENAME,
    LOGGER_FILENAME,
    RELEASE_FILENAME,
    EXCEPTIONS_FILENAME,
    UTILS_FILENAME,
    PYGITTOOLS_FILENAME,
    CLOUD_FILENAME,
    WIZARD_FILENAME,
    FORMATTER_FILENAME,
    CHANGELOG_FILENAME,
]

class ProjectType(Enum):
    PACKAGE = 'package'
    SCRIPT = 'script'
    
class ChangelogType(Enum):
    GENERATED = 'generated'
    PREPARED = 'prepared'

CONFIG_MANDATORY_FIELDS = [
    'project_type',
    'repo_name',
    'project_name',
    'author',
    'author_email',
    'short_description',
    'changelog_type',
    'year',
]

AUTOMATIC_RELEASE_COMMIT_MSG = "Automatic update of release data files."
