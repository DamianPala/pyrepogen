#!/usr/bin/env python
# -*- coding: utf-8 -*-


from enum import Enum
from pathlib import Path

MIN_PYTHON = (3, 7)
SUGGESTED_INITIAL_RELEASE_TAG = '0.1.0'


class ProjectType(Enum):
    PACKAGE = 'package'
    MODULE = 'module'
    

class ChangelogType(Enum):
    GENERATED = 'generated'
    PREPARED = 'prepared'


class DirName():
    TEMPLATES = 'templates'
    TESTS = 'tests'
    DOCS = 'docs'
    DISTRIBUTION = 'dist'
    REPOASSIST = 'repoassist'
    GIT = '.git'
    RELEASE = "release"
    HTMLCOV = 'htmlcov'


REPO_CONFIG_SECTION_NAME = 'repoconfig'
METADATA_CONFIG_SECTION_NAME = 'metadata'
GENERATOR_CONFIG_SECTION_NAME = 'pyrepogen'
    
TESTS_PATH = './' + DirName.TESTS
PROJECT_NAME_PATH_PLACEHOLDER = '<project_name>'
TEMPLATES_PACKAGE_PATH = 'templates/package'
TEMPLATES_PACKAGE_TESTS_PATH = 'templates/package/tests'
TEMPLATES_MODULE_PATH = 'templates/module'

REPOASSIST_VERSION = '{}_version'.format(DirName.REPOASSIST)
AUTOMATIC_RELEASE_COMMIT_MSG = "Automatic update of release data files."
LICENSE = 'MIT'
RELEASE_PACKAGE_SUFFIX = "_release"

ENTRY_POINT_PLACEHOLDER = '<project_name>'
MODULE_ENTRY_POINT = "{} = {}:main".format(ENTRY_POINT_PLACEHOLDER, ENTRY_POINT_PLACEHOLDER)
PACKAGE_ENTRY_POINT = "{} = {}.cli:main".format(ENTRY_POINT_PLACEHOLDER, ENTRY_POINT_PLACEHOLDER)


class FileName():
    REPO_CONFIG = 'gen_repo.cfg'
    SETUP_CFG = 'setup.cfg'
    SETUP_PY = 'setup.py'
    CHANGELOG = 'CHANGELOG.md'
    CHANGELOG_GENERATED = 'CHANGELOG_generated.md'
    CHANGELOG_PREPARED = 'CHANGELOG_prepared.md'
    AUTHORS = 'AUTHORS'
    GITIGNORE = '.gitignore'
    README = 'README.md'
    TODO = 'TODO.md'
    LICENSE = 'LICENSE'
    MAKEFILE = 'Makefile'
    CONFTEST = 'conftest.py'
    MODULE_SAMPLE = 'sample.py'
    MODULE_SAMPLE_TEST_FILENAME = 'sample_test.py'
    TOX = 'tox.ini'
    PYINIT = '__init__.py'
    MAIN = '__main__.py'
    CLI = 'cli.py'
    PACKAGE_SAMPLE_MODULE = 'modulo.py'
    PACKAGE_SAMPLE_TEST = 'modulo_test.py'
    SAMPLE_MODULE = 'module.py'
    REPOASSIST_MAIN = 'repoassist_main.py'
    COLREQS = 'colreqs.py'
    SETTINGS = 'settings.py'
    LOGGER = 'logger.py'
    RELEASE = 'release.py'
    EXCEPTIONS = 'exceptions.py'
    UTILS = 'utils.py'
    PYGITTOOLS = 'pygittools.py'
    CLOUD = 'cloud.py'
    WIZARD = 'wizard.py'
    FORMATTER = 'formatter.py'
    PREPARE = 'prepare.py'
    CLEAN = 'clean.py'
    CLOUD_CREDENTIALS = "cloud_credentials.txt"
    REQUIREMENTS = 'requirements.txt'
    REQUIREMENTS_DEV = 'requirements-dev.txt'


class Tools():
    FILE_FORMATTER = 'autopep8'
    LINTER = 'flake8'
    MERGE_TOOL = 'Meld Merge'
    PYTHON = 'python'


