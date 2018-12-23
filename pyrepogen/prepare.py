
import shutil
from pathlib import Path

from . import settings
from . import logger
from pyrepogen import PARDIR


logger = logger.get_logger(__name__)

def generate_standalone_repo(cwd='.'):
    generate_standalone_repo_dirs(cwd)
    generate_standalone_repo_files(cwd)
    _prepare_repoasist(cwd)


def generate_standalone_repo_dirs(cwd='.'):
    paths = []
    for dirname in settings.STANDALONE_REPO_DIRS_TO_GEN:
        try:
            Path(Path(cwd) / dirname).mkdir()
            logger.info("{} directory generated.".format(dirname))
        except FileExistsError:
            logger.warning("{} exists, no overwritten.".format(dirname))
            
        paths.append(Path(cwd) / dirname)
        
    return paths


def generate_standalone_repo_files(cwd='.', options=None):
    paths = []
    for filename in settings.STANDALONE_REPO_FILES_TO_GEN:
        if filename == settings.REQUIREMENTS_FILENAME:
            _prepare_requirements(Path(cwd) / filename, settings.REQUIREMENTS, cwd, options)
        elif filename == settings.REQUIREMENTS_DEV_FILENAME:
            _prepare_requirements(Path(cwd) / filename, settings.REQUIREMENTS_DEV, cwd, options)
        elif filename == settings.TOX_FILENAME:
            _copy_template_file(filename, Path(cwd) / filename, cwd, options)
        elif filename == settings.LICENSE_FILENAME:
            _copy_template_file(filename, Path(cwd) / filename, cwd, options)
        elif filename == settings.GITIGNORE_FILENAME:
            _copy_template_file(filename, Path(cwd) / filename, cwd, options)
        elif filename == settings.STANDALONE_SAMPLE_FILENAME:
            _copy_template_file(filename, Path(cwd) / filename, cwd, options)
        elif filename == settings.STANDALONE_SAMPLE_TEST_FILENAME:
            _copy_template_file(filename, Path(cwd) / settings.TESTS_DIRNAME / filename, cwd, options)
        elif filename == settings.PYINIT_FILENAME:
            _copy_template_file(settings.SAMPLE_MODULE_FILENAME, Path(cwd) / settings.TESTS_DIRNAME / filename, cwd, options)
        else:
            _generate_empty_file(Path(cwd) / filename, cwd, options)
            
    

def _generate_empty_file(path, cwd, options=None):
    try:
        if options and options.force:
            with open(Path(path), 'w'):
                pass
        else:
            with open(Path(path), 'x'):
                pass
        
        logger.info("{} file generated.".format(path.relative_to(cwd)))
    except FileExistsError:
        logger.warning("{} exists, no overwritten.".format(path.relative_to(cwd)))
        
        
def _copy_template_file(filename, dst, cwd, options=None):
    if Path(dst).exists() or (options and not options.force):
        logger.warning("{} exists, no overwritten.".format(Path(dst).relative_to(cwd)))
    else:
        shutil.copy(PARDIR / settings.TEMPLATES_DIRNAME / filename, dst)
        logger.info("{} file generated.".format(Path(dst).relative_to(cwd)))
        
        
def _copy_file(filename, dst, cwd, options=None):
    if Path(dst).exists() or (options and not options.force):
        logger.warning("{} exists, no overwritten.".format(dst.relative_to(cwd)))
    else:
        shutil.copy(PARDIR / filename, dst)
        logger.info("{} file generated.".format(dst.relative_to(cwd)))
        
        
def _prepare_requirements(path, reqs, cwd, options=None):
    try:
        if options and options.force:
            with open(Path(path), 'w') as file:
                for req in reqs:
                    file.write("{}\n".format(req))
        else:
            with open(Path(path), 'x') as file:
                for req in reqs:
                    file.write("{}\n".format(req))
        
        logger.info("{} file generated.".format(path.relative_to(cwd)))
    except FileExistsError:
        logger.warning("{} exists, no overwritten.".format(path.relative_to(cwd)))
    

def _prepare_repoasist(cwd, options=None):
    for filename in settings.REPOASSIST_FILES:
        if filename == settings.REPOASSIST_MAIN_FILENAME:
            _copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / settings.REPOASSIST_TARGET_MAIN_FILENAME, cwd, options=None)
        elif filename == settings.COLREQS_FILENAME:
            _copy_file(filename, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options=None)
        elif filename == settings.PYINIT_FILENAME:
            _copy_template_file(settings.SAMPLE_MODULE_FILENAME, Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options)
        else:
            _generate_empty_file(Path(cwd) / settings.REPOASSIST_DIRNAME / filename, cwd, options)
