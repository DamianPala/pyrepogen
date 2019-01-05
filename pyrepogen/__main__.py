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
from . import utils
from . import settings
from . import prepare
from . import (__version__, PACKAGENAME)


_logger = logger.create_logger(PACKAGENAME)

# TODO: test logging level setting

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Python Repo Generator")
    parser.add_argument('repo_path', nargs='?', action='store', default=None, 
                        help="Repo name or path to the directory when repository will be generated. If directory does not exist then will be created.")
    parser.add_argument('-c', '--config', dest='config', action='store', default=None, help="Path to repository config file.")
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help="Disable output")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help="Enable debug output")
    parser.add_argument('-f', '--force', dest='force', action='store_true', default=False, help="Override existing files.")
    parser.add_argument('-v', '--version', dest='version', action='store_true', default=False, help="Show package version.")
    args = parser.parse_args()
    
    logger.set_level(_logger, args)
    
    cwd = Path().cwd()
        
    if args.version:
        print(__version__)
    else:
        try:
            if args.repo_path:
                _logger.info("Generate repository from the predefined config file {} from your current directory.".format(settings.REPO_CONFIG_FILENAME))
                
                repo_path = utils.get_dir_from_arg(args.repo_path)
                if args.config:
                    config_path = utils.get_dir_from_arg(args.config)
                    if not config_path.exists():
                        raise exceptions.FileNotFoundError("Rrepository Config file not exists: {}".format(config_path), _logger)
                    
                    config = utils.read_config_file(config_path)
                else:
                    config_path = Path(cwd) / settings.REPO_CONFIG_FILENAME
                    if not config_path.exists():
                        _logger.error("Predefined repository config file {} not exists!".format(settings.REPO_CONFIG_FILENAME))
                        _logger.info("Creating the predefined repository config file {} in your current working directory...".format(settings.REPO_CONFIG_FILENAME))
                        prepare.generate_repo_config(cwd)
                        _logger.info("Predefined repository config file created. Please fill it with relevant data and try to generate repository again!")
                        sys.exit()
                    
                    config = utils.read_config_file(config_path)
                    
#                 TODO: check fields with specified value against incorrect value, check if field is not empty in validate config 
                utils.validate_repo_config_metadata(config['metadata'])
                    
                project_type = config['metadata']['project_type']
                is_cloud = config['metadata']['is_cloud']
                is_sample_layout = config['metadata']['is_sample_layout']
                
            else:
                _logger.info("Start Python Repository Generator Wizard!")
                config = {}
                config['metadata'] = {}
                
                config['metadata']['project_type'] = wizard.choose_one(__name__, "Python package or standalone script layout?", settings.ProjectType)
                project_type = config['metadata']['project_type']
                is_cloud = wizard.choose_bool(__name__, "Create a cloud server feature?")
                is_sample_layout = wizard.choose_bool(__name__, "Generate sample python files?")
                config['metadata']['repo_name'] = wizard.get_data(__name__, "Enter repository name")
                config['metadata']['project_name'] = wizard.get_data(__name__, "Enter project name")
                config['metadata']['author'] = wizard.get_data(__name__, "Enter author")
                config['metadata']['author_email'] = wizard.get_data(__name__, "Enter author email")
                config['metadata']['maintainer'] = wizard.get_data(__name__, "Enter maintainer")
                config['metadata']['maintainer_email'] = wizard.get_data(__name__, "Enter maintainer email")
                config['metadata']['short_description'] = wizard.get_data(__name__, "Enter short project description")
                config['metadata']['home_page'] = wizard.get_data(__name__, "Enter home page")
                config['metadata']['changelog_type'] = wizard.choose_one(__name__, "Select a changelog type", settings.ChangelogType)
                utils.add_auto_config_fields(config)
                
                prompt_dir = wizard.get_data(__name__, "Enter path to the directory where a repository will be generated (relative or absolute)")
                repo_path = utils.get_dir_from_arg(prompt_dir)

            args.cloud = is_cloud
            args.sample_layout = is_sample_layout
                
            if project_type == settings.ProjectType.PACKAGE.value:
                prepare.generate_package_repo(config, cwd=repo_path, options=args)
            elif project_type == settings.ProjectType.SCRIPT.value:
                prepare.generate_standalone_repo(config, cwd=repo_path, options=args)
            else:
                sys.exit("Unknown project type.")
        except exceptions.PyRepoGenError as e:
            e.logger.error(str(e))
            sys.exit("Repository generation error!")

        
if __name__ == '__main__':
    main()
    