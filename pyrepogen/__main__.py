#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import logging
import inspect
import sys
import datetime
from pathlib import Path
from pprint import pprint
from .mod1 import *
from . import logger
from . import wizard
from . import prepare
from . import exceptions


IS_DEBUG = True


_packagename = (Path(inspect.getfile(inspect.currentframe())) / '..').resolve().name
_logger = logger.create_logger(_packagename)

# TODO: test logging level setting



def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Python Repo Generator",
                                     epilog="""Available commands: ...""")
    parser.add_argument('repo_path', nargs='?', action='store', default=None, help="Repo name or path to the directory when repository will be generated. If directory does not exist then will be created.")
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help="Disable output")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help="Enable debug output")
    parser.add_argument('-f', '--force', dest='force', action='store_true', default=False, help="Override existing files.")
    parser.add_argument('-v', '--version', dest='version', action='store_true', default=False, help="Show package version.")
    args = parser.parse_args()
    
    logger.set_level(_logger, args)
        
    if args.version:
#         TODO: add show version
        pass
    else:
        try:
            if args.repo_path:
                _logger.info("Generate repository from predefined config") # TODO: add config file name in msg
                
                
            else:
                _logger.info("Start Python Repository Generator Wizard!")
                config = {}
                config['metadata'] = {}
                
                if not IS_DEBUG:
                    project_type = wizard.choose_one(__name__, "Python package or standalone script layout?", ['package', 'script'])
                    is_cloud = wizard.choose_bool(__name__, "Create a cloud server feature?")
                    is_sample_layout = wizard.choose_bool(__name__, "Generate sample python files?")
                    config['metadata']['repo_name'] = wizard.get_data(__name__, "Enter repository name")
                    config['metadata']['project_name'] = wizard.get_data(__name__, "Enter project name")
                    prompt_dir = wizard.get_data(__name__, "Enter path to the directory where a repository will be generated (relative or absolute)")
                    dest_dir = _get_dest_dir(prompt_dir)
                    config['metadata']['author'] = wizard.get_data(__name__, "Enter author")
                    config['metadata']['author_email'] = wizard.get_data(__name__, "Enter author email")
                    config['metadata']['maintainer'] = wizard.get_data(__name__, "Enter maintainer")
                    config['metadata']['maintainer_email'] = wizard.get_data(__name__, "Enter maintainer email")
                    config['metadata']['short_description'] = wizard.get_data(__name__, "Enter short project description")
                    config['metadata']['home_page'] = wizard.get_data(__name__, "Enter home page")
                    config['metadata']['year'] = str(datetime.datetime.now().year)
                    
                    args.cloud = is_cloud
                    args.sample_layout = is_sample_layout
                else:
                    _get_mock_data(config, args)
                    dest_dir = _get_dest_dir('sandbox')
                    project_type = 'script'
                
                if project_type == 'package':
                    pass
                elif project_type == 'script':
                    prepare.generate_standalone_repo(config, cwd=dest_dir, options=args)
                else:
                    sys.exit("Unknown project type.")
        except exceptions.PyRepoGenError as e:
            e.logger.error(str(e))
            sys.exit("Repository generation error!")
            


def _get_mock_data(config, args):
    config['metadata']['author'] = 'damian'
    config['metadata']['author_email'] = 'damian@mail.com'
    config['metadata']['home_page'] = 'myproject.com'
    config['metadata']['maintainer'] = 'mike'
    config['metadata']['maintainer_email'] = 'mike@mail.com'
    config['metadata']['project_name'] = 'my_project'
    config['metadata']['repo_name'] = 'myrepo'
    config['metadata']['short_description'] = 'This is super project.'
    config['metadata']['year'] = '2018'
    
    args.cloud = True
    args.sample_layout = True



def _get_dest_dir(prompt_dir):
    if Path(prompt_dir).is_absolute():
        return prompt_dir
    else:
        return (Path().cwd() / prompt_dir).resolve()
    
        
if __name__ == '__main__':
    main()
    