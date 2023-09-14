import pandas as pd
import re

# 从方程中提取K和B的值
def extract_values(equation):
    match = re.search(r"y = (-?\d+\.\d+)x (\+|-) (-?\d+\.\d+)", equation)
    if match:
        k_value = float(match.group(1))
        operator = match.group(2)
        b_value = float(match.group(3))
        if operator == "-":
            b_value = -b_value
        return k_value, b_value
    return None, None

# 读取x值和方程
x_values_df = pd.read_excel("x_values_by_category.xlsx", index_col=0)
huber_results = pd.read_excel("huber_regression_results.xlsx")

# 提取方程的K和B值
k_values, b_values = [], []
for equation in huber_results['Equation']:
    k, b = extract_values(equation)
    k_values.append(k)
    b_values.append(b)

# 使用方程计算y值
y_values_df = pd.DataFrame(index=x_values_df.index)
for category, k, b in zip(x_values_df.columns, k_values, b_values):
    # 确保列中的值是数值类型
    if x_values_df[category].dtype in ['float64', 'int64']:
        y_values_df[category] = x_values_df[category] * k + b

# 重置索引以将品类名称作为第一列
y_values_df.reset_index(inplace=True)
y_values_df = y_values_df.rename(columns={'index': 'Category'})

# 保存到Excel
y_values_df.to_excel("calculated_y_values.xlsx", index=False)

