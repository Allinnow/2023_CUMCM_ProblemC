from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.base import clone
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import joblib
import os

# 数据导入和预处理
def load_and_preprocess_data(filepath):
    data = pd.read_excel("filtered_combine_sales_data.xlsx")
    data = data.sort_values(by="销售日期")
    return data

# 平稳化处理: 使用滑动窗口平均
def stabilize_data(data, window_size=7):
    data['销量(千克)_smooth'] = data['销量(千克)'].rolling(window=window_size).mean()
    data = data.dropna()  
    return data

# 随机森林模型训练
def train_random_forest(data):
    X = data[['销售单价(元/千克)']]
    y = data['销量(千克)_smooth']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 使用均方误差来评估模型效果
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    return model, mse

# 主函数
def main(filepath):
    data = load_and_preprocess_data(filepath)
    product_names = data['单品名称'].unique()
    
    models = {}
    for product in product_names:
        product_data = data[data['单品名称'] == product]
        
        # 将数据分为三个周期
        period_length = len(product_data) // 3
        periods = [product_data.iloc[i*period_length: (i+1)*period_length] for i in range(3)]
        
        period_models = []
        for period_data in periods:
            stabilized_data = stabilize_data(period_data)
            model, mse = train_random_forest(stabilized_data)
            period_models.append((model, mse))
        
        # 选择MSE最小的模型作为该商品的模型
        best_model = min(period_models, key=lambda x: x[1])[0]
        models[product] = clone(best_model)
    
    return models

# 保存模型到指定目录
def save_models(models, dir_path="models"):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for product, model in models.items():
        model_path = os.path.join(dir_path, f"{product}.pkl")
        joblib.dump(model, model_path)

# 从指定目录加载模型
def load_model(product_name, dir_path="models"):
    model_path = os.path.join(dir_path, f"{product_name}.pkl")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        print(f"模型 {product_name} 不存在！")
        return None

# 预测指定商品在给定价格下的销量
def predict_sales(product_name, price, dir_path="models"):
    model = load_model(product_name, dir_path)
    if model:
        return model.predict([[price]])[0]
    else:
        return None


def main_with_save(filepath):
    models = main(filepath)
    save_models(models)
    return models

