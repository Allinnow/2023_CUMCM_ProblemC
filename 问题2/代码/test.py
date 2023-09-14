from scipy.optimize import minimize
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

# 读取数据
reordered_data = pd.read_excel("reordered_data.xlsx")
huber_results = pd.read_excel("huber_regression_results.xlsx")

# 提取K和B的值
k_values, b_values = [], []
for equation in huber_results['Equation']:
    k, b = extract_values(equation)
    k_values.append(k)
    b_values.append(b)

# 定义目标函数
def objective(x, i, t):
    y_it = k_values[i] * x[0] + b_values[i]
    return -1 * x[0] * y_it

# 定义约束条件
def constraint1(x, i, t):
    beta_value = reordered_data.iloc[t, i]
    return x[0] * (1 - beta_value) - reordered_data.iloc[t, i]

def constraint2(x, i, t):
    y_it = k_values[i] * x[0] + b_values[i]
    return reordered_data.iloc[t, i] - y_it

# 初始化结果存储DataFrame
result_df = pd.DataFrame(index=reordered_data.columns, columns=[f"Day_{t+1}" for t in range(reordered_data.shape[0])])

# 遍历每个i和t的组合
for i in range(reordered_data.shape[1]):
    x_values_for_category = []
    for t in range(reordered_data.shape[0]):
        constraints = ({'type': 'ineq', 'fun': constraint1, 'args': (i, t)},
                       {'type': 'ineq', 'fun': constraint2, 'args': (i, t)})
        result = minimize(objective, [0.1], constraints=constraints, args=(i, t), method='trust-constr')
        x_value = result.x[0]
        x_values_for_category.append(x_value)
    result_df.iloc[i, :] = x_values_for_category

# 输出到Excel
result_df.to_excel("x_values_by_category.xlsx")

