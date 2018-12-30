'''
Created on 12.11.2018

@author: Haz
'''

import subprocess


def init(cwd='.'):
    return _execute_cmd_and_strip(['git', 'init'], cwd)


def add(path, cwd='.'):
    return _execute_cmd_and_strip(['git', 'add', str(path)], cwd)


def commit(msg, cwd='.'):
    return _execute_cmd_and_strip(['git', 'commit', '-m', msg], cwd)


def get_latest_tag(cwd='.'):
    return _execute_cmd_and_strip(['git', 'describe', '--abbrev=0', '--tags'], cwd)


def delete_latest_tag(cwd='.'):
    ret = get_latest_tag(cwd)
    if ret['returncode'] == 0:
        return _execute_cmd_and_strip(['git', 'tag', '-d', ret['msg']], cwd)
    else:
        return {'msg': "No tag found.", 'returncode': 1}
    

def get_latest_tag_msg(cwd='.'):
    return _execute_cmd_and_strip(['git', 'for-each-ref', '--count=1', '--sort=-taggerdate', '--format', '%(contents)', 'refs/tags'], cwd)
    
    
def set_tag(cwd='.', tag=None, msg=None):
    return _execute_cmd_and_strip(['git', 'tag', '-a', tag, '-m', msg], cwd)
    
    
def list_tags(cwd='.'):
    try:
        process = subprocess.run(['git', 'tag'],
                              check = True,
                              cwd = cwd,
                              stdout = subprocess.PIPE,
                              stderr = subprocess.STDOUT,
                              encoding = "utf-8")
        return {'msg': process.stdout.strip().split('\n'), 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}


def list_git_repo_tree(cwd='.'):
    ret = _execute_cmd_and_split(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], cwd)
    ret['msg'] = ret['msg'][:-1]
    
    return ret
    
    
def is_work_tree(cwd='.'):
    try:
        process = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'],
                              check = True,
                              cwd = cwd,
                              stdout = subprocess.PIPE,
                              stderr = subprocess.STDOUT,
                              encoding = "utf-8")
        return {'msg': True if process.stdout.strip() == 'true' else False, 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}
    

def are_uncommited_changes(cwd='.'):
    try:
        process = subprocess.run(['git', '--no-pager', 'diff', '--no-ext-diff'],
                              check = True,
                              cwd = cwd,
                              stdout = subprocess.PIPE,
                              stderr = subprocess.STDOUT,
                              encoding = "utf-8")
        return {'msg': True if process.stdout else False, 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}
    
    
def get_latest_commit_hash(cwd='.'):
    return _execute_cmd_and_strip(["git", "log", "--pretty=format:%h", "-n", "1"], cwd)
    
    
def get_changelog(cwd='.'):
    return _execute_cmd_and_strip(["git", "for-each-ref", "--sort=-creatordate",
                               "--format=%(taggerdate:short) | Release: %(tag) \r\n%(contents)",
                               "refs/tags"], cwd)


def update_all_submodules(cwd='.'):
    return _execute_cmd_and_strip(["git", "submodule", "update", "--recursive", "--remote"], cwd)


def deinit_all_submodules(cwd='.'):
    return _execute_cmd_and_strip(["git", "submodule", "deinit", "--force", "--all"], cwd)


def clear_cache(path, cwd='.'):
    if not path:
        raise ValueError("path is not specified!")
    return _execute_cmd_and_strip(["git", "rm", "-rf", "--cached", path], cwd)


def _execute_cmd_and_split(args, cwd='.'):
    try:
        process = subprocess.run(args,
                              check=True,
                              cwd=str(cwd),
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              encoding="utf-8")
        return {'msg': process.stdout.split('\n'), 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}
    
    
def _execute_cmd_and_strip(args, cwd='.'):
    try:
        process = subprocess.run(args,
                              check=True,
                              cwd=str(cwd),
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              encoding="utf-8")
        return {'msg': process.stdout.strip(), 'returncode': process.returncode}
    except subprocess.CalledProcessError as e:
        return {'msg': e.output, 'returncode': e.returncode}
    
    
if __name__ == '__main__':
#     print(list_git_repo_tree())
    print(add('test.txt'))