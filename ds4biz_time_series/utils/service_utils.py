from pathlib import Path
from typing import List
import json

from sanic.exceptions import SanicException

from ds4biz_time_series.business.training import training_pipeline
from ds4biz_time_series.config.AppConfig import REPO_PATH
from ds4biz_time_series.dao.fs_dao import FileSystemDAO
from ds4biz_time_series.utils.core_utils import load_pipeline
from ds4biz_time_series.utils.data_utils import preprocessing_data
from ds4biz_time_series.utils.logger_utils import logger
from ds4biz_time_series.utils.serialization_utils import deserialize, serialize

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


def train_model(predictor_name, fit_params:dict, data:dict):
    predictor_path = repo_path / 'predictors' / predictor_name
    print("predictor: ", predictor_path)
    logger.debug(f"predictor{predictor_path}")
    predictor_blueprint = deserialize(predictor_path)
    dparams = dict(test_size=.2,
                   forecasting_horizon=None,
                   datetime_frequency="s",
                   # partial=False,
                   fit_params=dict(),
                   # cv=0,
                   report=False,
                   # history_limit=0,
                   task='forecasting',
                   # save_dataset=False
                   )
    params = {**dparams, **load_params(fit_params)}
    params["datetime_frequency"] = params["datetime_frequency"]
    predictor_blueprint["datetime_feature"] = params["datetime_feature"]
    predictor_blueprint["datetime_frequency"] = params["datetime_frequency"]
    serialize(predictor_path, predictor_blueprint)

    print("parameters::: ", params)
    data = data
    print("data", data)
    training_pipeline(predictor_blueprint=predictor_blueprint, data=data, **params)
    logger.debug("training done...")

def get_prediction(predictor_name, predict_params:dict, branch:str="development",  data:dict=None):
    """
    It loads the pipeline, preprocesses the data, and then predicts

    :param predictor_name: the name of the predictor you want to use
    :param predict_params: a dictionary with the following keys:
    :type predict_params: dict
    :param branch: The branch of the predictor you want to use, defaults to development
    :type branch: str (optional)
    :param data: the data to be predicted
    :type data: dict
    :return: The prediction is being returned.
    """
    path = repo_path / 'predictors' / predictor_name
    logger.debug(f"name: {predictor_name}")
    if path / branch not in list(path.glob('*')):
        raise Exception(f'Predictor "{predictor_name}" is not fitted')
    pipeline = load_pipeline(predictor_name, branch, repo_path=repo_path)
    data = preprocessing_data(data, datetime_feature=pipeline.datetime_feature,
                              datetime_frequency=pipeline.datetime_frequency, get_only_X=True)


    try:
        preds = pipeline.predict(X=data["X"],
                                 horizon=predict_params["forecasting_horizon"])  # , include_probs=params['include_probs'])
    except Exception as e:
        print("eeeee", e)
        logger.debug(f"predict error {e}")
        raise e
    # if params['include_probs']:
    #     preds = [[[c,float(p)] for c,p in el] for el in preds]
    # else:
    #     preds = preds.tolist()

    return preds



def get_model_evaluation(predictor_name, branch, evaluate_params: dict=None, data:dict=None):

    logger.debug("loading predictor pipeline...")
    pipeline = load_pipeline(predictor_name, branch, repo_path=repo_path)
    datetime = pipeline.date.strftime('%Y-%m-%d %H:%M:%S.%f')

    logger.debug("pre-processing evaluation data...")
    # y = FACTORY(body['target'])
    try:
        data = preprocessing_data(data, datetime_feature=pipeline.datetime_feature,
                                  datetime_frequency=pipeline.datetime_frequency)
    except Exception as e:
        print(f'----------------------{e}')
        logger.error(f"evaluate error:::{e}")
        raise e

    y = data["y"]
    X = data["X"]

    logger.debug("computing forecast report")
    report = pipeline.get_forecast_report(y=y, X=X)
    logger.debug(f"report: {report}")
    res = [{"report_test": report, "datetime": datetime,
            "task": "forecast"}]
    return res