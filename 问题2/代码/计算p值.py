import pandas as pd

# 读取数据
attachment_3_classified = pd.read_excel("附件3_分类后.xlsx")
arima_result = pd.read_excel("ARIMA_result.xlsx")

# 转换日期格式
arima_result['日期'] = pd.to_datetime(arima_result['Unnamed: 0'], origin='2020-07-01', unit='D')

# 合并数据
merged_data = attachment_3_classified.merge(arima_result, on='日期', how='right')

# 计算每一品类的每一天的成本价等效值
cost_equivalent_df = pd.DataFrame()
cost_equivalent_df['日期'] = arima_result['日期']

for category in arima_result.columns[1:-1]:
    daily_cost_values = []
    for date in arima_result['日期']:
        daily_data = merged_data[(merged_data['日期'] == date) & (merged_data['分类名称'] == category)]
        weighted_price = daily_data['批发价格(元/千克)'] * daily_data[category]
        if daily_data[category].sum() != 0:
            daily_cost = weighted_price.sum() / daily_data[category].sum()
        else:
            daily_cost = 0
        daily_cost_values.append(daily_cost)
    cost_equivalent_df[category] = daily_cost_values

# 保存到Excel
cost_equivalent_df.to_excel("p_value.xlsx", index=False)
