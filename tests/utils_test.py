
import pytest
import inspect
import shutil
import stat
from pathlib import Path
from pprint import pprint

from pyrepogen import utils, logger


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/utils_test'

_logger = logger.create_logger()


class Args:
    force = True
    cloud = False
    
    
def _error_remove_readonly(_action, name, _exc):
    Path(name).chmod(stat.S_IWRITE)
    Path(name).unlink()


def test_read_setup_cfg_SHOULD_read_config_properly():
    cwd = TESTS_SETUPS_PATH / 'test_read_setup_cfg_SHOULD_read_config_properly'
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    expected_config = {
        'metadata': {
            'author': 'Damian',
            'author_email': 'damian@mail.com',
            'home_page': 'page.com',
            'maintainer': 'Mike',
            'maintainer_email': 'mike@mail.com',
            'project_name': 'sample_project',
            'repo_name': 'sample-repo',
            'short_description': 'This is a sample project',
            'year': '2018'
        },    
    }
    
    config = utils.read_setup_cfg(cwd)
    pprint(config)
    
    assert config == expected_config
