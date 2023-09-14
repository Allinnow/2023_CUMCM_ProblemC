import pandas as pd

#读取数据
data = pd.read_excel("combine_sales_data.xlsx")

#为每个单品创建时间序列数据
pivot_data = data.pivot(index='销售日期', columns='单品名称', values='销量(千克)')

#计算时间序列之间的Spearman相关性
correlation_matrix = pivot_data.corr(method='spearman')

#输出
correlation_matrix.to_excel("correlation_matrix.xlsx")
