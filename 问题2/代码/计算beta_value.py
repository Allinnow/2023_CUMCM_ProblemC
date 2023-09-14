import pandas as pd

def compute_average_loss_rates(loss_rate_file, sales_data_file, output_file):
    loss_rate_data = pd.read_excel(loss_rate_file)
    loss_rate_data.set_index("小分类名称", inplace=True)
    loss_rate_map = loss_rate_data["平均损耗率(%)_小分类编码_不同值"].to_dict()

    sales_data = pd.read_excel(sales_data_file)
    
    average_loss_rates = {}
    for category in loss_rate_map.keys():
        average_loss_rates[category] = sales_data[category] * loss_rate_map[category] / 100
    average_loss_rate_df = pd.DataFrame(average_loss_rates)
    
    average_loss_rate_next_7_days = average_loss_rate_df.head(7)
    
    average_loss_rate_next_7_days.to_excel(output_file, index=False)

compute_average_loss_rates("附件4.xlsx", "ARIMA_result.xlsx", "beta_value.xlsx")