'''
Created on 20.12.2018

@author: Haz
'''


import argparse
import logging
import inspect
from pathlib import Path
from .logger import get_logger
from .mod1 import *
from . import wizard

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Python Repo Generator",
                                     epilog="""Available commands: ...""")
    parser.add_argument('repo_path', nargs='?', action='store', default=None, help="Repo name or path to the directory when repository will be generated. If directory does not exist then will be created.")
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help="Disable output")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help="Enable debug output")
    args = parser.parse_args()
    
    set_logger(args)
        
    logger.debug("debug log")
    
    if args.repo_path:
        logger.info("Generate repo")
    else:
        logger.info("Start Python Repository Generator Wizard!")
        is_python_package = wizard.choose_one(__name__, "Python package or standalone script layout?", ['package', 'script'])
        repo_name = wizard.get_data(__name__, "Enter repository name")
        project_name = wizard.get_data(__name__, "Enter project name")
        dest_dir = wizard.get_data(__name__, "Enter path to the directory where a repository will be generated")
        author = wizard.get_data(__name__, "Enter author")
        author_email = wizard.get_data(__name__, "Enter author email")
        maintainer = wizard.get_data(__name__, "Enter maintainer")
        maintainer_email = wizard.get_data(__name__, "Enter maintainer email")
        short_description = wizard.get_data(__name__, "Enter short project description")
        home_page = wizard.get_data(__name__, "Enter home page")
        
        
        
        
        
#         print(wizard.get_data(__name__, "Enter repository name"))
#         print(wizard.is_checkpoint_ok(__name__, "Is al ok?", choices=['y', 'n'], valid_value='y'))
#         print(wizard.choose_one(__name__, "Select one?", choices=['dev', 'release']))
    
#     print(args.repo_path)
    
#     logger.warn("Wath out!")
#     logger.info("I told you")
#     logger.tip("This is a tip")
#     mod1_msg()
#     logger.tip("This is a tip2")
#     logger.wizard("Input file name")
#     logger.checkpoint("This is checkpoitn")
    
    
def set_logger(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif not args.quiet:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.CRITICAL)

    
if __name__ == '__main__':
    main()
    