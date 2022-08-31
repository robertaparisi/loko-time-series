import pandas as pd

data = {"data":[{"Date_Time": "01/03/2010 08:00:20" },
       {"Date_Time": "01/10/2010 08:00:20"},
       {"Date_Time": "01/17/2010  08:00:20"},
       {"Date_Time": "01/24/2010  09:00:20"},
       {"Date_Time": "01/31/2010  08:20:40"}],
     "target":[1509634,1581344, 1614204, 1897725, 1759063]}

df = pd.DataFrame(data["data"])
print()
if len(df.columns)==1:
    dt_feature = df.columns[0]
    df["target"] = data["target"]
    df.set_index(dt_feature, inplace=True)
    print(df)