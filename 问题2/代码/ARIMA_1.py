import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

data = pd.read_excel("STL_残差_大类.xlsx", index_col='销售日期', parse_dates=True)

original_data = pd.read_excel("result_1.xlsx", parse_dates=['销售日期'])
original_data_pivot = original_data.pivot(index='销售日期', columns='分类名称', values='销量(千克)').fillna(0)

results_original = {}

for category in data.columns:
    
    series = data[category].dropna()

    best_aic = float('inf')
    best_order = None
    best_model = None

    for p in range(5):
        for d in range(2):
            for q in range(5):
                try:
                    model = ARIMA(series, order=(p, d, q)).fit()
                    if model.aic < best_aic:
                        best_aic = model.aic
                        best_order = (p, d, q)
                        best_model = model
                except:
                    continue

    model = ARIMA(series, order=best_order).fit()

    forecast_residuals = model.forecast(steps=10)
    
    last_known_point = original_data_pivot[category].iloc[-1]
    forecast_original = forecast_residuals + last_known_point

    forecast_original[forecast_original < 0] = 0

    results_original[category] = {
        "Best Order": best_order,
        "AIC": best_aic,
        "Forecast": forecast_original
    }

forecast_original_df = pd.DataFrame()

for category, info in results_original.items():
    forecast_original_df[category] = info['Forecast']

forecast_original_df.to_excel("ARIMA_original_result.xlsx")
