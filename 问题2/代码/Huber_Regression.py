import pandas as pd
from sklearn.linear_model import HuberRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 加载数据集
data = pd.read_excel("加权后_data.xlsx")

# 获取品类列表
unique_categories = data["分类名称"].unique()

# 初始化字典来存储每个品类的Huber回归方程、MSE和R^2
equations = {}
mse_values = {}
r2_values = {}

for category in unique_categories:
    category_data = data[data["分类名称"] == category]
    
    X = category_data[["分类销量加权单价(元/千克)"]]
    y = category_data["总销量(千克)"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = HuberRegressor()
    model.fit(X_train, y_train)
    

    y_pred = model.predict(X_test)
    

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    equation = f"y = {model.coef_[0]:.4f}x + {model.intercept_:.4f}"
    
    equations[category] = equation
    mse_values[category] = mse
    r2_values[category] = r2

for category, equation in equations.items():
    print(f"For {category}, the regression equation is: {equation}")

results_list = []

for category in unique_categories:

    results_list.append({
        "Category": category,
        "Equation": equations[category],
        "MSE": mse_values[category],
        "R^2": r2_values[category]
    })

results_df = pd.DataFrame(results_list)

results_df.to_excel("huber_regression_results.xlsx", index=False)
