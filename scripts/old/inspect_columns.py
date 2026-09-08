import pandas as pd

df = pd.read_csv("/Users/valeria/Desktop/nrao_project/data/OI_sample_large.csv")

print("rows:", len(df))
print("number of columns:", len(df.columns))
print()
print("all column names:")
for i, name in enumerate(df.columns):
    print(i, name)
print()
print("first 3 rows:")
print(df.head(3))