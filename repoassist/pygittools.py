#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import subprocess
from pathlib import Path


__version__ = '0.1.0'

GIT_SSH_COMMAND = 'GIT_SSH_COMMAND'


def init(cwd='.'):
    return _execute_cmd_and_strip(['git', 'init'], cwd=cwd)


def add(path, cwd='.'):
    return _execute_cmd_and_strip(['git', 'add', str(path)], cwd=cwd)


def add_origin(path, cwd='.'):
    return _execute_cmd_and_strip(['git', 'remote', 'add', 'origin', str(path)], cwd=cwd)


def commit(msg, cwd='.'):
    return _execute_cmd_and_strip(['git', 'commit', '-m', msg], cwd=cwd)


def push(ssh_key=None, cwd='.'):
    return _execute_cmd_and_strip(['git', 'push'], ssh_key=ssh_key, cwd=cwd)


def push_with_tags(ssh_key=None, cwd='.'):
    return _execute_cmd_and_strip(['git', 'push', '--follow-tags'], ssh_key=ssh_key, cwd=cwd)


def get_latest_tag(cwd='.'):
    return _execute_cmd_and_strip(['git', 'describe', '--abbrev=0', '--tags'], cwd=cwd)


def get_latest_tag_all_branches(cwd='.'):
    return _execute_cmd_and_strip(['git', 'describe', '--tags', '$(git rev-list --tags --max-count=1)'], cwd=cwd)


def revert(commit_rollback, cwd='.'):
    return _execute_cmd_and_strip(['git', 'reset', '--hard', 'HEAD~{}'.format(commit_rollback)], cwd=cwd)


def delete_latest_tag(all_branches=False, cwd='.'):
    if all_branches:
        ret = get_latest_tag_all_branches(cwd)
    else:
        ret = get_latest_tag(cwd)
    if ret['returncode'] == 0:
        return _execute_cmd_and_strip(['git', 'tag', '-d', ret['msg']], cwd=cwd)
    else:
        return {'msg': "No tag found.", 'returncode': 1}
    
    
def delete_tag(tag, cwd='.'):
    return _execute_cmd_and_strip(['git', 'tag', '-d', tag], cwd=cwd)
    

def get_latest_tag_msg(cwd='.'):
    return _execute_cmd_and_strip(['git', 'for-each-ref', '--count=1', '--sort=-taggerdate', '--format', '%(contents)', 'refs/tags'], cwd=cwd)
    
    
def set_tag(cwd='.', tag=None, msg=None):
    return _execute_cmd_and_strip(['git', 'tag', '-a', tag, '-m', msg], cwd=cwd)
    
    
def list_tags(cwd='.'):
    try:
        process = subprocess.run(['git', 'tag'],
                                  check=True,
                                  cwd=str(cwd),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  encoding="utf-8")
        return {'msg': process.stdout.strip().split('\n'), 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}


def list_git_repo_tree(cwd='.'):
    ret = _execute_cmd_and_split(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], cwd=cwd)
    ret['msg'] = ret['msg'][:-1]
    
    return ret
    

def is_any_commit(cwd='.'):
    ret = _execute_cmd_and_strip(['git', 'log'], cwd=cwd)
    return True if ret['returncode'] == 0 else False


def is_any_tag(cwd='.'):
    ret = list_tags(cwd)
    if ret['returncode'] == 0:
        return True if ret['msg'].__len__() else False
    
    
def is_origin_set(cwd='.'):
    ret = _execute_cmd_and_strip(['git', 'config', '--local', 'remote.origin.url'], cwd=cwd)
    return True if ret['returncode'] == 0 else False    
    
    
def is_work_tree(cwd='.'):
    try:
        process = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'],
                                  check=True,
                                  cwd=str(cwd),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  encoding="utf-8")
        return {'msg': True if process.stdout.strip() == 'true' else False, 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}
    

def are_uncommited_changes(cwd='.'):
    try:
        process = subprocess.run(['git', '--no-pager', 'diff', '--no-ext-diff'],
                                  check=True,
                                  cwd=str(cwd),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  encoding="utf-8")
        return {'msg': True if process.stdout else False, 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}
    
    
def get_latest_commit_hash(cwd='.'):
    return _execute_cmd_and_strip(["git", "log", "--pretty=format:%h", "-n", "1"], cwd=cwd)


def get_tag_commit_hash(tag, cwd='.'):
    return _execute_cmd_and_strip(["git", "log", "--pretty=format:%h", "-n", "1", tag], cwd=cwd)
    
    
def get_changelog(report_format=None, cwd='.'):
    if not report_format:
        report_format = "%(taggerdate:short) | Release: %(tag) \r\n%(contents)"
        
    return _execute_cmd_and_strip(["git", "for-each-ref", "--sort=-creatordate",
                               "--format={}".format(report_format),
                               "refs/tags"], cwd=cwd)


def update_all_submodules(ssh_key=None, cwd='.'):
    return _execute_cmd_and_strip(["git", "submodule", "update", "--recursive", "--remote"], ssh_key=ssh_key, cwd=cwd)


def deinit_all_submodules(cwd='.'):
    return _execute_cmd_and_strip(["git", "submodule", "deinit", "--force", "--all"], cwd=cwd)


def clear_cache(path, cwd='.'):
    if not path:
        raise ValueError("path is not specified!")
    return _execute_cmd_and_strip(["git", "rm", "-rf", "--cached", str(path)], cwd=cwd)


def get_commit_msgs_from_last_tag(cwd='.'):
    ret = get_latest_tag(cwd)
    if ret['returncode'] == 0:
            return _execute_cmd_and_strip(['git', 'log', '--pretty=%B', f'{ret["msg"]}..HEAD'], cwd)
    else:
        return _execute_cmd_and_strip(['git', 'log', '--pretty=%B', 'HEAD'], cwd)


def _execute_cmd_and_split(args, ssh_key=None, cwd='.'):
    if ssh_key:
        ssh_key_path = Path(ssh_key).resolve().as_posix()
        env = os.environ.copy()
        env[GIT_SSH_COMMAND] = f'ssh -i "{ssh_key_path}"'
    else:
        env = None
        
    try:
        process = subprocess.run(args,
                                 check=True,
                                 cwd=str(cwd),
                                 env=env,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 encoding="utf-8")
        return {'msg': process.stdout.split('\n'), 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}
    
    
def _execute_cmd_and_strip(args, ssh_key=None, cwd='.'):
    if ssh_key:
        ssh_key_path = Path(ssh_key).resolve().as_posix()
        env = os.environ.copy()
        env[GIT_SSH_COMMAND] = f'ssh -i "{ssh_key_path}"'
    else:
        env = None
        
    try:
        process = subprocess.run(args,
                                 check=True,
                                 cwd=str(cwd),
                                 env=env,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 encoding="utf-8")
        return {'msg': process.stdout.strip(), 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}
    
    
if __name__ == '__main__':
#     print(list_git_repo_tree())
#     print(add('test.txt'))
    
    print(get_changelog(report_format="### Version: %(tag) | Released: %(taggerdate:short) \r\n%(contents)"))
