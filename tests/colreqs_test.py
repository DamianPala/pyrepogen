
import pytest
import inspect
from pathlib import Path

from pyrepogen.colreqs import (_transform_to_min, _transform_to_latest, collect_reqs_latest)


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/colreqs_test'


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
    reqs_min = _transform_to_min(reqs)
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
    reqs_latest = _transform_to_latest(reqs)
    print(reqs_latest)
    
    assert reqs_latest == expected


def test_collect_reqs_latest():
    reqs = collect_reqs_latest(str(TESTS_SETUPS_PATH))
    
    assert reqs == ['pytest']
