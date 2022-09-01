from datetime import datetime
from pathlib import Path
from typing import Dict, Union
from sanic.exceptions import SanicException

import numpy as np
import pandas as pd

from ds4biz_time_series.business.ts_pipeline import TSPipeline
from ds4biz_time_series.config.AppConfig import REPO_PATH
from ds4biz_time_series.config.factory_config import FACTORY
from sktime.forecasting.model_selection import temporal_train_test_split
# from ds4biz_predictor_core.utils.ml_utils import save_pipeline

from ds4biz_time_series.dao.fs_dao import JSONFSDAO
from ds4biz_time_series.utils.core_utils import save_pipeline
from ds4biz_time_series.utils.logger_utils import logger

repo_path = Path(REPO_PATH)


def training_task(pred_id: str, data: Dict, datetime_feature:str,  datetime_frequency:str, task: str, test_size: Union[float, int], ts_pipeline: TSPipeline,
                  forecasting_horizon: Union[int, list], fit_params: dict):
    logger.debug("Pipeline START")
    target = data['target'] if task != 'classification' else [str(el) for el in data['target']]
    data = data.get("data", None)
    fitting_time = datetime.now()
    logger.debug(f"Splitting data, test size: {test_size}")
    df = pd.DataFrame(data)
    if not datetime_feature in df.columns:
            raise Exception("The datetime_feature specified doesn't match any features in your data, please check.")

    if len(df.columns)==1:
        print("solo una feature")
        df["target"] = target
        print("aggiornato ",df.columns)

        df[datetime_feature] = pd.PeriodIndex(df["Date_Time"], freq=datetime_frequency)
        # df[datetime_feature]= pd.to_datetime(df[datetime_feature])
        df.set_index(datetime_feature, inplace=True)
        print("settato indice")
        y_train, y_test = temporal_train_test_split(y=df, test_size=test_size)
        logger.debug("Training model")
        res = ts_pipeline.fit(y_train, horizon=forecasting_horizon, **fit_params)
    else:
        df.set_index(datetime_feature, inplace=True)
        X_train, X_test, y_train, y_test = temporal_train_test_split(y=target, X=df, test_size=test_size)
        X_train = pd.DataFrame(X_train).fillna(np.nan)
        print(X_train)
        logger.debug("Training model")
        res = ts_pipeline.fit(y_train, X_train, horizon=forecasting_horizon, **fit_params)

    ts_pipeline.date = fitting_time

    save_pipeline(ts_pipeline, branch="development", history_limit=1, repo_path=repo_path)
    logger.debug("Model trained")

    tsum = dict(
        # tdist=distro, cv_scores=scores, report_training=res_report_train, report_test=res_report_test,
        task=task, test_size=test_size)  # if report else None
    dao = JSONFSDAO(repo_path / "predictors" / pred_id / "history", history=True, date=fitting_time)
    dao.save(tsum, "train_summary.json")
    del dao
    logger.debug("Pipeline end")
    return res


def training_pipeline(predictor_blueprint: Dict, data: Dict, datetime_feature:str, datetime_frequency:str, task: str, test_size: Union[float, int], fit_params: Dict,
                      forecasting_horizon: Union[int, list]):
    print("dentro")
    pred_id = predictor_blueprint["id"]

    if task not in ["classification", "forecasting"]:
        # raise Exception(f"Task {task} not yet supported")
        raise SanicException(f"Task '{task}' not yet supported", status_code=501)

    ts_pipeline = TSPipeline(id=predictor_blueprint["id"])
    steps = predictor_blueprint.pop('steps')
    print("steps ", steps)
    # if steps["transformer"]=="auto":
    # if steps["model"]=="auto":
    for k, v in steps.items():
        print("agg....")
        ts_pipeline.add([k, FACTORY(v)])
    print("training task")
    training_task(pred_id, data, datetime_feature, datetime_frequency, task, test_size, ts_pipeline, forecasting_horizon, fit_params)
