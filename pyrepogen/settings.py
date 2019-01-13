#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
from enum import Enum
from pathlib import Path
import dataclasses
from collections import namedtuple

from . import (__version__, MIN_PYTHON)


SUGGESTED_INITIAL_RELEASE_TAG = '0.1.0'


class ProjectType(Enum):
    PACKAGE = 'package'
    MODULE = 'module'
    

class ChangelogType(Enum):
    GENERATED = 'generated'
    PREPARED = 'prepared'


class AuthorsType(Enum):
    GENERATED = 'generated'
    PREPARED = 'prepared'


class DirName():
    TEMPLATES = 'templates'
    TESTS = 'tests'
    DOCS = 'docs'
    DISTRIBUTION = 'dist'
    REPOASSIST = 'repoassist'
    GIT = '.git'
    RELEASE = 'release'
    HTMLCOV = 'htmlcov'


REPO_CONFIG_SECTION_NAME = 'repoconfig'
METADATA_CONFIG_SECTION_NAME = 'metadata'
GENERATOR_CONFIG_SECTION_NAME = 'pyrepogen'
    
TESTS_PATH = './' + DirName.TESTS
PROJECT_NAME_PATH_PLACEHOLDER = '<project_name>'
TEMPLATES_PACKAGE_PATH = 'templates/package'
TEMPLATES_PACKAGE_TESTS_PATH = 'templates/package/tests'
TEMPLATES_MODULE_PATH = 'templates/module'

REPOASSIST_VERSION = f'{DirName.REPOASSIST}_version'
AUTOMATIC_RELEASE_COMMIT_MSG = 'Automatic update of release data files.'
LICENSE = 'MIT'
RELEASE_PACKAGE_SUFFIX = '_release'
JINJA2_TEMPLATE_EXT = '.j2'

ENTRY_POINT_PLACEHOLDER = '<project_name>'
MODULE_ENTRY_POINT = f'{ENTRY_POINT_PLACEHOLDER} = {ENTRY_POINT_PLACEHOLDER}:main'
PACKAGE_ENTRY_POINT = f'{ENTRY_POINT_PLACEHOLDER} = {ENTRY_POINT_PLACEHOLDER}.cli:main'


class FileName():
    REPO_CONFIG = 'gen_repo.cfg'
    SETUP_CFG = 'setup.cfg'
    SETUP_PY = 'setup.py'
    CHANGELOG = 'CHANGELOG.md'
    CHANGELOG_GENERATED = 'CHANGELOG_generated.md'
    CHANGELOG_PREPARED = 'CHANGELOG_prepared.md'
    AUTHORS = 'AUTHORS'
    AUTHORS_PREPARED = 'AUTHORS_prepared.md'
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
    CLOUD_CREDENTIALS = 'cloud_credentials.txt'
    REQUIREMENTS = 'requirements.txt'
    REQUIREMENTS_DEV = 'requirements-dev.txt'


class Tools():
    FILE_FORMATTER = 'autopep8'
    LINTER = 'flake8'
    MERGE_TOOL = 'Meld Merge'
    PYTHON = 'python'


@dataclasses.dataclass
class Config():
    project_type : str
    project_name : str
    author : str
    author_email : str
    short_description : str
    changelog_type : str
    authors_type : str
    is_cloud : bool = None
    is_sample_layout : bool = None
    maintainer : str = ''
    maintainer_email : str = ''
    home_page : str = ''
    year : str = str(datetime.datetime.now().year)
    min_python : str = f'{MIN_PYTHON[0]}.{MIN_PYTHON[1]}'
    tests_path : str = TESTS_PATH
    description_file : str = FileName.README
    tests_dirname : str = DirName.TESTS
    repoassist_name : str = DirName.REPOASSIST
    license : str = LICENSE
    generator_section : str = GENERATOR_CONFIG_SECTION_NAME
    metadata_section : str = METADATA_CONFIG_SECTION_NAME
    keywords : list = None
    is_git : bool = False
    git_origin : str = ''
    pipreqs_ignore : list = None
    
    def __post_init__(self):
        setattr(self, REPOASSIST_VERSION, __version__)
    
    @staticmethod
    def get_fields():
        return [field.name for field in dataclasses.fields(Config)]
    
    @staticmethod
    def get_mandatory_fields():
        return [field.name for field in dataclasses.fields(Config) if field.default == dataclasses.MISSING]
    
    @staticmethod
    def get_default_fields():
        return dir(Config)
    

FileGenEntry = namedtuple('FileGeneratorEntry', 'src dst is_sample')

