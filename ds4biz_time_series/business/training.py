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
from ds4biz_time_series.utils.core_utils import save_pipeline, to_dataframe
from ds4biz_time_series.utils.logger_utils import logger

repo_path = Path(REPO_PATH)


def training_task(pred_id: str, data: Dict, datetime_feature: str, datetime_frequency: str, task: str, report: bool,
                  test_size: Union[float, int], ts_pipeline: TSPipeline,
                  forecasting_horizon: Union[int, list], fit_params: dict):
    logger.debug("Pipeline START")
    target = data['target'] if task != 'classification' else [str(el) for el in data['target']]
    data = data.get("data", None)
    fitting_time = datetime.now()
    logger.debug(f"transforming data into pandas df{data}")
    logger.debug("type of data %s" %str(type(data)))
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    df = pd.DataFrame(data)
    logger.debug("coosi e' ok")
    df = to_dataframe(data)
    logger.debug("qui si")
    logger.debug("shape %s" %str(df.shape))
    logger.debug("col %s" %str(df.columns))
    logger.debug("len %s" %str(len(df.columns)))

    logger.debug(f"dt f {datetime_feature}")
    logger.debug(f"dt freq {datetime_frequency}")
    dt = pd.PeriodIndex(df[datetime_feature], freq=datetime_frequency)
    logger.debug(f"oki{dt}")
    df[datetime_feature] = dt
    if not datetime_feature in df.columns:
        raise Exception("The datetime_feature specified doesn't match any features in your data, please check again.")

    if len(df.columns) == 1:
        logger.debug("using only one feature")
        df["target"] = target
        # df[datetime_feature]= pd.to_datetime(df[datetime_feature])
        df.set_index(datetime_feature, inplace=True)

        if report:
            logger.debug(f"Splitting data, test size: {test_size}")
            y_train, y_test = temporal_train_test_split(y=df, test_size=test_size)
        else:
            y_train = df
        X_train = None
        X_test = None
    else:
        logger.debug("using covariate to train models")
        df.set_index(datetime_feature, inplace=True)
        print("ciao")
        target = pd.DataFrame(target)
        target[datetime_feature] = df.index
        target.set_index(datetime_feature, inplace=True)
        logger.debug("sono dopo index")
        if report:
            logger.debug(f"Splitting data, test size: {test_size}")

            y_train, y_test, X_train, X_test  = temporal_train_test_split(y=target, X=df, test_size=test_size)
        else:
            X_train = df
            y_train = target

        # X_train = pd.DataFrame(X_train).fillna(np.nan)
        # X_test = pd.DataFrame(X_test).fillna(np.nan)
        # print("XTRAIN:::", X_train)
        # print("XTest:::", X_test)
    logger.debug("Training model")

    res = ts_pipeline.fit(y_train, X_train, horizon=forecasting_horizon, **fit_params)

    ts_pipeline.date = fitting_time

    save_pipeline(ts_pipeline, branch="development", history_limit=1, repo_path=repo_path)
    logger.debug("Model trained")

    res_report_train = None
    res_report_test = None
    if report:
        logger.debug("Computing Metrics")
        res_report_train = ts_pipeline.get_forecast_report(y=y_train, X=X_train)
        res_report_test = ts_pipeline.get_forecast_report(y=y_test, X=X_test)

    tsum = dict(
        # tdist=distro, cv_scores=scores,
        report_training=res_report_train,
        report_test=res_report_test,
        task=task, test_size=test_size)  # if report else None
    dao = JSONFSDAO(repo_path / "predictors" / pred_id / "history", history=True, date=fitting_time)
    dao.save(tsum, "train_summary.json")
    del dao
    logger.debug("Pipeline end")
    return res


def training_pipeline(predictor_blueprint: Dict, data: Dict, datetime_feature: str, datetime_frequency: str, task: str,
                      report: bool, test_size: Union[float, int], fit_params: Dict,
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
        logger.debug(f"step added....{k}")
        ts_pipeline.add([k, FACTORY(v)])
    logger.debug("training task starts")
    training_task(pred_id, data, datetime_feature, datetime_frequency, task, report, test_size, ts_pipeline,
                  forecasting_horizon, fit_params)
