import pandas as pd
import numpy as np
from scipy import stats

todo_data = pd.read_excel("result_1.xlsx")

todo_data["年份"] = todo_data["销售日期"].dt.year
unique_years = todo_data["年份"].unique()

def fun_1(data, category, year):
    year_data = data[(data["分类名称"] == category) & (data["年份"] == year)]["销量(千克)"]
    _, p_value = stats.shapiro(year_data)
    return p_value

p_values_dict = {}
all_categories = todo_data["分类名称"].unique()
for category in all_categories:
    p_values_dict[category] = {}
    for year in unique_years:
        p_values_dict[category][year] = fun_1(todo_data, category, year)

p_value = pd.DataFrame(p_values_dict).T
print(p_value)

