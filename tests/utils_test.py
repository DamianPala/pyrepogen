
import pytest
import inspect
import stat
import shutil
import time
from pathlib import Path
from pprint import pprint

from pyrepogen import utils, logger, settings, exceptions


TESTS_SETUPS_PATH = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent / 'tests_setups/utils_test'
SKIP_ALL_MARKED = False

_logger = logger.create_logger()


class Args:
    force = True
    cloud = False


def _error_remove_readonly(_action, name, _exc):
    Path(name).chmod(stat.S_IWRITE)
    Path(name).unlink()


@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_read_repo_config_file_SHOULD_read_config_properly():
    cwd = TESTS_SETUPS_PATH / 'test_read_repo_config_file_SHOULD_read_config_properly'
    Path(cwd).mkdir(parents=True, exist_ok=True)

    expected_config = settings.Config(
        project_type=settings.ProjectType.MODULE.value,
        repo_name='sample-repo',
        project_name='sample_project',
        author='Damian',
        author_email='damian@mail.com',
        short_description='This is a sample project.',
        changelog_type=settings.ChangelogType.GENERATED.value,
        is_cloud=True,
        is_sample_layout=True,
        home_page='page.com',
        maintainer='Mike',
        maintainer_email='mike@mail.com',
        is_git = True,
    )
    setattr(expected_config, settings.REPOASSIST_VERSION, settings.__version__)
    
    config = utils.read_repo_config_file(Path(cwd) / settings.FileName.REPO_CONFIG)
    pprint(config.__dict__)
    
    assert config.__dict__ == expected_config.__dict__
    
    
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_read_repo_config_file_SHOULD_raise_error_when_no_field():
    cwd = TESTS_SETUPS_PATH / 'test_read_repo_config_file_SHOULD_raise_error_when_no_field'
    Path(cwd).mkdir(parents=True, exist_ok=True)

    try:
        utils.read_repo_config_file(Path(cwd) / settings.FileName.REPO_CONFIG)
        assert False, "Error was expected but not occured!"
    except exceptions.ConfigError as e:
        assert "Invalid config file structure" in str(e)
    

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_get_repo_config_from_setup_cfg_SHOULD_read_config_properly():
    cwd = TESTS_SETUPS_PATH / 'test_get_repo_config_from_setup_cfg_SHOULD_read_config_properly'
    Path(cwd).mkdir(parents=True, exist_ok=True)


    expected_config = settings.Config(
        project_type=settings.ProjectType.MODULE.value,
        repo_name='sample-repo',
        project_name='sample_project',
        author='Damian',
        author_email='damian@mail.com',
        short_description='This is a sample project.',
        changelog_type=settings.ChangelogType.GENERATED.value,
        home_page='page.com',
        maintainer='Mike',
        maintainer_email='mike@mail.com',
        keywords=['sample_project'],
        license=settings.LICENSE,
    )

    config = utils.get_repo_config_from_setup_cfg(Path(cwd) / settings.FileName.SETUP_CFG)
    pprint(config.__dict__)

    assert config == expected_config
    

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_validate_config_SHOULD_raise_error_when_field_is_empty():
    config = settings.Config(
        project_type=settings.ProjectType.MODULE.value,
        repo_name='',
        project_name='sample_project',
        author='Damian',
        author_email='damian@mail.com',
        short_description='This is a sample project.',
        changelog_type=settings.ChangelogType.GENERATED.value,
        home_page='page.com',
        maintainer='Mike',
        maintainer_email='mike@mail.com',
        keywords=['sample_project'],
        license=settings.LICENSE,
    )
    
    try:
        utils._validate_config(config)
        assert False, "Error was expected but not occured!"
    except exceptions.ConfigError as e:
        assert "The repo_name field is empty in the config" in str(e)
        

