import pandas as pd

from ds4biz_time_series.utils.core_utils import to_dataframe
from ds4biz_time_series.utils.logger_utils import logger


def preprocessing_data(data, datetime_feature, datetime_frequency, task="forecasting"):

    data = data.get("data", None)
    print(data)
    target = data['target'] if task != 'classification' else [str(el) for el in data['target']]
    print(target)
    df = to_dataframe(data)

    print(df)
    print(target)
    print("data divided")
    if not datetime_feature in df.columns:
        raise Exception("The datetime_feature specified doesn't match any features in your data, please check again.")
    if len(df.columns)==1:
        logger.debug("only datetime feature available - no other covariates")
        df["target"] = target
        df[datetime_feature] = pd.PeriodIndex(df["Date_Time"], freq=datetime_frequency)
        df.set_index(datetime_feature, inplace=True)
        return dict(y=df, X=None)
    else:
        n_covariates = len(df)-1
        logger.debug("covariates available: %s" % str(n_covariates))
        df.set_index(datetime_feature, inplace=True)
        return dict(y=target, X=df)
