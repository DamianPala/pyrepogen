
import shutil
from pathlib import Path

from . import settings


def generate_standalone_repo_dirs(cwd='.'):
    paths = []
    for dirname in settings.STANDALONE_REPO_DIRS_TO_GEN:
        path = Path(cwd) / dirname
        if (path).exists():
            shutil.rmtree(path)
        path.mkdir()
        paths.append(path)
        
    return paths