validate_repo_config_metadata_testdata = [
    (    
        settings.Config(
            project_type='raise error',
            repo_name='sample-repo',
            project_name='sample_project',
            author='Damian',
            author_email='damian@mail.com',
            short_description='This is a sample project.',
            changelog_type=settings.ChangelogType.GENERATED.value,
            home_page='page.com',
            maintainer='Mike',
            maintainer_email='mike@mail.com',
            keywords=['sample_project'],
            license=settings.LICENSE,
            is_cloud=True,
            is_sample_layout=True,
        ), 
        "The project_type field has invalid value"
    ),
    (
        settings.Config(
            project_type=settings.ProjectType.MODULE.value,
            repo_name='sample-repo',
            project_name='sample_project',
            author='Damian',
            author_email='damian@mail.com',
            short_description='This is a sample project.',
            changelog_type='raise error',
            home_page='page.com',
            maintainer='Mike',
            maintainer_email='mike@mail.com',
            keywords=['sample_project'],
            license=settings.LICENSE,
            is_cloud=True,
            is_sample_layout=True,
        ),
        "The changelog_type field has invalid value"
    ),
    (    
        settings.Config(
            project_type=settings.ProjectType.MODULE.value,
            repo_name='sample-repo',
            project_name='sample_project',
            author='Damian',
            author_email='damian@mail.com',
            short_description='This is a sample project.',
            changelog_type=settings.ChangelogType.GENERATED.value,
            home_page='page.com',
            maintainer='Mike',
            maintainer_email='mike@mail.com',
            keywords=['sample_project'],
            license=settings.LICENSE,
            is_cloud='raise error',
            is_sample_layout=True,
        ),
        "The is_cloud field has invalid value"
    ),
    (
        settings.Config(
            project_type=settings.ProjectType.MODULE.value,
            repo_name='sample-repo',
            project_name='sample_project',
            author='Damian',
            author_email='damian@mail.com',
            short_description='This is a sample project.',
            changelog_type=settings.ChangelogType.GENERATED.value,
            home_page='page.com',
            maintainer='Mike',
            maintainer_email='mike@mail.com',
            keywords=['sample_project'],
            license=settings.LICENSE,
            is_cloud=True,
            is_sample_layout='raise error',
        ),
        "The is_sample_layout field has invalid value"
    ),
]
 
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
@pytest.mark.parametrize("config, expected", validate_repo_config_metadata_testdata)
def test_validate_repo_config_metadata_SHOULD_raise_error_when_field_is_invalid(config, expected):
    try:
        utils._validate_config(config, extra_fields=settings.GEN_REPO_CONFIG_MANDATORY_FIELDS)
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

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
@pytest.mark.parametrize("path, expected", get_dest_dir_testdata)
def test_get_dest_dir(path, expected):
    dest_dir = utils.get_dir_from_arg(path)
    
    print(dest_dir.as_posix())
    print(expected)
    
    assert dest_dir.as_posix() == expected
    

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_get_latest_file_SHOULD_return_if_path_not_exists():
    cwd = TESTS_SETUPS_PATH / 'test_get_latest_file_SHOULD_return_if_path_not_exists'

    assert utils.get_latest_file(cwd) == None
    

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_get_latest_file_SHOULD_return_if_path_is_empty():
    cwd = TESTS_SETUPS_PATH / 'test_get_latest_file_SHOULD_return_if_path_is_empty'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)

    assert utils.get_latest_file(cwd) == None    
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_get_latest_file_SHOULD_return_if_path_is_file():
    cwd = TESTS_SETUPS_PATH / 'test_get_latest_file_SHOULD_return_if_path_is_file'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)

    path = Path(cwd) / 'file.txt'
    path.touch()
    
    assert utils.get_latest_file(path) == None    
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        
        
@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_get_latest_file_SHOULD_return_if_path_does_not_contain_files():
    cwd = TESTS_SETUPS_PATH / 'test_get_latest_file_SHOULD_return_if_path_does_not_contain_files'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    Path(Path(cwd) / 'test1').mkdir(parents=True, exist_ok=True)
    Path(Path(cwd) / 'test2').mkdir(parents=True, exist_ok=True)

    assert utils.get_latest_file(cwd) == None
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
        

@pytest.mark.skipif(SKIP_ALL_MARKED, reason="Skipped on request")
def test_get_latest_file_SHOULD_return_proper_latest_file():
    cwd = TESTS_SETUPS_PATH / 'test_get_latest_file_SHOULD_return_proper_latest_file'
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)
    Path(cwd).mkdir(parents=True, exist_ok=True)
    
    Path(Path(cwd) / 'test1.txt').touch()
    time.sleep(1)
    Path(Path(cwd) / 'test2.txt').touch()
    time.sleep(1)
    Path(Path(cwd) / 'test3.txt').touch()

    assert utils.get_latest_file(cwd) == Path(cwd) / 'test3.txt'
    
    if Path(cwd).exists():
        shutil.rmtree(Path(cwd), ignore_errors=False, onerror=_error_remove_readonly)

        
        