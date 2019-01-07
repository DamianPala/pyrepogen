
import pytest
import inspect
import stat
import datetime
from pathlib import Path
from pprint import pprint

from pyrepogen import utils, logger, settings, exceptions
from pyrepogen.pygittools import add


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/utils_test'

_logger = logger.create_logger()


class Args:
    force = True
    cloud = False


def _error_remove_readonly(_action, name, _exc):
    Path(name).chmod(stat.S_IWRITE)
    Path(name).unlink()


def test_read_repo_config_file_SHOULD_read_config_properly():
    cwd = TESTS_SETUPS_PATH / 'test_read_repo_config_file_SHOULD_read_config_properly'
    Path(cwd).mkdir(parents=True, exist_ok=True)

    expected_config = {
        'project_type': settings.ProjectType.SCRIPT.value,
        'author': 'Damian',
        'author_email': 'damian@mail.com',
        'home_page': 'page.com',
        'maintainer': 'Mike',
        'maintainer_email': 'mike@mail.com',
        'project_name': 'sample_project',
        'repo_name': 'sample-repo',
        'short_description': 'This is a sample project.',
        'changelog_type': settings.ChangelogType.GENERATED.value,
        'is_cloud': 'True',
        'is_sample_layout': 'True',
    }
    utils.add_auto_config_fields(expected_config)
    
    
    config = utils.read_repo_config_file(Path(cwd) / settings.REPO_CONFIG_FILENAME)
    pprint(config)

    assert config == expected_config
    
    
def test_get_repo_config_from_setup_cfg_SHOULD_read_config_properly():
    cwd = TESTS_SETUPS_PATH / 'test_get_repo_config_from_setup_cfg_SHOULD_read_config_properly'
    Path(cwd).mkdir(parents=True, exist_ok=True)

    expected_config = {
        'project_type': settings.ProjectType.SCRIPT.value,
        'author': 'Damian',
        'author_email': 'damian@mail.com',
        'home_page': 'page.com',
        'maintainer': 'Mike',
        'maintainer_email': 'mike@mail.com',
        'project_name': 'sample_project',
        'repo_name': 'sample-repo',
        'short_description': 'This is a sample project.',
        'changelog_type': settings.ChangelogType.GENERATED.value,
        'description_file': settings.README_FILENAME,
        'keywords': ['sample_project'],
        'license': settings.LICENSE,
    }
    utils.add_auto_config_fields(expected_config)
    
    config = utils.get_repo_config_from_setup_cfg(Path(cwd) / settings.SETUP_CFG_FILENAME)
    pprint(config)

    for key in expected_config:
        assert config[key] == expected_config[key]
        
    
def test_validate_config_SHOULD_raise_error_when_field_is_empty():
    config = {
        'project_type': settings.ProjectType.SCRIPT.value,
        'repo_name': '',
        'project_name': 'sample_project',
        'author': 'Damian', 
        'author_email': 'mail@mail.com',
        'short_description': 'This is a sample project',
        'changelog_type': settings.ChangelogType.GENERATED.value,
        'year': '2018',
        'repoassist_version': '0.1.0',
        'min_python': '3.7',
        'tests_path': settings.TESTS_PATH
    }
    
    try:
        utils.validate_config_metadata(config)
        assert False, "Error was expected but not occured!"
    except exceptions.ConfigError as e:
        assert "The repo_name field is empty in the config" in str(e)
        
        
validate_repo_config_metadata_testdata = [
    (    
        {
            'project_type': 'raise error',
            'repo_name': 'myrepo',
            'project_name': 'sample_project',
            'author': 'Damian', 
            'author_email': 'mail@mail.com',
            'short_description': 'This is a sample project',
            'changelog_type': settings.ChangelogType.GENERATED.value,
            'year': '2018',
            'repoassist_version': '0.1.0',
            'min_python': '3.7',
            'tests_path': settings.TESTS_PATH,
            'is_cloud': 'true',
            'is_sample_layout': 'true',
        }, 
        "The project_type field has invalid value in the config"
    ),
    (    
        {
            'project_type': 'script',
            'repo_name': 'myrepo',
            'project_name': 'sample_project',
            'author': 'Damian', 
            'author_email': 'mail@mail.com',
            'short_description': 'This is a sample project',
            'changelog_type': 'raise error',
            'year': '2018',
            'repoassist_version': '0.1.0',
            'min_python': '3.7',
            'tests_path': settings.TESTS_PATH,
            'is_cloud': 'true',
            'is_sample_layout': 'true',
        }, 
        "The changelog_type field has invalid value in the config"
    ),
    (    
        {
            'project_type': 'script',
            'repo_name': 'myrepo',
            'project_name': 'sample_project',
            'author': 'Damian', 
            'author_email': 'mail@mail.com',
            'short_description': 'This is a sample project',
            'changelog_type': 'generated',
            'year': '2018',
            'repoassist_version': '0.1.0',
            'min_python': '3.7',
            'tests_path': settings.TESTS_PATH,
            'is_cloud': 'raise error',
            'is_sample_layout': 'true',
        }, 
        "The is_cloud field has invalid value in the config"
    ),
    (    
        {
            'project_type': 'script',
            'repo_name': 'myrepo',
            'project_name': 'sample_project',
            'author': 'Damian', 
            'author_email': 'mail@mail.com',
            'short_description': 'This is a sample project',
            'changelog_type': 'generated',
            'year': '2018',
            'repoassist_version': '0.1.0',
            'min_python': '3.7',
            'tests_path': settings.TESTS_PATH,
            'is_cloud': 'false',
            'is_sample_layout': 'raise error',
        }, 
        "The is_sample_layout field has invalid value in the config"
    ),
]
 
@pytest.mark.parametrize("config_metadata, expected", validate_repo_config_metadata_testdata)
def test_validate_repo_config_metadata_SHOULD_raise_error_when_field_is_invalid(config_metadata, expected):
    try:
        utils.validate_repo_config_metadata(config_metadata)
        assert False, "Error was expected but not occured!"
    except exceptions.ConfigError as e:
        assert expected in str(e)


get_dest_dir_testdata = [
    (r"repo", (Path().cwd() / "repo").as_posix()),
    (r"dir1/repo", (Path().cwd() / "dir1/repo").as_posix()),
    (r"./repo", (Path().cwd() / "repo").as_posix()),
    (r"dir1\repo", (Path().cwd() / "dir1/repo").as_posix()),
    (r"C:\dir1\repo", Path("C:/dir1/repo").as_posix()),
    (r"C:/dir1/repo", Path("C:/dir1/repo").as_posix()),
]

@pytest.mark.parametrize("path, expected", get_dest_dir_testdata)
def test_get_dest_dir(path, expected):
    dest_dir = utils.get_dir_from_arg(path)
    
    print(dest_dir.as_posix())
    print(expected)
    
    assert dest_dir.as_posix() == expected
    
