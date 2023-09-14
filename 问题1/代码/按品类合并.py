#按品类合并
import pandas as pd

#读取
file_path = "combine_sales_data.xlsx" 
sales_data = pd.read_excel(file_path)

#分组、求和
grouped_sales = sales_data.groupby(["销售日期", "分类名称"])["销量(千克)"].sum().reset_index()

# 保存
output_path = "result_1.xlsx"  
grouped_sales.to_excel(output_path, index=False)
