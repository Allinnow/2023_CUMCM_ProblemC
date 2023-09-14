import pandas as pd

data = pd.read_excel("附件2.xlsx")

#如果有就打印出来这一行
if data.isnull().any().any():
    miss = data[data.isnull().any(axis=1)]
    print(f"以下行包含缺失值:\n{miss.index.tolist()}")
else:
    print("没有缺失值")

