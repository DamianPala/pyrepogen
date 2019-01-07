#!/usr/bin/env python
# -*- coding: utf-8 -*-


from enum import Enum
from pathlib import Path
from test.test_linecache import TEST_PATH

MIN_PYTHON = (3, 7)

SUGGESTED_INITIAL_RELEASE_TAG = '0.1.0'

REPO_CONFIG_FILENAME = 'gen_repo.cfg'
REPO_CONFIG_SECTION_NAME = 'repoconfig'

METADATA_CONFIG_SECTION_NAME = 'metadata'
GENERATOR_CONFIG_SECTION_NAME = 'pyrepogen'

TEMPLATES_DIRNAME = 'templates'
TEMPLATES_PACKAGE_PATH = 'templates/package'
TEMPLATES_PACKAGE_TESTS_PATH = 'templates/package/tests'
TEMPLATES_MODULE_PATH = 'templates/module'
DOCS_DIRNAME = 'docs'
TESTS_DIRNAME = 'tests'
TESTS_PATH = './' + TESTS_DIRNAME
DISTRIBUTION_DIRNAME = 'dist'
REPOASSIST_DIRNAME = 'repoassist'
GIT_DIRNAME = '.git'
RELEASE_DIRNAME = "release"
HTMLCOV_DIRNAME = 'htmlcov'

RELEASE_PACKAGE_SUFFIX = "_release"

REPOASSIST_VERSION = '{}_version'.format(REPOASSIST_DIRNAME)
PROJECT_NAME_PATH_PLACEHOLDER = '<project_name>'
LICENSE = 'MIT'

class FileName():
    SETUP_CFG = 'setup.cfg'
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
    MERGE_TOOL = 'Meld Merge'

MODULE_REPO_FILES_TO_GEN = [
    {'src': Path('') / FileName.README, 'dst': Path('.') / FileName.README},
    {'src': Path('') / FileName.TODO, 'dst': Path('.') / FileName.TODO},
    {'src': Path('') / FileName.CONFTEST, 'dst': Path('.') / FileName.CONFTEST},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.GITIGNORE, 'dst': Path('.') / FileName.GITIGNORE},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.TOX, 'dst': Path('.') / FileName.TOX},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.MAKEFILE, 'dst': Path('.') / FileName.MAKEFILE},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.LICENSE, 'dst': Path('.') / FileName.LICENSE},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.SETUP_CFG, 'dst': Path('.') / FileName.SETUP_CFG},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.CLOUD_CREDENTIALS, 'dst': Path('.') / FileName.CLOUD_CREDENTIALS},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.REQUIREMENTS, 'dst': Path('.') / FileName.REQUIREMENTS},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.REQUIREMENTS_DEV, 'dst': Path('.') / FileName.REQUIREMENTS_DEV},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.SAMPLE_MODULE, 'dst': Path('.') / TESTS_DIRNAME / FileName.PYINIT},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.MODULE_SAMPLE, 'dst': Path('.') / (PROJECT_NAME_PATH_PLACEHOLDER + '.py')},
    {'src': Path(TEMPLATES_MODULE_PATH) / FileName.MODULE_SAMPLE_TEST_FILENAME, 'dst': Path('.') / TESTS_DIRNAME / (PROJECT_NAME_PATH_PLACEHOLDER + '_test.py')},
]

PACKAGE_REPO_FILES_TO_GEN = [
    {'src': Path('') / FileName.README, 'dst': Path('.') / FileName.README},
    {'src': Path('') / FileName.TODO, 'dst': Path('.') / FileName.TODO},
    {'src': Path('') / FileName.CONFTEST, 'dst': Path('.') / FileName.CONFTEST},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.GITIGNORE, 'dst': Path('.') / FileName.GITIGNORE},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.TOX, 'dst': Path('.') / FileName.TOX},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.PYINIT, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.PYINIT},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.MAIN, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.MAIN},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.CLI, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.CLI},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.PACKAGE_SAMPLE_MODULE, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / FileName.PACKAGE_SAMPLE_MODULE},
    {'src': Path(TEMPLATES_PACKAGE_TESTS_PATH) / FileName.PYINIT, 'dst': Path('.') / TESTS_DIRNAME / FileName.PYINIT},
    {'src': Path(TEMPLATES_PACKAGE_TESTS_PATH) / FileName.PACKAGE_SAMPLE_TEST, 'dst': Path('.') / TESTS_DIRNAME / FileName.PACKAGE_SAMPLE_TEST},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.MAKEFILE, 'dst': Path('.') / FileName.MAKEFILE},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.LICENSE, 'dst': Path('.') / FileName.LICENSE},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.SETUP_CFG, 'dst': Path('.') / FileName.SETUP_CFG},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.CLOUD_CREDENTIALS, 'dst': Path('.') / FileName.CLOUD_CREDENTIALS},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / FileName.REQUIREMENTS, 'dst': Path('.') / FileName.REQUIREMENTS},
    {'src': Path(TEMPLATES_DIRNAME) / FileName.REQUIREMENTS_DEV, 'dst': Path('.') / FileName.REQUIREMENTS_DEV},
]

REPO_DIRS_TO_GEN = [
    DOCS_DIRNAME,
    TESTS_DIRNAME,
    REPOASSIST_DIRNAME,
    str(Path(REPOASSIST_DIRNAME) / TEMPLATES_DIRNAME)
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

class ProjectType(Enum):
    PACKAGE = 'package'
    MODULE = 'module'
    
class ChangelogType(Enum):
    GENERATED = 'generated'
    PREPARED = 'prepared'

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

AUTOMATIC_RELEASE_COMMIT_MSG = "Automatic update of release data files."

# Only from root directory
FILES_TO_CLEAN = [
    '*.egg'
]

DIRS_TO_CLEAN = [
    {'name': '*.egg-info', 'flag': '.'},
    {'name': '__pycache__', 'flag': 'r'},
    {'name': 'pytest_cache', 'flag': 'r'},
    {'name': '.tox', 'flag': '.'},
    {'name': 'build', 'flag': '.'},
    {'name': 'dist', 'flag': '.'},
    {'name': 'venv*', 'flag': '.'},
    {'name': 'htmlcov', 'flag': '.'},
]
