from typing import Union, List

import numpy as np
import pandas as pd
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.base import ForecastingHorizon
# from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.arima import ARIMA


class TimeSeriesPredictor():
    def __init__(self, model=None):
        self.model = model or ARIMA()
        self.fitted = False

    def fit(self, y, test_size: Union[int, float], horizon:Union[int, list]=None, **kwargs):
        train, test = temporal_train_test_split(y, test_size=test_size)
        if horizon:
            if isinstance(horizon, int):
                horizon = np.arange(1, horizon + 1)
            fh = ForecastingHorizon(horizon, is_relative=True)
            self.model.fit(train, fh=fh, **kwargs)
        else:
            if self.model.get_tag("requires-fh-in-fit"):
                raise Exception("You have to specify an horizon in order to fit this model..")
            self.model.fit(train, **kwargs)
        self.fitted = True

    def predict(self, horizon: Union[int, List] = None):
        if horizon:
            fh = ForecastingHorizon(horizon, is_relative=True)
        else:
            fh = ForecastingHorizon([1], is_relative=True)
        return self.model.predict(fh)

    def partial_fit(self, df, update_params=False):
        self.model.update(df, update_params=update_params)

    def get_params(self):
        return self.model.get_fitted_params()

