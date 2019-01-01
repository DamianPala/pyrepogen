#!/usr/bin/env python
# -*- coding: utf-8 -*-


import configparser
import ftplib
import os
import datetime
import logging
from pathlib import Path

from . import exceptions
from . import settings
from . import wizard


_logger = logging.getLogger(__name__)


def upload_to_cloud(cwd='.', prompt=True):
    _logger.info("Upload packages to the cloud server...")
    latest_release_package_path = _get_latest_package_path(Path(cwd) / settings.RELEASE_DIRNAME)

    if prompt:
        if latest_release_package_path:
            if not wizard.is_checkpoint_ok(__name__, "Upload the {} package?".format(latest_release_package_path),
                                           ['y', 'n'], 'y'):
                latest_release_package_path = None

    if not latest_release_package_path:
        _logger.info("No package to upload.")
        return

    credentials = _read_cloud_credentials(cwd)
    cloud_project_bucket_path = _get_cloud_project_bucket_path(credentials)

    with ftplib.FTP(credentials['server'], credentials['username'], credentials['password']) as ftp_conn:
        _create_main_bucket_tree(ftp_conn, credentials)

        _upload_package(ftp_conn, latest_release_package_path, cloud_project_bucket_path, settings.RELEASE_DIRNAME)


def list_cloud(cwd='.'):
    _logger.info("List cloud buckets...")
    credentials = _read_cloud_credentials(cwd)
    with ftplib.FTP(credentials['server'], credentials['username'], credentials['password']) as ftp_conn:
        cloud_project_bucket_path = _get_cloud_project_bucket_path(credentials)

        if _is_cloud_project_bucket_exists(ftp_conn, credentials):
            _print_bucket_files(ftp_conn, cloud_project_bucket_path, settings.RELEASE_DIRNAME)
        else:
            _logger.info("There are no buckets on the cloud server.")


def download_package(cwd='.', package_name=None):
    if not package_name:
        package_name = input("Enter the name of the package to donwload: ")
    if settings.RELEASE_PACKAGE_SUFFIX in package_name:
        bucket = settings.RELEASE_DIRNAME
    else:
        raise exceptions.NameError("Incorrect package name!", logger=_logger)

    credentials = _read_cloud_credentials(cwd)
    cloud_project_bucket_path = _get_cloud_project_bucket_path(credentials)

    with ftplib.FTP(credentials['server'], credentials['username'], credentials['password']) as ftp_conn:
        ftp_conn.cwd(cloud_project_bucket_path)
        ftp_conn.cwd(bucket)
        if package_name not in ftp_conn.nlst():
            raise exceptions.FileNotFoundError(
                "{} package not found on the cloud server".format(package_name), logger=_logger)

        dir_where_to_download = Path(cwd) / settings.RELEASE_DIRNAME
        if not dir_where_to_download.exists():
            Path.mkdir(dir_where_to_download, parents=True)

        path_where_to_download = dir_where_to_download / package_name

        if (path_where_to_download).exists():
            _logger.warning("File {} already exists in {}.".format(package_name, path_where_to_download.parent))
            _logger.info("Downloading aborted.")
            return

        with open(path_where_to_download, 'wb') as file:
            ftp_conn.retrbinary("RETR " + package_name, file.write)

    if (path_where_to_download).exists():
        _logger.info("File {} downloding to {} directory completeted.".format(
            package_name, path_where_to_download.parent))
    else:
        raise exceptions.FileNotFoundError(
            "File {} downloading error! Please try again.".format(package_name),
            logger=_logger)


def _print_bucket_files(ftp_conn, cloud_project_bucket_path, bucket):
    ftp_conn.cwd(cloud_project_bucket_path)
    if bucket in ftp_conn.nlst():
        ftp_conn.cwd(bucket)
        files_in_bucket = list(ftp_conn.mlsd())
        files_in_bucket = sorted(files_in_bucket, key=lambda k: k[1]['modify'])
        if files_in_bucket:
            _logger.info("{} bucket files:".format(bucket))
            for bucket_file in files_in_bucket:
                _logger.info("{0:10} {1:10} {2} {3}".format(bucket_file[1]['unix.owner'],
                                                            bucket_file[1]['size'],
                                                            datetime.datetime.strptime(bucket_file[1]['modify'],
                                                                                       '%Y%m%d%H%M%S'),
                                                            bucket_file[0]))
        else:
            _logger.info("No files in bucket: {}".format(bucket))
    else:
        _logger.info("Bucket: {} not exists on cloud server.".format(bucket))


