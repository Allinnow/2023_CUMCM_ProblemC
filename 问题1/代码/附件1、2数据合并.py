import pandas as pd

data1 = pd.read_excel("附件1.xlsx")
data2 = pd.read_excel("附件2.xlsx")

#按单品编码合并
combined_data = pd.merge(data2, data1, on="单品编码", how="left")

#按品类分组
data_3 = combined_data.groupby(['销售日期', '单品编码', '单品名称', '分类名称']).agg(
    {
         '销量(千克)': 'sum',
         '销售单价(元/千克)': 'mean'
    }
).reset_index()

data_3.to_excel("combine_sales_data.xlsx", index=False)
