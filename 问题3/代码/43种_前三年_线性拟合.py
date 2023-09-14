import pandas as pd
import statsmodels.api as sm

data = pd.read_excel("filtered_combine_sales_data.xlsx")

regression_results = pd.DataFrame(columns=['Product Name', 'Intercept', 'Coefficient', 'R-squared'])


for product in data['单品名称'].unique():
    product_data = data[data['单品名称'] == product]
    

    X = product_data[['销售单价(元/千克)']]
    y = product_data['销量(千克)']

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()
    

    intercept = model.params[0]
    coefficient = model.params[1]
    r_squared = model.rsquared

    result = pd.DataFrame({
        'Product Name': [product],
        'Intercept': [intercept],
        'Coefficient': [coefficient],
        'R-squared': [r_squared]
    })
    regression_results = pd.concat([regression_results, result], ignore_index=True)

output_path = "regression_results.xlsx"
regression_results.to_excel(output_path, index=False)
