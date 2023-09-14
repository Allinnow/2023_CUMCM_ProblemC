import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取相关系数矩阵
correlation_matrix = pd.read_excel("strong_correlation_matrix.xlsx", index_col=0)

# 找出正负0.9以上的相关系数
strong_correlations = correlation_matrix[(correlation_matrix > 0.9) | (correlation_matrix < -0.9)]

# 将主对角线上的值设置为NaN，因为我们不关心每个变量与其自身的相关性
for i in range(strong_correlations.shape[0]):
    strong_correlations.iloc[i, i] = None

# 删除所有NaN值
strong_correlations = strong_correlations.dropna(how='all').dropna(axis=1, how='all')

# 设置图形大小
plt.figure(figsize=(20, 20))

# 绘制热图
sns.heatmap(strong_correlations, cmap='coolwarm', center=0, annot=True, fmt=".2f")

# 设置标题和显示图形
plt.title("Strong Correlations (>|0.9|)")
plt.show()
