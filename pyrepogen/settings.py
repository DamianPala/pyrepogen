#!/usr/bin/env python
# -*- coding: utf-8 -*-


from enum import Enum
from pathlib import Path
from test.test_linecache import TEST_PATH

MIN_PYTHON = (3, 7)

SUGGESTED_INITIAL_RELEASE_TAG = '0.1.0'

REQUIREMENTS_FILENAME = 'requirements.txt'
REQUIREMENTS_PACKAGE_FILENAME = 'requirements_package.txt'
REQUIREMENTS_STANDALONE_FILENAME = 'requirements_standalone.txt'
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


REPO_CONFIG_FILENAME = 'gen_repo.cfg'

TEMPLATES_DIRNAME = 'templates'
TEMPLATES_PACKAGE_PATH = 'templates/package'
TEMPLATES_PACKAGE_TESTS_PATH = 'templates/package/tests'
DOCS_DIRNAME = 'docs'
TESTS_DIRNAME = 'tests'
TESTS_PATH = './' + TESTS_DIRNAME
DISTRIBUTION_DIRNAME = 'dist'
REPOASSIST_DIRNAME = 'repoassist'
GIT_DIRNAME = '.git'
RELEASE_DIRNAME = "release"
HTMLCOV_DIRNAME = 'htmlcov'

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
TOX_PACKAGE_FILENAME = 'tox_package.ini'
TOX_FILENAME = 'tox.ini'
PYINIT_FILENAME = '__init__.py'
MAIN_FILENAME = '__main__.py'
CLI_FILENAME = 'cli.py'
PACKAGE_SAMPLE_MODULE_FILENAME = 'modulo.py'
PACKAGE_SAMPLE_TEST_FILENAME = 'package_test.py'
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
PREPARE_FILENAME = 'prepare.py'
CLEAN_FILENAME = 'clean.py'
CLOUD_CREDENTIALS_FILENAME = "cloud_credentials.txt"
REPOASSIST_VERSION = '{}_version'.format(REPOASSIST_DIRNAME)

PROJECT_NAME_PATH_PLACEHOLDER = '<project_name>'

FILE_FORMATTER = 'autopep8'
MERGE_TOOL = 'Meld Merge'

STANDALONE_REPO_FILES_TO_GEN = [
    {'src': Path('') / README_FILENAME, 'dst': Path('.') / README_FILENAME},
    {'src': Path('') / TODO_FILENAME, 'dst': Path('.') / TODO_FILENAME},
    {'src': Path('') / CONFTEST_FILENAME, 'dst': Path('.') / CONFTEST_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / GITIGNORE_FILENAME, 'dst': Path('.') / GITIGNORE_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / TOX_STANDALONE_FILENAME, 'dst': Path('.') / TOX_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / MAKEFILE_STANDALONE_FILENAME, 'dst': Path('.') / MAKEFILE_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / LICENSE_FILENAME, 'dst': Path('.') / LICENSE_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / SETUP_CFG_STANDALONE_FILENAME, 'dst': Path('.') / SETUP_CFG_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / CLOUD_CREDENTIALS_FILENAME, 'dst': Path('.') / CLOUD_CREDENTIALS_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / REQUIREMENTS_PACKAGE_FILENAME, 'dst': Path('.') / REQUIREMENTS_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / REQUIREMENTS_DEV_FILENAME, 'dst': Path('.') / REQUIREMENTS_DEV_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / SAMPLE_MODULE_FILENAME, 'dst': Path('.') / TESTS_DIRNAME / PYINIT_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / STANDALONE_SAMPLE_FILENAME, 'dst': Path('.') / (PROJECT_NAME_PATH_PLACEHOLDER + '.py')},
    {'src': Path(TEMPLATES_DIRNAME) / STANDALONE_SAMPLE_TEST_FILENAME, 'dst': Path('.') / TESTS_DIRNAME / (PROJECT_NAME_PATH_PLACEHOLDER + '_test.py')},
]

PACKAGE_REPO_FILES_TO_GEN = [
    {'src': Path('') / README_FILENAME, 'dst': Path('.') / README_FILENAME},
    {'src': Path('') / TODO_FILENAME, 'dst': Path('.') / TODO_FILENAME},
    {'src': Path('') / CONFTEST_FILENAME, 'dst': Path('.') / CONFTEST_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / GITIGNORE_FILENAME, 'dst': Path('.') / GITIGNORE_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / TOX_PACKAGE_FILENAME, 'dst': Path('.') / TOX_FILENAME},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / PYINIT_FILENAME, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / PYINIT_FILENAME},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / MAIN_FILENAME, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / MAIN_FILENAME},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / CLI_FILENAME, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / CLI_FILENAME},
    {'src': Path(TEMPLATES_PACKAGE_PATH) / PACKAGE_SAMPLE_MODULE_FILENAME, 'dst': Path('.') / PROJECT_NAME_PATH_PLACEHOLDER / PACKAGE_SAMPLE_MODULE_FILENAME},
    {'src': Path(TEMPLATES_PACKAGE_TESTS_PATH) / PYINIT_FILENAME, 'dst': Path('.') / TESTS_DIRNAME / PYINIT_FILENAME},
    {'src': Path(TEMPLATES_PACKAGE_TESTS_PATH) / PACKAGE_SAMPLE_TEST_FILENAME, 'dst': Path('.') / TESTS_DIRNAME / PACKAGE_SAMPLE_TEST_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / MAKEFILE_PACKAGE_FILENAME, 'dst': Path('.') / MAKEFILE_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / LICENSE_FILENAME, 'dst': Path('.') / LICENSE_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / SETUP_CFG_PACKAGE_FILENAME, 'dst': Path('.') / SETUP_CFG_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / CLOUD_CREDENTIALS_FILENAME, 'dst': Path('.') / CLOUD_CREDENTIALS_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / REQUIREMENTS_PACKAGE_FILENAME, 'dst': Path('.') / REQUIREMENTS_FILENAME},
    {'src': Path(TEMPLATES_DIRNAME) / REQUIREMENTS_DEV_FILENAME, 'dst': Path('.') / REQUIREMENTS_DEV_FILENAME},
]

REPO_DIRS_TO_GEN = [
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
    PREPARE_FILENAME,
    CLEAN_FILENAME,
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
    REPOASSIST_VERSION,
    'min_python',
    'tests_path'
]

REPO_CONFIG_MANDATORY_FIELDS = CONFIG_MANDATORY_FIELDS + [
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
