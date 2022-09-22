import pandas as pd

from ds4biz_time_series.utils.core_utils import to_dataframe
from ds4biz_time_series.utils.logger_utils import logger


def preprocessing_data(data, datetime_feature, datetime_frequency, task="forecasting", get_only_X = False):
    print("datetime feature::: ",datetime_feature)
    print("datetime frequency::: ",datetime_frequency)

    res_data = data.get("data", None)
    print(res_data)
    if not res_data:
        print("return 1")
        return dict(X=res_data)

    if not get_only_X:
        target = data['target'] if task != 'classification' else [str(el) for el in data['target']]

    df = to_dataframe(res_data)

    if not datetime_feature in df.columns:

        print(df.columns)
        raise Exception("The datetime_feature specified doesn't match any features in your data, please check again.")
    df[datetime_feature] = pd.PeriodIndex(df[datetime_feature], freq=datetime_frequency)

    if len(df.columns)==1:
        logger.debug("only datetime feature available - no other covariates")
        df.set_index(datetime_feature, inplace=True)
        target = df.copy()
        df = None
        if get_only_X:
            return dict(X=df)
        else:
            df["target"] = target
            return dict(y=df, X=None)
    else:
        n_covariates = len(df)
        logger.debug("covariates available: %s" % str(n_covariates))
        df.set_index(datetime_feature, inplace=True)
        print(df)
        if get_only_X:
            return dict(X=df)
        else:
            return dict(y=target, X=df)
