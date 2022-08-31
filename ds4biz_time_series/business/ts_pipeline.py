from typing import List, Union

import numpy as np
from sktime.forecasting.compose import TransformedTargetForecaster

from ds4biz_time_series.model.transformer_model import TimeSeriesTransformer
from sktime.forecasting.base import ForecastingHorizon

from ds4biz_time_series.utils.logger_utils import logger


class TSPipeline():
    def __init__(self, **kwargs):
        self.id = "Unknown"
        self.steps = []
        self.fitted = False
        self.__dict__.update(kwargs)
        print("tspipeline ",self.__dict__)

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
        print("================================== ",self.__dict__)
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
                print("------::: ",y)
                y = obj.fit_transform(y)
                print("oki")
                # y = y.astype(np.float)
                # logger.debug('X transformed size: %s' % str(X.shape))

            if name == 'model':
                logger.debug('MODEL: %s' % str(obj))
                print("XXXXX ",X)
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
                print("1uiiiii")

