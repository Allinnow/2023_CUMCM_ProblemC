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
    beta_value = reordered_data.iloc[t, i]  # Assuming β is in reordered_data
    return x[0] * (1 - beta_value) - reordered_data.iloc[t, i]

def constraint2(x, i, t):
    y_it = k_values[i] * x[0] + b_values[i]
    return reordered_data.iloc[t, i] - y_it  # Assuming a_it is in reordered_data

# 初始化结果存储列表
max_values = []

# 遍历每个i和t的组合
for i in range(reordered_data.shape[1]):
    for t in range(reordered_data.shape[0]):
        constraints = ({'type': 'ineq', 'fun': constraint1, 'args': (i, t)},
                       {'type': 'ineq', 'fun': constraint2, 'args': (i, t)})
        result = minimize(objective, [0.1], constraints=constraints, args=(i, t), method='trust-constr')  # 使用'trust-constr'方法
        max_value = -result.fun
        x_value = result.x[0]
        max_values.append((i, t, max_value, x_value))

# 打印结果
for value in max_values:
    i, t, max_value, x_value = value
    print(f"Category {i+1}, Day {t+1}: Max Value = {max_value}, x_it = {x_value}")