MODULE_REPO_FILES_TO_GEN = [
    FileGenEntry(src=Path('') / FileName.README, dst=Path('.') / FileName.README, is_sample=False),
    FileGenEntry(src=Path('') / FileName.TODO, dst=Path('.') / FileName.TODO, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.CONFTEST, dst=Path('.') / FileName.CONFTEST, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.GITIGNORE, dst=Path('.') / FileName.GITIGNORE, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.TOX, dst=Path('.') / FileName.TOX, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.MAKEFILE, dst=Path('.') / FileName.MAKEFILE, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.LICENSE, dst=Path('.') / FileName.LICENSE, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.SETUP_CFG, dst=Path('.') / FileName.SETUP_CFG, is_sample=False),
    FileGenEntry(src=Path(TEMPLATES_PACKAGE_PATH) / FileName.SETUP_PY, dst=Path('.') / FileName.SETUP_PY, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.CLOUD_CREDENTIALS, dst=Path('.') / FileName.CLOUD_CREDENTIALS, is_sample=False),
    FileGenEntry(src=Path(TEMPLATES_MODULE_PATH) / FileName.REQUIREMENTS, dst=Path('.') / FileName.REQUIREMENTS, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.REQUIREMENTS_DEV, dst=Path('.') / FileName.REQUIREMENTS_DEV, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.SAMPLE_MODULE, dst=Path('.') / DirName.TESTS / FileName.PYINIT, is_sample=False),
    FileGenEntry(src=Path(TEMPLATES_MODULE_PATH) / FileName.MODULE_SAMPLE, dst=Path('.') / (PROJECT_NAME_PATH_PLACEHOLDER + '.py'), is_sample=True),
    FileGenEntry(src=Path(TEMPLATES_MODULE_PATH) / FileName.MODULE_SAMPLE_TEST_FILENAME, dst=Path('.') / DirName.TESTS / (PROJECT_NAME_PATH_PLACEHOLDER + '_test.py'), is_sample=True),
]

PACKAGE_REPO_FILES_TO_GEN = [
    FileGenEntry(src=Path('') / FileName.README, dst=Path('.') / FileName.README, is_sample=False),
    FileGenEntry(src=Path('') / FileName.TODO, dst=Path('.') / FileName.TODO, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.CONFTEST, dst=Path('.') / FileName.CONFTEST, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.GITIGNORE, dst=Path('.') / FileName.GITIGNORE, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.TOX, dst=Path('.') / FileName.TOX, is_sample=False),
    FileGenEntry(src=Path(TEMPLATES_PACKAGE_PATH) / FileName.PYINIT, dst=Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.PYINIT, is_sample=True),
    FileGenEntry(src=Path(TEMPLATES_PACKAGE_PATH) / FileName.MAIN, dst=Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.MAIN, is_sample=True),
    FileGenEntry(src=Path(TEMPLATES_PACKAGE_PATH) / FileName.CLI, dst=Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.CLI, is_sample=True),
    FileGenEntry(src=Path(TEMPLATES_PACKAGE_PATH) / FileName.PACKAGE_SAMPLE_MODULE, dst=Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.PACKAGE_SAMPLE_MODULE, is_sample=True),
    FileGenEntry(src=Path(TEMPLATES_PACKAGE_TESTS_PATH) / FileName.PYINIT, dst=Path('.') / DirName.TESTS / FileName.PYINIT, is_sample=True),
    FileGenEntry(src=Path(TEMPLATES_PACKAGE_TESTS_PATH) / FileName.PACKAGE_SAMPLE_TEST, dst=Path('.') / DirName.TESTS / FileName.PACKAGE_SAMPLE_TEST, is_sample=True),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.MAKEFILE, dst=Path('.') / FileName.MAKEFILE, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.LICENSE, dst=Path('.') / FileName.LICENSE, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.SETUP_CFG, dst=Path('.') / FileName.SETUP_CFG, is_sample=False),
    FileGenEntry(src=Path(TEMPLATES_PACKAGE_PATH) / FileName.SETUP_PY, dst=Path('.') / FileName.SETUP_PY, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.CLOUD_CREDENTIALS, dst=Path('.') / FileName.CLOUD_CREDENTIALS, is_sample=False),
    FileGenEntry(src=Path(TEMPLATES_PACKAGE_PATH) / FileName.REQUIREMENTS, dst=Path('.') / FileName.REQUIREMENTS, is_sample=False),
    FileGenEntry(src=Path(DirName.TEMPLATES) / FileName.REQUIREMENTS_DEV, dst=Path('.') / FileName.REQUIREMENTS_DEV, is_sample=False),
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
    FileName.AUTHORS,
    FileName.PREPARE,
    FileName.CLEAN,
]

GEN_REPO_CONFIG_MANDATORY_FIELDS = [
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
