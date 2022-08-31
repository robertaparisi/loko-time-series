from pathlib import Path
from typing import List
import json

from sanic.exceptions import SanicException



from ds4biz_time_series.config.AppConfig import REPO_PATH
from ds4biz_time_series.dao.fs_dao import FileSystemDAO

repo_path = Path(REPO_PATH)

def get_all(repo: str) -> List[str]:
    path = repo_path / repo
    fsdao = FileSystemDAO(path)
    return sorted(fsdao.all(files=False))


def check_predictor_existence(path:Path):
    if path.exists():
        raise SanicException(f"Predictor '{path.name}' already exists!", status_code=409)

def check_existence(path:Path, obj_type:str):
    if not path.exists():
        print("qui")
        raise SanicException(f"{obj_type.capitalize()} '{path.name}' doesn't exists!", status_code=404)


def load_params(params):
    res = dict()
    for k in params:
        v = params.get(k)
        if v == 'none':
            res[k] = None
        else:
            try:
                res[k] = json.loads(params.get(k))
            except:
                res[k] = params.get(k)
    return res