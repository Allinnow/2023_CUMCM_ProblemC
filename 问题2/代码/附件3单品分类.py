import pandas as pd

# 读取两个附件的数据
attachment_1 = pd.read_excel("附件1.xlsx")
attachment_3 = pd.read_excel("附件3.xlsx")

# 使用附件1中的单品编码和分类名称为附件3中的单品编码进行分类
attachment_3 = attachment_3.merge(attachment_1[['单品编码', '分类名称']], on='单品编码', how='left')

# 保存结果到新的Excel文件
attachment_3.to_excel("附件3_分类后.xlsx", index=False)