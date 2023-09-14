import pandas as pd

data = pd.read_excel("combine_sales_data.xlsx")

data['销售加权单价'] = data['销量(千克)'] * data['销售单价(元/千克)']

grouped_data = data.groupby(['销售日期', '分类名称']).agg({
    '销量(千克)': 'sum',
    '销售加权单价': 'sum'
}).reset_index()

grouped_data.columns = ['销售日期', '分类名称', '总销量(千克)', '销售加权总价']

grouped_data['分类销量加权单价(元/千克)'] = grouped_data['销售加权总价'] / grouped_data['总销量(千克)']

grouped_data.to_excel("加权后_data.xlsx", index=False)
