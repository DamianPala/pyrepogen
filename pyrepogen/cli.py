#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import sys
from pathlib import Path
from . import logger
from . import wizard
from . import exceptions
from . import utils
from . import settings
from . import prepare
from . import (__version__)
from . import _logger


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Python Repo Generator')
    parser.add_argument('repo_path', nargs='?', action='store', default=None, 
                        help='Repo name or path to the directory when repository will be '
                        'generated. If directory does not exist then will be created. '
                        'Always enter with double quotes.')
    parser.add_argument('-c', '--config', dest='config', action='store', 
                        default=None, help='Path to repository config file.')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', 
                        default=False, help='Disable output')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', 
                        default=False, help='Enable debug output')
    parser.add_argument('-f', '--force', dest='force', action='store_true', 
                        default=False, help='Override existing files.')
    parser.add_argument('-v', '--version', dest='version', action='store_true', 
                        default=False, help='Show package version.')
    args = parser.parse_args()
    
    logger.set_level(_logger, args)
    
    cwd = Path().cwd()
        
    if args.version:
        print(__version__)
    else:
        try:
            if args.repo_path:
                repo_path = utils.get_dir_from_arg(args.repo_path)
                if args.config:
                    _logger.info(f'Generate repository from specified predefined config file {args.config}.')
                    config_path = utils.get_dir_from_arg(args.config)
                    if not config_path.exists():
                        raise exceptions.FileNotFoundError(f'Rrepository config file not exists: {config_path}', 
                                                           _logger)
                    
                    config = utils.read_repo_config_file(config_path)
                else:
                    _logger.info(f'Generate repository from the predefined config file '
                                 '{settings.FileName.REPO_CONFIG} from your current directory.')
                    config_path = Path(cwd) / settings.FileName.REPO_CONFIG
                    if not config_path.exists():
                        _logger.error(f'Predefined repository config file {settings.FileName.REPO_CONFIG} not exists!')
                        prepare.generate_repo_config(cwd, options=args)
                        sys.exit()
                    
                    config = utils.read_repo_config_file(config_path)
                    
            else:
                _logger.info('Start Python Repository Generator Wizard!')
                config_dict = {}
                
                config_dict['project_type'] = wizard.choose_one(__name__,
                                                                'Python package or standalone module layout?',
                                                                settings.ProjectType)
                config_dict['is_cloud'] = wizard.choose_bool(__name__, 'Create a cloud server feature?')
                config_dict['is_sample_layout'] = wizard.choose_bool(__name__, 'Generate sample python files?')
                config_dict['is_git'] = wizard.choose_bool(__name__, 'Initialize GIT repository?')
                if config_dict['is_git']:
                    config_dict['git_origin'] = wizard.get_data(__name__, 'Enter GIT origin url')
                config_dict['project_name'] = wizard.get_data_and_valid(__name__, 'Enter project name', [''])
                config_dict['author'] = wizard.get_data_and_valid(__name__, 'Enter author', [''])
                config_dict['author_email'] = wizard.get_data_and_valid(__name__, 'Enter author email', [''])
                config_dict['maintainer'] = wizard.get_data(__name__, 'Enter maintainer')
                config_dict['maintainer_email'] = wizard.get_data(__name__, 'Enter maintainer email')
                config_dict['short_description'] = wizard.get_data_and_valid(__name__, 
                                                                             'Enter short project description', [''])
                config_dict['home_page'] = wizard.get_data(__name__, 'Enter home page')
                config_dict['changelog_type'] = wizard.choose_one(__name__, 'Select a changelog type', 
                                                                  settings.ChangelogType)
                config_dict['authors_type'] = wizard.choose_one(__name__, 
                                                                f'Select an {settings.FileName.AUTHORS} file type',
                                                                settings.ChangelogType)
                
                config = settings.Config(**config_dict)
                
                prompt_dir = wizard.get_data(__name__, 
                                             'Enter path to the directory where a repository '
                                             'will be generated (relative or absolute)')
                repo_path = utils.get_dir_from_arg(prompt_dir)

            args.cloud = config.is_cloud
            args.sample_layout = config.is_sample_layout
            args.project_type = config.project_type
            
            prepare.generate_repo(config, cwd=repo_path, options=args)
            
        except exceptions.PyRepoGenError as e:
            e.logger.error(str(e))
            sys.exit('Repository generation error!')

        
if __name__ == '__main__':
    main()
