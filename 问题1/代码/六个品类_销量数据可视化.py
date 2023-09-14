#销量数据进行可视化

grouped_sales_data['销售日期'] = pd.to_datetime(grouped_sales_data['销售日期'])

grouped_by_month = grouped_sales_data.groupby([grouped_sales_data['销售日期'].dt.to_period("M"), '分类名称'])["销量(千克)"].sum().reset_index()
grouped_by_month['销售日期'] = grouped_by_month['销售日期'].dt.to_timestamp()

unique_categories = grouped_by_month['分类名称'].unique()

plt.figure(figsize=(15, 6 * len(unique_categories)))

for idx, category in enumerate(unique_categories, 1):
    plt.subplot(len(unique_categories), 1, idx)
    data = grouped_by_month[grouped_by_month['分类名称'] == category]
    plt.plot(data['销售日期'], data['销量(千克)'], marker='o', label=category)
    plt.title(f"品类 {category} 的按月销售趋势")
    plt.xlabel("日期")
    plt.ylabel("销量 (千克)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

plt.show()
