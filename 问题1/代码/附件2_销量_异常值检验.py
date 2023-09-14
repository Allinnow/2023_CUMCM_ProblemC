import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载数据集
data = pd.read_excel("附件2.xlsx")

# 计算Q1, Q3 和 IQR
Q1 = data['销量(千克)'].quantile(0.25)
Q3 = data['销量(千克)'].quantile(0.75)
IQR = Q3 - Q1

# 计算上界和下界
upper_bound = Q3 + 1.5 * IQR
lower_bound = Q1 - 1.5 * IQR

# 筛选出异常值
outliers = data[(data['销量(千克)'] < lower_bound) | (data['销量(千克)'] > upper_bound)]

# 可视化异常值
plt.figure(figsize=(10, 6))
sns.boxplot(data['销量(千克)'])
plt.title('销量(千克) 的箱线图')
plt.axhline(y=upper_bound, color='r', linestyle='--', label=f"Upper Bound ({upper_bound:.2f})")
plt.axhline(y=lower_bound, color='r', linestyle='--', label=f"Lower Bound ({lower_bound:.2f})")
plt.legend()
plt.show()

# 输出异常值的详情
print(outliers[['销售日期', '销量(千克)']])
