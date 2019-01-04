#!/usr/bin/env python
# -*- coding: utf-8 -*-


import inspect
import argparse
import sys
from pathlib import Path

from . import logger
from . import colreqs
from . import release
from . import exceptions
from . import cloud
from . import formatter


_PACKAGENAME = (Path(inspect.getfile(inspect.currentframe())) / '..').resolve().name
_logger = logger.create_logger(_PACKAGENAME)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Python Repository Assistant")
    subparsers = parser.add_subparsers(help="Available commands are:", dest='command', required=True)
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help="Disable output")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help="Enable debug output")
    subparsers.add_parser('update_reqs', help="Prepare requirements.txt and requirements-dev.txt files. If file exists, updates it.")
    subparsers.add_parser('release', help="Prepare a release package.")
    subparsers.add_parser('upload', help="Upload a release package to the cloud.")
    subparsers.add_parser('list_cloud', help="List buckets on the cloud server.")
    subparsers.add_parser('download_package', help="Download package from the cloud server.")
    format_parser = subparsers.add_parser('format', help="Format a python source file using autopep8.")
    format_parser.add_argument('path', action='store', default=None, help="Path to the python source file.")

    args = parser.parse_args()
    
    logger.set_level(_logger, args)
    
    cwd = Path().cwd()
    
    if args.command:
        command = args.command
        try:
            if command == 'update_reqs':
                reqs = colreqs.collect_reqs_latest(cwd)
                colreqs.write_requirements(reqs, cwd)
                colreqs.write_requirements_dev(cwd)
            elif command == 'release':
                release.make_release(cwd)
            elif command == 'upload':
                cloud.upload_to_cloud(cwd)
            elif command == 'list_cloud':
                cloud.list_cloud(cwd)
            elif command == 'download_package':
                cloud.download_package(cwd)
            elif command == 'format':
                formatter.format_file(args.path, cwd=cwd)
            else:
                _logger.error("Invalid command.")
        except exceptions.PyRepoGenError as e:
            e.logger.error(str(e))
            sys.exit("Repoasist error!")
            
    
if __name__ == '__main__':
    main()
    