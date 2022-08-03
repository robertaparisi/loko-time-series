
from typing import List
from sktime.forecasting.compose import TransformedTargetForecaster

from ds4biz_time_series.model.transformer_model import TimeSeriesTransformer



class TSPipeline():
    def __init__(self, model, transformers: List[TimeSeriesTransformer], ):
        self.transformers = transformers
        self.model = model

    def _unpack_transformer(self, transformer: TimeSeriesTransformer):
        return (transformer.name, transformer.transformer)

    def initialize_pipeline(self):
        pipeline_steps = [self._unpack_transformer(t) for t in self.transformers]
        pipeline_steps.append(self.model)
        pipeline = TransformedTargetForecaster(pipeline_steps)
        return pipeline