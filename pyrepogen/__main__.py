#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import logging
import inspect
from pathlib import Path
from .mod1 import *
from . import logger
from . import wizard

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
#     TODO: add option no template module generate
    args = parser.parse_args()
    
    logger.set_level(_logger, args)
        
    _logger.debug("debug log")
    
    print(args)
    
#     if args.repo_path:
#         _logger.info("Generate repo")
#     else:
#         _logger.info("Start Python Repository Generator Wizard!")
#         is_python_package = wizard.choose_one(__name__, "Python package or standalone script layout?", ['package', 'script'])
#         repo_name = wizard.get_data(__name__, "Enter repository name")
#         project_name = wizard.get_data(__name__, "Enter project name")
#         dest_dir = wizard.get_data(__name__, "Enter path to the directory where a repository will be generated")
#         author = wizard.get_data(__name__, "Enter author")
#         author_email = wizard.get_data(__name__, "Enter author email")
#         maintainer = wizard.get_data(__name__, "Enter maintainer")
#         maintainer_email = wizard.get_data(__name__, "Enter maintainer email")
#         short_description = wizard.get_data(__name__, "Enter short project description")
#         home_page = wizard.get_data(__name__, "Enter home page")
        
        
        
        
        
#         print(wizard.get_data(__name__, "Enter repository name"))
#         print(wizard.is_checkpoint_ok(__name__, "Is al ok?", choices=['y', 'n'], valid_value='y'))
#         print(wizard.choose_one(__name__, "Select one?", choices=['dev', 'release']))
    
#     print(args.repo_path)
    
    _logger.warning("Wath out!")
    _logger.info("I told you")
    _logger.tip("This is a tip")
    mod1_msg()
    _logger.tip("This is a tip2")
    _logger.wizard("Input file name")
    _logger.checkpoint("This is checkpoitn")
    
    
if __name__ == '__main__':
    main()
    