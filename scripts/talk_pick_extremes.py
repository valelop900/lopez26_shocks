import pandas as pd

small = pd.read_csv("notes/2026-07-31_w80_new_small24.csv")
large = pd.read_csv("notes/2026-07-22_w80_new_large.csv")

print(small.columns.tolist())
print("broadest small:")
print(small.sort_values(small.columns[-1], ascending=False).head(3))
print("narrowest large:")
print(large.sort_values(large.columns[-1]).head(3))