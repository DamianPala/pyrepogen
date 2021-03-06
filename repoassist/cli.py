#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import shutil
import argparse
from pathlib import Path

from . import logger
from . import colreqs
from . import release
from . import exceptions
from . import sicloudman
from . import meldformat
from . import clean
from . import utils
from . import settings
from . import _logger
from . import reltools


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Python Repository Assistant')
    subparsers = parser.add_subparsers(help='Available commands are:', dest='command', required=True)
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help='Disable output')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='Enable debug output')
    subparsers.add_parser('update_reqs', 
                          help='Prepare requirements.txt and requirements-dev.txt files. If file exists, updates it.')
    release_parser = subparsers.add_parser('release', help='Prepare a source distribution package.')
    release_parser.add_argument('force', nargs='?', action='store', default=False, 
                                help='Force action, no repository check, no git check.')
    install_parser = subparsers.add_parser('install', help='Install a package.')
    install_parser.add_argument('force', nargs='?', action='store', default=False, 
                                help='Force action, no repository check, no git check.')    
    subparsers.add_parser('upload', help='Upload a source distribution package to the cloud.')
    subparsers.add_parser('list_cloud', help='List buckets on the cloud server.')
    subparsers.add_parser('download_package', help='Download package from the cloud server.')
    subparsers.add_parser('clean', help='Clean repository from dummy files.')
    subparsers.add_parser('coverage_report', help='Show the html coverage report in the default system browser.')
    subparsers.add_parser('update', help='Update Repoassist to version from installed Pyrepogen.')
    format_parser = subparsers.add_parser('format', help='Format a python source file using autopep8.')
    format_parser.add_argument('path', action='store', default=None, help='Path to the python source file.')

    args = parser.parse_args()

    logger.set_level(_logger, args)

    if args.command:
        cwd = Path().cwd()
        command = args.command
        cloud_manager = sicloudman.CloudManager(settings.DirName.DISTRIBUTION,
                                                [sicloudman.Bucket(name='source', keywords=['.tar.gz']),
                                                 sicloudman.Bucket(name='binary', keywords=['.whl'])],
                                                credentials_path=settings.FileName.CLOUD_CREDENTIALS,
                                                get_logger=logger.get_logger,
                                                cwd=cwd)

        try:
            if command == 'update_reqs':
                config = utils.get_repo_config_from_setup_cfg(Path(cwd) / settings.FileName.SETUP_CFG)
                if config.project_type == settings.ProjectType.PACKAGE.value:
                    reqs_cwd = cwd / config.project_name
                else:
                    reqs_cwd = cwd
                reqs = colreqs.collect_reqs_min(config, prompt=True, cwd=reqs_cwd)
                colreqs.write_requirements(reqs, cwd)
                colreqs.write_requirements_dev(cwd)
            elif command == 'release':
                release.make_release(options=args, cwd=cwd)
            elif command == 'install':
                release.make_install(options=args, cwd=cwd)
            elif command == 'upload':
                cloud_manager.upload_artifacts()
            elif command == 'list_cloud':
                cloud_manager.list_cloud()
            elif command == 'download_package':
                cloud_manager.download_file()
            elif command == 'format':
                meldformat.format_file(meldformat.Formatter.AUTOPEP8, args.path, 
                                       setup_path=cwd / settings.FileName.SETUP_CFG, 
                                       get_logger=logger.get_logger)
            elif command == 'coverage_report':
                utils.coverage_report(cwd)
            elif command == 'update':
                if not shutil.which('pyrepogen'):
                    raise exceptions.RuntimeError('Pyrepogen not found. '
                                                  'Please check if it is installed properly', _logger)
                print(utils.execute_cmd(('pyrepogen', '-u', '.'), cwd).strip())
            elif command == 'clean':
                clean.clean(cwd)
            else:
                _logger.error('Invalid command.')
        except (exceptions.PyRepoGenError, sicloudman.SiCloudManError, meldformat.MeldFormatError, reltools.RelToolsError) as e:
            e.logger.error(str(e))
            sys.exit('Repoasist error!')
            
    
if __name__ == '__main__':
    main()
    