MODULE_REPO_FILES_TO_GEN = [
    {'src': Path('') / FileName.README, 'dst': Path('.') / FileName.README},
    {'src': Path('') / FileName.TODO, 'dst': Path('.') / FileName.TODO},
    {'src': Path('') / FileName.CONFTEST, 'dst': Path('.') / FileName.CONFTEST},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.GITIGNORE, 'dst': Path('.') / FileName.GITIGNORE},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.TOX, 'dst': Path('.') / FileName.TOX},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.MAKEFILE, 'dst': Path('.') / FileName.MAKEFILE},
    {'src': Path(DirName.TEMPLATES) / FileName.LICENSE, 'dst': Path('.') / FileName.LICENSE},
    {'src': Path(DirName.TEMPLATES) / FileName.SETUP_CFG, 'dst': Path('.') / FileName.SETUP_CFG},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.SETUP_PY, 'dst': Path('.') / FileName.SETUP_PY},
    {'src': Path(DirName.TEMPLATES) / FileName.CLOUD_CREDENTIALS, 'dst': Path('.') / FileName.CLOUD_CREDENTIALS},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.REQUIREMENTS, 'dst': Path('.') / FileName.REQUIREMENTS},
    {'src': Path(DirName.TEMPLATES) / FileName.REQUIREMENTS_DEV, 'dst': Path('.') / FileName.REQUIREMENTS_DEV},
    {'src': Path(DirName.TEMPLATES) / FileName.SAMPLE_MODULE, 'dst': Path('.') / DirName.TESTS / FileName.PYINIT},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.MODULE_SAMPLE, 'dst': Path('.') / (PROJECT_NAME_PATH_PLACEHOLDER + '.py')},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.MODULE_SAMPLE_TEST_FILENAME, 'dst': Path('.') / DirName.TESTS / (PROJECT_NAME_PATH_PLACEHOLDER + '_test.py')},
]

PACKAGE_REPO_FILES_TO_GEN = [
    {'src': Path('') / FileName.README, 'dst': Path('.') / FileName.README},
    {'src': Path('') / FileName.TODO, 'dst': Path('.') / FileName.TODO},
    {'src': Path('') / FileName.CONFTEST, 'dst': Path('.') / FileName.CONFTEST},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.GITIGNORE, 'dst': Path('.') / FileName.GITIGNORE},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.TOX, 'dst': Path('.') / FileName.TOX},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.PYINIT, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.PYINIT},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.MAIN, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.MAIN},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.CLI, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.CLI},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.PACKAGE_SAMPLE_MODULE, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.PACKAGE_SAMPLE_MODULE},
    {'src': Path(TEMPLATES_PACKAGE_TESTS_PATH) / FileName.PYINIT, 'dst': Path('.') / DirName.TESTS / FileName.PYINIT},
    {'src': Path(TEMPLATES_PACKAGE_TESTS_PATH) / FileName.PACKAGE_SAMPLE_TEST, 'dst': Path('.') / DirName.TESTS / FileName.PACKAGE_SAMPLE_TEST},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.MAKEFILE, 'dst': Path('.') / FileName.MAKEFILE},
    {'src': Path(DirName.TEMPLATES) / FileName.LICENSE, 'dst': Path('.') / FileName.LICENSE},
    {'src': Path(DirName.TEMPLATES) / FileName.SETUP_CFG, 'dst': Path('.') / FileName.SETUP_CFG},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.SETUP_PY, 'dst': Path('.') / FileName.SETUP_PY},
    {'src': Path(DirName.TEMPLATES) / FileName.CLOUD_CREDENTIALS, 'dst': Path('.') / FileName.CLOUD_CREDENTIALS},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.REQUIREMENTS, 'dst': Path('.') / FileName.REQUIREMENTS},
    {'src': Path(DirName.TEMPLATES) / FileName.REQUIREMENTS_DEV, 'dst': Path('.') / FileName.REQUIREMENTS_DEV},
]

REPO_DIRS_TO_GEN = [
    DirName.DOCS,
    DirName.TESTS,
    DirName.REPOASSIST,
    str(Path(DirName.REPOASSIST) / DirName.TEMPLATES)
]

REPOASSIST_FILES = [
    FileName.PYINIT,
    FileName.REPOASSIST_MAIN,
    FileName.COLREQS,
    FileName.SETTINGS,
    FileName.LOGGER,
    FileName.RELEASE,
    FileName.EXCEPTIONS,
    FileName.UTILS,
    FileName.PYGITTOOLS,
    FileName.CLOUD,
    FileName.WIZARD,
    FileName.FORMATTER,
    FileName.CHANGELOG,
    FileName.PREPARE,
    FileName.CLEAN,
]

REPO_CONFIG_MANDATORY_FIELDS = [
    'project_type',
    'repo_name',
    'project_name',
    'author',
    'author_email',
    'short_description',
    'changelog_type',
    'year',
    REPOASSIST_VERSION,
    'min_python',
    'tests_path'
]

EXTENDED_REPO_CONFIG_MANDATORY_FIELDS = REPO_CONFIG_MANDATORY_FIELDS + [
    'is_cloud',
    'is_sample_layout'
]

# Only from root directory
FILES_TO_CLEAN = [
    '*.egg'
]

DIRS_TO_CLEAN = [
    {'name': '*.egg-info', 'flag': '.'},
    {'name': '__pycache__', 'flag': 'r'},
    {'name': '.pytest_cache', 'flag': 'r'},
    {'name': '.tox', 'flag': '.'},
    {'name': 'build', 'flag': '.'},
    {'name': 'dist', 'flag': '.'},
    {'name': 'venv*', 'flag': '.'},
    {'name': 'htmlcov', 'flag': '.'},
]
