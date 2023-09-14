import pandas as pd

sorted_sales_data = pd.read_excel("sorted_sales_data_with_names.xlsx")
combine_sales_data = pd.read_excel("combine_sales_data.xlsx")

product_names_49 = sorted_sales_data["单品名称"].tolist()

filtered_data = combine_sales_data[combine_sales_data['单品名称'].isin(product_names_49)]

output_path = "filtered_combine_sales_data.xlsx"
filtered_data.to_excel(output_path, index=False)
