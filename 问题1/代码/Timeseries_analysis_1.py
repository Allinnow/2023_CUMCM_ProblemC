#时间序列分析，STL结果画图
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data_1 = pd.read_excel("result_1.xlsx")

full_series = pd.date_range(start="2020-07-01", end="2023-06-30")

miss_dict = {}

for category in data_1['分类名称'].unique():
    category_dates = data_1[data_1['分类名称'] == category]['销售日期']
    miss_dict[category] = full_series[~full_series.isin(category_dates)]

print(miss_dict)

todorow = []
for category, missing_dates in miss_dict.items():
    for date in missing_dates:
        todorow.append({'销售日期': date, '分类名称': category, '销量(千克)': 0})

data_1 = pd.concat([data_1, pd.data_1Frame(todorow)], ignore_index=True)

data_1 = data_1.sort_values(by=['分类名称', '销售日期'])

def fun1(data_1, category_names):
    fig, axes = plt.subplots(4, len(category_names), figsize=(18, 12))

    for i, category_name in enumerate(category_names):
        category_data_1 = data_1[data_1['分类名称'] == category_name].set_index('销售日期')['销量(千克)']
        
        stl_result = STL(category_data_1, seasonal=365).fit()
        
        category_data_1.plot(ax=axes[0, i], title="Original - " + category_name, color='lightblue')
        stl_result.trend.plot(ax=axes[1, i], title="Trend", color='lightblue')
        stl_result.seasonal.plot(ax=axes[2, i], title="Seasonal", color='lightblue')
        stl_result.resid.plot(ax=axes[3, i], title="Residual", color='lightblue')

    plt.tight_layout()
    plt.show()

category_names = data_1['分类名称'].unique()


fun1(data_1, category_names)
