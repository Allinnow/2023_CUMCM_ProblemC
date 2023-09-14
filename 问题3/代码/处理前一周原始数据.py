import pandas as pd

file_path = "6.24-6.30原始销售数据.xlsx"
df = pd.read_excel(file_path, header=None)
df.columns = ["销售日期", "扫码销售时间", "单品编码", "销量(千克)", "销售单价(元/千克)", "销售类型", "是否打折销售"]

mapping_df = pd.read_excel("附件1.xlsx")
code_to_name = dict(zip(mapping_df['单品编码'], mapping_df['单品名称']))

df['单品编码'] = df['单品编码'].map(code_to_name)

grouped_df = df.groupby(['单品编码', '销售日期'])['销量(千克)'].sum().reset_index()
pivot_df = grouped_df.pivot(index='单品编码', columns='销售日期', values='销量(千克)').reset_index()

pivot_df.fillna(0, inplace=True)


pivot_df['总销售量'] = pivot_df.iloc[:, 1:].sum(axis=1)


sorted_df = pivot_df.sort_values(by='总销售量', ascending=False)

output_file_path = "sorted_sales_data_with_names.xlsx"
sorted_df.to_excel(output_file_path, index=False)
