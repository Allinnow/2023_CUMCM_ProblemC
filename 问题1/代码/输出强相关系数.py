import pandas as pd
import numpy as np

correlation_df = pd.read_excel("correlation_matrix.xlsx", index_col=0)

strong_correlation_matrix = pd.DataFrame(np.nan, index=correlation_df.index, columns=correlation_df.columns)

mask = (correlation_df > 0.9) | (correlation_df < -0.9)
strong_correlation_matrix[mask] = correlation_df[mask]

strong_correlation_matrix.to_excel("strong_correlation_matrix.xlsx")
