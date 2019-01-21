#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import subprocess
from pathlib import Path


__version__ = '0.1.0'

GIT_SSH_COMMAND = 'GIT_SSH_COMMAND'


class PygittoolsError(Exception):
    def __init__(self, msg, returncode):
        super().__init__(msg)
        self.returncode = returncode
        
        
class CmdError(PygittoolsError):
    pass


class ValueError(PygittoolsError):
    pass


class TagNotFoundError(PygittoolsError):
    pass


def init(cwd='.'):
    return _execute_cmd(['git', 'init'], cwd=cwd)


def add(path, cwd='.'):
    return _execute_cmd(['git', 'add', str(path)], cwd=cwd)


def add_origin(path, cwd='.'):
    return _execute_cmd(['git', 'remote', 'add', 'origin', str(path)], cwd=cwd)


def commit(msg, cwd='.'):
    return _execute_cmd(['git', 'commit', '-m', msg], cwd=cwd)


def push(ssh_key=None, cwd='.'):
    return _execute_cmd(['git', 'push'], ssh_key=ssh_key, cwd=cwd)


def push_with_tags(ssh_key=None, cwd='.'):
    return _execute_cmd(['git', 'push', '--follow-tags'], ssh_key=ssh_key, cwd=cwd)


def get_latest_tag(cwd='.'):
    return _execute_cmd(['git', 'describe', '--abbrev=0', '--tags'], cwd=cwd)


def get_latest_tag_all_branches(cwd='.'):
    return _execute_cmd(['git', 'describe', '--tags', '$(git rev-list --tags --max-count=1)'], cwd=cwd)


def revert(commit_rollback, cwd='.'):
    return _execute_cmd(['git', 'reset', '--hard', 'HEAD~{}'.format(commit_rollback)], cwd=cwd)


def delete_latest_tag(all_branches=False, cwd='.'):
    try:
        if all_branches:
            latest_tag = get_latest_tag_all_branches(cwd)
        else:
            latest_tag = get_latest_tag(cwd)
    except CmdError:
        raise TagNotFoundError('No tag found.', returncode=1)
    
    return _execute_cmd(['git', 'tag', '-d', latest_tag], cwd=cwd)
        

def delete_tag(tag, cwd='.'):
    return _execute_cmd(['git', 'tag', '-d', tag], cwd=cwd)
    

def get_latest_tag_msg(cwd='.'):
    return _execute_cmd(['git', 'for-each-ref', '--count=1', '--sort=-taggerdate', '--format', '%(contents)', 'refs/tags'], cwd=cwd)
    
    
def set_tag(cwd='.', tag=None, msg=None):
    return _execute_cmd(['git', 'tag', '-a', tag, '-m', msg], cwd=cwd)
    
    
def list_tags(cwd='.'):
    return _execute_cmd(['git', 'tag'], cwd=cwd).split('\n')


def list_git_repo_tree(cwd='.'):
    return _execute_cmd(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], cwd=cwd).split('\n')
    

def is_any_commit(cwd='.'):
    try:
        _execute_cmd(['git', 'log'], cwd=cwd)
        return True
    except CmdError:
        return False    


def is_any_tag(cwd='.'):
    return list(filter(None, list_tags(cwd))).__len__() > 0

    
def is_origin_set(cwd='.'):
    try:
        _execute_cmd(['git', 'config', '--local', 'remote.origin.url'], cwd=cwd)
        return True
    except CmdError:
        return False
    
    
def is_work_tree(cwd='.'):
    return _execute_cmd(['git', 'rev-parse', '--is-inside-work-tree'], cwd=cwd).lower() == 'true'
    

# TOFO: change to bool
def are_uncommited_changes(cwd='.'):
    return _execute_cmd(['git', '--no-pager', 'diff', '--no-ext-diff'], cwd=cwd) != ''
    
    
def get_latest_commit_hash(cwd='.'):
    return _execute_cmd(["git", "log", "--pretty=format:%h", "-n", "1"], cwd=cwd)


def get_tag_commit_hash(tag, cwd='.'):
    return _execute_cmd(["git", "log", "--pretty=format:%h", "-n", "1", tag], cwd=cwd)
    
    
def get_changelog(report_format=None, cwd='.'):
    if not report_format:
        report_format = "%(taggerdate:short) | Release: %(tag) \r\n%(contents)"
        
    return _execute_cmd(["git", "for-each-ref", "--sort=-creatordate",
                               "--format={}".format(report_format),
                               "refs/tags"], cwd=cwd)


def update_all_submodules(ssh_key=None, cwd='.'):
    return _execute_cmd(["git", "submodule", "update", "--recursive", "--remote"], ssh_key=ssh_key, cwd=cwd)


def deinit_all_submodules(cwd='.'):
    return _execute_cmd(["git", "submodule", "deinit", "--force", "--all"], cwd=cwd)


def clear_cache(path, cwd='.'):
    if not path:
        raise ValueError("'path' argument is not specified!")
    return _execute_cmd(["git", "rm", "-rf", "--cached", str(path)], cwd=cwd)


def get_commit_msgs_from_last_tag(cwd='.'):
    latest_tag = get_latest_tag(cwd)
    if latest_tag:
        return _execute_cmd(['git', 'log', '--pretty=%B', f'{latest_tag}..HEAD'], cwd)
    else:
        return _execute_cmd(['git', 'log', '--pretty=%B', 'HEAD'], cwd)


def _execute_cmd(args, ssh_key=None, cwd='.'):
    cwd = Path(cwd).resolve()
    if not cwd.exists():
        raise CmdError('Current working directory not exists.', returncode=1)
    
    if ssh_key:
        ssh_key_path = Path(ssh_key).resolve().as_posix()
        env = os.environ.copy()
        env[GIT_SSH_COMMAND] = f'ssh -i "{ssh_key_path}"'
    else:
        env = None
        
    try:
        process = subprocess.run(args,
                                 check=True,
                                 cwd=cwd.__str__(),
                                 env=env,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 encoding="utf-8")
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise CmdError(e.output, returncode=e.returncode)
    
    
if __name__ == '__main__':
    print(get_changelog(report_format="### Version: %(tag) | Released: %(taggerdate:short) \r\n%(contents)"))
