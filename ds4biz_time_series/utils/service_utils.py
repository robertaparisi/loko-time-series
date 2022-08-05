from pathlib import Path
from typing import List

from ds4biz_time_series.config.AppConfig import REPO_PATH
from ds4biz_time_series.dao.fs_dao import FileSystemDAO

repo_path = Path(REPO_PATH)

def get_all(repo: str) -> List[str]:
    path = repo_path / repo
    fsdao = FileSystemDAO(path)
    return sorted(fsdao.all(files=False))