def _is_cloud_project_bucket_exists(ftp_conn, credentials):
    ftp_conn.cwd('/')

    if not credentials['main_bucket_path'] in ftp_conn.nlst():
        return False
    ftp_conn.cwd(credentials['main_bucket_path'])

    if credentials['client_name'] not in ftp_conn.nlst():
        return False
    ftp_conn.cwd(credentials['client_name'])

    if credentials['project_name'] not in ftp_conn.nlst():
        return False

    return True


def _get_cloud_project_bucket_path(credentials):
    return (Path('/') / credentials['main_bucket_path'] / credentials['client_name'] / credentials['project_name']
            ).as_posix()


def _upload_package(ftp_conn, package_path, cloud_project_bucket_path, bucket):
    ftp_conn.cwd(cloud_project_bucket_path)
    if package_path:
        package_name = package_path.name
        ftp_conn.cwd(bucket)
        buckets_contents = ftp_conn.nlst()
        if package_name not in buckets_contents:
            fh = open(package_path, 'rb')
            ftp_conn.storbinary('STOR ' + package_name, fh)
            fh.close()
            if package_name in ftp_conn.nlst():
                _logger.info(
                    "File {} uploaded properly to directory {} of the cloud server!".format(
                        package_name, ftp_conn.pwd()))
            else:
                _logger.info("File {} uploading error!".format(package_name))
        else:
            _logger.info("{} already on server's bucket: {}.".format(package_path.name, ftp_conn.pwd()))


def _get_latest_package_path(path):
    if Path(path).exists():
        if os.listdir(path):
            files_list = []
            for item in Path(path).iterdir():
                if item.is_file():
                    files_list.append((Path(item).stat().st_mtime, item))
        else:
            return None
    else:
        return None

    return max(files_list)[1]


def _read_cloud_credentials(cwd='.'):
    file_path = Path(cwd) / settings.CLOUD_CREDENTIALS_FILENAME

    if not file_path.exists():
        raise exceptions.FileNotFoundError(
            "{} file not found!".format(
                settings.CLOUD_CREDENTIALS_FILENAME),
            logger=_logger)

    with open(file_path, 'r') as file:
        properties_string = '[dummy_section]\n' + file.read()

    credentials = configparser.RawConfigParser()
    credentials.read_string(properties_string)

    credentials_dict = {}

    for param in credentials['dummy_section']:
        credentials_dict[param] = credentials['dummy_section'][param].strip()

    for field in credentials_dict:
        if not credentials_dict[field]:
            raise exceptions.CredentialsError(
                "{} field is empty in {} file!".format(
                    field, settings.CLOUD_CREDENTIALS_FILENAME), logger=_logger)

    return credentials_dict


def _create_main_bucket_tree(ftp_conn, credentials):
    if not credentials['main_bucket_path'] in ftp_conn.nlst():
        raise exceptions.BucketNotFoudError(
            "Bucket {} not found on server!".format(
                credentials['main_bucket_path']), logger=_logger)

    ftp_conn.cwd(credentials['main_bucket_path'])

    if credentials['client_name'] not in ftp_conn.nlst():
        ftp_conn.mkd(credentials['client_name'])
    ftp_conn.cwd(credentials['client_name'])

    if credentials['project_name'] not in ftp_conn.nlst():
        ftp_conn.mkd(credentials['project_name'])
    ftp_conn.cwd(credentials['project_name'])

    if settings.RELEASE_DIRNAME not in ftp_conn.nlst():
        ftp_conn.mkd(settings.RELEASE_DIRNAME)
