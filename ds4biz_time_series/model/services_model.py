class FitServiceArgs():
    def __init__(self, datetime_feature, datetime_frequency, task="forecasting", forecasting_horizon=None, report=False, test_size=0.2, **kwargs):
        self.task = task
        self.forecasting_horizon = forecasting_horizon
        self.report = report
        self.test_size = test_size
        self.datetime_feature = datetime_feature
        self.datetime_frequency = datetime_frequency

    def to_dict(self):
        return self.__dict__


class PredictServiceArgs():
    def __init__(self, forecasting_horizon, **kwargs):
        self.forecasting_horizon = forecasting_horizon

    def to_dict(self):
        return self.__dict__


if __name__ == '__main__':

    es = dict(datetime_feature="ciao", datetime_frequency="7d", task="forecasting", forecasting_horizon=2, report=True, test_size=2, miao="b", cane="d")
    fs = FitServiceArgs(**es).to_dict()
    print(fs)