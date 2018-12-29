#!/usr/bin/env python
# -*- coding: utf-8 -*-


import inspect
import argparse
from pathlib import Path

from . import logger
from . import settings
from . import colreqs
from . import release

_packagename = (Path(inspect.getfile(inspect.currentframe())) / '..').resolve().name
_logger = logger.create_logger(_packagename)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Python Repository Assistant",
#                                      usage="""%(prog)s <command> [<args>]
# 
# Available commands are:
#     reqs    Prepare a requirements.txt file
# """
)
#     parser.add_argument('command', action='store', default=None, help="Run specified command.")
    subparsers = parser.add_subparsers(help="Run specified command.", dest='command', required=True)
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help="Disable output")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help="Enable debug output")
    subparsers.add_parser('update_reqs', help="Prepare requirements.txt and requirements-dev.txt files. If file exists, updates it.")
    subparsers.add_parser('release', help="Prepare a release package.")
    subparsers.add_parser('upload', help="Upload a release package to the cloud.")
    args = parser.parse_args()
    
    logger.set_level(_logger, args)
    
    
    if args.command:
        command = args.command
        if command == 'update_reqs':
            cwd = Path().cwd()
            reqs = colreqs.collect_reqs_latest(cwd)
            colreqs.write_requirements(reqs, cwd)
            colreqs.write_requirements_dev(cwd)
        elif command == 'release':
            
            
    
if __name__ == '__main__':
    main()