
import pytest
import inspect
import os
import stat
import shutil
from pathlib import Path

from pyrepogen import logger
_logger = logger.create_logger(name=None)
from pyrepogen import colreqs, settings


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/colreqs_test'



def _error_remove_readonly(_action, name, _exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)
    

transform_to_min_testdata = [
    (
        ['setuptools==40.5.0', 'pytest==3.7.2', 'Jinja2==2.7.3'],
        ['setuptools>=40.5.0', 'pytest>=3.7.2', 'Jinja2>=2.7.3'],
    ),
    (
        ['setuptools==40.5.0', 'pytest>=3.7.2', 'Jinja2==2.7.3'],
        ['setuptools>=40.5.0', 'pytest>=3.7.2', 'Jinja2>=2.7.3'],
    ),
]
@pytest.mark.parametrize("reqs, expected", transform_to_min_testdata)
def test_transform_to_min(reqs, expected):
    reqs_min = colreqs._transform_to_min(reqs)
    print(reqs_min)
    
    assert reqs_min == expected


transform_to_latest_testdata = [
    (
        ['setuptools==40.5.0', 'pytest==3.7.2', 'Jinja2==2.7.3'],
        ['setuptools', 'pytest', 'Jinja2'],
    ),
    (
        ['setuptools==40.5.0', 'pytest>=3.7.2', 'Jinja2==2.7.3'],
        ['setuptools', 'pytest', 'Jinja2'],
    ),
]
@pytest.mark.parametrize("reqs, expected", transform_to_latest_testdata)
def test_transform_to_latest(reqs, expected):
    reqs_latest = colreqs._transform_to_latest(reqs)
    print(reqs_latest)
    
    assert reqs_latest == expected


def test_collect_reqs_latest_SHOULD_collect_reqs_properly():
    cwd = TESTS_SETUPS_PATH / 'test_collect_reqs_latest_SHOULD_collect_reqs_properly'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    reqs = colreqs.collect_reqs_latest(cwd)
    print(reqs)
    
    assert reqs == ['pytest']
    
    
def test_collect_reqs_latest_SHOULD_exclude_repoassist_reqs_properly():
    cwd = TESTS_SETUPS_PATH / 'test_collect_reqs_latest_SHOULD_exclude_repoassist_reqs_properly'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    reqs = colreqs.collect_reqs_latest(cwd)
    print(reqs)
    
    assert reqs == ['pytest']


def test_write_requirements_SHOULD_print_proper_message_when_prepare(caplog):
    cwd = TESTS_SETUPS_PATH / 'test_write_requirements_SHOULD_print_proper_message_when_prepare'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    reqs_path = Path(cwd) / settings.FileName.REQUIREMENTS
    if (reqs_path).exists():
        reqs_path.unlink()
    
    reqs = ['flask', 'pytest>=3.7.2', 'Jinja2==2.7.3']
    ret_path = colreqs.write_requirements(reqs, cwd)
    
    shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    
    assert "requirements.txt file prepared" in caplog.text
    assert ret_path == reqs_path
    
    
def test_write_requirements_SHOULD_print_proper_message_when_update(caplog):
    cwd = TESTS_SETUPS_PATH / 'test_write_requirements_SHOULD_print_proper_message_when_update'
    Path(cwd).mkdir(parents=True, exist_ok=True)
     
    reqs_path = Path(cwd) / settings.FileName.REQUIREMENTS
    with open(reqs_path, 'w'):
        pass
     
    reqs = ['flask', 'pytest>=3.7.2', 'Jinja2==2.7.3']
    ret_path = colreqs.write_requirements(reqs, cwd)
    
    shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
     
    assert "requirements.txt file updated" in caplog.text
    assert ret_path == reqs_path
    
    
def test_write_requirements_dev_SHOULD_not_overwriting_reqs_if_exists(caplog):
    cwd = TESTS_SETUPS_PATH / 'test_write_requirements_dev_SHOULD_not_overwriting_reqs_if_exists'
    Path(cwd).mkdir(parents=True, exist_ok=True)
     
    reqs_path = Path(cwd) / settings.FileName.REQUIREMENTS_DEV
    with open(reqs_path, 'w'):
        pass
     
    ret_path = colreqs.write_requirements_dev(cwd)
    
    shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    
    assert "requirements-dev.txt file already exists, not overwritten" in caplog.text
    assert ret_path == reqs_path
    