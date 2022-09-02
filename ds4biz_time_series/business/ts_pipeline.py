from typing import List, Union

import numpy as np
from sktime.forecasting.compose import TransformedTargetForecaster

from ds4biz_time_series.model.transformer_model import TimeSeriesTransformer
from sktime.forecasting.base import ForecastingHorizon

from ds4biz_time_series.utils.logger_utils import logger
from sktime.performance_metrics.forecasting import mean_squared_error, mean_absolute_error, MeanAbsolutePercentageError



class TSPipeline():
    def __init__(self, **kwargs):
        self.id = "Unknown"
        self.steps = []
        self.fitted = False
        self.__dict__.update(kwargs)
        print("tspipeline ", self.__dict__)

    #
    # def _unpack_transformer(self, transformer: TimeSeriesTransformer):
    #     return (transformer.name, transformer.transformer)

    def add(self, obj):
        self.steps.append(obj)

    #
    # def initialize_pipeline(self):
    #     pipeline_steps = [self._unpack_transformer(t) for t in self.transformers]
    #     pipeline_steps.append(self.model)
    #     self.pipeline = TransformedTargetForecaster(pipeline_steps)

    def fit(self, y, X=None, horizon: Union[int, list] = None, **kwargs):
        print("================================== ", self.__dict__)
        logger.info(f"fitting predictor {self.id}")
        logger.debug('y size: %s' % str(len(y)))
        # logger.debug("n. target: ", str(y.shape[1]))
        if X:
            logger.debug('X size: %s' % str(X.shape))
        for i in range(len(self.steps)):
            name, obj = self.steps[i]
            logger.debug(f'Fitting {name}')
            if name == 'transformer':
                logger.debug('TRANSFORMER: %s' % str(obj))
                print("------::: ", y)
                y = obj.fit_transform(y)
                print("oki")
                # y = y.astype(np.float)
                # logger.debug('X transformed size: %s' % str(X.shape))

            if name == 'model':
                logger.debug('MODEL: %s' % str(obj))
                print("covariates data:  ", X)
                # m = obj.fit(y = y, x=X, **kwargs)
                if horizon:
                    if isinstance(horizon, int):
                        horizon = np.arange(1, horizon + 1)
                    fh = ForecastingHorizon(horizon, is_relative=True)

                    obj.fit(y=y, X=X, fh=fh)
                else:
                    if obj.get_tag("requires-fh-in-fit"):
                        raise Exception("You have to specify an horizon in order to fit this model..")
                    obj.fit(y=y, X=X, **kwargs)
                print("end fitting - ts_pipeline")

    def predict(self, X=None, horizon: Union[int, list] = None, **kwargs):

        logger.debug('PREDICT')
        # logger.debug('X size: %s' % str(X.shape))
        for name, obj in self.steps:
            if name == 'transformer':
                logger.debug('TRANSFORMER: %s' % str(obj))
                if X != None:
                    X = obj.transform(X)
                    X = X.astype(np.float)
                    logger.debug('X transformed size: %s' % str(X.shape))
            if name == 'model':

                logger.debug('MODEL: %s' % str(obj))
                if horizon:
                    if isinstance(horizon, int):
                        horizon = np.arange(1, horizon + 1)
                else:
                    horizon = [1]
                fh = ForecastingHorizon(horizon, is_relative=True)
                # if include_probs:
                #     if hasattr(obj, "predict_proba"):
                #         classes = obj.classes_
                #         try:
                #             return [sorted(zip(classes, row), key=lambda x: x[1], reverse=True)
                #                     for row in obj.predict_proba(X, **kwargs)]
                #         except AttributeError:
                #             raise PredictProbaException("%s has not predict_proba" % obj.__class__.__name__)
                #     else:
                #         raise PredictProbaException("%s has not predict_proba" % obj.__class__.__name__)
                # else:
                preds = obj.predict(fh=fh, X=X, **kwargs)
                preds = preds.to_dict()
                return preds

    def get_forecast_report(self, y, X=None):
        # horizon =
        print(X)
        y_pred = self.predict(X=X)

        report = dict(
                    MAPE = MeanAbsolutePercentageError(y, y_pred),
                    SMAPE = MeanAbsolutePercentageError(y, y_pred),

                    MSE = mean_squared_error(y, y_pred),
                    RMSE = mean_squared_error(y, y_pred, squared=False),
                    MAE = mean_absolute_error(y, y_pred),

                    # R2 = r2_score(y, y_pred),
                    # EXPLAINED_VARIANCE = explained_variance_score(y, y_pred),
                    PERC_ERROR = mean_absolute_error(y, y_pred) * 100.0 / (max(y) - min(y)),
                    PERC_ERROR_RECOMPUTED = (abs(np.array(y_pred) - np.array(y)) / (np.array(y) + 1)).mean(),
                    scatter = dict(y_true=y, y_pred=y_pred.tolist()))
        logger.debug('MSE SCORE: %s' % str(report['MSE']))
        logger.debug('R2: %s' % str(report['R2']))
        return report

    # def partial_fit(self, df, update_params=False):
    #     """
    #     > The function takes in a dataframe and updates the model parameters
    #
    #     :param df: The dataframe to be used for training
    #     :param update_params: If True, the model parameters are updated. If False, the model parameters are not updated,
    #     defaults to False (optional)
    #     """
        # self.model.update(df, update_params=update_params)

    # def get_params(self):
    #     """
    #     It returns the parameters of the model that have been fitted to the data
    #     :return: The fitted parameters of the model.
    #     """
    #     return self.model.get_fitted_params()