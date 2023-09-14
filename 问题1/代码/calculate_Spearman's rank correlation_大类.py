import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data = pd.read_excel("result_1.xlsx")

data_1 = data.pivot(index='销售日期', columns='分类名称', values='销量(千克)')

matrix_1 = data_1.corr(method='spearman')

plt.figure(figsize=(10, 8))
sns.heatmap(matrix_1, annot=True, cmap='coolwarm', center=0)
plt.title('Spearman Rank Correlation Between 6 Categories')
plt.show()