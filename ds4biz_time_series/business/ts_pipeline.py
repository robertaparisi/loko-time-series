
from typing import List, Union

import numpy as np
from sktime.forecasting.compose import TransformedTargetForecaster

from ds4biz_time_series.model.transformer_model import TimeSeriesTransformer
from sktime.forecasting.base import ForecastingHorizon



class TSPipeline():
    def __init__(self, model, transformers: List[TimeSeriesTransformer], ):
        self.transformers = transformers
        self.model = model

    def _unpack_transformer(self, transformer: TimeSeriesTransformer):
        return (transformer.name, transformer.transformer)

    def initialize_pipeline(self):
        pipeline_steps = [self._unpack_transformer(t) for t in self.transformers]
        pipeline_steps.append(self.model)
        self.pipeline = TransformedTargetForecaster(pipeline_steps)

    def fit(self, y, horizon:Union[int, list]=None, **kwargs):
        if horizon:
            if isinstance(horizon, int):
                horizon = np.arange(1, horizon + 1)
            fh = ForecastingHorizon(horizon, is_relative=True)

        self.pipeline.fit(y)
        else:
            if self.model.get_tag("requires-fh-in-fit"):
                raise Exception("You have to specify an horizon in order to fit this model..")
            self.model.fit(train, **kwargs)



