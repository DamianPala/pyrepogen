#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
from pathlib import Path

from . import pygittools 
from .exceptions import (ExecuteCmdError)


def execute_cmd(args, cwd='.'):
    try:
        process = subprocess.run(args, 
                                 check=True,
                                 cwd=str(cwd),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 encoding="utf-8")
        return process.stdout
    except subprocess.CalledProcessError as e:
        raise ExecuteCmdError(e.returncode, msg=e.output)
    
    
def execute_cmd_and_split_lines_to_list(args, cwd='.'):
    try:
        process = subprocess.run(args,
                                 check=True,
                                 cwd=str(cwd),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 encoding="utf-8")
        return process.stdout.split('\n')
    except subprocess.CalledProcessError as e:
        raise ExecuteCmdError(e.returncode, msg=e.output)
    
    
def get_git_repo_tree(cwd='.'):
    return [Path(cwd).resolve() / path for path in pygittools.list_git_repo_tree(str(cwd))['msg']]